from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imagenes.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
db = SQLAlchemy(app)

class Imagen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    imagen = db.Column(db.String(100), nullable=False)

# Datos de ejemplo (puedes reemplazar esto con tu propia lógica de datos)
datos = [
    {"id": 1, "nombre": "Armario", "imagen": "armario.jpg"},
    {"id": 2, "nombre": "Cocina", "imagen": "cocina.jpg"},
    {"id": 3, "nombre": "Sala", "imagen": "decor1.jpg"},
    {"id": 4, "nombre": "Mesa", "imagen": "decor2.jpg"},
    {"id": 5, "nombre": "Gradas", "imagen": "gradas.jpg"},
    {"id": 6, "nombre": "Mesa", "imagen": "mesa.jpg"},
    {"id": 7, "nombre": "Mueble", "imagen": "mueble.jpg"},
    {"id": 8, "nombre": "Silla", "imagen": "silla.jpg"},
    {"id": 9, "nombre": "Pasamanos", "imagen": "pasamanos.jpg"},
    {"id": 10, "nombre": "Ventana", "imagen": "ventanas.jpg"},
    {"id": 11, "nombre": "Closet", "imagen": "trabajo_madera.jpg"},
]

# Configuración de la paginación
ELEMENTOS_POR_PAGINA = 3

class PaginaForm(FlaskForm):
    pagina = StringField('Página')
    submit = SubmitField('Ir')

@app.route('/', methods=['GET', 'POST'])
def index():
    # Página actual (por defecto 1)
    pagina = request.args.get('pagina', 1, type=int)

    # Calcular el índice de inicio y final para la página actual
    inicio = (pagina - 1) * ELEMENTOS_POR_PAGINA
    fin = inicio + ELEMENTOS_POR_PAGINA

    # Obtener los datos para la página actual desde la base de datos
    datos_pagina = Imagen.query.slice(inicio, fin).all()

    # Formulario de paginación
    form = PaginaForm()
    if form.validate_on_submit():
        return redirect(url_for('index', pagina=form.pagina.data))

    return render_template('index.html', datos=datos_pagina, pagina=pagina, form=form, ELEMENTOS_POR_PAGINA=ELEMENTOS_POR_PAGINA)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)