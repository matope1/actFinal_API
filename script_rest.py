import requests
import os
import time
import msvcrt  # libreria para hacer que el usuario al pulsar cualquier tecla vuleva al menu interactivo
from API_KEY import API_KEY, API_KEY_NAME

# menu interactivo
def menu():
    os.system("cls")
    print(
    " 1 - Comprobar conexion \n" \
    " 2 - Mostrar todos los empleados \n"  \
    " 3 - Mostrar los empleados segun la funcion en el restaurante \n" \
    " 4 - Añadir empleado \n" \
    " 5 - Eliminar empleado \n" \
    " 6 - Salir \n\n"
    )
    button = input("Selecciona una opcion: ")
    

    # Accion segun la opcion elegida
    if button == "1":
        comprobar_conexion()
        volver_menu()
    elif button == "2":
        ver_empleados()
        volver_menu()
    elif button == "3":
        ver_emple_por_funcion()
        volver_menu()
    elif button == "4":
        añadir_empleado()
        volver_menu()
    elif button == "5":
        eliminar_empleado()
        volver_menu()
    elif button == "6":
        exit()
    else:
        os.system("cls")
        print("No ha elegido una opcion correcta...")
        time.sleep(1)
        menu()

def volver_menu():
        print("Pulse cualquier tecla para volver al menu: ")
        msvcrt.getch()
        os.system("cls")
        menu()

def comprobar_conexion():
    url = "http://127.0.0.1:8000/"

    headers = {
    API_KEY_NAME: API_KEY
    }
    response = requests.get(url, headers=headers)
    print(f"Código de respuesta: {response.status_code}")
    print(f"Respuesta: {response.json()}")




# Lamada a mostrar todos los empleados
def ver_empleados():
    url = "http://127.0.0.1:8000/empleados"

    headers = {
    API_KEY_NAME: API_KEY
    }
    response = requests.get(url, headers=headers)
    print(f"Código de respuesta: {response.status_code}")
    print(f"Respuesta: {response.json()}")

# Llamada a mostrar empleados segun la funcion que tengan(cocinero, limpiador...)
def ver_emple_por_funcion():

    func_emple = input("Que empleados quieres mostrar(cocinero, pinche, camarero o limpiador)")
    url = f"http://127.0.0.1:8000/empleados/funcion/{func_emple}"

    headers = {
    API_KEY_NAME: API_KEY
    }
    response = requests.get(url, headers=headers)
    print(f"Código de respuesta: {response.status_code}")
    print(f"Respuesta: {response.json()}")


def añadir_empleado():

    nombre = input("Nombre de la persona: ")
    funcion = input("Funcion en el restaurante(cocinero, camarero, pinche, limpiador): ")
    años_trabajando = int(input("Años en la empresa: "))

    url = "http://127.0.0.1:8000/empleado/nuevo"

    data = {
    "name": nombre,
    "func_emple": funcion,
    "years_work": años_trabajando
    }

    headers = {
    API_KEY_NAME: API_KEY
    }

    response = requests.post(url, headers=headers, json=data)
    print(f"Código de respuesta: {response.status_code}")
    # print(f"Respuesta: {response.json()}")
    try:
        print(f"Respuesta: {response.json()}")
    except ValueError:
        print("Respuesta no es JSON válido:")
        print(response.text)



def eliminar_empleado():



    name = input("Indique el nombre del empleado a eliminar: )")
    confirmacion = input(f"Seguro que desea eliminar a {name} de la base de datos? indique\n Y/N")

    if confirmacion.lower() == "y":
        url = f"http://127.0.0.1:8000/empleado/despido/{name}"

        data = {
        "name": name
        }

        headers = {
        API_KEY_NAME: API_KEY
        }
        response = requests.delete(url, headers=headers, json=data)
        print(f"Código de respuesta: {response.status_code}")
        print(f"Respuesta: {response.json()}")
    # else:
    #     volver_menu()

menu()
