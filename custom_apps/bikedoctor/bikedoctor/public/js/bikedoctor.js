/*
 * bike.doctor ERP - JavaScript-Funktionen
 * 
 * Erstellt: 05.05.2025
 * Änderungen:
 * - Initiale Erstellung der JavaScript-Funktionen für die bike.doctor-App
 * - Implementierung von Hilfsfunktionen für die Reparaturverwaltung
 */

frappe.provide("bikedoctor");

// Hauptmodul für bike.doctor-Funktionalitäten
bikedoctor = {
    // Initialisierung
    init: function() {
        // Eventhandler für Formulare registrieren
        bikedoctor.registerHandlers();
        
        // Benutzerdefinierte Dashboard-Widgets initialisieren
        if(frappe.router.current_route[0] === "dashboard") {
            bikedoctor.initDashboard();
        }
    },
    
    // Eventhandler registrieren
    registerHandlers: function() {
        // Handler für Fahrradformular
        frappe.ui.form.on("Bicycle", {
            refresh: function(frm) {
                bikedoctor.setupBicycleForm(frm);
            },
            
            // Automatisch Seriennummer generieren, wenn nicht vorhanden
            before_save: function(frm) {
                if(!frm.doc.serial_number && frm.doc.brand && frm.doc.model) {
                    // Seriennummer basierend auf Marke, Modell und Zeitstempel erstellen
                    let brand = frm.doc.brand.substring(0, 3).toUpperCase();
                    let model = frm.doc.model.substring(0, 3).toUpperCase();
                    let timestamp = Date.now().toString().substring(6);
                    frm.set_value('serial_number', `${brand}-${model}-${timestamp}`);
                }
            }
        });
        
        // Handler für Reparaturformular
        frappe.ui.form.on("Bicycle Repair", {
            refresh: function(frm) {
                bikedoctor.setupRepairForm(frm);
            },
            
            // Gesamtkosten neu berechnen, wenn sich Teile oder Arbeitskosten ändern
            parts_add: function(frm) {
                bikedoctor.calculateTotalCost(frm);
            },
            parts_remove: function(frm) {
                bikedoctor.calculateTotalCost(frm);
            },
            labor_cost: function(frm) {
                bikedoctor.calculateTotalCost(frm);
            }
        });
    },
    
    // Setup für das Fahrradformular
    setupBicycleForm: function(frm) {
        // Benutzerdefinierte Buttons für Fahrradformular
        if(!frm.is_new()) {
            // Button für QR-Code-Generierung
            frm.add_custom_button(__('QR-Code generieren'), function() {
                bikedoctor.generateQRCode(frm);
            });
            
            // Button für Reparaturhistorie
            frm.add_custom_button(__('Reparaturhistorie anzeigen'), function() {
                bikedoctor.showRepairHistory(frm);
            });
            
            // Button für neue Reparatur anlegen
            frm.add_custom_button(__('Neue Reparatur'), function() {
                bikedoctor.createNewRepair(frm);
            }, __('Aktionen'));
            
            // Button für Wartungserinnerung
            frm.add_custom_button(__('Wartungserinnerung senden'), function() {
                bikedoctor.sendMaintenanceReminder(frm);
            }, __('Aktionen'));
        }
    },
    
    // Setup für das Reparaturformular
    setupRepairForm: function(frm) {
        // Benutzerdefinierte Buttons für Reparaturformular
        if(!frm.is_new()) {
            // Button für Statusaktualisierung
            frm.add_custom_button(__('Status aktualisieren'), function() {
                bikedoctor.updateRepairStatus(frm);
            });
            
            // Button für Kundennachricht
            frm.add_custom_button(__('Kunde benachrichtigen'), function() {
                bikedoctor.notifyCustomer(frm);
            }, __('Kommunikation'));
            
            // Button für Rechnung erstellen
            if(frm.doc.status === "Abgeschlossen" && !frm.doc.invoice) {
                frm.add_custom_button(__('Rechnung erstellen'), function() {
                    bikedoctor.createInvoice(frm);
                }, __('Abrechnung'));
            }
        }
    },
    
    // Berechnet die Gesamtkosten einer Reparatur
    calculateTotalCost: function(frm) {
        let total = 0;
        
        // Teilekosten summieren
        if(frm.doc.parts && frm.doc.parts.length) {
            frm.doc.parts.forEach(function(part) {
                total += (part.rate || 0) * (part.quantity || 0);
            });
        }
        
        // Arbeitskosten hinzufügen
        if(frm.doc.labor_cost) {
            total += frm.doc.labor_cost;
        }
        
        frm.set_value('total_cost', total);
    },
    
    // Generiert einen QR-Code für ein Fahrrad
    generateQRCode: function(frm) {
        // QR-Code-Daten vorbereiten
        let qrData = {
            bicycle_id: frm.doc.name,
            brand: frm.doc.brand,
            model: frm.doc.model,
            serial_number: frm.doc.serial_number
        };
        
        // QR-Code generieren und anzeigen
        let qrDataString = JSON.stringify(qrData);
        
        frappe.show_alert({
            message: __('QR-Code wird generiert...'),
            indicator: 'blue'
        });
        
        // QR-Code-Generierungs-API aufrufen
        frappe.call({
            method: "bikedoctor.api.generate_qr_code",
            args: {
                data: qrDataString
            },
            callback: function(r) {
                if(r.message) {
                    // QR-Code-Dialog anzeigen
                    let d = new frappe.ui.Dialog({
                        title: __('QR-Code für ') + frm.doc.bicycle_name,
                        fields: [
                            {
                                fieldtype: 'HTML',
                                fieldname: 'qr_display',
                                label: __('QR-Code'),
                                options: `<div class="text-center">
                                    <img src="${r.message}" style="max-width: 100%;">
                                    <p class="text-muted">${__('QR-Code für schnelle Fahrradidentifikation')}</p>
                                </div>`
                            }
                        ],
                        primary_action_label: __('Herunterladen'),
                        primary_action: function() {
                            // QR-Code-Bild herunterladen
                            let a = document.createElement('a');
                            a.href = r.message;
                            a.download = `bicycle-qr-${frm.doc.name}.png`;
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                        }
                    });
                    d.show();
                }
            }
        });
    },
    
    // Zeigt die Reparaturhistorie eines Fahrrads an
    showRepairHistory: function(frm) {
        frappe.call({
            method: "bikedoctor.bicycle_management.get_repair_history",
            args: {
                bicycle: frm.doc.name
            },
            callback: function(r) {
                if(r.message && r.message.length) {
                    let repairs = r.message;
                    
                    // Dialog mit Reparaturhistorie erstellen
                    let d = new frappe.ui.Dialog({
                        title: __('Reparaturhistorie für ') + frm.doc.bicycle_name,
                        fields: [
                            {
                                fieldtype: 'HTML',
                                fieldname: 'repair_history',
                                options: bikedoctor.renderRepairHistory(repairs)
                            }
                        ]
                    });
                    d.show();
                } else {
                    frappe.msgprint(__('Keine Reparaturhistorie gefunden.'));
                }
            }
        });
    },
    
    // Rendert die HTML-Darstellung der Reparaturhistorie
    renderRepairHistory: function(repairs) {
        let html = `<div class="repair-history">
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>${__('Datum')}</th>
                        <th>${__('Beschreibung')}</th>
                        <th>${__('Status')}</th>
                        <th>${__('Kosten')}</th>
                        <th>${__('Aktion')}</th>
                    </tr>
                </thead>
                <tbody>`;
        
        repairs.forEach(function(repair) {
            let statusClass = '';
            
            // CSS-Klasse basierend auf Status setzen
            if(repair.status === 'Abgeschlossen') {
                statusClass = 'repair-status-completed';
            } else if(repair.status === 'In Arbeit') {
                statusClass = 'repair-status-in-progress';
            } else if(repair.status === 'Wartend') {
                statusClass = 'repair-status-waiting';
            } else if(repair.status === 'Eingegangen') {
                statusClass = 'repair-status-new';
            } else if(repair.status === 'Storniert') {
                statusClass = 'repair-status-cancelled';
            }
            
            html += `<tr>
                <td>${frappe.datetime.str_to_user(repair.repair_date)}</td>
                <td>${repair.description || ''}</td>
                <td><span class="repair-status ${statusClass}">${repair.status}</span></td>
                <td>${frappe.format(repair.cost, {fieldtype: 'Currency'})}</td>
                <td><a href="#Form/Bicycle Repair/${repair.name}">${__('Anzeigen')}</a></td>
            </tr>`;
        });
        
        html += `</tbody></table></div>`;
        
        return html;
    },
    
    // Erstellt eine neue Reparatur für ein Fahrrad
    createNewRepair: function(frm) {
        frappe.new_doc('Bicycle Repair', {
            bicycle: frm.doc.name,
            customer: frm.doc.customer,
            repair_date: frappe.datetime.nowdate()
        });
    },
    
    // Sendet eine Wartungserinnerung an den Kunden
    sendMaintenanceReminder: function(frm) {
        frappe.prompt([
            {
                fieldname: 'reminder_message',
                label: __('Erinnerungsnachricht'),
                fieldtype: 'Text',
                default: __('Ihr Fahrrad ist für eine Wartung fällig. Bitte vereinbaren Sie einen Termin in unserer Werkstatt.')
            },
            {
                fieldname: 'send_email',
                label: __('E-Mail senden'),
                fieldtype: 'Check',
                default: 1
            },
            {
                fieldname: 'send_sms',
                label: __('SMS senden'),
                fieldtype: 'Check',
                default: 0
            }
        ], function(values) {
            frappe.call({
                method: "bikedoctor.notifications.send_maintenance_reminder",
                args: {
                    bicycle: frm.doc.name,
                    message: values.reminder_message,
                    send_email: values.send_email,
                    send_sms: values.send_sms
                },
                callback: function(r) {
                    if(r.message) {
                        frappe.show_alert({
                            message: __('Wartungserinnerung gesendet.'),
                            indicator: 'green'
                        });
                    }
                }
            });
        }, __('Wartungserinnerung senden'), __('Senden'));
    },
    
    // Aktualisiert den Status einer Reparatur
    updateRepairStatus: function(frm) {
        // Dialog mit Statusoptionen anzeigen
        let statusOptions = [
            {value: 'Eingegangen', label: __('Eingegangen')},
            {value: 'In Arbeit', label: __('In Arbeit')},
            {value: 'Wartend', label: __('Wartend auf Teile')},
            {value: 'Abgeschlossen', label: __('Abgeschlossen')},
            {value: 'Storniert', label: __('Storniert')}
        ];
        
        frappe.prompt([
            {
                fieldname: 'status',
                label: __('Neuer Status'),
                fieldtype: 'Select',
                options: statusOptions,
                default: frm.doc.status
            },
            {
                fieldname: 'update_note',
                label: __('Hinweis zur Aktualisierung'),
                fieldtype: 'Small Text'
            },
            {
                fieldname: 'notify_customer',
                label: __('Kunde benachrichtigen'),
                fieldtype: 'Check',
                default: 1,
                depends_on: "eval:doc.status !== values.status"
            }
        ], function(values) {
            // Status aktualisieren
            frm.set_value('status', values.status);
            
            // Wenn Reparatur abgeschlossen, Datum setzen
            if(values.status === 'Abgeschlossen' && !frm.doc.completion_date) {
                frm.set_value('completion_date', frappe.datetime.nowdate());
            }
            
            // Kommentar zur Statusaktualisierung hinzufügen
            if(values.update_note) {
                frm.set_value('diagnostics', (frm.doc.diagnostics || '') + 
                    `\n\n${frappe.datetime.now_datetime()}: ${__('Status geändert zu')} ${values.status}. ${values.update_note}`);
            }
            
            // Speichern
            frm.save();
            
            // Kunde benachrichtigen, wenn gewünscht
            if(values.notify_customer && values.status !== frm.doc.status) {
                bikedoctor.notifyCustomer(frm, values.status);
            }
        }, __('Reparaturstatus aktualisieren'), __('Aktualisieren'));
    },
    
    // Benachrichtigt den Kunden über den Status einer Reparatur
    notifyCustomer: function(frm, newStatus) {
        let status = newStatus || frm.doc.status;
        
        // Statusspezifische Nachrichtenvorlage vorbereiten
        let messageTemplate = '';
        
        if(status === 'Eingegangen') {
            messageTemplate = __('Ihre Fahrradreparatur wurde erfasst und wartet auf Bearbeitung.');
        } else if(status === 'In Arbeit') {
            messageTemplate = __('Wir arbeiten aktuell an Ihrem Fahrrad.');
        } else if(status === 'Wartend') {
            messageTemplate = __('Wir warten auf Ersatzteile für Ihr Fahrrad.');
        } else if(status === 'Abgeschlossen') {
            messageTemplate = __('Die Reparatur Ihres Fahrrads ist abgeschlossen. Sie können es abholen.');
        } else if(status === 'Storniert') {
            messageTemplate = __('Die Reparatur Ihres Fahrrads wurde storniert.');
        }
        
        // Dialog mit Nachrichtenoptionen anzeigen
        frappe.prompt([
            {
                fieldname: 'subject',
                label: __('Betreff'),
                fieldtype: 'Data',
                default: __('Update zu Ihrer Fahrradreparatur')
            },
            {
                fieldname: 'message',
                label: __('Nachricht'),
                fieldtype: 'Text',
                default: `${__('Sehr geehrte(r)')} ${frm.doc.customer_name},\n\n${messageTemplate}\n\n${__('Reparaturnummer:')} ${frm.doc.name}\n${__('Fahrrad:')} ${frm.doc.bicycle_name}\n\n${__('Mit freundlichen Grüßen,')}\nbike.doctor Team`
            },
            {
                fieldname: 'send_email',
                label: __('E-Mail senden'),
                fieldtype: 'Check',
                default: 1
            },
            {
                fieldname: 'send_sms',
                label: __('SMS senden'),
                fieldtype: 'Check',
                default: 0
            }
        ], function(values) {
            frappe.call({
                method: "bikedoctor.notifications.notify_customer",
                args: {
                    bicycle_repair: frm.doc.name,
                    subject: values.subject,
                    message: values.message,
                    send_email: values.send_email,
                    send_sms: values.send_sms
                },
                callback: function(r) {
                    if(r.message) {
                        frappe.show_alert({
                            message: __('Kunde wurde benachrichtigt.'),
                            indicator: 'green'
                        });
                    }
                }
            });
        }, __('Kunde benachrichtigen'), __('Senden'));
    },
    
    // Erstellt eine Rechnung für eine abgeschlossene Reparatur
    createInvoice: function(frm) {
        frappe.call({
            method: "bikedoctor.bicycle_management.create_invoice",
            args: {
                repair: frm.doc.name
            },
            callback: function(r) {
                if(r.message) {
                    frappe.show_alert({
                        message: __('Rechnung erstellt: ') + r.message,
                        indicator: 'green'
                    });
                    
                    // Formular aktualisieren
                    frm.reload_doc();
                }
            }
        });
    },
    
    // Initialisiert das Dashboard
    initDashboard: function() {
        // Benutzerdefinierte Dashboard-Widgets laden
        frappe.call({
            method: "bikedoctor.dashboard.get_workshop_dashboard_data",
            callback: function(r) {
                if(r.message) {
                    let data = r.message;
                    // Dashboard-Widgets rendern
                    // (würde in einer realen Implementierung spezifische DOM-Manipulation enthalten)
                }
            }
        });
    }
};

// Initialisierung nach dem Laden der Seite
$(document).ready(function() {
    bikedoctor.init();
});
