// customer.js für bike.doctor ERPNext-Erweiterung
// Erstellt am 2025-05-05
// Diese Datei erweitert die Kundenfunktionalität in ERPNext
// - Fügt Werkstattbezogene Felder zum Kundendokument hinzu
// - Verknüpft Kunden mit ihren Fahrrädern

frappe.ui.form.on('Customer', {
    refresh: function(frm) {
        // Füge einen Button hinzu, um Fahrräder für diesen Kunden anzuzeigen
        frm.add_custom_button(__('Bikes'), function() {
            frappe.route_options = {
                'owner': frm.doc.name
            };
            frappe.set_route('List', 'Bike Details');
        }, __('View'));
        
        // Füge einen Button hinzu, um einen Werkstattauftrag für diesen Kunden zu erstellen
        frm.add_custom_button(__('Workshop Order'), function() {
            frappe.new_doc('Workshop Order', {
                'customer': frm.doc.name,
                'customer_name': frm.doc.customer_name
            });
        }, __('Create'));
        
        // Füge einen Button hinzu, um den Werkstattverlauf für diesen Kunden anzuzeigen
        frm.add_custom_button(__('Workshop History'), function() {
            frappe.route_options = {
                'customer': frm.doc.name
            };
            frappe.set_route('List', 'Workshop Order');
        }, __('View'));
    },
    
    validate: function(frm) {
        // Zusätzliche Validierungslogik für Werkstattkunden
        console.log("Validating workshop customer data");
    }
});
