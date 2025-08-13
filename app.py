from flask import Flask, render_template, request
from email_utils import send_email
from datetime import date
from flask_migrate import Migrate  # Importar Migrate
from models import db, get_all_vehicles, get_vehicles_due_today

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_flash'  # si usas flash messages

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicles.db'  # Ajusta según tu DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar db y Migrate
db.init_app(app)
migrate = Migrate(app, db)  # Inicializamos Migrate con la app y db

ALERT_DAYS = 7  # Definición de ALERT_DAYS

@app.route("/")
def home():
    q = request.args.get("q", "")
    vehicles = get_all_vehicles(q)  # Llama a la función para obtener los vehículos
    return render_template(
        "index.html",
        vehicles=vehicles,
        today=date.today(),
        config={"ALERT_DAYS": ALERT_DAYS}
    )

@app.route("/send_alerts")
def send_alerts():
    vehicles_due = get_vehicles_due_today()
    for vehicle in vehicles_due:
        send_email(vehicle)
    return f"Se enviaron {len(vehicles_due)} alertas."

@app.route("/add", methods=["GET", "POST", "HEAD"])
def add_vehicle():
    from models import Vehicle
    if request.method == "POST":
        # Recuperar los datos del formulario y añadir el vehículo
        make = request.form["make"]
        model = request.form["model"]
        plate = request.form["plate"]
        owner_email = request.form["owner_email"]
        oil_date = request.form["oil_date"]
        itv_date = request.form["itv_date"]
        new_vehicle = Vehicle(
            make=make,
            model=model,
            plate=plate,
            owner_email=owner_email,
            oil_date=oil_date if oil_date else None,
            itv_date=itv_date if itv_date else None
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return redirect(url_for("home"))  # Redirige a la página principal
    return render_template("add_vehicle.html")

@app.route("/edit/<int:vehicle_id>", methods=["GET", "POST", "HEAD"])
def edit_vehicle(vehicle_id):
    from models import Vehicle
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if request.method == "POST":
        vehicle.make = request.form["make"]
        vehicle.model = request.form["model"]
        vehicle.plate = request.form["plate"]
        vehicle.owner_email = request.form["owner_email"]
        vehicle.oil_date = request.form["oil_date"]
        vehicle.itv_date = request.form["itv_date"]
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit_vehicle.html", v=vehicle)

@app.route("/delete/<int:vehicle_id>", methods=["POST"])
def delete_vehicle(vehicle_id):
    from models import Vehicle
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
