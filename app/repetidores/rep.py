from fastapi import APIRouter, HTTPException, Request,status,Form
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from  models.modelos import Reporte,CreacionReporte,CustomerUdate
from sqlmodel import Session, select
from db.sql_model import SessionDep,create_tables_db
from fastapi.templating import Jinja2Templates
from typing import Annotated

router = APIRouter(lifespan=create_tables_db)

templates = Jinja2Templates(directory="app/templates")


@router.get("/lista_reportes",response_model=list[Reporte],tags=["Rep"])
async def list_reportes(session: SessionDep,request:Request):
    datos = session.exec(select(Reporte).order_by(Reporte.pk.desc()).offset(0).limit(50)).all()
    return templates.TemplateResponse("lista_reportes.html",{"request":request,"lista_reportes":datos})

# registros = session.query(Registro).order_by(Registro.fecha_creacion.desc()).offset(skip).limit(limit).all()
#         return registros


@router.get("/reportes,{reporte_pk}",response_model=Reporte,
tags=["Rep"])
async def read_reporte(reporte_pk: int, session: SessionDep,request:Request):
    reporte_db = session.get(Reporte,reporte_pk)
    if not reporte_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="Reporte no encontrado")
    
    return templates.TemplateResponse("lista_individual.html",{'request':request,"reporte":reporte_db})

@router.get("/reportes/eliminar,{reporte_pk}",tags=["Rep"])
async def delete_reporte(request:Request,reporte_pk: int, session: SessionDep):
    reporte_db = session.get(Reporte,reporte_pk)
    if not reporte_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="Reporte no encontrado")
    session.delete(reporte_db)
    session.commit()
    # session.refresh(reporte_db)
    return RedirectResponse("/lista_reportes")


@router.patch("/reportes/update,{reporte_pk}",tags=["Rep"],
              status_code=status.HTTP_201_CREATED)
async def update_reporte(reporte_pk:int,reporte_data:CustomerUdate,
                         session: SessionDep):
    reporte_db = session.get(Reporte,reporte_pk)
    if not reporte_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="Reporte no encontrado")
    reporte_data_dict = reporte_data.model_dump(exclude_unset=True)
    reporte_db.sqlmodel_update(reporte_data_dict)
    session.add(reporte_db)
    session.commit()
    session.refresh(reporte_db)
    return HTMLResponse("/formulario")


@router.get("/formulario_actualizacion/edit/{reporte_pk}",response_class=HTMLResponse,tags=["Rep"])
async def get_form_actualizacion(request:Request,reporte_pk:int,session: SessionDep):
    reporte = session.get(Reporte,reporte_pk)
    if not reporte:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Reporte No encontrado")
    form = CustomerUdate()
    return templates.TemplateResponse("formulario_actualizacion.html",{"request":request,"form":form,
                                                                       "reporte":reporte})

@router.get("/formulario",response_class=FileResponse,tags=["Rep"])
def get_form(request:Request):
    """
    get_form = Retorno de formulario ingreso información

    _extended_summary_

    Args:
        request (Request): Metodo Request 

    Returns:
        _type_: Formulario Html
    """
    return templates.TemplateResponse("formulario.html",{"request":request})


@router.post("/reporte/add",response_class=RedirectResponse,tags=["Rep"])
async def create_ad(session:SessionDep,
                    #numero_documento: str = Form(...),
                    fecha: str = Form(...),
                    asunto: str = Form(...),
                    fuente: str = Form(...),
                    temas: str = Form(...),
                    lugar: str = Form(...),
                    latitud: float = Form(...),
                    longitud: float = Form(...),
                    informacion: str = Form(...),
                    resumen: str = Form(...)):
    """
    create_ad _summary_

    _extended_summary_

    Args:
        session (SessionDep): sesión en base de datos
        fecha (str, optional): _description_. Defaults to Form(...).
        asunto (str, optional): _description_. Defaults to Form(...).
        fuente (str, optional): _description_. Defaults to Form(...).
        temas (str, optional): _description_. Defaults to Form(...).
        lugar (str, optional): _description_. Defaults to Form(...).
        latitud (float, optional): _description_. Defaults to Form(...).
        longitud (float, optional): _description_. Defaults to Form(...).
        informacion (str, optional): _description_. Defaults to Form(...).
        resumen (str, optional): _description_. Defaults to Form(...).

    Returns:
        _type_: Insert datos de formulario html a base de datos, retorno a formulario de toma de datos
    """
    datos = CreacionReporte(#numero_documento=numero_documento,
                    fecha=fecha,asunto=asunto,fuente=fuente,temas=temas,lugar=lugar,
                    latitud=latitud,longitud=longitud,informacion=informacion,
                    resumen=resumen)
    
    reporte = Reporte.model_validate(datos.model_dump())
    session.add(reporte)
    session.commit()
    session.refresh(reporte)
    return RedirectResponse("/formulario",status_code=status.HTTP_303_SEE_OTHER)

