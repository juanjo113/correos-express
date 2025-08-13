import time
from datetime import datetime, timedelta
from flask import Flask
from models import db, Vehicle
from config import Config
from email_utils import send_email

# Worker simple que comprueba cada 6 horas
CHECK_INTERVAL_SECONDS = 6 * 60 * 60

def create_worker_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

app = create_worker_app()


def should_notify(due_date, last_notified, today, alert_days):
    if not due_date:
        return False
    # Aviso si está dentro de la ventana o vencido
    if due_date <= today + timedelta(days=alert_days):
        # Evita repetir varias veces el mismo día
        return (last_notified is None) or (last_notified < today)
    return False


def build_email(v, today):
    parts = []
    if v.oil_date:
        parts.append(f"Cambio de aceite: {v.oil_date:%d/%m/%Y}")
    if v.itv_date:
        parts.append(f"ITV: {v.itv_date:%d/%m/%Y}")
    detalle = '<br>'.join(parts) if parts else '—'
    html = f"""
    <h2>Aviso de mantenimiento – {v.make} {v.model} ({v.plate})</h2>
    <p>Fecha: {today:%d/%m/%Y}</p>
    <p><strong>Próximas fechas:</strong><br>{detalle}</p>
    <p>Accede a la aplicación para confirmar o ajustar las fechas.</p>
    """
    return html


def check_and_notify():
    with app.app_context():
        today = datetime.utcnow().date()
        alert_days = app.config['ALERT_DAYS']
        vehicles = Vehicle.query.all()
        for v in vehicles:
            updated = False
            if should_notify(v.oil_date, v.oil_notified_on, today, alert_days):
                send_email(
                    v.owner_email,
                    f"Aviso: cambio de aceite – {v.plate}",
                    build_email(v, today)
                )
                v.oil_notified_on = today
                updated = True
            if should_notify(v.itv_date, v.itv_notified_on, today, alert_days):
                send_email(
                    v.owner_email,
                    f"Aviso: ITV – {v.plate}",
                    build_email(v, today)
                )
                v.itv_notified_on = today
                updated = True
            if updated:
                db.session.commit()


if __name__ == '__main__':
    while True:
        try:
            check_and_notify()
        except Exception as e:
            # Log simple
            print('Error en scheduler:', e, flush=True)
        time.sleep(CHECK_INTERVAL_SECONDS)
