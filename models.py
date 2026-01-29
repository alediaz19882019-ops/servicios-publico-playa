
from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------- MODELO USUARIO --------------------
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# -------------------- MODELO REPORTE --------------------
class Reporte(db.Model):
    __tablename__ = 'reportes'
    ID = db.Column(db.String(50), primary_key=True)
    colonia = db.Column(db.String(100), nullable=False)
    REPORTES = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(100))
    COLOR = db.Column(db.String(50))
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    foto = db.Column(db.String(255))

# -------------------- MODELO CONSUMO --------------------
class Consumo(db.Model):
    __tablename__ = 'consumo'
    id = db.Column(db.Integer, primary_key=True)
    RPU = db.Column(db.String(50), nullable=False)
    semaforo_energetico = db.Column(db.String(20))
    beneficiario = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    area = db.Column(db.String(100))
    responsable = db.Column(db.String(100))
    clasificacion = db.Column(db.String(50))
    tarifa = db.Column(db.String(50))
    lectura_actual = db.Column(db.Float)
    lectura_anterior = db.Column(db.Float)
    consumo_kwh = db.Column(db.Float)
    importe_recibo = db.Column(db.Float)
    importe_estado_cuenta = db.Column(db.Float)
    kwh_totales = db.Column(db.Float)
    importe_total_recibos = db.Column(db.Float)
    importe_total_pagado_poliza_sp = db.Column(db.Float)
    observaciones = db.Column(db.Text)
    carga_censo_kw = db.Column(db.Float)
    corriente_censo_amp = db.Column(db.Float)
    consumo_ideal = db.Column(db.Float)
    consumo_12hrs = db.Column(db.Float)
    consumo_24hrs = db.Column(db.Float)
    status = db.Column(db.String(50))
    pdf = db.Column(db.String(200))
    xlm = db.Column(db.String(200))

    def __repr__(self):
        return f"<Consumo RPU={self.RPU}, Consumo={self.consumo_kwh} kWh>"
    

    
from extensions import db

class Sector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sector = db.Column(db.String(100), nullable=False)
    rpu = db.Column(db.String(50), nullable=False)
    clasificacion = db.Column(db.String(50), nullable=False)
    colonia = db.Column(db.String(100), nullable=False)
    simbolo = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Sector {self.sector}>"
    
