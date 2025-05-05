# setup_roles_and_permissions.py
# Erstellt am: 2025-05-05
# Dieses Skript richtet die notwendigen Rollen und Berechtigungen für die bike.doctor ERP-App ein
# Es sollte nur einmal nach der Installation ausgeführt werden

import frappe
from frappe.permissions import add_permission

def setup_roles():
    """
    Erstellt die Rollen für das Workshop-Modul
    """
    # Workshop Manager Rolle
    if not frappe.db.exists("Role", "Workshop Manager"):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": "Workshop Manager",
            "desk_access": 1,
            "is_custom": 1,
            "disabled": 0,
            "two_factor_auth": 0
        }).insert(ignore_permissions=True)
        print("Rolle 'Workshop Manager' erstellt")
    
    # Workshop Technician Rolle
    if not frappe.db.exists("Role", "Workshop Technician"):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": "Workshop Technician",
            "desk_access": 1,
            "is_custom": 1,
            "disabled": 0,
            "two_factor_auth": 0
        }).insert(ignore_permissions=True)
        print("Rolle 'Workshop Technician' erstellt")
    
    # Workshop Reception Rolle
    if not frappe.db.exists("Role", "Workshop Reception"):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": "Workshop Reception",
            "desk_access": 1,
            "is_custom": 1,
            "disabled": 0,
            "two_factor_auth": 0
        }).insert(ignore_permissions=True)
        print("Rolle 'Workshop Reception' erstellt")

def setup_permissions():
    """
    Konfiguriert die Berechtigungen für Workshop-DocTypes
    """
    doctypes = ["Workshop Order", "Workshop Job Card", "Bike Details", "Bike Brand"]
    
    # Workshop Manager - volle Berechtigungen
    for dt in doctypes:
        add_permission(dt, "Workshop Manager", 0, permission_type="read")
        add_permission(dt, "Workshop Manager", 0, permission_type="write")
        add_permission(dt, "Workshop Manager", 0, permission_type="create")
        add_permission(dt, "Workshop Manager", 0, permission_type="delete")
        add_permission(dt, "Workshop Manager", 0, permission_type="submit")
        add_permission(dt, "Workshop Manager", 0, permission_type="cancel")
        add_permission(dt, "Workshop Manager", 0, permission_type="report")
    
    # Workshop Technician - eingeschränkte Berechtigungen
    add_permission("Workshop Job Card", "Workshop Technician", 0, permission_type="read")
    add_permission("Workshop Job Card", "Workshop Technician", 0, permission_type="write")
    add_permission("Workshop Job Card", "Workshop Technician", 0, permission_type="submit")
    add_permission("Bike Details", "Workshop Technician", 0, permission_type="read")
    
    # Workshop Reception - Annahme/Ausgabe Berechtigungen
    add_permission("Workshop Order", "Workshop Reception", 0, permission_type="read")
    add_permission("Workshop Order", "Workshop Reception", 0, permission_type="write")
    add_permission("Workshop Order", "Workshop Reception", 0, permission_type="create")
    add_permission("Workshop Order", "Workshop Reception", 0, permission_type="submit")
    add_permission("Bike Details", "Workshop Reception", 0, permission_type="read")
    add_permission("Bike Details", "Workshop Reception", 0, permission_type="write")
    add_permission("Bike Details", "Workshop Reception", 0, permission_type="create")

def create_demo_users():
    """
    Erstellt Demo-Benutzer mit den entsprechenden Rollen
    """
    # Workshop Manager
    if not frappe.db.exists("User", "workshop.manager@bikedoctor.test"):
        user = frappe.get_doc({
            "doctype": "User",
            "email": "workshop.manager@bikedoctor.test",
            "first_name": "Workshop",
            "last_name": "Manager",
            "enabled": 1,
            "username": "workshopmanager",
            "send_welcome_email": 0
        })
        user.append("roles", {"role": "Workshop Manager"})
        user.new_password = "BikeManager@123"
        user.insert(ignore_permissions=True)
        print("Benutzer 'Workshop Manager' erstellt")
    
    # Workshop Technician
    if not frappe.db.exists("User", "technician@bikedoctor.test"):
        user = frappe.get_doc({
            "doctype": "User",
            "email": "technician@bikedoctor.test",
            "first_name": "Workshop",
            "last_name": "Technician",
            "enabled": 1,
            "username": "technician",
            "send_welcome_email": 0
        })
        user.append("roles", {"role": "Workshop Technician"})
        user.new_password = "BikeTech@123"
        user.insert(ignore_permissions=True)
        print("Benutzer 'Workshop Technician' erstellt")
    
    # Workshop Reception
    if not frappe.db.exists("User", "reception@bikedoctor.test"):
        user = frappe.get_doc({
            "doctype": "User",
            "email": "reception@bikedoctor.test",
            "first_name": "Workshop",
            "last_name": "Reception",
            "enabled": 1,
            "username": "reception",
            "send_welcome_email": 0
        })
        user.append("roles", {"role": "Workshop Reception"})
        user.new_password = "BikeRec@123"
        user.insert(ignore_permissions=True)
        print("Benutzer 'Workshop Reception' erstellt")

def execute():
    """
    Führt das komplette Setup aus
    """
    print("Starte Setup für Benutzer und Berechtigungen...")
    setup_roles()
    setup_permissions()
    create_demo_users()
    frappe.db.commit()
    print("Setup für Benutzer und Berechtigungen abgeschlossen!")

if __name__ == "__main__":
    execute()