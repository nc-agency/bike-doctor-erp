# bikedoctor.py für bike.doctor ERPNext-Erweiterung
# Erstellt am 2025-05-05
# Diese Datei definiert die Module und Funktionen der bike.doctor Werkstattverwaltung
# - Organisation aller DocTypes und Berichte in sinnvolle Kategorien
# - Definition der Navigationsstruktur innerhalb des Moduls

from frappe import _

def get_data():
	return [
		{
			"label": _("Workshop Operations"),
			"icon": "fa fa-wrench",
			"items": [
				{
					"type": "doctype",
					"name": "Workshop Order",
					"label": _("Workshop Order"),
					"description": _("Manage workshop repair orders")
				},
				{
					"type": "doctype",
					"name": "Workshop Job Card",
					"label": _("Job Card"),
					"description": _("Track repairs and maintenance tasks")
				},
				{
					"type": "doctype",
					"name": "Bike Details",
					"label": _("Bike Details"),
					"description": _("Customer bike information")
				}
			]
		},
		{
			"label": _("Inventory"),
			"icon": "fa fa-archive",
			"items": [
				{
					"type": "doctype",
					"name": "Workshop Item",
					"label": _("Workshop Parts"),
					"description": _("Manage parts and components for repairs")
				},
				{
					"type": "doctype",
					"name": "Workshop Tool",
					"label": _("Workshop Tools"),
					"description": _("Manage specialty tools for bike repairs")
				}
			]
		},
		{
			"label": _("Setup"),
			"icon": "fa fa-cog",
			"items": [
				{
					"type": "doctype",
					"name": "Workshop Settings",
					"label": _("Workshop Settings"),
					"description": _("Configure workshop operations")
				},
				{
					"type": "doctype",
					"name": "Service Type",
					"label": _("Service Types"),
					"description": _("Define types of services offered")
				},
				{
					"type": "doctype",
					"name": "Bike Brand",
					"label": _("Bike Brands"),
					"description": _("Manage supported bike brands")
				}
			]
		},
		{
			"label": _("Reports"),
			"icon": "fa fa-list",
			"items": [
				{
					"type": "report",
					"name": "Workshop Efficiency",
					"doctype": "Workshop Job Card",
					"is_query_report": True
				},
				{
					"type": "report",
					"name": "Parts Usage Analysis",
					"doctype": "Workshop Item",
					"is_query_report": True
				},
				{
					"type": "report",
					"name": "Workshop Revenue",
					"doctype": "Workshop Order",
					"is_query_report": True
				}
			]
		}
	]
