from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from models import get_all_vehicles, get_vehicles_due_today

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicles.db'  # O ajusta según tu DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

ALERT_DAYS = 7  # Definición de ALERT_DAYS

@app.route("/")
def home():
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
    vehicles_due = get_vehicles_due_today()
    # Aquí asegúrate de que send_email sea adecuado
    for vehicle in vehicles_due:
        send_email(vehicle)
    return f"Se enviaron {len(vehicles_due)} alertas."

if __name__ == "__main__":
    app.run(debug=True)
