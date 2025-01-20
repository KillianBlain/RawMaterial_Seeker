import sqlite3
import matplotlib.pyplot as plt
import csv
from tkinter import *
import os

def formulation_creation():
    connection_db = sqlite3.connect("raw_material.db")
    cursor = connection_db.cursor()
    formulation = []
    intro = Label(widget, text='Creating a new formulation', fg='black')
    intro.grid()
    i = True
    while i :
        ingredient_property = Label(widget, text="Enter the researched property of your raw material :", fg='black')
        ingredient_property.grid()
        ingredient_property = Entry(widget)
        ingredient_property.grid()
        button = Button(widget, text = "research", command = ingredient_research(ingredient_property))
        button.grid()
        cosing = Label(widget, text="Enter the COSING number of the chosen raw material :", fg='black')
        cosing.grid()
        cosing = Entry(widget)
        cosing.grid()
        button2 = Button(widget, text = "add ingredient to formulation", command = add_form())
        button2.grid()

def ingredient_research(ingredient_property):
    connection_db = sqlite3.connect("raw_material.db")
    cursor = connection_db.cursor()
    ingredient_property = f"%{ingredient_property}%" #f-string function to add % around ingredient_property
    cosing = cursor.execute("SELECT COSING_Ref_No, INCI_name FROM INGREDIENTS WHERE Chem_IUPACName_Description LIKE ?", (ingredient_property,))
    line = cursor.fetchone()
    while line:
        line.grid()
        line = cursor.fetchone()
    connection_db.close()
    
def add_form():
    formulation.append(cosing)
    formulation.grid()
    return formulation

def ingredient_research_fonctionnelle_sans_affichage():
    connection_db = sqlite3.connect("raw_material.db")
    cursor = connection_db.cursor()
    formulation = []
    i = True
    while i :
        ingredient_property = str(input("Enter the researched property of your raw material : ")) 
        ingredient_property = f"%{ingredient_property}%" #f-string function to add % around ingredient_property
        cosing = cursor.execute("SELECT COSING_Ref_No, INCI_name FROM INGREDIENTS WHERE Chem_IUPACName_Description LIKE ?", (ingredient_property,))
        line = cursor.fetchone()
        while line:
            print(line)
            line = cursor.fetchone()
        cosing = str(input("Enter the COSING number of the chosen raw material : "))
        v = float(input("Enter the desired volume (mL) : "))
        formulation.append([cosing, v])
        print(formulation)
        i = str(input("Enter 'yes' if you want to enter a new raw materiel or 'no' if you doesn't want to add a new one : "))
        if i != "yes" :
            i = False
    return formulation

def recupere():
    showinfo("Alerte", entree.get())

def show_formulation (formulation, cursor) :
    nom_tranches = []
    taille_tranches = []
    for ingredient in formulation :
        requete = 'SELECT INCI_name, Function FROM INGREDIENTS WHERE COSING_Ref_No = ' + ingredient [0] ;
        cursor.execute(requete)
        elt = cursor.fetchone()
        nom_tranches.append (elt [0] + " (" + ingredient [0] + ")")
        taille_tranches.append (ingredient [1])
        print ("- ", ingredient [1], "ml de ", elt [0], "(",elt [1], ") [", ingredient [0], "]")
        plt.pie(taille_tranches, labels = nom_tranches, autopct = "%1.1f%%")
        plt.title("Composition of the formulation")
        plt.show()

def save_formulation (formulation, cursor, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["COSING_Ref_No", "INCI_name", "Function", "Volume (ml)"])
        for ingredient in formulation:
            requete = 'SELECT INCI_name, Function FROM INGREDIENTS WHERE COSING_Ref_No = ' + ingredient [0] ;
            cursor.execute(requete)
            elt = cursor.fetchone()
            if elt:
                writer.writerow([ingredient[0], elt[0], elt[1], ingredient[1]])
    print("Formulation saved into",filename,".")
    
def quit_program(): #trouver une fonction plus gentille ?
    os._exit(0)

def connection_db():
    connection_db = sqlite3.connect("raw_material.db")
    print("database raw_material.db connected")
    return connection_db
    
def deconnection_db():
    connection_db.close()
    print("database raw_material.db deconnected")

# Création de la fenêtre
window = Tk()
window.title("Raw_Material_Seeker")
window.geometry("800x500")

# Création du cadre-conteneur pour les menus
zoneMenu = Frame(window, borderwidth=3, bg='#557788')
zoneMenu.grid(row=0,column=0)

# Création de la zone widget
widget = Frame(window)
widget.grid()

# Création de l'onglet Fichier
folder_menu = Menubutton(zoneMenu, text='Fichier', width='20', borderwidth=2, bg='gray', activebackground='darkorange',relief = RAISED)
folder_menu.grid(row=0,column=0)

# Création de l'onglet database
data_base_menu = Menubutton(zoneMenu, text='Base de données', width='20', borderwidth=2, bg='gray', activebackground='darkorange',relief = RAISED)
data_base_menu.grid(row=0,column=1)
data_base_roll = Menu(data_base_menu)
data_base_roll.add_command(label='Connect a database', command = connection_db)
data_base_roll.add_command(label='Disconnect a database', command = deconnection_db)

# Création de l'onglet Format
menuFormat = Menubutton(zoneMenu, text='Format', width='20', borderwidth=2, bg='gray', activebackground='darkorange',relief = RAISED)
menuFormat.grid(row=0,column=2)

# Création d'un menu défilant
menuDeroulant1 = Menu(folder_menu)
menuDeroulant1.add_command(label='Create a formulation', command = formulation_creation)
menuDeroulant1.add_command(label="Add a material")
menuDeroulant1.add_command(label="Save formulation", command = save_formulation)
menuDeroulant1.add_separator()
menuDeroulant1.add_command(label="Quit", command = quit_program)

# Attribution du menu déroulant au menu Affichage
folder_menu.configure(menu=menuDeroulant1)
data_base_menu.configure(menu=data_base_roll)

#Ajout d'une phrase de bienvenue
titre = Label(widget, text="Welcome to the raw_material_seeker !")
titre.grid()

# boucle tkinter (doit rester à la fin)
window.mainloop()
       
