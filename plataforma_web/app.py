"""
FastAPI App
"""
from fastapi import FastAPI

from plataforma_web.autoridades.views import router as autoridades
from plataforma_web.distritos.views import router as distritos
from plataforma_web.listas_de_acuerdos.views import router as listas_de_acuerdos
from plataforma_web.listas_de_acuerdos_acuerdos.views import router as listas_de_acuerdos_acuerdos
from plataforma_web.materias.views import router as materias


app = FastAPI()
app.include_router(autoridades, prefix="/autoridades")
app.include_router(distritos, prefix="/distritos")
app.include_router(listas_de_acuerdos, prefix="/listas_de_acuerdos")
app.include_router(listas_de_acuerdos_acuerdos, prefix="/listas_de_acuerdos_acuerdos")
app.include_router(materias, prefix="/materias")


@app.get("/")
async def root():
    """Mensaje de Bienvenida"""
    return {"message": "Hola. Soy 'Plataforma Web API OAuth2' del Poder Judicial del Estado de Coahuila de Zaragoza."}
