from tkinter import *
import tkinter as tk 
from ventas import Ventas
from inventario import Inventario
from PIL import Image, ImageTk

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0,y=0,width=800,height=400)#ubicacion
        self.config(bg="#C6D9E3")
        self.widgets()

    def show_frames(self, container):#para distintas ventanas
        top_level= tk.Toplevel(self) #ventanas independientes 
        frame= container(top_level)
        frame.config(bg="#C6D9E3")
        frame.pack(fill="both", expand=True) #empaquetar 
        top_level.geometry("1000x650+120+20")
        top_level.resizable (False,False) #para que no se redimencione
        
        top_level.transient(self.master)
        top_level.grab_set()
        top_level.focus_set
        top_level.lift()

    def ventas(self):
        self.show_frames(Ventas)

    def inventario(self):
        self.show_frames(Inventario)

    def widgets (self):

        frame1 = tk.Frame(self, bg="#C6D9E3") #primera ventana
        frame1.pack()
        frame1.place(x=0, y=0, width=800, height=400)

        btnventas = Button(frame1,bg="#f4b400", fg="white", font="sans 18 bold",text="Ventas", command=self.ventas)
        btnventas.place(x=500, y=30, width=240, height=60)
        
        btninventario=Button(frame1,bg="red",fg="white",font="sans 18 bold",text="Inventario", command=self.inventario)
        btninventario.place(x=500, y=130, width=240, height=60)


        self.logo_image = Image.open("imagenes/Papeleria.png")
        self.logo_image = self.logo_image.resize((280,280))
        self.logo_image= ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(frame1, image=self.logo_image, bg="#C6D9E3")
        self.logo_label.place(x=100, y=30)

        derechos_de_autor_label= tk.Label(frame1,text="© 2024 Future LVHC. Todos los derechos reservados", font="sans 12 bold",bg= "#C6D9E3", fg="black")
        derechos_de_autor_label.place(x=180, y=350)