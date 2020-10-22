from app import app

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class Usuarios(db.Model):
    __tablename__ = 'Usuarios'
    DNI = db.Column(db.Integer, primary_key=True)
    Clave = db.Column(db.String(150), nullable=False)
    Tipo = db.Column(db.String(8), nullable=False)
    pedidos = db.relationship('Pedidos', backref='usuario', cascade='all', lazy='dynamic')


class Pedidos(db.Model):
    __tablename__ = 'Pedidos'
    NumPedido = db.Column(db.Integer, primary_key=True)
    Fecha = db.Column(db.DateTime, nullable=False)
    Total = db.Column(db.Float, nullable=False)
    Cobrado = db.Column(db.Boolean, nullable=False)
    Observacion = db.Column(db.String(30))
    DNIMozo = db.Column(db.Integer, db.ForeignKey(Usuarios.DNI), nullable=False)
    Mesa = db.Column(db.Integer, nullable=False)
    items = db.relationship('Items', backref='pedidoss', cascade='all', lazy='dynamic')


class Productos(db.Model):
    __tablename__ = 'Productos'
    NumProducto = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(150), nullable=False, unique=True)
    PrecioUnitario = db.Column(db.Integer, nullable=False)
    items = db.relationship('Items', backref='prods', cascade='all', lazy='dynamic')

class Items(db.Model):
    __tablename__ = 'ItemsPedidos'
    NumItem = db.Column(db.Integer, primary_key=True)
    NumPedido = db.Column(db.Integer, db.ForeignKey(Pedidos.NumPedido), nullable=False)
    NumProducto = db.Column(db.Integer, db.ForeignKey(Productos.NumProducto), nullable=False)
    Precio = db.Column(db.Float, nullable=False)
    Estado = db.Column(db.String(10), nullable=False)