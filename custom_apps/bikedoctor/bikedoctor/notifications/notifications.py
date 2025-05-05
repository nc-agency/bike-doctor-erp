# -*- coding: utf-8 -*-
# bike.doctor ERP - Notifications Module
# 
# Erstellt: 05.05.2025
# Änderungen:
# - Initiale Erstellung des Notifications Moduls für bike.doctor
# - Implementierung der E-Mail- und SMS-Benachrichtigungsfunktionen

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import now, nowdate, get_url, get_datetime
import json

def get_notification_config():
    """
    Liefert die Benachrichtigungskonfiguration für die bike.doctor App
    Wird von ERPNext verwendet, um Benachrichtigungen im Desk anzuzeigen
    
    Returns:
        dict: Benachrichtigungskonfiguration
    """
    return {
        "for_doctype": {
            "Bicycle Repair": {
                "status": ["in", ["Eingegangen", "In Arbeit", "Wartend"]]
            },
            "Bicycle": {
                "status": ["in", ["In Reparatur"]]
            },
            "Item": {
                "is_stock_item": 1,
                "disabled": 0,
                "has_variants": 0,
                "re_order_level": [">", 0],
                "projected_qty": ["<", "re_order_level"],
                "item_group": ["like", "%Fahrr%"]
            }
        },
        "for_module_doctypes": {
            "Bikedoctor": ["Bicycle", "Bicycle Repair", "Bicycle Component"]
        }
    }

@frappe.whitelist()
def notify_customer(bicycle_repair, subject, message, send_email=1, send_sms=0):
    """
    Benachrichtigt den Kunden über den Status einer Fahrradreparatur
    
    Args:
        bicycle_repair (str): ID der Fahrradreparatur
        subject (str): Betreff der Nachricht
        message (str): Inhalt der Nachricht
        send_email (int, optional): E-Mail senden (1 oder 0). Standard ist 1.
        send_sms (int, optional): SMS senden (1 oder 0). Standard ist 0.
    
    Returns:
        dict: Ergebnis der Benachrichtigung
    """
    # Berechtigung prüfen
    if not frappe.has_permission("Bicycle Repair", "write", bicycle_repair):
        frappe.throw(_("Keine Berechtigung zum Benachrichtigen des Kunden"))
    
    # In boolesche Werte umwandeln
    send_email = bool(int(send_email))
    send_sms = bool(int(send_sms))
    
    if not (send_email or send_sms):
        frappe.throw(_("Wählen Sie mindestens eine Benachrichtigungsmethode aus"))
    
    # Fahrradreparatur abrufen
    repair = frappe.get_doc("Bicycle Repair", bicycle_repair)
    
    # Ergebnis-Dictionary initialisieren
    result = {"email_sent": False, "sms_sent": False}
    
    # Prüfen, ob ein Kunde zugeordnet ist
    if not repair.customer:
        frappe.throw(_("Dieser Reparatur ist kein Kunde zugeordnet"))
    
    # E-Mail senden, wenn aktiviert
    if send_email:
        customer_email = frappe.db.get_value("Customer", repair.customer, "email_id")
        
        if not customer_email:
            frappe.msgprint(_("Kunde hat keine E-Mail-Adresse hinterlegt"))
        else:
            # E-Mail-Vorlage vorbereiten
            email_args = {
                "recipients": [customer_email],
                "sender": frappe.db.get_value("Email Account", {"default_outgoing": 1}, "email_id") or "noreply@bike.doctor",
                "subject": subject,
                "message": message,
                "reference_doctype": "Bicycle Repair",
                "reference_name": bicycle_repair,
                "reply_to": frappe.db.get_value("Email Account", {"default_outgoing": 1}, "email_id") or "noreply@bike.doctor"
            }
            
            # Fahrradreparatur-Link hinzufügen
            repair_url = get_url(f"/desk#Form/Bicycle%20Repair/{bicycle_repair}")
            email_args["message"] += f"\n\n<a href='{repair_url}'>{_('Reparaturdetails anzeigen')}</a>"
            
            # E-Mail senden
            try:
                frappe.sendmail(**email_args)
                result["email_sent"] = True
            except Exception as e:
                frappe.log_error(f"Fehler beim Senden der E-Mail an {customer_email}: {str(e)}")
                frappe.msgprint(_("E-Mail konnte nicht gesendet werden: {0}").format(str(e)))
    
    # SMS senden, wenn aktiviert
    if send_sms:
        customer_mobile = frappe.db.get_value("Customer", repair.customer, "mobile_no")
        
        if not customer_mobile:
            frappe.msgprint(_("Kunde hat keine Mobilnummer hinterlegt"))
        else:
            # SMS senden, wenn SMS-Gateway konfiguriert ist
            try:
                from frappe.core.doctype.sms_settings.sms_settings import send_sms
                
                # Nur Text, keine HTML-Tags
                sms_message = frappe.utils.strip_html(message)
                
                # Auf maximale SMS-Länge beschränken
                if len(sms_message) > 160:
                    sms_message = sms_message[:157] + "..."
                
                send_sms([customer_mobile], sms_message)
                result["sms_sent"] = True
            except Exception as e:
                frappe.log_error(f"Fehler beim Senden der SMS an {customer_mobile}: {str(e)}")
                frappe.msgprint(_("SMS konnte nicht gesendet werden: {0}").format(str(e)))
    
    # Kommunikation in der Kundenhistorie speichern
    communication = frappe.get_doc({
        "doctype": "Communication",
        "communication_type": "Automated",
        "communication_medium": "Email" if send_email else "SMS",
        "subject": subject,
        "content": message,
        "status": "Linked",
        "sent_or_received": "Sent",
        "reference_doctype": "Bicycle Repair",
        "reference_name": bicycle_repair
    })
    
    communication.insert(ignore_permissions=True)
    
    # Kommentar zur Fahrradreparatur hinzufügen
    frappe.get_doc({
        "doctype": "Comment",
        "comment_type": "Info",
        "reference_doctype": "Bicycle Repair",
        "reference_name": bicycle_repair,
        "content": _("Kunde benachrichtigt:") + f" {subject}"
    }).insert(ignore_permissions=True)
    
    return result

@frappe.whitelist()
def send_maintenance_reminder(bicycle, message, send_email=1, send_sms=0):
    """
    Sendet eine Wartungserinnerung an den Kunden für ein bestimmtes Fahrrad
    
    Args:
        bicycle (str): ID des Fahrrads
        message (str): Inhalt der Nachricht
        send_email (int, optional): E-Mail senden (1 oder 0). Standard ist 1.
        send_sms (int, optional): SMS senden (1 oder 0). Standard ist 0.
    
    Returns:
        dict: Ergebnis der Benachrichtigung
    """
    # Berechtigung prüfen
    if not frappe.has_permission("Bicycle", "write", bicycle):
        frappe.throw(_("Keine Berechtigung zum Senden einer Wartungserinnerung"))
    
    # In boolesche Werte umwandeln
    send_email = bool(int(send_email))
    send_sms = bool(int(send_sms))
    
    if not (send_email or send_sms):
        frappe.throw(_("Wählen Sie mindestens eine Benachrichtigungsmethode aus"))
    
    # Fahrrad abrufen
    bike = frappe.get_doc("Bicycle", bicycle)
    
    # Prüfen, ob ein Kunde zugeordnet ist
    if not bike.customer:
        frappe.throw(_("Diesem Fahrrad ist kein Kunde zugeordnet"))
    
    # Betreff der Erinnerung
    subject = _("Wartungserinnerung für {0}").format(bike.bicycle_name)
    
    # Ergebnis-Dictionary initialisieren
    result = {"email_sent": False, "sms_sent": False}
    
    # E-Mail senden, wenn aktiviert
    if send_email:
        customer_email = frappe.db.get_value("Customer", bike.customer, "email_id")
        
        if not customer_email:
            frappe.msgprint(_("Kunde hat keine E-Mail-Adresse hinterlegt"))
        else:
            # E-Mail-Vorlage vorbereiten
            email_args = {
                "recipients": [customer_email],
                "sender": frappe.db.get_value("Email Account", {"default_outgoing": 1}, "email_id") or "noreply@bike.doctor",
                "subject": subject,
                "message": message,
                "reference_doctype": "Bicycle",
                "reference_name": bicycle
            }
            
            # Fahrrad-Link hinzufügen
            bike_url = get_url(f"/desk#Form/Bicycle/{bicycle}")
            email_args["message"] += f"\n\n<a href='{bike_url}'>{_('Fahrraddetails anzeigen')}</a>"
            
            # Button zum Terminbuchen hinzufügen, wenn Online-Terminbuchung aktiviert ist
            if frappe.db.get_single_value("Bikedoctor Settings", "enable_online_booking"):
                booking_url = get_url("/book-appointment?bicycle=" + bicycle)
                email_args["message"] += f"\n\n<a href='{booking_url}' class='btn btn-primary'>{_('Termin buchen')}</a>"
            
            # E-Mail senden
            try:
                frappe.sendmail(**email_args)
                result["email_sent"] = True
            except Exception as e:
                frappe.log_error(f"Fehler beim Senden der Wartungserinnerung an {customer_email}: {str(e)}")
                frappe.msgprint(_("E-Mail konnte nicht gesendet werden: {0}").format(str(e)))
    
    # SMS senden, wenn aktiviert
    if send_sms:
        customer_mobile = frappe.db.get_value("Customer", bike.customer, "mobile_no")
        
        if not customer_mobile:
            frappe.msgprint(_("Kunde hat keine Mobilnummer hinterlegt"))
        else:
            # SMS senden, wenn SMS-Gateway konfiguriert ist
            try:
                from frappe.core.doctype.sms_settings.sms_settings import send_sms
                
                # Nur Text, keine HTML-Tags
                sms_message = frappe.utils.strip_html(message)
                
                # Auf maximale SMS-Länge beschränken
                if len(sms_message) > 160:
                    sms_message = sms_message[:157] + "..."
                
                send_sms([customer_mobile], sms_message)
                result["sms_sent"] = True
            except Exception as e:
                frappe.log_error(f"Fehler beim Senden der SMS an {customer_mobile}: {str(e)}")
                frappe.msgprint(_("SMS konnte nicht gesendet werden: {0}").format(str(e)))
    
    # Kommunikation in der Kundenhistorie speichern
    communication = frappe.get_doc({
        "doctype": "Communication",
        "communication_type": "Automated",
        "communication_medium": "Email" if send_email else "SMS",
        "subject": subject,
        "content": message,
        "status": "Linked",
        "sent_or_received": "Sent",
        "reference_doctype": "Bicycle",
        "reference_name": bicycle
    })
    
    communication.insert(ignore_permissions=True)
    
    # Kommentar zum Fahrrad hinzufügen
    frappe.get_doc({
        "doctype": "Comment",
        "comment_type": "Info",
        "reference_doctype": "Bicycle",
        "reference_name": bicycle,
        "content": _("Wartungserinnerung gesendet")
    }).insert(ignore_permissions=True)
    
    return result