
import sqlite3 
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox

class Ventas (tk.Frame):
    db_name= "database.db" #Llamando el archivo de la base de datos.
    def __init__(self, parent):
        super().__init__(parent)
        self.numero_factura_actual = self.obtener_numero_factura_actual()
        self.widgets()
        self.mostrar_numero_factura()

    def widgets(self):

        frame1= tk.Frame(self, bg="#dddddd", highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0 , y=0, width=1100, height=100)
        
        titulo = tk.Label(self, text="VENTAS", bg="#dddddd", font="sans 30 bold", anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=900, height=90)
 
        frame2 = tk.Frame(self, bg="#C6D9E3", highlightbackground="green", highlightthickness=1)
        frame2.place(x=0, y=100, width= 1100, height=550)

        lblframe = LabelFrame(frame2, text="Informacion de la venta", bg="#C6D9E3", font= "sans 12 bold")
        lblframe.place(x=10, y=10, width=1060 ,height=80)

        label_numero_factura = tk.Label(lblframe, text= "Numero de \nfactura",bg="#C6D9E3",font= "sans 12 bold")
        label_numero_factura.place (x=10, y=5)
        self.numero_factura = tk.StringVar()

        self.entry_numero_factura = ttk.Entry(lblframe, textvariable=self.numero_factura, state="readonly", font= "sans 12 bold")
        self.entry_numero_factura.place (x=100, y=10, width=80)
        
        label_nombre = tk.Label(lblframe,text="productos:", bg="#C6D9E3", font="sans 12 bold")
        label_nombre.place(x=180, y=12)
        self.entry_nombre = ttk.Combobox(lblframe, font="sans 12 bold", state="readonly") #se desplegaran los productos que se tienen en la base de datos.
        self.entry_nombre.place(x=280, y=10, width=180)

        self.cargar_productos()

        label_valor = tk.Label(lblframe, text="Precio:",bg="#C6D9E3",font="sans 12 bold" )
        label_valor.place(x=470, y=12)
        self.entry_valor = ttk.Entry(lblframe, font="sans 12 bold") #state="readonly")
        self.entry_valor.place(x=540, y=10, width=180)

        self.entry_nombre.bind("<<ComboboxSelected>>", self.actualizar_precio) #al seleccionar el producto se actualizara el precio.

        label_cantidad = tk.Label(lblframe, text="Cantidad:", bg="#C6D9E3", font="sans 12 bold")  #indica la cantidad de el producto.
        label_cantidad.place(x=730, y=12)
        self.entry_cantidad = ttk.Entry (lblframe, font="sans 12 bold")
        self.entry_cantidad.place(x=820, y=2, width=50, height=50)

        treFrame = tk.Frame (frame2, bg="blue")   #La tabla que cargara los productos.
        treFrame.place(x=150, y=120, width=800, height=200)

        scrol_y = ttk.Scrollbar(treFrame, orient=VERTICAL)
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.tree = ttk.Treeview (treFrame, columns=("Producto","Precio","Cantidad","Subtotal"), show="headings", height=10, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set)
        scrol_y.config (command=self.tree.yview)
        scrol_x.config (command=self.tree.xview)

        self.tree.heading("#1", text="Producto")
        self.tree.heading("#2", text="Precio")
        self.tree.heading("#3", text="Cantidad")
        self.tree.heading("#4", text="Subtotal")

        self.tree.column("Producto", anchor="center")
        self.tree.column("Precio", anchor="center")
        self.tree.column("Cantidad", anchor="center")
        self.tree.column("Subtotal", anchor="center")

        self.tree.pack(expand=True, fill=BOTH)

        lblframe1 = LabelFrame (frame2, text="Opciones", bg= "#C6D9E3", font="sans 12 bold")
        lblframe1.place (x=10, y=380, width=980, height=100)

        boton_agregar = tk.Button (lblframe1, text="Agregar Articulo", bg= "#109DFA", font="sans 12 bold", command=self.registrar)
        boton_agregar.place(x=50, y=10, width=240, height=50)

        boton_pagar = tk.Button (lblframe1, text="Pagar", bg= "#6DC36D", font="sans 12 bold", command=self.abrir_ventana_pago)
        boton_pagar.place(x=400, y=10, width=240, height=50)

        boton_facturas = tk.Button (lblframe1, text="Ver Facturas", bg= "#109DFA", font="sans 12 bold", command=self.abrir_ventana_factura)
        boton_facturas.place(x=700, y=10, width=240, height=50)

        self.label_suma_total = tk.Label (frame2, text="Total a Pagar: Bs 0", bg="#109DFA", font="sans 25 bold") #mostrara el total de los productos que se incresen a la tabla
        self.label_suma_total.place(x=360, y=335)
    
    def cargar_productos(self):
        try:
           conn = sqlite3.connect(self.db_name) #conexion a la base de datos.
           c = conn.cursor() #Para cargar los productos
           c.execute("SELECT nombre FROM inventario") #llamando a la base de datos.
           productos = c.fetchall() #para obtener los resultados de la consulta.
           self.entry_nombre["values"] = [producto[0]for producto in productos] #indicando que se va a seleccionar de una lista.
           if not productos: #con esto hara la consulta
               print("No se encontraron productos en la base de datos.") #cuando no exista el producto arrojara este mensaje.
           conn.close() #esto cierra la conexion con la base de datos una vez se haga la consulta.
        except sqlite3.Error as e: #la "e" sera la variable que muestre el error que se esta presentando
            print("Error al cargar productos desde la base de datos:", e)
    
    def actualizar_precio (self, event):
        nombre_producto = self.entry_nombre.get() #el "get" permite obtener el valor que se selecciono en el combobox
        print(nombre_producto)
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            sql = "SELECT precio FROM inventario WHERE nombre = '{}'".format(nombre_producto)
            print(sql)
            c.execute(sql)
#            c.execute("SELECT precio FROM inventario WHERE nombre = ?",(nombre_producto))
            precio = c.fetchone() #el "fetchone" tiene el resultado de la consulta. 
            print(precio[0])
            if (precio):
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END) #para que limpie el campo desde cero hasta el final.
                self.entry_valor.insert(0, precio[0]) #se va a insertar el producto
                self.entry_valor.config(state="readonly") #se configurara el producto, haciendo que una vez insertado no se modificara el precio
            else:
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END) 
                self.entry_valor.insert(0, "Precio no disponible")
                self.entry_valor.config(state="readonly")
        except sqlite3.Error as e:
             messagebox.showerror("Error", f"Error al obtener el precio:{e}")
        finally:
            conn.close() #cerrara la conexion al hacer la consulta.
    
    def actualizar_total(self):
        total = 0.0 #donde se va a iniciar. 
        for child in self.tree.get_children(): # "child son los datos que estan ingresando a la tabla"
            subtotal = float(self.tree.item(child, "values") [3])
            total += subtotal
        self.label_suma_total.config(text=f"Total a Pagar: Bs {total:.2f}") #arrojara la suma de el precio de los productos.

    def registrar(self): #se registraran 3 variables, producto, precio, cantidad
        producto = self.entry_nombre.get()
        precio = self.entry_valor.get()
        cantidad = self.entry_cantidad.get()

        if producto and precio and cantidad: 
            try:
                cantidad = int(cantidad)
                if not self.verificar_stock(producto, cantidad):
                   messagebox.showerror("Error","Stock insuficientes para el producto seleccionado")
                   return
                precio = float(precio)
                subtotal = cantidad * precio


                self.tree.insert("", "end", values=(producto, f"{precio:.2f}", cantidad, f"{subtotal:.2f}"))
               
                self.entry_nombre.set("") #para que se limpie el combobox
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.config(state="readonly")
                self.entry_cantidad.delete(0, tk.END)

                self.actualizar_total()
            except ValueError:
               messagebox.showerror("Error","Cantidad o precio no valido")
        else:
            messagebox.showerror("Error", "Debe completar todos los campos")
    
    def verificar_stock(self, nombre_producto, cantidad): #verifica que se tenga la cantidad de un producto y que haya ese producto.
        try:
            conn =sqlite3.connect(self.db_name) #variable para conectarse a la base de datos.
            c = conn.cursor() #cursor para seleccionar de la base de datos la tabla inventario.
            c.execute("SELECT stock FROM inventario WHERE nombre = ?",(nombre_producto,)) #selecciona la columna stock.
            stock = c.fetchone()
            if stock and stock[0] >= cantidad: #verificara si en la base da datos se tiene la cantidad de stock que se solicita en la venta.
                return True
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al verificar el stock: {e}")
            return False
        finally:
            conn.close() #cerrando consulta

    def obtener_total(self): #para realizar el pago
        total =0.0
        for child in self.tree.get_children(): 
            subtotal= float(self.tree.item(child, "values") [3])
            total += subtotal #suma el subtotal al total.
        return total
    

    def abrir_ventana_pago(self):
        if not self.tree.get_children():
            messagebox.showerror("Error","No hay articulos para pagar") #al presionar el boton pagar abrira la ventana pagar, verificara si no hay productos en la tabla, si no nos hay se utilizara esta linea de codigo.
            return

        ventana_pago= Toplevel(self)
        ventana_pago.title("Realizar pago")
        ventana_pago.geometry("400x400")
        ventana_pago.config(bg="#109DFA")
        ventana_pago.resizable(False, False)

        label_total = tk.Label(ventana_pago, bg="#109DFA", text=f"Total a pagar: Bs {self.obtener_total():.2f}", font="sans 14 bold")
        label_total.place(x=70, y=20)


        label_cantidad_pagada = tk.Label(ventana_pago, bg="#109DFA", text="Cantidad pagada:", font="sans 14 bold")
        label_cantidad_pagada.place (x=100, y=90)
        entry_cantidad_pagada= ttk.Entry(ventana_pago, font="sans 14 bold")
        entry_cantidad_pagada.place(x=100, y=130)

        label_cambio = tk.Label(ventana_pago, bg="#109DFA", text="", font="Arial 12") #muestra si se debe dar dinero de cambio al cliente.
        label_cambio.place(x=100, y=190)

     
        def calcular_cambio():
            try:
                cantidad_pagada = float(entry_cantidad_pagada.get())
                total = self.obtener_total()
                cambio = cantidad_pagada - total #se restara el total de los productos con el monto que da el cliente "cantidad pagada". y es aca en donde se verifica si hay que darle cambio al cliente.
                if cambio < 0:
                    messagebox.showerror("Error", "La cantidad pagada es insufuciente") #si la cantidad pagada, es menor al monto entonces no se procesa la venta.
                    return
                label_cambio.config(text=f"Vuelto: Bs {cambio:.2f}")
            except ValueError:
                messagebox.showerror("Error","Cantidad pagada no valida")
        boton_calcular = tk.Button(ventana_pago, text="Calcular Cambio", bg= "white", font="sans 12 bold", command= calcular_cambio)
        boton_calcular.place(x=100 , y=240)

        boton_pagar = tk.Button(ventana_pago, text="Pagar", bg="red", font="sans 12 bold", command= lambda: self.pagar(ventana_pago,entry_cantidad_pagada, label_cambio))# command=lambda: self.pagar(ventana_pago, entry_cantidad_pagada, label_cambio))
        boton_pagar.place (x=100 , y=340)

    def pagar(self, ventana_pago, entry_cantidad_pagada, label_cambio):
        try:
            cantidad_pagada= float(entry_cantidad_pagada.get())
            total = self.obtener_total()
            cambio = cantidad_pagada - total
            if cambio <0:
                messagebox.showerror("Error", "La cantidad pagada es insufuciente")
                return
            
            conn = sqlite3.connect(self.db_name) #conexion a la base de datos.
            c = conn.cursor()
            try:
                for child in self.tree.get_children(): 
                    item = self.tree.item(child, "values")
                    nombre_producto = item [0]
                    cantidad_vendida = int(item[2])
                    if not self.verificar_stock(nombre_producto,cantidad_vendida):
                        messagebox.showerror("Error", f"Stock insuficiente para el producto: {nombre_producto}") #para obtener el nombre del producto
                        return

                    c.execute("INSERT INTO ventas (factura, nombre_articulo, valor_articulo, cantidad, subtotal) VALUES (?,?,?,?,?)",
                              (self.numero_factura_actual, nombre_producto, float(item[1]), cantidad_vendida, float(item[3]))) #para ejecutar la consulta
                    c.execute("UPDATE inventario SET stock = stock - ? WHERE nombre = ?",(cantidad_vendida, nombre_producto)) #Esta funcion hara que si se vende un producto se reste en el inventario la cantidad que se tiene
                conn.commit() #para que se guarde en la tabla    
                messagebox.showinfo("Exito", "Venta Registrada Exitosamente")

                self.numero_factura_actual += 1   #para que se incremente la factura a medida que se vaya comprando
                self.mostrar_numero_factura()

                for child in self.tree.get_children():
                    self.tree.delete(child) #aca se indica que para cuando se guarde la factura la tabla quede nuevamente en blanco
                self.label_suma_total.config(text="Total a Pagar: 0 Bs") #para que el total tambien se limpie
                
                ventana_pago.destroy() #con esto se cerrara la ventana 

            except sqlite3.Error as e:
                conn.rollback () #revierte pa transaccion en caso de error para que no se guarden los datos.
                messagebox.showerror("Error", f"Error al registrar la venta: {e}")
            finally:
                conn.close()
        except ValueError:
            messagebox.showerror("Error","Cantidad pagada no valida")      

    def obtener_numero_factura_actual(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute ("SELECT MAX(factura) FROM ventas") #colsulta que seleccionara el numero de factura maximo.
            max_factura = c.fetchone()[0]
            if max_factura:
                return max_factura +1
            else:
                return 1 #si no hay facturas regresa el 1 
        except sqlite3.Error as e: 
            messagebox.showerror("Error",f"Error al obtener el numero de factura: {e}")
            return 1     #indicando que retorne al 1
        finally:
            conn.close() #cierra la conexion con la base de datos.

    def mostrar_numero_factura(self):  
        self.numero_factura.set(self.numero_factura_actual) #el "set" hara que lo muestre.

    def abrir_ventana_factura(self):
        ventana_facturas = Toplevel (self)
        ventana_facturas.title("Facturas")
        ventana_facturas.geometry("800x500")
        ventana_facturas.config(bg="#109DFA")
        ventana_facturas.resizable(False, False)

        facturas= Label(ventana_facturas, bg="#109DFA",text="Facturas Registradas",font="sans 36 bold")
        facturas.place(x=150, y=15)

        treFrame = tk.Frame(ventana_facturas, bg= "#109DFA")
        treFrame.place(x=10, y=100, width=780, height=380) 

        scrol_y = ttk.Scrollbar(treFrame, orient=VERTICAL)
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        tree_facturas = ttk.Treeview(treFrame, columns=("ID","Factura","Producto","Precio","Cantidad","Subtotal"), show="headings", height=10, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set)
        scrol_y.config(command=tree_facturas.yview)
        scrol_x.config(command=tree_facturas.xview)

        tree_facturas.heading("#1", text="ID")
        tree_facturas.heading("#2", text="Factura")
        tree_facturas.heading("#3", text="Producto")
        tree_facturas.heading("#4", text="Precio")
        tree_facturas.heading("#5", text="Cantidad")
        tree_facturas.heading("#6", text="Subtotal")

        tree_facturas.column("ID", width=40, anchor="center")
        tree_facturas.column("Factura", width=100, anchor="center")
        tree_facturas.column("Producto", width=200,anchor="center")
        tree_facturas.column("Precio", width=130, anchor="center")
        tree_facturas.column("Cantidad",width=130, anchor="center")
        tree_facturas.column("Subtotal",width=130, anchor="center")

        tree_facturas.pack(expand=True, fill=BOTH)

        self.cargar_facturas(tree_facturas)

    def cargar_facturas(self, tree):
        try:
            conn =sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT * FROM ventas")
            facturas = c.fetchall() #para obtener todos los datos que se piden en la factura.
            for factura in facturas:
                self.tree.insert("", "end", values=factura)
            conn.close() #cierra la conexion una vez esten insertado los valores.
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar las facturas: {e}")     


