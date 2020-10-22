from Modelo import Modelo

from Vista import Vista


class Controlador:
    __vista = None
    __modelo = None

    def __init__(self):
        self.__modelo = Modelo()
        self.__vista = Vista()

    # Páigna principal
    def pagprincipal(self):
        return self.__vista.inicio()

    def comprobar(self, usuario, contrasena):
        tipo, e = self.__modelo.comprobarusuario(usuario, contrasena)
        if tipo == 'Mozo':
            return self.pagmozo()
        elif tipo == 'Cocinero':
            return self.pagcocinero(None)
        else:
            return self.pagerror(e)

    # Página de mozo
    def pagmozo(self):
        return self.__vista.mozo()

    # Página de cocinero
    def pagcocinero(self, item):
        self.__modelo.actualizarestado(item)
        pedidos = self.__modelo.getpedidos()  # Pedidos con items pendientes
        return self.__vista.cocinero(pedidos)

    # Función agregar pedido
    def pagagregarpedido(self, lista):
        productos = self.__modelo.getproductos()
        return self.__vista.agregarpedido(productos, lista)

    def crearpedido(self, prods, total, obs, mesa):
        self.__modelo.crearpedido(total, obs, mesa)
        self.__modelo.crearitem(prods)
        self.__modelo.finalizarpedido()

    def calculartotal(self, lista):
        total = 0
        for t in lista:
            total += t
        return total

    # Función listar pedidos por mozo
    def paglistarpedidos(self):
        pedidos = self.__modelo.getpedidosusuario()  # Pedidos de un usuario
        return self.__vista.listarpedidos(pedidos)

    # Función registrar cobro
    def pagregistrarcobro(self, num):
        return self.__vista.registrarcobro(num)

    def regcobro(self, pedido):
        self.__modelo.cobrar(pedido)
        return self.__vista.mozo()

    # Página de error
    def pagerror(self, error):
        return self.__vista.error(error)
