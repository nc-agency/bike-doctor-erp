# bike_details.py für bike.doctor ERPNext-Erweiterung
# Erstellt am 2025-05-05
# Diese Datei definiert die Logik für den Bike Details DocType
# - Verwaltet Fahrradinformationen für Kunden
# - Integriert mit Workshop Orders und Customer-Objekten

import frappe
from frappe import _
from frappe.model.document import Document

class BikeDetails(Document):
    def validate(self):
        self.validate_owner()
        self.set_title()
        
    def validate_owner(self):
        # Überprüfe, ob der Besitzer existiert
        if self.owner_type == "Customer" and self.owner:
            customer = frappe.db.exists("Customer", self.owner)
            if not customer:
                frappe.throw(_("Customer {0} does not exist").format(self.owner))
                
    def set_title(self):
        """Setze einen aussagekräftigen Titel für das Fahrrad"""
        if self.bike_brand and self.bike_model:
            if self.year:
                self.title = f"{self.year} {self.bike_brand} {self.bike_model}"
            else:
                self.title = f"{self.bike_brand} {self.bike_model}"
        elif self.bike_brand:
            self.title = self.bike_brand
        else:
            self.title = "Unnamed Bike"
            
        # Füge die Rahmennummer hinzu, falls vorhanden
        if self.frame_number:
            self.title += f" ({self.frame_number})"
    
    def get_service_history(self):
        """Ruft den Serviceverlauf für dieses Fahrrad ab"""
        workshop_orders = frappe.get_all(
            "Workshop Order",
            filters={"bike": self.name},
            fields=["name", "status", "start_date", "completion_date"]
        )
        
        return workshop_orders
    
    def get_total_service_cost(self):
        """Berechnet die Gesamtkosten für Wartungen dieses Fahrrads"""
        result = frappe.db.sql("""
            SELECT SUM(grand_total) as total_cost
            FROM `tabWorkshop Order`
            WHERE bike = %s AND status = 'Delivered'
        """, self.name, as_dict=True)
        
        return result[0].total_cost if result and result[0].total_cost else 0
    
    def create_qr_code(self):
        """Erstellt einen QR-Code für die Fahrradidentifikation"""
        import qrcode
        import io
        import base64
        from PIL import Image
        
        # QR-Code-Inhalt (Fahrrad-ID und grundlegende Informationen)
        qr_data = f"BikeID:{self.name}\nBrand:{self.bike_brand}\nModel:{self.bike_model}\nFrame:{self.frame_number}"
        
        # QR-Code erstellen
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        # In Base64 konvertieren
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return qr_base64
