from flask import render_template


class Vista:
    def inicio(self):
        return render_template('inicio.html')

    def mozo(self):
        return render_template('mozo.html')

    def cocinero(self, pedidos):
        return render_template('cocinero.html', pedidos=pedidos)

    def error(self, e):
        return render_template('error.html', error=e)

    def agregarpedido(self, prods, lista):
        return render_template('agregarpedido.html', productos=prods, items=lista)

    def registrarcobro(self, num):
        return render_template('regcobro.html', num=num)

    def listarpedidos(self, pedidos):
        return render_template('listarpedidos.html', pedidos=pedidos)

