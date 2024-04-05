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
@app.get("/")
def main():
    return {"hello world"}        

    

if __name__ == "__main__":
    app.run(debug=True)
