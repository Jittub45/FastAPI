from fastapi import FastAPI , Path, HTTPException, Query # type: ignore
from fastapi.responses import JSONResponse # type: ignore 
from pydantic import BaseModel, Field, computed_field # type: ignore
from typing import Annotated, Literal, Optional
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
        
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    gender: Annotated[Optional[Literal['male', 'femalt']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


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

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code = 404, detail = 'Patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #rcidying_patient_info -> pydentic obj -> updated bmi + verdict
    existing_patient_info['id'] = patient_id 
    patient_pydentic_obj = Patient(**existing_patient_info) 

    # pydantic object to dict
    existing_patient_info = patient_pydentic_obj.model_dump(exclude=['id'])  

    # add this dict to data 
    data[patient_id] = existing_patient_info

    #save the data
    save_data(data)

    return JSONResponse(status_code = 200, content={'message': 'Patient updated successfully'})


@app.delete('/delete/{paient_id}')
def delete_patient(patient_id:str):

    #load the data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code = 404, detail = 'Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code = 200, content={'message': 'Patient deleted successfully'})