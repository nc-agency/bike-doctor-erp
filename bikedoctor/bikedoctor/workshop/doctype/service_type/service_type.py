# service_type.py für bike.doctor ERPNext-Erweiterung
# Erstellt am 2025-05-05
# Diese Datei definiert die Logik für den Service Type DocType
# - Verwaltet verschiedene Arten von Werkstattdiensten
# - Definiert Standardpreise und geschätzte Zeiten

import frappe
from frappe import _
from frappe.model.document import Document

class ServiceType(Document):
    def validate(self):
        self.validate_item()
        
    def validate_item(self):
        # Überprüfe, ob das zugehörige Item existiert
        if self.service_item:
            item = frappe.db.exists("Item", self.service_item)
            if not item:
                frappe.throw(_("Service Item {0} does not exist").format(self.service_item))
    
    def get_price(self):
        """Holt den aktuellen Preis für diesen Service"""
        if not self.service_item:
            return 0
            
        # Hole den Standardpreis des Items
        price = frappe.db.get_value("Item Price", 
                                   {"item_code": self.service_item, 
                                    "selling": 1,
                                    "price_list": frappe.db.get_single_value("Selling Settings", "selling_price_list")},
                                   "price_list_rate")
        
        if price:
            return price
        else:
            return self.default_rate
            
    def create_service_item(self, item_name=None):
        """Erstellt automatisch einen Serviceartikel, falls noch nicht vorhanden"""
        if self.service_item:
            frappe.msgprint(_("Service Item already exists: {0}").format(self.service_item))
            return self.service_item
            
        # Standardname, falls nicht angegeben
        if not item_name:
            item_name = f"Service: {self.service_name}"
            
        # Erstelle neues Item
        item = frappe.new_doc("Item")
        item.item_code = item_name
        item.item_name = item_name
        item.item_group = "Services"
        item.description = self.description
        item.is_stock_item = 0
        item.is_sales_item = 1
        item.is_service_item = 1
        item.stock_uom = "Hour"
        
        # Speichere das Item
        item.insert()
        
        # Aktualisiere diesen Service-Typ mit dem neuen Item
        self.service_item = item.name
        self.save()
        
        frappe.msgprint(_("Service Item {0} created").format(item.name))
        return item.name
