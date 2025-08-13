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
