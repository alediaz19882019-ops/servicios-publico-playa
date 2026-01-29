from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, FileField, SubmitField, FloatField
# Se agregó EqualTo para validar que las contraseñas coincidan
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileAllowed

# -------------------- FORMULARIO LOGIN --------------------
class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(message="El usuario es obligatorio")])
    password = PasswordField('Contraseña', validators=[DataRequired(message="La contraseña es obligatoria")])
    submit = SubmitField('Iniciar sesión')

# -------------------- FORMULARIO REGISTRO --------------------
class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    
    # Campo corregido: se agrega confirm_password que faltaba
    confirm_password = PasswordField('Confirmar Contraseña', 
        validators=[
            DataRequired(message="Por favor confirma tu contraseña"), 
            EqualTo('password', message='Las contraseñas deben coincidir')
        ])
    
    submit = SubmitField('Registrarse')

# -------------------- FORMULARIO REPORTE --------------------
class ReporteForm(FlaskForm):
    ID = StringField('ID', validators=[DataRequired()])
    colonia = StringField('Colonia', validators=[DataRequired()])
    REPORTES = StringField('Descripción del Reporte', validators=[DataRequired()])
    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    SYMBOL = StringField('Símbolo', validators=[DataRequired()])
    location = StringField('Ubicación', validators=[DataRequired()])
    COLOR = StringField('Color', validators=[DataRequired()])
    lat = FloatField('Latitud', validators=[DataRequired()])
    long = FloatField('Longitud', validators=[DataRequired()])
    foto = FileField('Subir Foto', validators=[FileAllowed(['jpg', 'png'], 'Solo imágenes JPG o PNG')])
    submit = SubmitField('Guardar Reporte')
