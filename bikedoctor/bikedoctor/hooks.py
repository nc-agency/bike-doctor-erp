# hooks.py für bike.doctor ERPNext-Erweiterung
# Erstellt am 2025-05-05
# Definiert alle ERPNext-Hooks für die Integration der bikedoctor-App
# - Erstellt Workshop-spezifische DocTypes
# - Erweitert ERPNext um Workshop-Funktionalität
# - Integriert Frontend-Komponenten

from . import __version__ as app_version

app_name = "bikedoctor"
app_title = "BikeDoctor Workshop Management"
app_publisher = "bike.doctor"
app_description = "Integrierte Werkstattverwaltung für Fahrradwerkstätten"
app_email = "test@test.com"
app_license = "MIT"

# Hooks für ERPNext-Integration
fixtures = [
    {"dt": "Custom Field", "filters": [["app_name", "=", "bikedoctor"]]},
    {"dt": "Property Setter", "filters": [["app_name", "=", "bikedoctor"]]},
    {"dt": "Role", "filters": [["name", "in", ["Workshop Manager", "Workshop Technician"]]]},
]

# DocTypes, die diese App erstellt
doctype_js = {
    "Customer": "public/js/customer.js",
    "Item": "public/js/item.js",
    "Sales Invoice": "public/js/sales_invoice.js"
}

# Benutzerrollen, die diese App definiert
roles = [
    {"role": "Workshop Manager", "desk_access": 1},
    {"role": "Workshop Technician", "desk_access": 1}
]

# Frontend-Ressourcen
app_include_css = [
    "/assets/bikedoctor/css/bikedoctor.css"
]

app_include_js = [
    "/assets/bikedoctor/js/bikedoctor.js"
]

website_route_rules = [
    {"from_route": "/workshop", "to_route": "Workshop"},
    {"from_route": "/workshop/<path:name>", "to_route": "workshop_details"}
]

scheduler_events = {
    "daily": [
        "bikedoctor.bikedoctor.tasks.daily"
    ],
    "weekly": [
        "bikedoctor.bikedoctor.tasks.weekly"
    ]
}

# Einstellungsseite
website_context = {
    "favicon": "/assets/bikedoctor/images/favicon.ico",
    "splash_image": "/assets/bikedoctor/images/splash.png"
}
