from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader


# Configura tu API Key
API_KEY = "Z3VpbGxlcm1vMTIz"
API_KEY_NAME = "key_pass"

# FastAPI buscará la API Key en los headers
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Función para validar la API Key
def f_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="API Key inválida"
        )
    return api_key
