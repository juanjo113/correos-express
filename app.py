from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehiculos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_USERNAME'] = 'tucorreo@example.com'  # Cambia esto por tu correo
app.config['MAIL_PASSWORD'] = 'tucontraseña'  # Cambia esto por tu contraseña
app.config['MAIL_DEFAULT_SENDER'] = 'tucorreo@example.com'  # Cambia esto
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

db = SQLAlchemy(app)
mail = Mail(app)

class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    fecha_cambio_aceite = db.Column(db.Date, nullable=False)
    fecha_itv = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Vehiculo {self.marca} {self.modelo}>'

# Verifica si es necesario enviar un correo
def verificar_fechas():
    vehiculos = Vehiculo.query.all()
    hoy = datetime.today().date()

    for vehiculo in vehiculos:
        if vehiculo.fecha_cambio_aceite <= hoy:
            enviar_correo(vehiculo, 'Cambio de aceite')
        if vehiculo.fecha_itv <= hoy:
            enviar_correo(vehiculo, 'ITV')

# Función para enviar correo
def enviar_correo(vehiculo, tipo):
    message = Message(
        f'{tipo} para tu vehículo {vehiculo.marca} {vehiculo.modelo}',
        recipients=['tucorreo@example.com'],  # Cambia esto por tu correo
        body=f'Es hora de realizar el {tipo} para el vehículo {vehiculo.marca} {vehiculo.modelo}.'
    )
    mail.send(message)

# Tarea para verificar las fechas cada día
scheduler = BackgroundScheduler()
scheduler.add_job(func=verificar_fechas, trigger="interval", days=1)
scheduler.start()

@app.route('/')
def index():
    vehiculos = Vehiculo.query.all()
    return render_template('index.html', vehiculos=vehiculos)

@app.route('/add', methods=['GET', 'POST'])
def add_vehicle():
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        fecha_cambio_aceite = datetime.strptime(request.form['fecha_cambio_aceite'], '%Y-%m-%d').date()
        fecha_itv = datetime.strptime(request.form['fecha_itv'], '%Y-%m-%d').date()

        nuevo_vehiculo = Vehiculo(
            marca=marca,
            modelo=modelo,
            fecha_cambio_aceite=fecha_cambio_aceite,
            fecha_itv=fecha_itv
        )

        db.session.add(nuevo_vehiculo)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_vehicle.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
