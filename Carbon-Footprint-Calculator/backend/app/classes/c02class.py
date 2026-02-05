from pydantic import BaseModel



"""
co2_value, category, suggestion, result = predict_individual_co2(
        pvkm=60,
        puvkm=60,
        pjc=5,
        tkm=5,      # Train Km
        ekwh=250,
        wul=20,
        wk=0.5,
        dt="Veg"
    )
"""
class individual(BaseModel):
    userid:str
    pvkm: float
    puvkm:float
    pjc:float
    tkm: float
    ekwh:float
    wul :float
    wk:float
    dt : str


#predicion, result = predict_app_co2(20.0, 7.2, 2.5, "Communication")

class application(BaseModel):
    user_id:str
    cpu:float
    ram :float
    duriation:float
    app_name:str
