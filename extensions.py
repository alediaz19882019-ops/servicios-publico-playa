from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 

# 1. Creamos los objetos de extensión sin inicializar con la app todavía
db = SQLAlchemy()
bcrypt = Bcrypt() 
login_manager = LoginManager()

# 2. Esta es la función que tu app.py intenta importar y ejecutar
def init_extensions(app):
    """
    Inicializa todas las extensiones de Flask con la instancia de la aplicación.
    """
    db.init_app(app)
    bcrypt.init_app(app) 
    login_manager.init_app(app)
    
    # Configuraciones específicas para Flask-Login
    login_manager.login_view = 'login'
    login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
