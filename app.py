from flask import Flask, render_template, request, redirect, url_for
from email_utils import send_email
from datetime import date
from flask_migrate import Migrate
from models import db, get_all_vehicles, get_vehicles_due_today

import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave_secreta_para_flash")

# Configuración de la base de datos para Render (PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///vehicles.db'  # Fallback si no hay variable de entorno
).replace("postgres://", "postgresql://")  # Fix para SQLAlchemy

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar db y Migrate
db.init_app(app)
migrate = Migrate(app, db)

ALERT_DAYS = 7

# Evitar error con HEAD requests
@app.before_request
def handle_head_requests():
    if request.method == "HEAD":
        return "", 200

@app.route("/", methods=["GET", "HEAD"])
def home():
    q = request.args.get("q", "")
    vehicles = get_all_vehicles(q)
    return render_template(
        "index.html",
        vehicles=vehicles,
        today=date.today(),
        config={"ALERT_DAYS": ALERT_DAYS}
    )

@app.route("/send_alerts", methods=["GET", "HEAD"])
def send_alerts():
    vehicles_due = get_vehicles_due_today()
    for vehicle in vehicles_due:
        send_email(vehicle)
    return f"Se enviaron {len(vehicles_due)} alertas."

@app.route("/add", methods=["GET", "POST", "HEAD"])
def add_vehicle():
    from models import Vehicle
    if request.method == "POST":
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
        return redirect(url_for("home"))
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
