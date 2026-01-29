
from flask import render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
import pandas as pd

from forms import RegistrationForm, LoginForm, ReporteForm
from models import User, Reporte, Consumo, Sector, db
from extensions import bcrypt

UPLOAD_FOLDER = 'static/uploads'

def configure_routes(app):

    # -------------------- RUTA PRINCIPAL --------------------
    @app.route('/')
    def home():
        return render_template('home.html')

    # -------------------- LOGIN --------------------
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('select_location'))

        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                session['user_name'] = user.username
                flash('Inicio de sesión exitoso.', 'green')
                return redirect(url_for('select_location'))
            else:
                flash('Usuario o contraseña incorrectos.', 'red')

        return render_template('login.html', form=form)

    # -------------------- REGISTRO --------------------
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('select_location'))

        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)

            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Cuenta creada. Por favor, inicia sesión.', 'green')
                return redirect(url_for('login'))
            except Exception:
                db.session.rollback()
                flash('Error: El usuario o email ya existe.', 'red')

        return render_template('register.html', form=form)

    # -------------------- LOGOUT --------------------
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        session.pop('user_name', None)
        flash('Sesión cerrada correctamente.', 'blue')
        return redirect(url_for('login'))

    # -------------------- SELECCIÓN DE UBICACIÓN --------------------
    @app.route('/select-location')
    @login_required
    def select_location():
        user_name = session.get('user_name', 'Usuario')
        locations = [
            {"id": 1, "name": "Alumbrado Público", "endpoint": "alumbrado"},
            {"id": 2, "name": "Espacios Públicos", "endpoint": "espacios_publicos"},
            {"id": 3, "name": "Mantenimiento e Higiene Urbana", "endpoint": "mantenimiento"},
            {"id": 4, "name": "Normatividad y Saneamiento Ambiental", "endpoint": "normatividad"},
            {"id": 5, "name": "Call Center", "endpoint": "call_center"},
            {"id": 6, "name": "Otros", "endpoint": "otros"}
        ]
        return render_template('select_location.html', user_name=user_name, locations=locations)

    # -------------------- RUTAS DE SECCIONES --------------------
    @app.route('/alumbrado')
    @login_required
    def alumbrado():
        return render_template('alumbrado.html')

    @app.route('/espacios-publicos')
    @login_required
    def espacios_publicos():
        return render_template('espacios_publicos.html')

    @app.route('/mantenimiento')
    @login_required
    def mantenimiento():
        return render_template('mantenimiento.html')

    @app.route('/normatividad')
    @login_required
    def normatividad():
        return render_template('normatividad.html')

    @app.route('/call-center')
    @login_required
    def call_center():
        return render_template('call_center.html')

    @app.route('/otros')
    @login_required
    def otros():
        return render_template('otros.html')

    # -------------------- MONITOREO Y DATOS --------------------
    @app.route('/monitoreo-consumo')
    @login_required
    def monitoreo_consumo():
        registros = Consumo.query.all()
        return render_template('monitoreo_consumo.html', registros=registros)

    @app.route('/guardar-datos', methods=['POST'])
    @login_required
    def guardar_datos():
        return jsonify({'status': 'ok', 'message': 'Datos guardados correctamente'})

    @app.route('/eliminar-registro/<int:id>', methods=['DELETE'])
    @login_required
    def eliminar_registro(id):
        registro = Consumo.query.get(id)
        if registro:
            db.session.delete(registro)
            db.session.commit()
            return jsonify({'status': 'ok', 'message': 'Registro eliminado correctamente'})
        return jsonify({'status': 'error', 'message': 'Registro no encontrado'})

    # -------------------- MAPA DE SECTORES --------------------
    @app.route('/mapas-sectores')
    @login_required
    def mapas_sectores():
        return render_template('mapas_sectores.html')

    # -------------------- API PARA SECTORES --------------------
    @app.route('/api/sectores')
    @login_required
    def api_sectores():
        try:
            ruta_csv = os.path.join(UPLOAD_FOLDER, 'sectores.csv')
            sectores_lista = []

            if os.path.exists(ruta_csv):
                # Leer CSV
                df = pd.read_csv(ruta_csv)
                data = df.to_dict(orient="records")

                for item in data:
                    sectores_lista.append({
                        "id": item.get('id'),
                        "rpu": item.get('rpu'),
                        "clasificacion": item.get('clasificacion'),
                        "colonia": item.get('colonia'),
                        "color": item.get('color', 'blue'),
                        "lat": float(item.get('latitud', 0)),
                        "lng": float(item.get('longitud', 0))
                    })
            else:
                # Si no hay CSV, usar datos de la BD
                sectores_db = Sector.query.all()
                for s in sectores_db:
                    sectores_lista.append({
                        "id": s.id,
                        "rpu": s.rpu,
                        "clasificacion": s.clasificacion,
                        "colonia": s.colonia,
                        "color": s.color or "green",
                        "lat": float(s.lat) if s.lat else 0,
                        "lng": float(s.lng) if s.lng else 0
                    })

            return jsonify(sectores_lista)

        except Exception as e:
            return jsonify({'status': 'error', 'message': f'Error procesando datos: {e}'})

