from flask import Flask
from models import get_vehicles_due_today
from email_utils import send_alert_email
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "Sistema de Vehículos activo"

# Endpoint para enviar alertas
@app.route("/send_alerts")
def send_alerts():
    vehicles_due = get_vehicles_due_today(days_before=int(ALERT_DAYS))
    for vehicle in vehicles_due:
        send_alert_email(vehicle)
    return f"Se enviaron {len(vehicles_due)} alertas."

if __name__ == "__main__":
    app.run()
