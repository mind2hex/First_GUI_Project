#!/usr/bin/python3
import pathlib
import json
from hashlib import md5

def database_directory_check():
    """ This function create ./DATABASE directory if it doesn't exist """
    if pathlib.Path("./DATABASE").exists() == False:
        if operative_system() == "Linux":
            pathlib.mkdir("./DATABASE")
        elif operative_system() == "Windows":
            pathlib.Path("./DATABASE").mkdir()

def database_files_check():
    """ This function create ./DATABASE/<files> if it doesn't exist """
    if pathlib.Path("./DATABASE/inventory.json").exists() == False:
        pathlib.Path("./DATABASE/inventory.json").touch()

def database_JSON_format_check():
    """ This function check JSON format of the database file """
    # Checking DATABASE json format
    try:
        json.load(open("./DATABASE/inventory.json","r"))
    except:
        generate_empty_inventory()

def database_template_check():
    """ Check database format or template """
    # Checking DATABASE json correct template
    aux = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    try:
        lista = json.load(open("./DATABASE/inventory.json","r"))
        for i in range(len(aux)):
            lista[i][aux[i]]
    except:
        generate_empty_inventory()

def database_generate_backup():
    """ This function generate backups every time the program is launched
    - The limit of backup is 1000
    - If the checksum of the original database is equal to one of the already created database, then no backup is created
    """
    status = False
    md5checksum_original_file = md5(open("./DATABASE/inventory.json", "rb").read()).hexdigest()  # checksum of the original DB
    for i in range(1000):
        if pathlib.Path(f"./DATABASE/inventory.json.backup({i})").exists() == True:
            md5checksum_backup_file = md5(open(f"./DATABASE/inventory.json.backup({i})", "rb").read()).hexdigest()
            # If both checksum are equal, then the DATABASE is not modified.
            if md5checksum_original_file == md5checksum_backup_file:
                status = True
                break
            continue
        else:
            with open("./DATABASE/inventory.json", "r") as src_file:
                info = src_file.read()
                dst_file = open(f"./DATABASE/inventory.json.backup({i})", "w")
                dst_file.write(info)
            status = True
            break

    if status == False:
        print(" Database backups reached to the limit ")
        # Finish this

def generate_empty_inventory():
    lista = json_inventory_format()
    handler = open("./DATABASE/inventory.json","w")
    handler.write(json.dumps(lista, sort_keys=True, indent=4))

def json_inventory_format():
    """ Return basic format of the database or inventory """
    aux = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    lista = []
    for i in range(len(aux)):
        lista.append({aux[i]:[]})
    return lista

def database_routine():
    database_directory_check()
    database_files_check()
    database_JSON_format_check()
    database_template_check()
    database_generate_backup()

if __name__ == "__main__":
    pass
