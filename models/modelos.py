from datetime import date,datetime

from pydantic import BaseModel
from typing import Optional
from sqlmodel import SQLModel,Field,Integer,Column,String


def nom_doc_tiempo():
    datos_numero_documento = "".join(datetime.now().strftime("%Y%m%d%H%M%S"))
    fecha = "".join(datetime.now().strftime("%Y-%m-%d"))
    return datos_numero_documento,fecha

class CreacionModeloReporte(SQLModel):
    """
    CreacionModeloReporte _summary_

    _extended_summary_

    Args:
        SQLModel (_type_): Creacion de la tabla que es parte de la base de datos
    """
    #numero_documento : str = Field(default=f"{nom_doc_tiempo()[0]}")
    fecha: date = Field(default=f"{nom_doc_tiempo()[1]}")
    asunto: str = Field(default=None)
    fuente: str = Field(default=None)
    temas: str = Field(default=None)
    lugar: str = Field(default=None)
    latitud: float = Field(default=None)
    longitud: float = Field(default=None)
    informacion: Optional[str] | None = Field(default=None)
    resumen: Optional[str] | None = Field(default=None)

class CreacionReporte(CreacionModeloReporte):
    """
    CreacionReporte _summary_

    _extended_summary_

    Args:
        CreacionModeloReporte (_type_): Esta clase retorna a router para devolver solo los campos
        que se van a diligenciar en el formulario sin la pk o llave primaria
    """
    ...

class Reporte(CreacionModeloReporte,table=True):
    """
    Reporte _summary_

    _extended_summary_

    Args:
        CreacionModeloReporte (_type_): _description_
        table (bool, optional): _description_. Defaults to True.
        Esta clase incluye la pk o llave principal al modelo de tabla 
        para el registro en la base de datos,
        debe ser diferente para poder que se autoincremente en la base de datos
        Es importante diferenciar esta clase para que funcione
    """
    pk: int | None = Field(default=None,primary_key=True,index=True)
    numero_documento : str = Field(default=f"{nom_doc_tiempo()[0]}")


class CustomerUdate(CreacionReporte):
    ...

