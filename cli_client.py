import os
import getpass
import requests
import curses
from support_functions_ostack import get_token_for_admin, get_token_for_admin_in_project, get_flavors, get_images,build_network, build_subnet, build_port,get_console_url_per_instance,create_topology, autenticar_usuario

LOGO = """
░█████╗░██╗░░░░░░█████╗░██╗░░░██╗██████╗░                 ██╗███╗░░██╗████████╗███████╗██████╗░███████╗░█████╗░░█████╗░███████╗
██╔══██╗██║░░░░░██╔══██╗██║░░░██║██╔══██╗                 ██║████╗░██║╚══██╔══╝██╔════╝██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝ 
██║░░╚═╝██║░░░░░██║░░██║██║░░░██║██║░░██║                 ██║██╔██╗██║░░░██║░░░█████╗░░██████╔╝█████╗░░███████║██║░░╚═╝█████╗░░
██║░░██╗██║░░░░░██║░░██║██║░░░██║██║░░██║                 ██║██║╚████║░░░██║░░░██╔══╝░░██╔══██╗██╔══╝░░██╔══██║██║░░██╗██╔══╝░░
╚█████╔╝███████╗╚█████╔╝╚██████╔╝██████╔╝                 ██║██║░╚███║░░░██║░░░███████╗██║░░██║██║░░░░░██║░░██║╚█████╔╝███████╗ 
░╚════╝░╚══════╝░╚════╝░░╚═════╝░╚═════╝░                 ╚═╝╚═╝░░╚══╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░░╚═╝░╚════╝░╚══════╝
"""

# Base de datos de usuarios simulada (usuario, contraseña, rol)
#usuarios creados en openstack 
usuarios = {
    "fernando": {"id": "dfb0a7d3a33c450da4359cd9077f2b3b", "rol": "admin"},
    "alexia": {"id": "46d691402a94430dac111990116f95a1", "rol": "cliente"},
    "oskar": {"id": "052d82b6f2874eefa8e63b99410feb48", "rol": "cliente"}
}

# Función para el inicio de sesión
def login():
    while True:
        usuario = input("Ingrese su nombre de usuario: ")
        password = getpass.getpass("Ingrese su contraseña: ")
        isauth, user_TOKEN = autenticar_usuario(usuario, password)
        
        if isauth:
            return usuarios[usuario]['rol'], usuarios[usuario]['id']
        else:
            print("Credenciales incorrectas")

        '''
        if usuario in usuarios and usuarios[usuario]["password"] == password:
            return usuarios[usuario]["rol"],usuario
        else:
            print("Credenciales incorrectas. Inténtelo de nuevo.")
        '''

def menu_selector(opciones, mensaje):
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(1)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    highlight_text = curses.color_pair(1)

    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, mensaje)
        for i, opcion in enumerate(opciones):
            x = 2
            y = i + 1
            if i == current_row:
                stdscr.attron(highlight_text)
                stdscr.addstr(y, x, f"{i + 1}. {opcion}")
                stdscr.attroff(highlight_text)
            else:
                stdscr.addstr(y, x, f"{i + 1}. {opcion}")

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(opciones) - 1:
            current_row += 1
        elif key == 10:  # Enter key
            break

    curses.endwin()
    return current_row

def menu_cliente():
    while True:
        print("******    MENU CLIENTE    ******")
        print("******      Opciones      ******")
        print("1) Crear Slice")
        print("2) Listar Slice")
        print("3) Cerrar sesión")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Preguntar por el número de VMs a crear
            num_vms = input("Número de VMs a crear: ")
            topologia_name = input("Nombre de la topología: ")
            # Preguntar por la topología
            available_options = available_topologies(int(num_vms))
            print("Selecciona la topología:")
            for key, topology in available_options.items():
                print(f"{key}. {topology}")

            while True:
                topology_choice = input("Opción: ")
                if topology_choice in available_options:
                    topology = available_options[topology_choice]
                    break
                else:
                    print("Opción no válida. Vuelve a intentarlo.")

            # Crear una lista para almacenar la información de cada VM
            images_list = get_images()
            images_names_list = [i['name'] for i in images_list]
            images_ids_list = [i['id'] for i in images_list]
            opciones_imagenes = images_names_list
            vms_info = []

            flavor_list = get_flavors()
            flavors_name_list = [i['name'] for i in flavor_list]
            flavor_ids_list = [i['id'] for i in flavor_list]
            opciones_flavors = flavors_name_list


            for i in range(int(num_vms)):
                # Preguntar por el nombre de la VM
                nombre_vm = input(f"Nombre de la VM {i + 1}: ")

                # Preguntar por la imagen para cada VM
                print("Seleccione una imagen:")
                #opciones_imagenes = ["imagen1", "imagen2", "imagen3"]
                for j, imagen in enumerate(opciones_imagenes):
                    print(f"{j + 1}. {imagen}")
                while True:
                    try:
                        indice_imagen_seleccionada = int(input("Opción: "))
                        if 1 <= indice_imagen_seleccionada <= len(opciones_imagenes):
                            break
                        else:
                            print("Opción no válida. Introduzca un número válido.")
                    except ValueError:
                        print("Por favor, ingrese un número entero.")

                #imagen_vm = opciones_imagenes[indice_imagen_seleccionada - 1]
                imagen_vm = images_ids_list[indice_imagen_seleccionada - 1]
                topology_description = "ninguna"
                # Preguntar por el flavor para cada VM
                print("Seleccione un flavor:")

                #opciones_flavors = ["flavor1", "flavor2", "flavor3"]
                for k, flavor in enumerate(opciones_flavors):
                    print(f"{k + 1}. {flavor}")
                while True:
                    try:
                        indice_flavor_seleccionado = int(input("Opción: "))
                        if 1 <= indice_flavor_seleccionado <= len(opciones_flavors):
                            break
                        else:
                            print("Opción no válida. Introduzca un número válido.")
                    except ValueError:
                        print("Por favor, ingrese un número entero.")

                flavor_vm = flavor_ids_list[indice_flavor_seleccionado - 1]

                # Almacenar la información de la VM en la lista
                vm_info = {
                    "Nombre": nombre_vm,
                    "Imagen": imagen_vm,
                    "Flavor": flavor_vm,
                    "Nombre Topología": topologia_name,
                    "Topología": topology,
                    "Descripcion" : topology_description
                }
                vms_info.append(vm_info)

            # Hacer lo que sea necesario con los datos recopilados
            print("Datos recopilados para todo el Slice:")
            print("---------------------------------")
            print(f"Nombre de la Topología: {topologia_name}")
            print(f"Topología: {topology}")
            print(f"User id:  {userid}")
            print("---------------------------------")
            print("Datos recopilados para cada VM:")
            for vm_info in vms_info:
                print(f"Nombre: {vm_info['Nombre']}")
                print(f"Imagen: {vm_info['Imagen']}")
                print(f"Flavor: {vm_info['Flavor']}")
                
                print("---------------------------------")

            print(userid)
            create_topology(vms_info, topology, topologia_name, topology_description, userid)

            
        elif opcion == "2":
            print("Opción 2: Listar Slice")
            # Agrega aquí la lógica para listar slices si es necesario
        elif opcion == "3":
            confirmacion = input("¿Desea cerrar sesión? (a) Sí / (b) No: ")
            if confirmacion.lower() == "a":
                return
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")


def display_final_options():
    while True:
        print("******    Opciones    ******")
        print("1. Volver al menú principal")
        print("2. Cerrar sesión")
        choice = input("Selecciona una opción: ")

        if choice == '1':
            return True  # True significa que el usuario quiere volver al menú principal
        elif choice == '2':
            return False  # False significa que el usuario quiere cerrar la sesión
        else:
            print("Opción inválida. Inténtalo de nuevo.")

def available_topologies(num_vms):
    topologies = {}
    
    # Para topología Lineal y Bus, siempre es posible
    topologies["1"] = "Lineal"
    topologies["4"] = "Bus"
    
    # Para Malla, verificar si el número es un cuadrado perfecto
    if int(num_vms ** 0.5) ** 2 == num_vms:
        topologies["2"] = "Malla"
    
    # Para Árbol, verificar si el número puede formar un árbol "casi completo"
    k = 0
    nodes = 0
    while nodes < num_vms:
        nodes += 2 ** k
        k += 1
            
    # Para Anillo, siempre es posible si num_vms >= 3
    if num_vms >= 3:
        topologies["3"] = "Anillo"
    


    return topologies

# Menú para el admin
def menu_admin():
    while True:
        print("******    MENU ADMIN    ******")
        print("******     Opciones     ******")
        print("1) Ver lista de Slice solicitados por el cliente")
        print("2) Crear clientes")
        print("3) Cerrar sesión")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("Opción 1: Ver lista de Slice solicitados por el cliente")
        elif opcion == "2":
            print("Opción 2: Crear clientes")
        elif opcion == "3":
            confirmacion = input("¿Desea cerrar sesión? (a) Sí / (b) No: ")
            if confirmacion.lower() == "a":
                return

# Programa principal
def main():
    while True:
        print("\n" + LOGO)
        print("Bienvenido al sistema")

        # Inicio de sesión
        global userid

        rol, userid = login()

        # Menú según el rol
        if rol == "cliente":
            menu_cliente()
        elif rol == "admin":
            menu_admin()

if __name__ == "__main__":
    main()
