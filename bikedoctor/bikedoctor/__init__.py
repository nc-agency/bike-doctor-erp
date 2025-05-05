# __init__.py für bike.doctor ERPNext-Erweiterung
# Erstellt am 2025-05-05
# App-Metadaten und Version

__version__ = '0.0.1'

app_name = "bikedoctor"
app_title = "BikeDoctor Workshop Management"
app_publisher = "bike.doctor"
app_description = "Integrierte Werkstattverwaltung für Fahrradwerkstätten"
app_email = "test@test.com"
app_license = "MIT"

# Einstellungen für das Frontend
app_icon = "octicon octicon-tools"
app_color = "#4287f5"

# Hooks für ERPNext-Integration
app_include_js = "/assets/bikedoctor/js/bikedoctor.min.js"
app_include_css = "/assets/bikedoctor/css/bikedoctor.css"

# Dokumenttypen, die diese App erstellt
fixtures = [
    {"dt": "Custom Field", "filters": [["app_name", "=", "bikedoctor"]]},
    {"dt": "Property Setter", "filters": [["app_name", "=", "bikedoctor"]]},
    {"dt": "Role", "filters": [["name", "in", ["Workshop Manager", "Workshop Technician"]]]},
]
