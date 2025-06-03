# API - Administracion de Empleados de Restaurante

## Funcion de uso
- Este programa de backend esta creado con FastAPI, su funcion es la administracion basica de empleados en un restaurante


## Estructura
Menu interactuvo. El archivo script_request ejecuta un menu interactuvo en consola para elegir entre:
- Comprobar conexion
- Ver empleados
- Ver empleados agrupados por el cargo laboral que selecciones
- Añadir un empleado
- Eliminar un empleado

## Desplegar

- Sigue los siguiente pasos, abre la terminal e introduce los pasos uno a uno
```
git clone https://github.com/matope1/actFinal_API
cd actFinal_API
```
```
python -m venv api_guille_empleados
```
```
api_guille_empleados\Scripts\activate # En windows
```
```
source api_guille_empleados/bin/activate  #  En Linux/Mac 
```
```
pip install -r requirements.txt
```
```
uvicorn main:app --reload
```
- en otra terminal para usar esta para logs
```
python script_rest.py
```
ó
```
python3 script_rest.py
```
