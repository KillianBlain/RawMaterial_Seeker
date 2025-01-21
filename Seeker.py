import sqlite3
import matplotlib.pyplot as plt
import csv
from tkinter import *
import os

def formulation_creation():
    
    formulation = []
    
    intro_text = Label(widget, text='Creating a new formulation', fg='black')
    intro_text.grid()
    
    ingredient_property_label = Label(widget, text="Enter the researched property of your raw material :", fg='black')
    ingredient_property_label.grid()
    ingredient_property_entry = Entry(widget)
    ingredient_property_entry.grid()
    research_button = Button(widget, text = "start research", command = lambda : ingredient_research)
    research_button.grid()
    
    cosing_label = Label(widget, text="Enter the COSING number of the chosen raw material :", fg='black')
    cosing_label.grid()
    cosing_entry = Entry(widget)
    cosing_entry.grid()
    adding_button = Button(widget, text = "add ingredient to formulation", command = add_form)
    adding_button.grid()

def add_to_formulation():
    cosing_value = cosing_entry.get()
    if cosing_value:
        formulation.append(cosing_value)
        print("Current formulation:", formulation)

def ingredient_research(ingredient_property):
   connection_db = sqlite3.connect("raw_material.db")
   cursor = connection_db.cursor()
   ingredient_property = f"%{ingredient_property}%" #f-string function to add % around ingredient_property
   cursor.execute("SELECT COSING_Ref_No, INCI_name FROM INGREDIENTS WHERE Chem_IUPACName_Description LIKE ?", (ingredient_property,))
    
   for line in cursor.fetchall():
       result_label = Label(widget, text=f"{line[0]} - {line[1]}")
       result_label.grid()
    
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

# Create the main window
window = Tk()
window.title("Raw Material Seeker")
window.geometry("800x500")

# Create the menu frame
zone_menu = Frame(window, borderwidth=3, bg='#557788')
zone_menu.grid(row=0, column=0)

# Create the widget frame
widget = Frame(window)
widget.grid()

# Menu buttons
folder_menu = Menubutton(zone_menu, text='File', width='20', borderwidth=2, bg='gray', activebackground='darkorange', relief=RAISED)
folder_menu.grid(row=0, column=0)

#folder menu
folder_menu_roll = Menu(folder_menu)
folder_menu_roll.add_command(label='Create a formulation', command=formulation_creation)
folder_menu_roll.add_command(label='Save formulation', command=save_formulation)
folder_menu_roll.add_command(label="Add a material to db")
folder_menu_roll.add_command(label="Delete a material from db")
folder_menu_roll.add_separator()
folder_menu_roll.add_command(label='Quit', command=quit_program)
folder_menu.configure(menu=folder_menu_roll)

#db menu
data_base_menu = Menubutton(zone_menu, text='Database', width='20', borderwidth=2, bg='gray', activebackground='darkorange', relief=RAISED)
data_base_menu.grid(row=0, column=1)
data_base_roll = Menu(data_base_menu)
data_base_roll.add_command(label='Connect to database', command=connection_db)
data_base_roll.add_command(label='Disconnect from database', command=deconnection_db)
data_base_menu.configure(menu=data_base_roll)

# Welcome message
title_label = Label(widget, text="Welcome to the Raw Material Seeker!")
title_label.grid()

# Run the Tkinter main loop
window.mainloop()
