from fastapi import FastAPI , Path, HTTPException, Query # type: ignore
from fastapi.responses import JSONResponse 
from pydantic import BaseModel, Field, computed_field # type: ignore
from typing import Annotated, Literal
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description = 'ID of the patient in the database', example='P001')]
    name: Annotated[str, Field(..., description = 'Name of the patient', example='John Doe')]
    city: Annotated[str, Field(..., description = 'City of the patient', example='Delhi')]
    age: Annotated[int, Field(...,gt=0, lt=120, description = 'Age of the patient')]
    gender: Annotated[Literal['Male', 'Female', 'Others'], Field(..., description = "Gender of the patient")]
    height: Annotated[float, Field(..., gt= 0, description = 'Height of the patient in m', example=175.5)] 
    weight: Annotated[float, Field(..., gt=0, description = 'Weight of the patient in kg', example=70.0)]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    @computed_field
    @property  
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif 18.5 <= self.bmi < 24.9:
            return 'Normal weight'
        elif 25 <= self.bmi < 29.9:
            return 'Overweight'
        else:
            return 'Obesity'

def load_data():
    with open("patients.json", "r") as file:
        data = json.load(file)

    return data

def save_data(data):
    with open("patients.json", "w") as file:
        json.dump(data, file)

@app.get("/")
def hello():
    return {"message": "Patient Management API"}

@app.get("/about")
def about():
    return {"message": "A fully fuctional API to manage patient records."}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/view/{patient_id}")
def view_patient(patient_id: str = Path(..., description = 'ID of the patient in the database', example='P001')):
    #Load all the patient data
    data = load_data()

    
    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code = 404, detail = 'Patient not found')

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description = 'Sort patient on the basis of height, weight or bmi'), order: str = Query('asc', description = 'Order of sorting, either asc or desc')):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code = 400, detail = f'Invalid sort field. Select from {valid_fields}') 
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code = 400, detail = 'Invalid order. Use asc or desc')   
    
    data = load_data()

    sort_order = True if order == 'asc' else False

    sorted_data = sorted(data.values(), key= lambda x: x.get(sort_by, 0), reverse= sort_order)
    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    # laod all the patient data
    data = load_data()

    # Check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code = 400, detail = 'Patient with this ID already exists')
    
    # Add the new patient data to database
    data[patient.id] = patient.model_dump(exclude=['id']) #convetrt pydentic model to dict and exclude id field

    #save into the json file
    save_data(data)
    
    return JSONResponse(status_code = 201, content={'message': 'Patient created successfully'})