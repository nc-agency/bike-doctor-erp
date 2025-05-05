// bikedoctor.js für bike.doctor ERPNext-Erweiterung
// Erstellt am 2025-05-05
// Diese Datei enthält die JavaScript-Funktionen für die bike.doctor-App
// - Hauptdatei für allgemeine Frontend-Funktionalität
// - Wird in allen ERPNext-Seiten eingebunden

frappe.provide("bikedoctor");

// Globale BikeDoctor-Namespace-Konfiguration
bikedoctor = {
    // App-Einstellungen
    settings: {
        moduleIcon: "octicon octicon-tools",
        moduleColor: "#4287f5",
        appName: "BikeDoctor Workshop Management"
    },
    
    // Initialisierung der App nach dem Laden
    init: function() {
        console.log("BikeDoctor Workshop Management initialized");
        // Weitere Initialisierungslogik
    },
    
    // Hilfsfunktionen für die Werkstattverwaltung
    workshop: {
        calculateServiceCost: function(hours, rate) {
            return hours * rate;
        },
        
        getTotalPartsCost: function(parts) {
            let total = 0;
            parts.forEach(part => {
                total += part.amount;
            });
            return total;
        },
        
        formatDate: function(date) {
            if (!date) return "";
            return frappe.datetime.str_to_user(date);
        },
        
        refreshJobCardStatus: function(jobCardName) {
            if (!jobCardName) return;
            
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Workshop Job Card",
                    name: jobCardName
                },
                callback: function(response) {
                    if (response.message) {
                        let doc = response.message;
                        let message = `Job Card ${doc.name} - Status: ${doc.status}`;
                        frappe.show_alert(message, 5);
                    }
                }
            });
        }
    }
};

// Initialisierungsfunktion beim Laden
$(document).ready(function() {
    bikedoctor.init();
});
