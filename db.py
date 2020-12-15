from typing import Dict
from pydantic import BaseModel,FilePath
from datetime import date

today = date.today()

class DocInDB(BaseModel):
    iddoc: int
    nomdoc: str
    feccarguedoc: str
    fecvencimientodoc: str
    pathdoc: str
    idusuario:int

database_docs = Dict[str, DocInDB]
database_docs = {
    1: DocInDB(**{"iddoc":1,
                "nomdoc":"resolucion 20 del 2020",
                "feccarguedoc":today.strftime("%d/%m/%Y"),
                "fecvencimientodoc":"12/12/2023",
                "pathdoc":"/uploadfiles/resolucion_20.pdf",
                "idusuario":1}),
    2: DocInDB(**{"iddoc":2,
                "nomdoc":"resolucion 21 del 2020",
                "feccarguedoc":today.strftime("%d/%m/%Y"),
                "fecvencimientodoc":"31/12/2021",
                "pathdoc":"/uploadfiles/resolucion_21.pdf",
                "idusuario":1}),
}

def obtener_documentos():
    return database_docs

def obtener_lista_documentos():
    lista_documentos = []
    for iddoc in database_docs:
        lista_documentos.append(database_docs[iddoc])
    return lista_documentos
