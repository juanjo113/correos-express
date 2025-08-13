from flask import Flask, render_template
from models import get_vehicles_due_today
from email_utils import send_email
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# Endpoint para enviar alertas
@app.route("/send_alerts")
def send_alerts():
    vehicles_due = get_vehicles_due_today(days_before=int(ALERT_DAYS))
    for vehicle in vehicles_due:
        send_alert_email(vehicle)
    return f"Se enviaron {len(vehicles_due)} alertas."

if __name__ == "__main__":
    app.run()
