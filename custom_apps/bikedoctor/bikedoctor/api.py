# -*- coding: utf-8 -*-
# bike.doctor ERP - API-Funktionen
# 
# Erstellt: 05.05.2025
# Änderungen:
# - Initiale Erstellung der API-Funktionen für die bike.doctor-App
# - Implementierung von QR-Code-Generierung und anderen API-Funktionen

from __future__ import unicode_literals
import frappe
from frappe import _
import json
import io
import base64
import qrcode
from PIL import Image, ImageDraw, ImageFont
from frappe.utils import get_url, format_date, nowdate, add_days, cint

@frappe.whitelist()
def generate_qr_code(data):
    """
    Generiert einen QR-Code für ein Fahrrad mit eingebettetem Logo
    
    Args:
        data (str): JSON-Zeichenfolge mit Fahrraddaten
    
    Returns:
        str: Base64-kodiertes QR-Code-Bild
    """
    try:
        # QR-Code mit Fahrraddaten erstellen
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # QR-Code in Bild umwandeln
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')
        
        # Bildgröße ermitteln
        width, height = qr_img.size
        
        # Text "bike.doctor" auf den QR-Code zeichnen
        draw = ImageDraw.Draw(qr_img)
        
        # Text in der Mitte platzieren
        text = "bike.doctor"
        
        # Versuchen, eine Schriftart zu laden, oder Standardschrift verwenden
        try:
            font = ImageFont.truetype("Arial", 20)
        except IOError:
            font = ImageFont.load_default()
        
        # Textgröße berechnen
        text_width, text_height = draw.textsize(text, font=font)
        text_position = ((width - text_width) // 2, (height - text_height) // 2)
        
        # Text mit weißem Hintergrund zeichnen
        text_box_size = (text_width + 10, text_height + 10)
        text_box_position = (text_position[0] - 5, text_position[1] - 5)
        draw.rectangle([text_box_position, (text_box_position[0] + text_box_size[0], text_box_position[1] + text_box_size[1])], fill="white")
        
        # Text zeichnen
        draw.text(text_position, text, fill="black", font=font)
        
        # QR-Code als Base64-Zeichenfolge zurückgeben
        buffer = io.BytesIO()
        qr_img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return "data:image/png;base64," + img_str
        
    except Exception as e:
        frappe.log_error(f"QR-Code-Generierungsfehler: {str(e)}")
        return None

@frappe.whitelist()
def get_bicycle_details(bicycle):
    """
    Holt detaillierte Informationen zu einem Fahrrad
    
    Args:
        bicycle (str): Fahrrad-ID
    
    Returns:
        dict: Detaillierte Fahrraddaten
    """
    try:
        bike = frappe.get_doc("Bicycle", bicycle)
        
        # Sicherstellen, dass Berechtigungen vorhanden sind
        bike.check_permission("read")
        
        # Aktive Reparaturen holen
        active_repairs = frappe.get_all("Bicycle Repair", 
            filters={"bicycle": bicycle, "status": ["in", ["Eingegangen", "In Arbeit", "Wartend"]]},
            fields=["name", "status", "description", "repair_date", "estimated_completion_date"])
        
        # Letzte abgeschlossene Reparatur holen
        last_repair = frappe.get_all("Bicycle Repair", 
            filters={"bicycle": bicycle, "status": "Abgeschlossen"},
            fields=["name", "completion_date", "description"],
            order_by="completion_date desc",
            limit=1)
        
        # Komponenten formatieren
        components = []
        if bike.components:
            for component in bike.components:
                components.append({
                    "type": component.component_type,
                    "brand": component.brand,
                    "model": component.model,
                    "condition": component.condition,
                    "installation_date": format_date(component.installation_date) if component.installation_date else None
                })
        
        # Ergebnis zusammenstellen
        result = {
            "bicycle": {
                "name": bike.name,
                "bicycle_name": bike.bicycle_name,
                "brand": bike.brand,
                "model": bike.model,
                "type": bike.type,
                "year": bike.year,
                "color": bike.color,
                "serial_number": bike.serial_number,
                "frame_number": bike.frame_number,
                "wheel_size": bike.wheel_size,
                "weight": bike.weight,
                "status": bike.status,
                "purchase_date": format_date(bike.purchase_date) if bike.purchase_date else None,
                "last_service_date": format_date(bike.last_service_date) if bike.last_service_date else None,
                "warranty_expiry": format_date(bike.warranty_expiry) if bike.warranty_expiry else None,
                "value": bike.value,
                "image_url": bike.bicycle_image
            },
            "customer": {
                "name": bike.customer,
                "customer_name": bike.customer_name
            },
            "components": components,
            "active_repairs": active_repairs,
            "last_repair": last_repair[0] if last_repair else None,
            "total_repairs": frappe.db.count("Bicycle Repair", {"bicycle": bicycle})
        }
        
        return result
        
    except Exception as e:
        frappe.log_error(f"Fehler beim Abrufen der Fahrraddetails: {str(e)}")
        return None

@frappe.whitelist()
def get_repair_status(repair):
    """
    Ruft den Status einer Reparatur ab
    
    Args:
        repair (str): Reparatur-ID
    
    Returns:
        dict: Reparaturstatus und Details
    """
    try:
        repair_doc = frappe.get_doc("Bicycle Repair", repair)
        
        # Berechtigungen überprüfen
        repair_doc.check_permission("read")
        
        # Verwendete Teile abrufen
        parts = []
        if repair_doc.parts:
            for part in repair_doc.parts:
                parts.append({
                    "item_code": part.item_code,
                    "item_name": part.item_name,
                    "quantity": part.quantity,
                    "rate": part.rate,
                    "amount": part.amount
                })
        
        # Status zusammenstellen
        result = {
            "repair": {
                "name": repair_doc.name,
                "status": repair_doc.status,
                "description": repair_doc.description,
                "diagnostics": repair_doc.diagnostics,
                "repair_date": format_date(repair_doc.repair_date),
                "estimated_completion_date": format_date(repair_doc.estimated_completion_date) if repair_doc.estimated_completion_date else None,
                "completion_date": format_date(repair_doc.completion_date) if repair_doc.completion_date else None,
                "priority": repair_doc.priority,
                "is_maintenance": repair_doc.is_maintenance,
                "labor_cost": repair_doc.labor_cost,
                "total_cost": repair_doc.total_cost,
                "invoice": repair_doc.invoice
            },
            "bicycle": {
                "name": repair_doc.bicycle,
                "bicycle_name": repair_doc.bicycle_name
            },
            "customer": {
                "name": repair_doc.customer,
                "customer_name": repair_doc.customer_name
            },
            "parts": parts,
            "technician": repair_doc.technician
        }
        
        return result
        
    except Exception as e:
        frappe.log_error(f"Fehler beim Abrufen des Reparaturstatus: {str(e)}")
        return None

@frappe.whitelist()
def schedule_maintenance_reminder():
    """
    Geplante Funktion zum Senden von Wartungserinnerungen
    Wird über den Scheduler regelmäßig aufgerufen
    
    Returns:
        int: Anzahl der gesendeten Erinnerungen
    """
    # Definition, wann Wartungen fällig sind (in Tagen seit der letzten Wartung)
    maintenance_intervals = {
        "City": 365,        # Stadtrad: jährlich
        "Mountain Bike": 180,  # MTB: alle 6 Monate
        "Rennrad": 180,     # Rennrad: alle 6 Monate
        "Trekking": 270,    # Trekking: alle 9 Monate
        "E-Bike": 120,      # E-Bike: alle 4 Monate
        "Kinderrad": 365,   # Kinderrad: jährlich
        "Lastenrad": 120,   # Lastenrad: alle 4 Monate
        "Sonstiges": 270    # Sonstige: alle 9 Monate
    }
    
    today = nowdate()
    count = 0
    
    # Suche nach Fahrrädern mit fälliger Wartung
    bikes_needing_maintenance = []
    
    for bike_type, interval in maintenance_intervals.items():
        # Fahrräder des jeweiligen Typs suchen
        bikes = frappe.get_all("Bicycle", 
            filters={
                "type": bike_type, 
                "status": ["!=", "Ausrangiert"]
            },
            fields=["name", "bicycle_name", "customer", "customer_name", "last_service_date"]
        )
        
        for bike in bikes:
            # Prüfen, ob letzte Wartung zu lange her ist
            if bike.last_service_date:
                last_service = frappe.utils.getdate(bike.last_service_date)
                days_since_service = frappe.utils.date_diff(today, last_service)
                
                if days_since_service >= interval:
                    # Prüfen, ob bereits eine Erinnerung innerhalb der letzten 30 Tage gesendet wurde
                    recent_reminder = frappe.db.exists("Communication", {
                        "reference_doctype": "Bicycle",
                        "reference_name": bike.name,
                        "communication_type": "Automated",
                        "communication_medium": "Email",
                        "subject": ["like", "%Wartungserinnerung%"],
                        "creation": [">", add_days(today, -30)]
                    })
                    
                    if not recent_reminder:
                        bikes_needing_maintenance.append(bike)
            else:
                # Keine Wartung in der Vergangenheit
                purchase_date = frappe.db.get_value("Bicycle", bike.name, "purchase_date")
                if purchase_date:
                    purchase = frappe.utils.getdate(purchase_date)
                    days_since_purchase = frappe.utils.date_diff(today, purchase)
                    
                    # Wenn das Fahrrad länger als der Wartungsintervall im Besitz ist
                    if days_since_purchase >= interval:
                        bikes_needing_maintenance.append(bike)
    
    # Erinnerungen senden
    for bike in bikes_needing_maintenance:
        try:
            subject = f"Wartungserinnerung für {bike.bicycle_name}"
            message = f"""Sehr geehrte(r) {bike.customer_name},

Ihr Fahrrad **{bike.bicycle_name}** ist für eine Wartung fällig.

Bitte vereinbaren Sie einen Termin in unserer Werkstatt, um die optimale Leistung und Sicherheit Ihres Fahrrads zu gewährleisten.

Mit freundlichen Grüßen,
Ihr bike.doctor Team"""

            # E-Mail-Kommunikation erstellen
            communication = frappe.get_doc({
                "doctype": "Communication",
                "subject": subject,
                "content": message,
                "communication_type": "Automated",
                "communication_medium": "Email",
                "sent_or_received": "Sent",
                "reference_doctype": "Bicycle",
                "reference_name": bike.name,
                "sender": frappe.db.get_value("Email Account", {"default_outgoing": 1}, "email_id") or "noreply@bike.doctor",
                "recipients": frappe.db.get_value("Customer", bike.customer, "email_id")
            })
            
            communication.insert(ignore_permissions=True)
            
            # E-Mail senden
            communication.send_email()
            
            count += 1
            
        except Exception as e:
            frappe.log_error(f"Fehler beim Senden der Wartungserinnerung für Fahrrad {bike.name}: {str(e)}")
    
    return count
