# -*- coding: utf-8 -*-
# bike.doctor ERP - Bicycle Management Module
# 
# Erstellt: 05.05.2025
# Änderungen:
# - Initiale Erstellung des Bicycle Management Moduls
# - Implementierung der Kern-Business-Logik für die Fahrradwerkstatt
# - Integration mit ERPNext-Verkaufs- und Lagerverwaltungsmodulen

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import nowdate, add_days, flt, cint, formatdate

def on_sales_invoice_submit(doc, method):
    """
    Wird aufgerufen, wenn eine Verkaufsrechnung eingereicht wird.
    Prüft auf Fahrradreparaturen und aktualisiert deren Status.
    
    Args:
        doc: Die Verkaufsrechnung, die eingereicht wird
        method: Die aufgerufene Methode (wird nicht verwendet)
    """
    if not doc.bicycle_repair:
        return
    
    # Fahrradreparatur holen
    try:
        repair = frappe.get_doc("Bicycle Repair", doc.bicycle_repair)
        
        # Setzen der Rechnung und Aktualisierung des Status
        repair.db_set("invoice", doc.name)
        
        # Wenn die Reparatur noch nicht abgeschlossen ist, jetzt abschließen
        if repair.status != "Abgeschlossen":
            repair.db_set("status", "Abgeschlossen")
            repair.db_set("completion_date", nowdate())
        
        # Fahrrad aktualisieren
        if repair.bicycle:
            bicycle = frappe.get_doc("Bicycle", repair.bicycle)
            
            # Wenn dies eine Wartung ist, aktualisiere das letzte Servicedatum
            if repair.is_maintenance:
                bicycle.db_set("last_service_date", repair.completion_date or nowdate())
            
            # Setze den Status des Fahrrads auf "Einsatzbereit"
            bicycle.db_set("status", "Einsatzbereit")
            
        # Benachrichtigung erstellen
        frappe.msgprint(_("Fahrradreparatur {0} wurde mit dieser Rechnung verknüpft und abgeschlossen").format(repair.name))
    
    except Exception as e:
        frappe.log_error(f"Fehler bei der Aktualisierung der Fahrradreparatur {doc.bicycle_repair}: {str(e)}")

@frappe.whitelist()
def get_repair_history(bicycle):
    """
    Ruft die Reparaturhistorie für ein bestimmtes Fahrrad ab
    
    Args:
        bicycle (str): ID des Fahrrads
    
    Returns:
        list: Liste der Reparaturen mit Details
    """
    # Berechtigung prüfen
    if not frappe.has_permission("Bicycle", "read", bicycle):
        frappe.throw(_("Keine Berechtigung zum Lesen des Fahrrads"))
    
    # Alle Reparaturen des Fahrrads abrufen
    repairs = frappe.get_all("Bicycle Repair", 
        filters={"bicycle": bicycle},
        fields=[
            "name", "repair_date", "completion_date", "status", 
            "description", "total_cost", "is_maintenance",
            "technician", "invoice"
        ],
        order_by="repair_date desc"
    )
    
    # Zusätzliche Informationen zu den Reparaturen hinzufügen
    for repair in repairs:
        # Format-Datumsangaben für die Anzeige
        repair.repair_date_formatted = formatdate(repair.repair_date)
        if repair.completion_date:
            repair.completion_date_formatted = formatdate(repair.completion_date)
        
        # Verwendete Teile zählen
        repair.parts_count = frappe.db.count("Bicycle Repair Part", {"parent": repair.name})
        
        # Technikernamen abrufen, falls vorhanden
        if repair.technician:
            repair.technician_name = frappe.db.get_value("Employee", repair.technician, "employee_name")
    
    return repairs

@frappe.whitelist()
def create_invoice(repair):
    """
    Erstellt eine Verkaufsrechnung für eine Fahrradreparatur
    
    Args:
        repair (str): ID der Fahrradreparatur
    
    Returns:
        str: ID der erstellten Rechnung
    """
    # Berechtigung prüfen
    if not frappe.has_permission("Bicycle Repair", "write", repair):
        frappe.throw(_("Keine Berechtigung zum Bearbeiten der Fahrradreparatur"))
    
    repair_doc = frappe.get_doc("Bicycle Repair", repair)
    
    # Prüfen, ob bereits eine Rechnung existiert
    if repair_doc.invoice:
        frappe.throw(_("Diese Reparatur wurde bereits mit der Rechnung {0} abgerechnet").format(repair_doc.invoice))
    
    # Prüfen, ob ein Kunde zugeordnet ist
    if not repair_doc.customer:
        frappe.throw(_("Dieser Reparatur ist kein Kunde zugeordnet"))
    
    # Rechnungsposten vorbereiten
    items = []
    
    # Teile zur Rechnung hinzufügen
    if repair_doc.parts:
        for part in repair_doc.parts:
            items.append({
                "item_code": part.item_code,
                "item_name": part.item_name,
                "description": part.description or part.item_name,
                "qty": part.quantity,
                "rate": part.rate,
                "uom": frappe.db.get_value("Item", part.item_code, "stock_uom") or "Stk",
                "income_account": get_income_account(part.item_code, repair_doc.customer),
                "warehouse": get_warehouse(),
                "bicycle_repair": repair_doc.name
            })
    
    # Arbeitskosten zur Rechnung hinzufügen
    if repair_doc.labor_cost:
        # Arbeitskosten-Artikel suchen oder erstellen
        labor_item_code = get_labor_item()
        
        items.append({
            "item_code": labor_item_code,
            "item_name": _("Arbeitskosten für {0}").format(repair_doc.bicycle_name or "Fahrrad"),
            "description": repair_doc.description or _("Arbeitskosten für Reparatur"),
            "qty": 1,
            "rate": repair_doc.labor_cost,
            "uom": "Std",
            "income_account": get_income_account(labor_item_code, repair_doc.customer),
            "bicycle_repair": repair_doc.name
        })
    
    if not items:
        frappe.throw(_("Keine Artikel oder Arbeitskosten für die Rechnungserstellung vorhanden"))
    
    # Zahlungsfrist festlegen (14 Tage)
    due_date = add_days(nowdate(), 14)
    
    # Rechnung erstellen
    invoice = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": repair_doc.customer,
        "due_date": due_date,
        "items": items,
        "bicycle_repair": repair_doc.name,
        "remarks": _("Rechnung für Fahrradreparatur {0}").format(repair_doc.name),
        "update_stock": 1  # Lagerbestand aktualisieren
    })
    
    # Artikelsteuern hinzufügen
    invoice.set_taxes()
    
    # Rechnung speichern
    invoice.insert()
    
    # Referenz auf die Rechnung in der Reparatur speichern
    repair_doc.db_set("invoice", invoice.name)
    
    # Wenn die Reparatur abgeschlossen ist, aber kein Fertigstellungsdatum hat
    if repair_doc.status == "Abgeschlossen" and not repair_doc.completion_date:
        repair_doc.db_set("completion_date", nowdate())
    
    return invoice.name

def get_income_account(item_code, customer):
    """
    Bestimmt das Erlöskonto für einen Artikel
    
    Args:
        item_code (str): Artikelcode
        customer (str): Kundencode
    
    Returns:
        str: Erlöskonto
    """
    # Standardwerte für Erlöskonten abrufen
    item_defaults = frappe.db.get_value("Item Default", 
        {"parent": item_code, "company": frappe.defaults.get_user_default("Company")},
        "income_account")
    
    if item_defaults:
        return item_defaults
    
    # Falls keine Artikelstandards vorhanden sind, Kundengruppe verwenden
    customer_group = frappe.db.get_value("Customer", customer, "customer_group")
    if customer_group:
        customer_group_defaults = frappe.db.get_value("Customer Group", 
            customer_group, "default_income_account")
        
        if customer_group_defaults:
            return customer_group_defaults
    
    # Wenn alles andere fehlschlägt, Unternehmensstandard verwenden
    company = frappe.defaults.get_user_default("Company")
    default_income_account = frappe.db.get_value("Company", company, "default_income_account")
    
    if not default_income_account:
        frappe.throw(_("Standarderlöskonto für das Unternehmen {0} nicht festgelegt").format(company))
    
    return default_income_account

def get_warehouse():
    """
    Bestimmt das Standardlager für Verkäufe
    
    Returns:
        str: Lagerkurzzeichen
    """
    company = frappe.defaults.get_user_default("Company")
    default_warehouse = frappe.db.get_value("Company", company, "default_warehouse")
    
    if not default_warehouse:
        # Suche nach dem ersten Fertigwarenlager
        warehouses = frappe.get_all("Warehouse", 
            filters={"company": company, "warehouse_type": "Stores"},
            order_by="is_group, name",
            limit=1)
        
        if warehouses:
            default_warehouse = warehouses[0].name
        else:
            frappe.throw(_("Kein Standardlager für das Unternehmen {0} gefunden").format(company))
    
    return default_warehouse

def get_labor_item():
    """
    Holt oder erstellt einen Artikel für Arbeitskosten
    
    Returns:
        str: Artikelcode für Arbeitskosten
    """
    # Standardartikel für Arbeitskosten suchen
    labor_item_code = "WERKSTATT-ARBEIT"
    
    # Prüfen, ob der Artikel bereits existiert
    if not frappe.db.exists("Item", labor_item_code):
        # Artikel erstellen, wenn er nicht existiert
        labor_item = frappe.get_doc({
            "doctype": "Item",
            "item_code": labor_item_code,
            "item_name": "Werkstattarbeit",
            "item_group": "Dienstleistungen",
            "stock_uom": "Std",
            "is_stock_item": 0,
            "is_sales_item": 1,
            "is_purchase_item": 0,
            "is_service_item": 1,
            "description": "Arbeitskosten für Fahrradreparaturen und -wartungen"
        })
        
        labor_item.insert(ignore_permissions=True)
    
    return labor_item_code

@frappe.whitelist()
def update_bicycle_status(bicycle, status, update_note=None):
    """
    Aktualisiert den Status eines Fahrrads
    
    Args:
        bicycle (str): ID des Fahrrads
        status (str): Neuer Status
        update_note (str, optional): Hinweis zur Aktualisierung
    
    Returns:
        dict: Ergebnis der Aktualisierung
    """
    # Berechtigung prüfen
    if not frappe.has_permission("Bicycle", "write", bicycle):
        frappe.throw(_("Keine Berechtigung zum Bearbeiten des Fahrrads"))
    
    # Gültige Status prüfen
    valid_statuses = ["Neu", "Einsatzbereit", "In Reparatur", "Verkauft", "Ausrangiert"]
    if status not in valid_statuses:
        frappe.throw(_("Ungültiger Status: {0}").format(status))
    
    # Fahrrad aktualisieren
    bicycle_doc = frappe.get_doc("Bicycle", bicycle)
    bicycle_doc.status = status
    
    # Hinweis hinzufügen, wenn vorhanden
    if update_note:
        bicycle_doc.notes = (bicycle_doc.notes or "") + \
            f"\n\n{nowdate()}: Status geändert zu '{status}'. {update_note}"
    
    bicycle_doc.save()
    
    # Kommentar erstellen
    frappe.get_doc({
        "doctype": "Comment",
        "comment_type": "Info",
        "reference_doctype": "Bicycle",
        "reference_name": bicycle,
        "content": _("Status geändert zu '{0}'").format(status) + 
            (f": {update_note}" if update_note else "")
    }).insert(ignore_permissions=True)
    
    return {"success": True, "message": _("Status erfolgreich aktualisiert")}
