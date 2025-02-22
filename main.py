from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Pet(BaseModel):
    id: int
    name: str
    age: int
    type: str

pets = []

@app.post("/pets/", response_model=Pet, status_code=201)
def create_pet(pet: Pet):
    pets.append(pet)
    return pet

@app.get("/pets/", response_model=List[Pet])
def get_pets():
    return pets

@app.get("/pets/{pet_id}", response_model=Pet)
def get_pet(pet_id: int):
    for pet in pets:
        if pet.id == pet_id:
            return pet
    raise HTTPException(status_code=404, detail="Pet not found")

@app.put("/pets/{pet_id}", response_model=Pet)
def update_pet(pet_id: int, name: str = None, age: int = None):
    for pet in pets:
        if pet.id == pet_id:
            if name:
                pet.name = name
            if age is not None:
                pet.age = age
            return pet
    raise HTTPException(status_code=404, detail="Pet not found")

@app.delete("/pets/{pet_id}", status_code=204)
def delete_pet(pet_id: int):
    for index, pet in enumerate(pets):
        if pet.id == pet_id:
            pets.pop(index)
            return
    raise HTTPException(status_code=404, detail="Pet not found")

@app.get("/pets/average-age/")
def get_average_age():
    if not pets:
        raise HTTPException(status_code=404, detail="No pets found")
    total_age = 0
    for pet in pets:
        total_age += pet.age
    average_age = total_age / len(pets)
    return {"average_age": average_age}