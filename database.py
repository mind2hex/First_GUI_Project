#!/usr/bin/python3
import pathlib
import json
from hashlib import md5
from platform import system as operative_system
import re

def sales_log():
    """ This function create ./VENTAS directory if it doesn't exist
    This directory stores sales log from every person or vehicule
    """
    if pathlib.Path("./VENTAS").exists() == False:
        pathlib.Path("./VENTAS").mkdir()

def database_directory_check():
    """ This function create ./DATABASE directory if it doesn't exist """
    if pathlib.Path("./DATABASE").exists() == False:
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
    # Creating ./VENTAS directory
    sales_log()

    # Creating ./DATABASE directory
    database_directory_check()

    # Checking ./DATABASE/inventory.json integrity
    database_files_check()

    # Checking ./DATABASE/inventory.json correct json format
    database_JSON_format_check()

    # Checking Basic ./DATABASE/inventory.json template
    database_template_check()

    # Generating ./DATABASE/inventory.json backup if it has changed
    database_generate_backup()

def database_name_find(pattern):
    """ Find all names that match with pattern
    return Values:
      A list with the matched entries and his data
      oterwise return Null
    """
    lista = []
    aux = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    info = json.load(open("./DATABASE/inventory.json", "r"))
    for i in range(len(aux)):
        for j in range(len(info[i][aux[i]])):
            if re.match(pattern, " ".join(info[i][aux[i]][j])) != None:
                lista.append(info[i][aux[i]][j])

    return lista


def database_modify_entry(name, type, modify):
    """find name in inventory, select type and replaces his value with modify """
    lista = ["NOMBRE", "DESCRIPCION", "CANTIDAD", "PR1", "PR2", "PR3"]
    for i in range(len(lista)):
        if type == lista[i]:
            index = i

    lista = []
    aux = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    info = json.load(open("./DATABASE/inventory.json", "r"))
    for i in range(len(aux)):
        for j in range(len(info[i][aux[i]])):
            if info[i][aux[i]][j][0] == name:
                info[i][aux[i]][j][index] = str(modify)

    
    handler = open("./DATABASE/inventory.json","w")
    handler.write(json.dumps(info, sort_keys=True, indent=4))

def database_add_entry(name, description, cant, val1, val2, val3):
        """ as its name tell us 
        return values:
        - True  -> If There is no problem during writing on database
        - False -> If there is a problem
        """
        info = json.load(open("./DATABASE/inventory.json", "r"))
        aux = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        
        value = [ name.upper(), description.upper(), \
                  cant, val1, val2, val3 ]
        
        info[aux.index(name.upper()[0])][name[0].upper()].append(value)
        to_write = json.dumps(info, sort_keys=True, indent=4)
        with open("./DATABASE/inventory.json", "w") as handler:
            handler.write(to_write)
            return True
        
def database_name_exist(name):
    """ Find name in the Database
    return Values:
      True  -> if name exist in database
      False -> if it doesn't exist
    """

    aux = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    info = json.load(open("./DATABASE/inventory.json", "r"))
    status = False
    for i in range(len(aux)):
        for j in range(len(info[i][aux[i]])):
             if name in info[i][aux[i]][j]:
                 status = True
                 break
        if status == True:
            break

    return status

def sales_record_exist(name):
    """ Find if file name exist inside the directory ./SALES
    return Values:
      True  -> if name exist inside ./SALES directory
      False -> if it doesn't
    """
    for i in pathlib.Path("./VENTAS").glob("**/*"):
        if name.upper() in repr(i):
            return True

    return False

def sales_record_create(name):
    """ Creates entry inside the directory ./SALES """
    pathlib.Path(f"./VENTAS/{name.upper()}.log").touch()


if __name__ == "__main__":
    pass
