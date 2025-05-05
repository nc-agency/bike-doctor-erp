# workshop_job_card.py für bike.doctor ERPNext-Erweiterung
# Erstellt am 2025-05-05
# Diese Datei definiert die Logik für den Workshop Job Card DocType
# - Tracking von Arbeitszeiten und Teilen für Reparaturen
# - Statusverwaltung von Reparaturarbeiten
# - Integration mit dem Werkstattauftragssystem

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import time_diff_in_hours, now_datetime, get_datetime

class WorkshopJobCard(Document):
    def validate(self):
        self.validate_times()
        self.calculate_total_time()
        self.calculate_parts_total()
        self.update_parent_order()
        
    def validate_times(self):
        # Prüfe Start- und Endzeiten
        if self.actual_end_time and get_datetime(self.actual_start_time) > get_datetime(self.actual_end_time):
            frappe.throw(_("End Time cannot be before Start Time"))
    
    def calculate_total_time(self):
        # Berechne die tatsächliche Arbeitszeit
        if self.actual_start_time and self.actual_end_time:
            self.total_time = time_diff_in_hours(self.actual_end_time, self.actual_start_time)
        else:
            self.total_time = 0
            
    def calculate_parts_total(self):
        # Berechne die Gesamtkosten für verwendete Teile
        self.total_parts_cost = 0
        for part in self.parts:
            part.amount = part.qty * part.rate
            self.total_parts_cost += part.amount
    
    def update_parent_order(self):
        # Aktualisiere den übergeordneten Werkstattauftrag
        if self.workshop_order and not frappe.flags.in_test:
            workshop_order = frappe.get_doc("Workshop Order", self.workshop_order)
            
            # Berechne die Kosten für Teile und Dienstleistungen
            parts_cost = 0
            job_cards = frappe.get_all("Workshop Job Card", 
                                     filters={"workshop_order": self.workshop_order},
                                     fields=["total_parts_cost"])
                                     
            for jc in job_cards:
                parts_cost += jc.total_parts_cost
                
            # Update des Werkstattauftrags
            workshop_order.db_set("total_parts_cost", parts_cost)
            workshop_order.db_set("grand_total", parts_cost + workshop_order.total_service_cost + workshop_order.additional_costs)
    
    def start_job(self):
        if self.status == "Completed":
            frappe.throw(_("Cannot start a completed job"))
            
        self.status = "In Progress"
        self.actual_start_time = now_datetime()
        self.save()
        
        frappe.msgprint(_("Job started at {0}").format(self.actual_start_time))
        
    def complete_job(self):
        if not self.actual_start_time:
            frappe.throw(_("Job has not been started"))
            
        self.status = "Completed"
        self.actual_end_time = now_datetime()
        self.save()
        
        frappe.msgprint(_("Job completed at {0}").format(self.actual_end_time))
        
    def add_parts(self, item_code, qty, rate=None):
        """Hilfsfunktion zum Hinzufügen von Teilen zur Job-Karte"""
        if not item_code:
            frappe.throw(_("Item Code is required"))
            
        # Hole Artikeldetails, falls rate nicht angegeben wurde
        if not rate:
            item = frappe.get_doc("Item", item_code)
            rate = item.standard_rate
            
        # Prüfe, ob das Teil bereits in der Liste existiert
        for part in self.parts:
            if part.item_code == item_code:
                part.qty += qty
                return
                
        # Füge neues Teil hinzu
        self.append("parts", {
            "item_code": item_code,
            "qty": qty,
            "rate": rate
        })
        
        self.save()
        frappe.msgprint(_("Part {0} added to job card").format(item_code))
