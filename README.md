# Registradora LVHC
Este codigo es diseñado con el fin de crear una registradora que trabaja con bases de datos esta especificamente trabaja con sqlite.

Para trabajar con sqlite la base de datos, se necesita descargar un programa llamado _DB Browser for SQlite_ el cual es una herramienta gratuita y de codigo abierto que permite crear, administrar, y explorar bases de datos SQLite de forma visual.
Es una herramienta bastante practica y sencilla de manejar.

Este es el link de la descarga para el _SQlite_: https://sqlitebrowser.org/dl/

## Archivos para que el programa funcione.
El codigo esta dividivo en 5 archivos los cuales son los siguientes:

## 1.  index.py
Es el archivo desde donde se ejecuta el programa.

## 2.  manager.py
Proporciona la ventana pincipal en donde estan alojados los botones de venta e inventario.

## 3. container.py
En este archivo tenemos lo que son las configuraciones de visualizacion de las ventanas venta e inventario
y tenemos tambien las configuraciones para que se muestre el logo.

## 4. inventario.py
Este archivo contiene todo los referente a inventario, paa ser especificos el inventario un inventario es una herramienta fundamental para la gestión de una empresa, ya que permite controlar los activos, optimizar las compras, prevenir pérdidas y mejorar la eficiencia. En este caso nuestra Registradora esta basada en una papeleria en donde encontraremos productos como borradores, sacapuntas, fichas etc.
Estos productos se encuentran guardados dentro de la base de la base de datos.

La ventana de inventario permite tanto registrar como modificar los productos que se encuentran en la base de datos.

Cuenta con una tabla en donde se muestran los productos que se tienen.

## 5. ventas.py
Aca se tienen funcones que permiten poder seleccionar los productos que se deseen comprar, y meintras hace eso va totalizando y arrojando la cantidad esto en "Bs"
que significa "Bolivares" los cuales son la moneda oficial de Venezuela.

En esta ventana se muestra un entry (entrada de datos) que contiene los productos que estan en la base de datos, al seleccionar uno de esos productos automaticamente se mostrata el precio en el renglon de precio. Manualmente habra que colocar la cantidad de ese producto que se desee y luego presionar el boton agregar para que el producto sea agregado a la tabla.
Desde esta ventana tambien esta una funcion que permite poder pagar el o los productos, cada que se haga una compra se va generando una factura que se visualizan presionando en el boton de ver facturas.





