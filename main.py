#!/usr/bin/python3

import tkinter as tk

AUTHOR = "JOHAN | mind2hex"
VERSION = "[v1.0]"

def root_initialization():
    # root windows initialization
    root = tk.Tk()
    root.title("MotoGP  DATABASE")
    root.geometry("1450x900")
    root.resizable(0, 0)
    root.configure(background="black")
    return root

def search_string(string):
    # Routines to search string in DATABASE
    # string probably will be an ID for every product of the storage
    print(string)

def exit_procedures(root):
    # Routines to save db...
    root.destroy()
    exit(0)

if __name__ == "__main__":
    root = root_initialization()

    # Header image
    canvas = tk.Canvas(root, widt=4000, height=180, bg="black", bd=0, confine=1)
    canvas.pack(side="top")
    img = tk.PhotoImage(file="./resources/main_title.png")
    canvas.create_image(500,100, image=img)

    # program_info_label
    program_info_lbl = tk.Label(root, justify="left",
    text=f"""
    AUTHOR  = {AUTHOR}
    VERSION  = {VERSION}
    """)
    program_info_lbl.pack(anchor="nw")

    # Searching section
    entry_search  = tk.Entry(font="arial", justify="left")
    entry_search.place(relx=0.93, rely=0.204, anchor="ne", height=30, width=200)

    button_search = tk.Button(root, text=" Buscar ", font="arial", command= lambda: search_string(entry_search.get()))
    button_search.place(relx=1.0, rely=0.204, anchor="ne", height=30, width=100)

    # Inventory section
    button_show_inventory = tk.Button(root, text="Mostrar Inventario", font="arial")
    button_show_inventory.place(relx=0.40, rely=0.35, height=50, width=200)

    button_modify_inventory = tk.Button(root, text="Modificar Inventario", font="arial")
    button_modify_inventory.place(relx=0.40, rely=0.42, height=50, width=200)

    button_add_to_inventory = tk.Button(root, text="Agregar al inventario", font="arial")
    button_add_to_inventory.place(relx=0.40, rely=0.49, height=50, width=200)

    button_remove_from_inventory = tk.Button(root, text="Quitar del inventario", font="arial")
    button_remove_from_inventory.place(relx=0.40, rely=0.56, height=50, width=200)

    button_exit = tk.Button(root, text="Salir", font="arial", command= lambda: exit_procedures(root))
    button_exit.place(relx=0.40, rely=0.66, height=50, width=200)

    root.mainloop()
