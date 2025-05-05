# -*- coding: utf-8 -*-
# bike.doctor App für ERPNext - Hooks-Datei
# 
# Erstellt: 04.05.2025
# Änderungen:
# - Initiale Erstellung der hooks.py für die Integration der bike.doctor-App in ERPNext
#
# Diese Datei definiert Hooks, die ERPNext nutzt, um die bike.doctor-App zu integrieren.

from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "bikedoctor"
app_title = "bike.doctor"
app_publisher = "bike.doctor Team"
app_description = "ERPNext-Anwendung für die Fahrradwerkstatt bike.doctor"
app_icon = "octicon octicon-tools"
app_color = "#5BC0DE"
app_email = "info@bike.doctor"
app_license = "MIT"

# DocTypes
# --------
fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
                    "Customer-bicycle_owner"
                ]
            ]
        ]
    }
]

# Includes in <head>
# ------------------
# include js, css files in header of desk.html
app_include_css = "/assets/bikedoctor/css/bikedoctor.css"
app_include_js = "/assets/bikedoctor/js/bikedoctor.js"

# include js, css files in header of web template
web_include_css = "/assets/bikedoctor/css/bikedoctor-web.css"
web_include_js = "/assets/bikedoctor/js/bikedoctor-web.js"

# Home Pages
# ----------
# application home page (will override Website Settings)
home_page = "bikedoctor-home"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

notification_config = "bikedoctor.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
    "Bicycle": "bikedoctor.permissions.get_bicycle_permission_query_conditions",
    "Bicycle Repair": "bikedoctor.permissions.get_bicycle_repair_permission_query_conditions"
}

has_permission = {
    "Bicycle": "bikedoctor.permissions.has_bicycle_permission",
    "Bicycle Repair": "bikedoctor.permissions.has_bicycle_repair_permission"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Sales Invoice": {
        "on_submit": "bikedoctor.bicycle_management.on_sales_invoice_submit",
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "bikedoctor.tasks.daily"
    ],
    "weekly": [
        "bikedoctor.tasks.weekly"
    ],
    "monthly": [
        "bikedoctor.tasks.monthly"
    ]
}
