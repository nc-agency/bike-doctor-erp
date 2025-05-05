# desktop.py für bike.doctor ERPNext-Erweiterung 
# Erstellt am 2025-05-05
# Diese Datei definiert, wie die App im ERPNext-Desktop angezeigt wird
# - Fügt Werkstatt-Bereich zum ERPNext-Desktop hinzu
# - Definiert Icon und Farbe für bessere Benutzerführung

from frappe import _

def get_data():
	return [
		{
			"module_name": "BikeDoctor Workshop Management",
			"color": "#4287f5",
			"icon": "octicon octicon-tools",
			"type": "module",
			"label": _("Bike Workshop")
		}
	]
