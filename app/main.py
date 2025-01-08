from datetime import datetime
from fastapi import FastAPI,Request
import zoneinfo
import json
from app.repetidores import rep
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

@app.get("/",tags=["Home"])
def root(request:Request):
    """
    root _summary_

    _extended_summary_

    Returns:
        _type_: Saludo de Bienvenida
    """
    tz = zoneinfo.ZoneInfo("America/Bogota")
    hora = datetime.now(tz).strftime("%A %d. %B %Y, %H:%M:%S")
    saludo = {"saludos":"Diego",
              "fecha":hora}
    return templates.TemplateResponse("index.html",{"request":request,
                                                    "bienvenida":saludo})



app.include_router(rep.router)
