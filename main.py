import shutil
from typing import Callable
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
import pydantic
import db
from db import database_docs, DocInDB
from datetime import date
from typing import Dict

app = FastAPI()

today = date.today()


@app.get("/listfiles")
async def files():
    return db.obtener_lista_documentos()

@app.post("/upload-file/")
async def create_upload_file(iddoc:int,fecvencimientodoc:str,
                nomdoc:str,
                idusuario:int,uploaded_file: UploadFile = File(...)):
    file_location = f"uploadfiles/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    if iddoc in database_docs:
       raise HTTPException(status_code=406, detail="El documento ya existe!")
    else:
        database_docs[iddoc] = DocInDB(**{"iddoc" : iddoc,
                                            "nomdoc" : nomdoc,
                                            "feccarguedoc": today.strftime("%d/%m/%Y"),
                                            "fecvencimientodoc": fecvencimientodoc,
                                            "pathdoc": "/uploadfiles/" + uploaded_file.filename,
                                            "idusuario": idusuario})
    return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}

@app.post("/descripcion-file/")
async def descripcion_file(datos:DocInDB):

    if datos.iddoc in database_docs:
       raise HTTPException(status_code=406, detail="El documento ya existe!")
    else:
        database_docs[datos.iddoc] = datos  
    return {"mensaje": "Documento Creado"}