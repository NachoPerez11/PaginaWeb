from flask import request

from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('Config.py')


@app.route('/')
def comienzo():
    return ctrl.pagprincipal()


@app.route('/comprobar', methods=['POST', 'GET'])
def comprobarusuario():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contraseña']
        return ctrl.comprobar(usuario, contrasena)


@app.route('/paginicial/', methods=['POST', 'GET'])
def funciones():
    if request.method == 'POST':
        if request.form['funcion'] == 'Crear nuevo pedido':
            return ctrl.pagagregarpedido([''])
        elif request.form['funcion'] == 'Listar pedidos':
            return ctrl.paglistarpedidos()
        else:
            return ctrl.pagerror('Para ingresar a las funcionalidades de mozo, haga click en los botones indicados')


@app.route('/paginicialcocinero/', methods=['POST', 'GET'])
def funcioncocinero():
    if request.method == 'GET':
        return ctrl.pagcocinero(request.args['item'])


@app.route('/funcion/', methods=['POST', 'GET'])
def funcionmozo():
    if request.method == 'GET':
        lista.append(request.args['name'])
        total.append(float(request.args['precio']))
        return ctrl.pagagregarpedido(lista)
    else:
        calc = ctrl.calculartotal(total)
        obs = request.form['obs']
        mesa = request.form['mesa']
        ctrl.crearpedido(lista, calc, obs, mesa)
        lista.clear()
        return ctrl.pagmozo()


@app.route('/cobrar/', methods=['POST', 'GET'])
def cobrar():
    if request.method == 'GET':
        numpedido = request.args['num']
        return ctrl.pagregistrarcobro(numpedido)
    else:
        num = request.form['numitem']
        if request.form['cobro'] == 'Cobrar pedido':
            return ctrl.regcobro(num)
        else:
            return ctrl.pagmozo()


if __name__ == '__main__':
    from Controlador import Controlador
    from ClaseModelo import db
    lista = []
    total = []
    ctrl = Controlador()
    db.create_all()
    db.init_app(app)
    app.run(debug=True)
