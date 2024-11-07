import sqlite3
import matplotlib.pyplot as plt
import csv

def ingredient_research(cursor):
    ingredient_property = str(input("Renseigner la propriété de l'ingrédient recherchée : ")) 
    ingredient_property = f"%{ingredient_property}%" #f-string function to add % around ingredient_property
    cursor.execute("SELECT COSING_Ref_No, INCI_name FROM INGREDIENTS WHERE Chem_IUPACName_Description LIKE ?", (ingredient_property,))
    line = cursor.fetchone()
    while line:
        print(line)
        line = cursor.fetchone()
    cosing = str(input("Renseigner le numéro de COSING choisi : "))
    return cosing

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
        plt.title("Composition de la formulation")
        plt.show()

def save_formulation (formulation, cursor, filename="formulation.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["COSING_Ref_No", "INCI_name", "Function", "Volume (ml)"])
        for ingredient in formulation:
            requete = 'SELECT INCI_name, Function FROM INGREDIENTS WHERE COSING_Ref_No = ' + ingredient [0] ;
            cursor.execute(requete)
            elt = cursor.fetchone()
            if elt:
                writer.writerow([ingredient[0], elt[0], elt[1], ingredient[1]])
    print(f"Formulation sauvegardée dans {filename}")

connection_db = sqlite3.connect("raw_material.db")
cursor = connection_db.cursor()

formulation = []

i = True
while i :
    cosing = ingredient_research(cursor)
    v = float(input("Entrer le volume à utiliser : "))
    formulation.append([cosing, v])
    i = str(input("Entrer 'oui' si vous souhaitez entrer une nouvelle MP ou 'non' si vous ne souhaitez plus en ajouter : "))
    if i != "oui" :
        i = False

show_formulation (formulation, cursor)
save_formulation (formulation, cursor)
   
connection_db.close()
