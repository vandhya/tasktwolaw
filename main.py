from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()

class CarsCls:
    def __init__(self, *, chassis:str, name: str, year: int, passedEmission:bool):
        self.chassis = chassis
        self.name = name
        self.year = year
        self.passedEmission = passedEmission

class Cars(BaseModel):
    chassis:str
    name: str
    year: int
    passedEmission:bool

    class Config:
        orm_mode = True

cars = {'GDA':CarsCls(chassis="GDA",name="Subaru Impreza WRX STI",year=2000,passedEmission=False),
        'GDB':CarsCls(chassis="GDB",name="Subaru Impreza WRX STI",year=2004,passedEmission=True)}


print(cars.keys())

@app.get('/')
def root():
    return {'hello':'dummy'}

# instruction 1
@app.get('/cars/{chassis}/{year}')
def getEmission(chassis:str, year:int):
    car = cars.get(chassis)
    if car is not None:
        if car.year == year:
            return{'chassis':car.chassis, 'name':car.name, 'year':car.year,'passedEmission':car.passedEmission}
        else:
            return{'error':'model year not found'}
    else:
        return {'error':'car not found'}

# instruction 2
@app.post('/add')
def addCar(chassis:str = Form(...), name: str= Form(...), year: int=Form(...),passedEmission:bool=Form(...)):
    newCar = CarsCls(chassis=chassis,name=name,year=year,passedEmission=passedEmission)
    cars[chassis] = newCar
    print(cars.keys())
    return {'chassis':newCar.chassis, 'name':newCar.name, 'year':newCar.year,'passedEmission':newCar.passedEmission}

# instruction 3
@app.post('/addJSON')
def addCar(car:Cars):
    cars[car.chassis] = CarsCls(chassis=car.chassis,name=car.name,year=car.year,passedEmission=car.passedEmission)
    print(cars.keys())
    return {'chassis':car.chassis, 'name':car.name, 'year':car.year,'passedEmission':car.passedEmission}
    
@app.get('/getAll')
def getAllCars():
    return cars

@app.put('/edit')
def editCar(car:Cars):
    cars[car.chassis] = CarsCls(chassis=car.chassis,name=car.name,year=car.year,passedEmission=car.passedEmission)
    return {'success':'vehicle updated'}

@app.delete('/delete')
def deleteCar(chassis:str = Form(...)):
    cars.pop(chassis)
    return {'success':'vehicle deleted'}