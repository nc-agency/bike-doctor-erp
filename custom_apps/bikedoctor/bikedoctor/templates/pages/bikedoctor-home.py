# -*- coding: utf-8 -*-
# bike.doctor ERP - Homepage Controller
# 
# Erstellt: 05.05.2025
# Änderungen:
# - Initiale Erstellung des Homepage-Controllers für die bike.doctor-App
# - Funktionen für das Anzeigen der bike.doctor-Homepage

from __future__ import unicode_literals
import frappe
from frappe import _

def get_context(context):
    """
    Liefert den Kontext für die Homepage-Vorlage
    """
    context.title = "bike.doctor - Fahrradwerkstatt-Managementsystem"
    
    # Füge benutzerdefinierte Daten zum Kontext hinzu, wenn das System initialisiert ist
    if frappe.db.get_value("System Settings", None, "setup_complete"):
        # Statistiken für die Homepage laden
        context.stats = get_workshop_stats()
        
        # Prüfen, ob der Benutzer eingeloggt ist
        if frappe.session.user != "Guest":
            context.is_logged_in = True
            # Lade personalisierte Daten für angemeldete Benutzer
            context.user_name = frappe.get_doc("User", frappe.session.user).full_name
    
    return context

def get_workshop_stats():
    """
    Liefert Statistiken für die Werkstatt-Homepage
    """
    stats = {}
    
    # Nur ausführen, wenn die Datenbank initialisiert ist
    if frappe.db.get_value("System Settings", None, "setup_complete"):
        try:
            # Offene Reparaturen zählen
            stats["active_repairs"] = frappe.db.count("Bicycle Repair", 
                filters={"status": ["in", ["Eingegangen", "In Arbeit", "Wartend"]]})
            
            # Fahrräder in der Datenbank zählen
            stats["registered_bicycles"] = frappe.db.count("Bicycle")
            
            # Heute abgeschlossene Reparaturen
            stats["completed_today"] = frappe.db.count("Bicycle Repair", 
                filters={"status": "Abgeschlossen", 
                        "completion_date": frappe.utils.nowdate()})
        except:
            # Falls die Tabellen noch nicht existieren
            stats["active_repairs"] = 0
            stats["registered_bicycles"] = 0
            stats["completed_today"] = 0
    
    return stats
