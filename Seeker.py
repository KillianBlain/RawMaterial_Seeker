import sqlite3
import matplotlib.pyplot as plt
import csv
from tkinter import *

formulation = []

def formulation_creation():
    
    def ingredient_research():
        ingredient_property_value = ingredient_property_entry.get()
        connection_db = sqlite3.connect("raw_material.db")
        cursor = connection_db.cursor()
        ingredient_property_value = f"%{ingredient_property_value}%" #f-string function to add % around ingredient_property
        cursor.execute("SELECT COSING_Ref_No, INCI_name FROM INGREDIENTS WHERE Chem_IUPACName_Description LIKE ?", (ingredient_property_value,))
        
        #Frame for the research widget
        research_widget = Frame(window, borderwidth=10, relief=GROOVE, width=420, height=400)
        research_widget.place(x=350, y=35)
        research_widget.pack_propagate(False) #lock width and height from the Frame
        text = Label(research_widget, text='Results founds in database', fg='red')
        text.pack()
        
        for line in cursor.fetchall():
            result_label = Label(research_widget, text=f"{line[0]} - {line[1]}")
            result_label.pack()
    
    def add_to_formulation():
        cosing_value = cosing_entry.get()
        formulation.append(cosing_value)
        print("Current formulation:", formulation)
    
    welcome_label.pack_forget()#delete the welcome message
    
    # Create the widget frame
    widget = Frame(window, borderwidth=10, relief = GROOVE)
    widget.place(x=5, y=35)
    
    intro_frame = Frame(widget, borderwidth=2, relief = GROOVE)
    intro_frame.pack(pady=5)
    intro_text = Label(intro_frame, text='Creating a new formulation', fg='black')
    intro_text.pack()
    
    ingredient_property_frame = Frame(widget, borderwidth=2) #create a new frame for the ingredient property part
    ingredient_property_frame.pack()
    ingredient_property_label = Label(ingredient_property_frame, text="Enter the researched property of your raw material :", fg='black')
    ingredient_property_label.pack()
    ingredient_property_entry = Entry(ingredient_property_frame)
    ingredient_property_entry.pack()
    ingredient_property_value = ingredient_property_entry.get()
    research_button = Button(ingredient_property_frame, text = "start research", command = ingredient_research)
    research_button.pack(pady=10)
    
    cosing_frame = Frame(widget, borderwidth=2, relief = GROOVE)
    cosing_frame.pack()
    cosing_label = Label(cosing_frame, text="Enter the COSING number of the chosen raw material :", fg='black')
    cosing_label.pack()
    cosing_entry = Entry(cosing_frame)
    cosing_entry.pack(padx=10)
    adding_button = Button(cosing_frame, text = "add ingredient to formulation", command = add_to_formulation)
    adding_button.pack(pady=10)
    
    widget.mainloop()
    
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
    
def quit_program():
    window.destroy()

def connection_db():
    connection_db = sqlite3.connect("raw_material.db")
    print("database raw_material.db connected")
    return connection_db
    
def deconnection_db():
    connection_db.close()
    print("database raw_material.db deconnected")

# Create the main window
window = Tk()
window.geometry("800x500")
window.title("Raw Material Seeker") #main window title
window['bg']='white' #background color of main window
window.resizable(height=False,width=False) #main window is not resizable

# Create the menu frame
zone_menu = Frame(window, borderwidth=0, bg='#557788')
zone_menu.pack(side=TOP, anchor="w", fill=X)  # Place the menu frame at the top-left

#folder menu
folder_menu = Menubutton(zone_menu, text='File', width='20', borderwidth=2, bg='gray', activebackground='darkorange', relief=RAISED)
folder_menu.pack(side=LEFT, padx=0, pady=0)  # Place File button to the left

#folder menu roll
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
data_base_menu.pack(side=LEFT, padx=0, pady=0) 
data_base_roll = Menu(data_base_menu)
data_base_roll.add_command(label='Connect to database', command=connection_db)
data_base_roll.add_command(label='Disconnect from database', command=deconnection_db)
data_base_menu.configure(menu=data_base_roll)

# Welcome message
welcome_label = Label(window, text="Welcome to the Raw Material Seeker!")
welcome_label.pack()

# Run the Tkinter main loop
window.mainloop()
