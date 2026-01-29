
import os
import sys
from flask import Flask
from extensions import init_extensions, db, login_manager
from models import User, Reporte

print(">>> Iniciando script app.py con SQLite y Login Fix...")

# Intentamos importar configure_routes desde routes.py
try:
    from routes import configure_routes
    print(">>> Flask y extensiones importadas correctamente")
except ImportError as e:
    print(f">>> ERROR de importación: {e}")
    sys.exit(1)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev_key_123'

    # --- CONFIGURACIÓN PARA SQLITE ---
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensiones
    init_extensions(app)

    # --- FIX: USER LOADER PARA FLASK-LOGIN ---
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception:
            return None

    # Configurar las rutas del CRUD
    try:
        configure_routes(app)
        print(">>> Rutas del CRUD cargadas correctamente")
    except Exception as e:
        print(f">>> ERROR al cargar rutas: {e}")

    # --- CREACIÓN AUTOMÁTICA DE TABLAS ---
    with app.app_context():
        try:
            db.create_all()
            print(">>> BASE DE DATOS SQLITE LISTA: Archivo 'database.db' verificado.")
        except Exception as e:
            print(f">>> ERROR al crear la base de datos: {e}")

    return app

# Crear la instancia de la aplicación
application = create_app()

if __name__ == "__main__":
    try:
        print(">>> Arrancando servidor en http://localhost:5000")
        application.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f">>> ERROR FATAL durante el arranque: {e}")


