import hashlib

from ClaseModelo import Usuarios, Productos, Pedidos, db, Items

from datetime import datetime


class Modelo:
    __listaitems = []
    __usuario = None
    __pedidos = None
    __productos = None

    '''
    
    Métodos globales
    
    '''

    def actpedidos(self):
        self.__pedidos = Pedidos.query.all()

    def actproductos(self):
        self.__productos = Productos.query.all()

    '''
    
    Iniciar sesión
    
    '''

    def getusuario(self, user):
        self.__usuario = Usuarios.query.filter_by(DNI=user).first()
        if self.__usuario is not None:
            return self.__usuario, self.__usuario.Tipo
        else:
            return None, None

    def comprobarusuario(self, usuario, contrasena):
        cond = None
        error = ''
        if usuario != '' and contrasena != '':
            obj, tipo = self.getusuario(usuario)
            if tipo is not None:
                clave = str(self.cifrarcontrasena(contrasena))
                if clave == obj.Clave:
                    cond = tipo
                else:
                    error = 'Contraseña incorrecta'
            else:
                error = 'Usuario inexistente'
        else:
            error = 'Debe ingresar los datos requeridos'
        return cond, error

    def cifrarcontrasena(self, clave):
        result = hashlib.md5(bytes(clave, encoding='UTF-8'))
        return result.hexdigest()

    '''
    
    Agregar pedido
    
    '''

    def getproductos(self):
        self.actproductos()
        return self.__productos

    def crearpedido(self, total, obs, mesa):
        num = db.session.query(Pedidos).order_by(Pedidos.NumPedido.desc()).first()
        if num is None:
            num = 0
        else:
            num = int(num.NumPedido)
        pedido = Pedidos(NumPedido=num + 1, Fecha=datetime.now(), Total=float(total), Cobrado=False,
                         Observacion=obs, DNIMozo=self.__usuario.DNI, Mesa=mesa)
        db.session.add(pedido)
        db.session.commit()

    def crearitem(self, prods):
        for p in range(len(prods)):
            prod = self.buscarproducto(prods[p])
            if prod is not None:
                unitem = Items(NumPedido=db.session.query(Pedidos).order_by(Pedidos.NumPedido.desc()).first().NumPedido,
                               NumProducto=prod.NumProducto,
                               Precio=prod.PrecioUnitario,
                               Estado='Pendiente')
                db.session.add(unitem)
        db.session.commit()

    def buscarproducto(self, prod):
        self.actproductos()
        i = 0
        while i < len(self.__productos) and self.__productos[i].Nombre != prod:
            i += 1
        if i < len(self.__productos):
            return self.__productos[i]
        else:
            return None

    def finalizarpedido(self):
        for i in self.__listaitems:
            db.session.add(i)
            db.commit()

    '''

    Página de cocineros
    
    '''

    def actualizarestado(self, item):
        if item is not None:
            self.actpedidos()
            for p in self.__pedidos:
                for i in p.items:
                    if str(i.NumItem) == item:
                        i.Estado = 'Listo'
                        db.session.commit()

    def getpedidos(self):
        self.actpedidos()
        pedidoss = []
        for i in range(len(self.__pedidos)):
            cant = 0
            j = 0
            for k in self.__pedidos[i].items:
                cant += 1
            while j < cant and self.__pedidos[i].items[j].Estado != 'Pendiente':
                j += 1
            if j < cant:
                pedidoss.append(self.__pedidos[i])
        return pedidoss

    def getprodsitems(self, pedidos):
        prods = []  # Para manejar el indice de los items
        nomprods = []  # Guarda los productos
        nums = []
        items = []
        for i in range(len(pedidos)):
            for h in pedidos[i].items:
                if h.Estado == 'Pendiente':
                    nomprods.append(Productos.query.filter_by(NumProducto=h.NumProducto).first())
                    nums.append(h.NumItem)
            prods.append(nomprods)
            items.append(nums)
        return prods, items

    '''
    
    Listar pedidos 
    
    '''

    def getpedidosusuario(self):
        self.actpedidos()
        pedidoss = []
        if self.__pedidos:
            for p in self.__pedidos:
                if p.Cobrado is not False or p.Cobrado == 0:
                    if p.DNIMozo == self.__usuario.DNI:
                        pedidoss.append(p)
        return pedidoss

    '''
    
    Cobrar pedido
    
    '''

    def cobrar(self, num):
        if num != '':
            Pedidos.query.filter_by(NumPedido=num).delete()
            Items.query.filter_by(NumPedido=num).delete()
            db.session.commit()
