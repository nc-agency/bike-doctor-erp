# bike_brand.py für bike.doctor ERPNext-Erweiterung
# Erstellt am 2025-05-05
# Diese Datei definiert die Logik für den Bike Brand DocType
# - Verwaltung von Fahrradmarken und zugehörigen Informationen
# - Einfache Kategorisierung von Fahrrädern

import frappe
from frappe import _
from frappe.model.document import Document

class BikeBrand(Document):
    def validate(self):
        self.validate_duplicate()
        
    def validate_duplicate(self):
        # Überprüfe auf doppelte Markeneinträge (unabhängig von Groß-/Kleinschreibung)
        exists = frappe.db.sql("""
            SELECT name FROM `tabBike Brand`
            WHERE name != %s AND LOWER(brand_name) = %s
        """, (self.name, self.brand_name.lower()))
        
        if exists:
            frappe.throw(_("Bike Brand {0} already exists").format(exists[0][0]))
            
    def get_bikes(self):
        """Gibt alle Fahrräder dieser Marke zurück"""
        return frappe.get_all(
            "Bike Details",
            filters={"bike_brand": self.name},
            fields=["name", "bike_model", "year", "owner", "owner_name"]
        )
        
    def get_bike_count(self):
        """Zählt die Anzahl der Fahrräder dieser Marke"""
        return frappe.db.count("Bike Details", {"bike_brand": self.name})
