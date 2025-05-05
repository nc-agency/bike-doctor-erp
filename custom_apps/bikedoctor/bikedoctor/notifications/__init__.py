# -*- coding: utf-8 -*-
# bike.doctor ERP - Notifications Module Initialization
# 
# Erstellt: 05.05.2025
# Änderungen:
# - Initiale Erstellung der Initialisierungsdatei für das Notifications Modul

from __future__ import unicode_literals
from bikedoctor.notifications.notifications import (
    get_notification_config,
    notify_customer,
    send_maintenance_reminder
)