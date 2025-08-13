from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from email_utils import send_email

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicles.db'  # Ajusta según tu DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from models import db  # Mover la importación aquí para evitar ciclo de importación

db.init_app(app)

ALERT_DAYS = 7  # Definición de ALERT_DAYS

@app.route("/")
def home():
    from models import get_all_vehicles  # Importamos dentro de la función para evitar circularidad
    q = request.args.get("q", "")  # Obtiene el término de búsqueda (si lo hay)
    vehicles = get_all_vehicles(q)  # Llama a la función para obtener los vehículos
    return render_template(
        "index.html",  # Plantilla
        vehicles=vehicles,
        today=date.today(),
        config={"ALERT_DAYS": ALERT_DAYS}
    )

@app.route("/send_alerts")
def send_alerts():
    from models import get_vehicles_due_today  # Importamos aquí para evitar circularidad
    vehicles_due = get_vehicles_due_today()
    # Aquí asegúrate de que send_email sea adecuado
    for vehicle in vehicles_due:
        send_email(vehicle)
    return f"Se enviaron {len(vehicles_due)} alertas."

if __name__ == "__main__":
    app.run(debug=True)
