# workshop_order.py für bike.doctor ERPNext-Erweiterung
# Erstellt am 2025-05-05
# Diese Datei definiert die Hauptlogik für den Workshop Order DocType
# - Implementiert die Werkstattauftrags-Kernfunktionalität
# - Integriert mit ERPNext-Kunden und Abrechnungssystem
# - Verwaltet Statusänderungen und Benachrichtigungen

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, nowdate, add_days

class WorkshopOrder(Document):
    def validate(self):
        self.validate_dates()
        self.update_status()
        
    def validate_dates(self):
        if getdate(self.completion_date) < getdate(self.start_date):
            frappe.throw(_("Completion Date cannot be before Start Date"))
            
        if getdate(self.start_date) < getdate(nowdate()):
            # Warnung, wenn Startdatum in der Vergangenheit liegt
            frappe.msgprint(_("Start Date is in the past"))
    
    def update_status(self):
        # Automatische Statusaktualisierung basierend auf Job Cards
        total_job_cards = frappe.get_all("Workshop Job Card", 
                                        filters={"workshop_order": self.name}, 
                                        fields=["status"])
        
        if not total_job_cards:
            self.status = "Draft"
            return
            
        completed = 0
        for job_card in total_job_cards:
            if job_card.status == "Completed":
                completed += 1
                
        if completed == len(total_job_cards):
            self.status = "Ready for Delivery"
        elif completed > 0:
            self.status = "In Progress"
        else:
            self.status = "Open"
    
    def on_submit(self):
        # Erstelle Benachrichtigung für Werkstattleiter
        self.notify_workshop_manager()
        
        # Erstelle Job Cards, falls noch keine existieren
        if not frappe.get_all("Workshop Job Card", filters={"workshop_order": self.name}):
            self.create_job_cards()
            
    def notify_workshop_manager(self):
        frappe.sendmail(
            recipients=frappe.get_all("User", 
                                    filters={"role": "Workshop Manager"}, 
                                    fields=["email"]),
            subject=_("New Workshop Order: {0}").format(self.name),
            message=_("A new workshop order has been submitted for {0} ({1})").format(
                self.customer_name, self.bike_model
            ),
            reference_doctype=self.doctype,
            reference_name=self.name
        )
        
    def create_job_cards(self):
        """Erstellt Job Cards basierend auf den ausgewählten Services"""
        for service in self.services:
            job_card = frappe.new_doc("Workshop Job Card")
            job_card.workshop_order = self.name
            job_card.bike = self.bike
            job_card.service_type = service.service_type
            job_card.description = service.description
            job_card.estimated_hours = service.estimated_hours
            job_card.save()

        frappe.msgprint(_("{0} Job Cards created").format(len(self.services)))
        
    def create_invoice(self):
        """Erstellt eine Verkaufsrechnung basierend auf dem Werkstattauftrag"""
        if self.status != "Ready for Delivery":
            frappe.throw(_("Cannot create invoice until order is Ready for Delivery"))
            
        # Prüfe, ob bereits eine Rechnung für diesen Auftrag existiert
        existing_invoice = frappe.get_all("Sales Invoice",
                                     filters={"workshop_order": self.name,
                                              "docstatus": ["!=", 2]})
        if existing_invoice:
            frappe.throw(_("Invoice already exists for this workshop order"))
            
        # Erstelle neue Rechnung
        invoice = frappe.new_doc("Sales Invoice")
        invoice.customer = self.customer
        invoice.workshop_order = self.name
        
        # Füge Dienstleistungen hinzu
        for service in self.services:
            invoice.append("items", {
                "item_code": service.service_item,
                "qty": 1,
                "rate": service.rate,
                "description": service.description
            })
            
        # Füge verwendete Teile hinzu
        job_cards = frappe.get_all("Workshop Job Card", 
                               filters={"workshop_order": self.name},
                               fields=["name"])
                               
        for job_card in job_cards:
            parts = frappe.get_all("Workshop Job Card Part", 
                              filters={"parent": job_card.name},
                              fields=["item_code", "qty", "rate", "description"])
            
            for part in parts:
                invoice.append("items", {
                    "item_code": part.item_code,
                    "qty": part.qty,
                    "rate": part.rate,
                    "description": part.description
                })
                
        # Speichere die Rechnung
        invoice.save()
        
        frappe.msgprint(_("Sales Invoice {0} created").format(invoice.name))
        return invoice.name
