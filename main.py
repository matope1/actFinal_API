from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator, model_validator

import logging 

from typing import List
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,  Session

from API_KEY import f_api_key  # Importo variable de archivo API_KEY.py

# Funcion de sesion db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Crear una app para administrar empleados de un restaurante

# Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Base de datos = empleados.db
DATABASE_URL = "sqlite:///./empleados.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base  = declarative_base()


# sql
class emple(Base):
    __tablename__ = "emple"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)
    func_emple = Column(String, nullable=False, index=True)     # Funcion del empleado
    years_work = Column(Integer, nullable=True)     # Años dentro de la empresa
    trust = Column(String, nullable=True)       # si tiene mas de 5 años, se considera una persona confiable


Base.metadata.create_all(bind=engine)

# pydantic
class employees(BaseModel):
    name: str
    func_emple: str
    years_work: int

    # La funcion del empleado debe ser las listadas, si no, da error
    @field_validator("func_emple")
    def clase_listada(cls, emple):
        list_func = ["camarero", "cocinero", "pinche", "limpiador"]
        if emple not in list_func:
            raise ValueError("El empleado debera tener la funcion de: camarero, cocinero, pinche o limpiador")
        return emple

# emple_db: List[employees] = []





app = FastAPI(
    version = "1.0.0",
    title = "Empleados del restaurante"
)

# Función para manejar los errores ValueError
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}  # Mostramos el mensaje de error
    )

# muestra el estado
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response Status: {response.status_code}")
    
    return response


# Comprobar conexion
@app.get("/")
def test_Conex():
    logger.info(f"--CONEXION EXITOSA--")
    return {"message" : "Ha podido acceder a la plantilla de empleados"}


# Mostrar todos los empleados
@app.get("/empleados", response_model=list[employees])
def sow_all_emple(db: Session = Depends(get_db), token: str = Depends(f_api_key)): # authentificacion basica
    logger.info(f"Solicitud enviada para MOSTRAR TODOS los empleados")
    # si no hay empleados, muestra un mensaje
    empleados = db.query(emple).all()
    if not empleados:

        raise HTTPException(status_code=404, detail="No hay empleados registrados")
    return empleados


# Mostrar empleado por cargo o funcion (cocinero, camarero...)
@app.get("/empleados/funcion/{func_emple}", response_model=List[employees])
def empleados_por_funcion(func_emple: str, 
                          db: Session = Depends(get_db), # Session db
                          token: str = Depends(f_api_key) # Auth basica
                          ):

    empleados = db.query(emple).filter(emple.func_emple == func_emple).all()
    logger.info(f"Recibida petición para mostrar empleados que tienen la funcion de {func_emple}")
    # Mensaje al cliente 404, y logg para el servidor si no existe la funcion
    if not empleados:
        logger.warning(f"No se encontraron empleados con función: {func_emple}")
        raise HTTPException(status_code=404, detail="No se encontraron empleados con esa función")

    return empleados


# Crear empleado
@app.post("/emple/", response_model=list[employees])
def new_emple(name: employees, 
              db: Session = Depends(get_db), 
              token: str = Depends(f_api_key)
              ):
    logger.info(f"--El empleado {name} se ha REGISTRADO CORRECTAMENTE--")
        ## Registrarlo de DDBB....
    
    # si lleva mas de 5 años en "trusted" en cambio sera "not trusted"
    if name.years_work > 5:
        prod_trust = "trusted"
    else:
        prod_trust = "not trusted"

    # Si el empleado ya existe con el mismo nombre, no se podra añadir
    db = SessionLocal()
    existe = db.query(emple).filter(emple.name == name.name).first()
    if existe:
        db.close()
        raise HTTPException(status_code=400, detail="El empleado ya está registrado")


    emple_db = emple(
        name=name.name,
        func_emple=name.func_emple,
        years_work=name.years_work,
        trust=prod_trust)
    
    db.add(emple_db)
    db.commit()
    db.refresh(emple_db)
    db.close()
    
    # Respuesta json
    return {
        "status":"Success",
        "msg": "Empleado registrado correctamente",
        "Empleado": {
            "name": name.name,
            "function": name.func_emple,
            "years_work": name.years_work,
            "trust": prod_trust
        }
    }


# Eliminar empleado
@app.delete("/empleados/{name}", response_model=list[employees])
def delete_empleado(name: str,       # Nombre de empleado de la BBDD que queremos eliminar
                    db: Session = Depends(get_db),   # Ejecuta sesion de BBDD mientras dura la funcion
                    token: str = Depends(f_api_key)  # Auth Basica
                    ):

    empleado = db.query(emple).filter(emple.name == name).first()

    # Mensaje de error si el empleado no existe
    if not empleado:
        logger.warning(f"No se encontraron empleado {name}")
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    db.delete(empleado)
    db.commit()
    return {"status": "Success",
        "mensaje": f"Empleado {name} eliminado exitosamente"}


