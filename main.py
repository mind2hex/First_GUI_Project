#!/usr/bin/python3

import tkinter as tk
import json
import pathlib


AUTHOR = "JOHAN | mind2hex"
VERSION = "[v1.0]"

def DB_CHECK():
    """ this function check DATABASE integrity """
    # Checking DATABASE directory
    if pathlib.Path("./DATABASE").exists() == False:
        # Creating DATABASE if directory doesn't exist
        pathlib.mkdir("./DATABASE")

    # Checking DATABASE file
    if pathlib.Path("./DATABASE/inventory.json").exists() == False:
        pathlib.Path("./DATABASE/inventory.json").touch()

    # Checking DATABASE json format
    try:
        json.load(open("./DATABASE/inventory.json","r"))
    except json.decoder.JSONDecodeError:
        # Basic format of the inventory.json file
        lista = json_inventory_format()

        # Saving basic format into a new inventory.json file
        handler = open("./DATABASE/inventory.json","w")
        handler.write(json.dumps(lista, sort_keys=True, indent=4))

    # Checking DATABASE json correct template
    aux = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    try:
        lista = json.load(open("./DATABASE/inventory.json","r"))
        for i in range(len(aux)):
            lista[i][aux[i]]

    except KeyError or IndexError:
        lista = json_inventory_format()
        handler = open("./DATABASE/inventory.json","w")
        handler.write(json.dumps(lista, sort_keys=True, indent=4))

    # Generating backup
    with open("./DATABASE/inventory.json", "r") as src_file:
        info = src_file.read()

        dst_file = open("./DATABASE/inventory.json.backup", "w")
        dst_file.write(info)

def json_inventory_format():
    aux = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    lista = []
    for i in range(len(aux)):
        lista.append({aux[i]:[]})

    return lista

def search_string(string):
    # Routines to search string in DATABASE
    # string probably will be an ID for every product of the storage
    print(string)

def exit_procedures(root):
    # Routines to save db...
    root.destroy()
    exit(0)

class MOTOGP_DATABASE:
    def __init__(self, master):
        """ Starting Main Window """
        self.master = master
        self.master.title("MotoGP DATABASE")
        self.master.geometry("1250x680")
        self.master.resizable(0,0)
        self.master.configure(background="black")

        # Top image configuration
        self.canvas = tk.Canvas(self.master, widt=4000, height=180, bg="black", bd=0)
        self.canvas.pack(side="top")
        self.img = tk.PhotoImage(file="./resources/main_title.png")
        self.canvas.create_image(500,100, image=self.img)

        # Search section
        self.search_frame = tk.Frame(bg="black")

        self.button_search = tk.Button(self.search_frame, text=" Buscar ", font="arial",
        relief="flat", command= lambda: search_string(self.entry_search.get()))
        self.button_search.pack(side="right")

        self.entry_search  = tk.Entry(self.search_frame, font="arial", justify="left", width=30,
        bd=5)
        self.entry_search.pack(side="right")

        self.search_frame.pack(side="top", fill=tk.X)

        # Inventory section
        self.main_frame = tk.Frame(self.master, relief="groove", bg="black")
        self.button_show_inventory = tk.Button(self.main_frame, text="Mostrar Inventario",
                                               font="arial", command=self.show_inventory,
                                               width=30, height=2)
        self.button_show_inventory.pack()

        self.button_modify_inventory = tk.Button(self.main_frame, text="Modificar Inventario",
                                                 font="arial", width=30, height=2)
        self.button_modify_inventory.pack()

        self.button_add_to_inventory = tk.Button(self.main_frame, text="Agregar al inventario",
                                                 font="arial", width=30, height=2, command=self.add_inventory)
        self.button_add_to_inventory.pack()

        self.button_remove_from_inventory = tk.Button(self.main_frame, text="Quitar del inventario",
                                                      font="arial", width=30, height=2, command=self.remove_inventory)
        self.button_remove_from_inventory.pack()

        self.button_exit = tk.Button(self.main_frame, text="Salir", font="arial",
                                     command= lambda: exit_procedures(self.master),
                                     width=30, height=2)
        self.button_exit.pack()

        self.main_frame.pack(fill=tk.X)

    def show_inventory(self):
        self.show_inventory_window = tk.Toplevel(self.master, bg="grey")
        self.app = show_inventory_manager(self.show_inventory_window)

    def add_inventory(self):
        self.add_inventory_window = tk.Toplevel(self.master, bg="grey")
        self.app = add_inventory_manager(self.add_inventory_window)

    def remove_inventory(self):
        self.remove_inventory_window = tk.Toplevel(self.master, bg="grey")
        self.app = remove_inventory_manager(self.remove_inventory_window)


class show_inventory_manager:
    def __init__(self, master):
        """ Inventory list window initialization """
        self.master = master
        self.master.title("Inventory list")
        self.master.geometry("1200x600")
        self.master.resizable(0,0)

        # Title section
        self.title_frame = tk.Frame(self.master)
        self.title_frame.pack(side="top", fill=tk.X)

        # TITLE-NAME _ width pair
        self.aux = (("NOMBRE",20), ("DESCRIPCION",40), ("CANTIDAD",13), ("PRECIO LLEGADA",18),
        ("PRECIO TALLERES",18), ("PRECIO PUBLICO",18))

        self.label_title = [0, 1, 2, 3, 4, 5]
        self.counter     = 0
        for i,j in self.aux:
            self.label_title[self.counter] = tk.Label(self.title_frame, text=i, font="ARIAL", width=j,
            height=3, relief="groove")
            self.label_title[self.counter].pack(side="left")
            self.counter += 1

        # list section
        self.list_frame = tk.Frame(self.master)
        self.list_frame.pack(fill=tk.X)

        self.scrollbar = tk.Scrollbar(self.list_frame, command = self.yview)#, command=scroll_handler)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.inventory_list = [0, 1, 2, 3, 4, 5]
        self.counter = 0
        self.scroll_function_list = [self.yscroll1, self.yscroll2, self.yscroll3, self.yscroll4, self.yscroll5, self.yscroll6]
        for i in [20, 40, 14, 18, 18, 18]:
            self.inventory_list[self.counter] = tk.Listbox(self.list_frame,
            yscrollcommand = self.scroll_function_list[self.counter], font="arial", heigh=40, width=i, relief="groove")
            self.inventory_list[self.counter].pack(side="left")
            self.counter += 1

        # inserting values from database to list
        self.aux        = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.info       = json.load(open("./DATABASE/inventory.json", "r"))
        self.text_lines = ["", "", "", "", "", ""]
        self.counter    = 0
        for i in range(len(self.aux)):
            for j in range(len(self.info[i][self.aux[i]])):
                for x in range(6):
                    self.inventory_list[x].insert(tk.END, str(self.info[i][self.aux[i]][j][x]))

        # Final part
        self.footer_total_frame = tk.Frame(self.master)
        self.footer_total_frame.pack(side="right")

        self.footer_total = [0, 0, 0]
        self.footer_total[0] = tk.Label(self.footer_total_frame, width=20)
        self.footer_total[0].pack(fill=tk.X)


    def yscroll1(self, *args):
        if self.inventory_list[1].yview() != self.inventory_list[0].yview():
            self.inventory_list[1].yview_moveto(args[0])

        if self.inventory_list[2].yview() != self.inventory_list[0].yview():
            self.inventory_list[2].yview_moveto(args[0])

        if self.inventory_list[3].yview() != self.inventory_list[0].yview():
            self.inventory_list[3].yview_moveto(args[0])

        if self.inventory_list[4].yview() != self.inventory_list[0].yview():
            self.inventory_list[4].yview_moveto(args[0])

        if self.inventory_list[5].yview() != self.inventory_list[0].yview():
            self.inventory_list[5].yview_moveto(args[0])

        self.scrollbar.set(*args)

    def yscroll2(self, *args):
        if self.inventory_list[0].yview() != self.inventory_list[1].yview():
            self.inventory_list[0].yview_moveto(args[0])

        if self.inventory_list[2].yview() != self.inventory_list[1].yview():
            self.inventory_list[2].yview_moveto(args[0])

        if self.inventory_list[3].yview() != self.inventory_list[1].yview():
            self.inventory_list[3].yview_moveto(args[0])

        if self.inventory_list[4].yview() != self.inventory_list[1].yview():
            self.inventory_list[4].yview_moveto(args[0])

        if self.inventory_list[5].yview() != self.inventory_list[1].yview():
            self.inventory_list[5].yview_moveto(args[0])
        self.scrollbar.set(*args)

    def yscroll3(self, *args):
        if self.inventory_list[0].yview() != self.inventory_list[2].yview():
            self.inventory_list[0].yview_moveto(args[0])

        if self.inventory_list[1].yview() != self.inventory_list[2].yview():
            self.inventory_list[1].yview_moveto(args[0])

        if self.inventory_list[3].yview() != self.inventory_list[2].yview():
            self.inventory_list[3].yview_moveto(args[0])

        if self.inventory_list[4].yview() != self.inventory_list[2].yview():
            self.inventory_list[4].yview_moveto(args[0])

        if self.inventory_list[5].yview() != self.inventory_list[2].yview():
            self.inventory_list[5].yview_moveto(args[0])
        self.scrollbar.set(*args)

    def yscroll4(self, *args):
        if self.inventory_list[0].yview() != self.inventory_list[3].yview():
            self.inventory_list[0].yview_moveto(args[0])

        if self.inventory_list[1].yview() != self.inventory_list[3].yview():
            self.inventory_list[1].yview_moveto(args[0])

        if self.inventory_list[2].yview() != self.inventory_list[3].yview():
            self.inventory_list[2].yview_moveto(args[0])

        if self.inventory_list[4].yview() != self.inventory_list[3].yview():
            self.inventory_list[4].yview_moveto(args[0])

        if self.inventory_list[5].yview() != self.inventory_list[3].yview():
            self.inventory_list[5].yview_moveto(args[0])
        self.scrollbar.set(*args)

    def yscroll5(self, *args):
        if self.inventory_list[0].yview() != self.inventory_list[4].yview():
            self.inventory_list[0].yview_moveto(args[0])

        if self.inventory_list[1].yview() != self.inventory_list[4].yview():
            self.inventory_list[1].yview_moveto(args[0])

        if self.inventory_list[2].yview() != self.inventory_list[4].yview():
            self.inventory_list[2].yview_moveto(args[0])

        if self.inventory_list[3].yview() != self.inventory_list[4].yview():
            self.inventory_list[3].yview_moveto(args[0])

        if self.inventory_list[5].yview() != self.inventory_list[4].yview():
            self.inventory_list[5].yview_moveto(args[0])
        self.scrollbar.set(*args)

    def yscroll6(self, *args):
        if self.inventory_list[0].yview() != self.inventory_list[5].yview():
            self.inventory_list[0].yview_moveto(args[0])

        if self.inventory_list[1].yview() != self.inventory_list[5].yview():
            self.inventory_list[1].yview_moveto(args[0])

        if self.inventory_list[2].yview() != self.inventory_list[5].yview():
            self.inventory_list[2].yview_moveto(args[0])

        if self.inventory_list[3].yview() != self.inventory_list[5].yview():
            self.inventory_list[3].yview_moveto(args[0])

        if self.inventory_list[4].yview() != self.inventory_list[5].yview():
            self.inventory_list[4].yview_moveto(args[0])
        self.scrollbar.set(*args)

    def yview(self, *args):
        for i in range(6):
            self.inventory_list[i].yview(*args)

    def calculate_total_from_DB():
        # Calculating total 1
        self.aux        = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.info       = json.load(open("./DATABASE/inventory.json", "r"))
        for i in range(len(self.aux)):
            for j in range(len(self.info[i][self.aux[i]])):
                pass

class add_inventory_manager:
    def __init__(self, master):
        """ Inventory list window initialization """
        self.master = master
        self.master.title("Inventory list")
        self.master.geometry("800x175")
        self.master.resizable(0,0)

        # FRAME 1
        self.test_frame_1 = tk.Frame(self.master)
        self.test_frame_1.pack(fill=tk.X)
        self.name_label = tk.Label(self.test_frame_1, relief="groove", borderwidth=2,
                                   width=12, height=1, text="NOMBRE", font=("ARIAL", 12))
        self.name_label.pack(side="left")
        self.name_entry = tk.Entry(self.test_frame_1, font=("ARIAL", 12))
        self.name_entry.pack(fill=tk.X, padx=4)

        # FRAME 2
        self.test_frame_2 = tk.Frame(self.master)
        self.test_frame_2.pack(fill=tk.X)
        self.desc_label = tk.Label(self.test_frame_2, relief="groove", borderwidth=2,
                                   width=12, height=1, text="DESCRIPCION", font=("ARIAL", 12))
        self.desc_label.pack(side="left")
        self.desc_entry = tk.Entry(self.test_frame_2, font=("ARIAL", 12))
        self.desc_entry.pack(fill=tk.X, padx=4)

        # FRAME 3
        self.test_frame_3 = tk.Frame(self.master)
        self.test_frame_3.pack(fill=tk.X)
        self.cant_label = tk.Label(self.test_frame_3, relief="groove", borderwidth=2,
                                   width=12, height=1, text="CANTIDAD", font=("ARIAL", 12))
        self.cant_label.pack(side="left")
        self.cant_entry = tk.Entry(self.test_frame_3, font=("ARIAL", 12))
        self.cant_entry.pack(fill=tk.X, padx=4)

        # FRAME 4
        self.test_frame_4 = tk.Frame(self.master)
        self.test_frame_4.pack(fill=tk.X)
        self.tot1_label = tk.Label(self.test_frame_4, relief="groove", borderwidth=2,
        width=12, height=1, text="PR LLEGADA", font=("ARIAL",12))
        self.tot1_label.pack(side="left")
        self.tot1_entry = tk.Entry(self.test_frame_4, font=("ARIAL",12))
        self.tot1_entry.pack(fill=tk.X, padx=4)

        # FRAME 5
        self.test_frame_5 = tk.Frame(self.master)
        self.test_frame_5.pack(fill=tk.X)
        self.tot2_label = tk.Label(self.test_frame_5, relief="groove", borderwidth=2,
                                   width=12, height=1, text="PR TALLERES", font=("ARIAL",12))
        self.tot2_label.pack(side="left")
        self.tot2_entry = tk.Entry(self.test_frame_5, font=("ARIAL",12))
        self.tot2_entry.pack(fill=tk.X, padx=4)

        # FRAME 6
        self.test_frame_6 = tk.Frame(self.master)
        self.test_frame_6.pack(fill=tk.X)
        self.tot3_label = tk.Label(self.test_frame_6, relief="groove", borderwidth=2,
                                   width=12, height=1, text="PR PUBLICO", font=("ARIAL",12))
        self.tot3_label.pack(side="left")
        self.tot3_entry = tk.Entry(self.test_frame_6, font=("ARIAL",12))
        self.tot3_entry.pack(fill=tk.X, padx=4)

        # button frame
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(fill=tk.X)
        self.add_button = tk.Button(self.button_frame, text="AGREGAR", font=("arial", 12),
                                    relief="groove", borderwidth=4, command=self.press_button, width=8,
                                    height=1)
        self.add_button.pack()
        
    def press_button(self):
        """ function handler for add button """

        status = True
        name_val = self.name_entry.get()
        desc_val = self.desc_entry.get()
        cant_val = self.cant_entry.get()
        tot1_val = self.tot1_entry.get()
        tot2_val = self.tot2_entry.get()
        tot3_val = self.tot3_entry.get()
        
        lista = [(name_val, "NOMBRE"), (cant_val, "CANTIDAD"),
                 (tot1_val, "PRECIO LLEGADA"), (tot2_val, "PRECIO TALLERES"),
                 (tot3_val, "PRECIO PUBLICO")]

        # THis validation check needs more work
        aux = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "

        if len(desc_val) == 0 or desc_val.isspace() == True:
            self.error_label(f" No se ha introducido: DESCRIPCION ")
            status = False
            return 0

        for i in desc_val.upper():
            if i not in aux:
                self.error_label(f" Caracter invalido en: DESCRIPCION ")
                status = False
                return 0
        
        for i,j in lista:
            if j in ["NOMBRE"]:
                if len(i) == 0 or i.isspace() == True:
                    self.error_label(f" No se ha introducido: {j} ")
                    status = False
                    break

                if i.isalnum() == False:
                    self.error_label(f" Caracter invalido: {j} ")
                    status = False
                    break
            else:
                if len(i) == 0 or i.isspace() == True:
                    self.error_label(f" No se ha introducido: {j} ")
                    status = False
                    break

                if i.isdigit() == False:
                    self.error_label(f" Numero invalido: {j} ")
                    status = False
                    break

        
        if status == True:
            if self.check_repeated(name_val) == False:
                self.add_entries_to_inventory(name_val, desc_val, cant_val,
                                              tot1_val, tot2_val, tot3_val)
            else:
                self.error_label(f" El elemento [{name_val.upper()}] ya esta en el inventario " )

    def check_repeated(self, string):
        """ Checkin for repeated names inside DB """
        info = json.load(open("./DATABASE/inventory.json","r"))
        aux = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        
        for i in info[aux.index(string[0].upper())][string[0].upper()]:
            if string.upper() in i:
                return True
        else:
            return False    
            

    def add_entries_to_inventory(self, name_val, desc_val, cant_val,
                                 tot1_val, tot2_val, tot3_val):
        """ as its name tell us """
        info = json.load(open("./DATABASE/inventory.json", "r"))
        aux = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

        value = [ name_val.upper(), desc_val.upper(), cant_val, tot1_val,
                  tot2_val, tot3_val ]

        info[aux.index(name_val.upper()[0])][name_val[0].upper()].append(value)
        to_write = json.dumps(info, sort_keys=True, indent=4)
        with open("./DATABASE/inventory.json", "w") as handler:
            handler.write(to_write)
            self.error_label(f" [{name_val}] Agregado correctamente ")

        
    def error_label(self, string):
        self.new_window = tk.Toplevel()
        self.error_lbl = tk.Label(self.new_window, text=string, font=("arial",12))
        self.error_lbl.pack()

        self.ok_button = tk.Button(self.new_window, text="ok", font=("arial",12), relief="groove",
                                   borderwidth=4, command=self.new_window.destroy)
        self.ok_button.pack()
    
class remove_inventory_manager:
    def __init__(self, master):
        """ Remove from inventory window manager """
        self.master = master
        self.master.title("Eliminar del inventario")
        self.master.geometry("800x175")
        self.master.resizable(0,0)

        # FRAME 1
        self.test_frame_1 = tk.Frame(self.master)
        self.test_frame_1.pack(fill=tk.X)
        self.name_label = tk.Label(self.test_frame_1, relief="groove", borderwidth=2,
                                   width=18, height=1, text="Introduzca el nombre", font=("ARIAL", 12))
        self.name_label.pack(side="left")
        self.name_entry = tk.Entry(self.test_frame_1, font=("ARIAL", 12))
        self.name_entry.pack(fill=tk.X, padx=4)

        self.check_button = tk.Button(self.master, text="REMOVER", font=("arial", 12),
                                      command=self.remove_handler)
        self.check_button.pack()

    def remove_handler(self):
        """ Validating entry button data """
        data = self.name_entry.get()
        status = True
        if len(data) == 0 or data.isspace == True:
            self.error_label(" No ha introducido nada ")
            status = False
            
        elif data.isalnum() == False:
            self.error_label(" Ah introducido un valor incorrecto ")
            status = False

        if status == True:
            """ Buscando el elemento en la base de datos """
            aux = "ABCDEFGHIJKLMNOPQRSTUVWXYZ01256789"
            status = False
            info = json.load(open("./DATABASE/inventory.json", "r"))
            first_letter = data[0].upper()
            # Iterating elements by letter in the database
            for i in range(len(info[aux.index(first_letter)][first_letter])):

                

                # first element (name) of the lists == data, then delete it
                if info[aux.index(first_letter)][first_letter][i][0] == data.upper():
                    info[aux.index(first_letter)][first_letter].pop(i)
                    with open("./DATABASE/inventory.json", "w") as handler:
                        handler.write(json.dumps(info, sort_keys=True, indent=4))
                        self.error_label(" Elemento eliminado de la base de datos ")
                    return 0
            else:
                self.error_label(f" El elemento ({data.upper()}) no existe ")
                return 0

                
    def error_label(self, string):
        self.new_window = tk.Toplevel()
        self.error_lbl = tk.Label(self.new_window, text=string, font=("arial",12))
        self.error_lbl.pack()

        self.ok_button = tk.Button(self.new_window, text="ok", font=("arial",12), relief="groove",
                                   borderwidth=4, command=self.new_window.destroy)
        self.ok_button.pack()
        

def main():
    DB_CHECK()
    root = tk.Tk()
    app  = MOTOGP_DATABASE(root)
    root.mainloop()

if __name__ == "__main__":
    main()
