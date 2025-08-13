from flask import Flask
from models import get_vehicles_due_today
from email_utils import send_alert_email
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "Sistema de Vehículos activo"
