from typing import Annotated
import pandas as pd # type: ignore
from fastapi.responses import FileResponse# type: ignore

from fastapi import FastAPI, File, UploadFile,Header # type: ignorer
from fastapi.responses import HTMLResponse# type: ignore
import convert_functions as func
import stops_times as stops_tim
import stops as stp
from fastapi.middleware.cors import CORSMiddleware# type: ignore

app = FastAPI()

# CORS configuration
origins = ["*"]  # Adjust this according to your requirements

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Add OPTIONS here
    allow_headers=["*"],
)

   
 
@app.post("/files/{name}")
async def create_files(name:str):
    print(name)
    return FileResponse("GeneratedFiles/"+name)


@app.post("/uploadfiles/")
async def create_upload_files(file: UploadFile):
    if(not file):
        return {"message": "No file sent"}
    else :
        file_content = await file.read()
        tree= func.parse_gtfs_file(file_content)
        func.extract_Trips_Routes_CSV(tree)
        stops_tim.extaract_Stops_times(tree)
        stp.extract_stops_files(tree)
        string_array = ["trips.txt", "routes.txt", "shapes.txt", "stops_times.txt","stops.txt","agency.txt"]
        return string_array


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/trips.txt" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>

</body>
    """
    return HTMLResponse(content=content)
    


