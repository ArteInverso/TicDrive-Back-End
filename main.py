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
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

today = date.today()

origins = [
    "localhost.tiangolo.com", 
    "localhost.tiangolo.com",
    "localhost",
    "localhost:8081",
    "http://181.131.100.129",
    "http://181.131.100.129:8081"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/listfiles")
async def files():
    return db.obtener_lista_documentos()

@app.post("/upload-file/")
async def create_upload_file(iddoc:int,fecvencimientodoc:str,
                nomdoc:str,
                idusuario:int,uploaded_file: UploadFile = File(...)):
#codigo antiguo
#   file_location = f"uploadfiles/{uploaded_file.filename}"
#   with open(file_location, "wb+") as file_object:
#       file_object.write(uploaded_file.file.read())
# fin codigo antiguo
       
#nuevo codigo
    file_to = '/' + uploaded_file.filename
#conexion con DrpBox
    dbx = dropbox.Dropbox('ZLnvyxN_O3oAAAAAAAAAAROUWKg5XPiHwDd4fH-djVUAfupDPYiVJuayBgJJWsxA')
    #dbx.files_upload(open(file_from, 'rb').read(), file_to)
    dbx.files_upload(uploaded_file.file.read(), file_to)
#fin nuevo codigo
    if iddoc in database_docs:
       raise HTTPException(status_code=406, detail="El documento ya existe!")
    else:
        database_docs[iddoc] = DocInDB(**{"iddoc" : iddoc,
                                            "nomdoc" : nomdoc,
                                            "feccarguedoc": today.strftime("%d/%m/%Y"),
                                            "fecvencimientodoc": fecvencimientodoc,
                                            "pathdoc": "/uploadfiles/" + uploaded_file.filename,
                                            "idusuario": idusuario})
    return {"info": f"Archivo '{uploaded_file.filename}' ha sido cargado en dropbox y la informacion ha sido grabada con exito"}
#   return {"info": f"Archivo '{uploaded_file.filename}' ha sido cargado en '{file_location}' y la informacion ha sido grabada con exito"}