import os
import getpass
import requests
LOGO = """
░█████╗░██╗░░░░░░█████╗░██╗░░░██╗██████╗░                 ██╗███╗░░██╗████████╗███████╗██████╗░███████╗░█████╗░░█████╗░███████╗
██╔══██╗██║░░░░░██╔══██╗██║░░░██║██╔══██╗                 ██║████╗░██║╚══██╔══╝██╔════╝██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝ 
██║░░╚═╝██║░░░░░██║░░██║██║░░░██║██║░░██║                 ██║██╔██╗██║░░░██║░░░█████╗░░██████╔╝█████╗░░███████║██║░░╚═╝█████╗░░
██║░░██╗██║░░░░░██║░░██║██║░░░██║██║░░██║                 ██║██║╚████║░░░██║░░░██╔══╝░░██╔══██╗██╔══╝░░██╔══██║██║░░██╗██╔══╝░░
╚█████╔╝███████╗╚█████╔╝╚██████╔╝██████╔╝                 ██║██║░╚███║░░░██║░░░███████╗██║░░██║██║░░░░░██║░░██║╚█████╔╝███████╗ 
░╚════╝░╚══════╝░╚════╝░░╚═════╝░╚═════╝░                 ╚═╝╚═╝░░╚══╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░░╚═╝░╚════╝░╚══════╝
"""

# Base de datos de usuarios simulada (usuario, contraseña, rol)
usuarios = {
    "cliente1": {"password": "123456", "rol": "cliente"},
    "admin1": {"password": "adminpass", "rol": "admin"},
}

# Función para el inicio de sesión
def login():
    while True:
        usuario = input("Ingrese su nombre de usuario: ")
        password = getpass.getpass("Ingrese su contraseña: ")

        if usuario in usuarios and usuarios[usuario]["password"] == password:
            return usuarios[usuario]["rol"]
        else:
            print("Credenciales incorrectas. Inténtelo de nuevo.")

# Menú para el cliente
def menu_cliente():
    while True:
        print("******    MENU CLIENTE    ******")
        print("******      Opciones      ******")
        print("1) Crear Slice")
        print("2) Listar Slice")
        print("3) Cerrar sesión")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("---------------------------------")
            num_vms = input("Número de VMs a crear: ")
            print("---------------------------------")
            # Preguntar por la Memoria RAM para cada VM
            ram = input("Cantidad de Memoria RAM en GB para cada VM: ")
            # Preguntar por el Almacenamiento para cada VM
            storage = input("Cantidad de Almacenamiento en GB para cada VM: ")

            # Preguntar por los Cores para cada VM
            cores = input("Número de Cores para cada VM: ")

            while True:
                available_options = available_topologies(int(num_vms))
                print("Selecciona la topología:")

                # Crear una nueva lista para almacenar las claves ordenadas
                sorted_keys = sorted(available_options.keys(), key=lambda x: int(x))

                # Crear un diccionario de mapeo
                mapping = {}
                for index, key in enumerate(sorted_keys, 1):
                    mapping[str(index)] = key
                    print(f"{index}. {available_options[key]}")

                topology_choice = input("Opción: ")
                original_key = mapping.get(topology_choice, None)
                topology = available_options.get(original_key, None)
                if topology is not None:  # Si se seleccionó una opción válida, salir del bucle
                    break
                else:
                    print("Opción no válida. Vuelve a intentarlo.")

            # Hacer lo que sea necesario con los datos recopilados, ya que no hay una solicitud REST en este caso
            print("Datos recopilados:")
            print(f"Número de VMs: {num_vms}")
            print(f"Topología seleccionada: {topology}")
            print(f"Memoria RAM: {ram} GB")
            print(f"Almacenamiento: {storage} GB")
            print(f"Número de Cores: {cores}")

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
    topologies["5"] = "Bus"
    
    # Para Malla, verificar si el número es un cuadrado perfecto
    if int(num_vms ** 0.5) ** 2 == num_vms:
        topologies["2"] = "Malla"
    
    # Para Árbol, verificar si el número puede formar un árbol "casi completo"
    k = 0
    nodes = 0
    while nodes < num_vms:
        nodes += 2 ** k
        k += 1
    
    # Restricción para que Árbol solo aparezca si hay al menos 4 nodos
    if num_vms >= 4:
        topologies["3"] = "Árbol"
        
    # Para Anillo, siempre es posible si num_vms >= 3
    if num_vms >= 3:
        topologies["4"] = "Anillo"
    
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
        rol = login()

        # Menú según el rol
        if rol == "cliente":
            menu_cliente()
        elif rol == "admin":
            menu_admin()

if __name__ == "__main__":
    main()
