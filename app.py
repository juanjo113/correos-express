from flask import Flask, render_template, request
from models import get_vehicles_due_today, get_all_vehicles  # get_all_vehicles debe existir para listar
from email_utils import send_email
from datetime import date

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_flash'  # si usas flash messages

ALERT_DAYS = 7  # define esta variable

@app.route("/")
def home():
    q = request.args.get("q", "")
    vehicles = get_all_vehicles(q)  # si tienes función de búsqueda, si no solo get_all_vehicles()
    return render_template(
        "index.html",
        vehicles=vehicles,
        today=date.today(),
        config={"ALERT_DAYS": ALERT_DAYS}
    )

@app.route("/send_alerts")
def send_alerts():
    vehicles_due = get_vehicles_due_today(days_before=ALERT_DAYS)
    for vehicle in vehicles_due:
        send_email(vehicle)  # Aquí asegúrate de que send_email reciba los parámetros correctos
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
