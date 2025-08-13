from flask import Flask, render_template, request
from email_utils import send_email
from datetime import date

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_flash'  # si usas flash messages

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicles.db'  # Ajusta según tu DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from models import db  # Aquí importamos `db` después de que Flask esté inicializado

db.init_app(app)  # Inicializamos SQLAlchemy

ALERT_DAYS = 7  # define esta variable

@app.route("/")
def home():
    from models import get_all_vehicles  # Importamos dentro de la función para evitar importaciones circulares
    q = request.args.get("q", "")
    vehicles = get_all_vehicles(q)  # Llama a la función
    return render_template(
        "index.html",
        vehicles=vehicles,
        today=date.today(),
        config={"ALERT_DAYS": ALERT_DAYS}
    )

@app.route("/send_alerts")
def send_alerts():
    from models import get_vehicles_due_today  # Importamos aquí para evitar importaciones circulares
    vehicles_due = get_vehicles_due_today(days_before=ALERT_DAYS)
    for vehicle in vehicles_due:
        send_email(vehicle)  # Asegúrate de que send_email reciba los parámetros correctos
    return f"Se enviaron {len(vehicles_due)} alertas."

# Aquí añade endpoints de ejemplo para que no fallen los url_for en plantilla:
@app.route("/add")
def add_vehicle():
    return "Formulario para añadir vehículo (pendiente)"

@app.route("/edit/<int:vehicle_id>")
def edit_vehicle(vehicle_id):
    return f"Editar vehículo {vehicle_id} (pendiente)"

@app.route("/delete/<int:vehicle_id>", methods=["POST"])
def delete_vehicle(vehicle_id):
    # Lógica para borrar vehículo (pendiente)
    return f"Vehículo {vehicle_id} eliminado (pendiente)"

if __name__ == "__main__":
    app.run(debug=True)
