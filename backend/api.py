from fastapi import FastAPI
from pydantic import BaseModel
import pickle

# create instance of fastapi
api = FastAPI()


# using Pydantic models to declare request body
# base data as derived from Streamlit Frontend
class TitanicData(BaseModel):
    age: int
    pclassAux: int
    family_size: int
    sex: str
    embarked: str


# define post method to use the input values
# get prediction from model
@api.post("/predict/")
def predict_proba(data: TitanicData):
    # initialize default array
    arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # child
    arr[1] = int(data.age <= 16)

    # passenger class
    if data.pclassAux == 1:
        arr[3] = 1
    if data.pclassAux == 2:
        arr[4] = 1
    if data.pclassAux == 3:
        arr[5] = 1

    # male/female
    if data.sex == "female":
        arr[6] = 1
    else:
        arr[7] = 1

    # embarked
    if data.embarked == "Cherbourg":
        arr[8] = 1
    if data.embarked == "Queenstown":
        arr[9] = 1
    if data.embarked == "Southampton":
        arr[10] = 1

    # load the Random Forest Classifier
    # pickle file from https://github.com/tlary/Kaggle_Titanic
    with open("./models/rfSimple.pkl", 'rb') as file:
        rf = pickle.load(file)

    # make predictions
    arr = [arr]
    survival_proba = rf.predict_proba(arr)[0, 1]
    survival_proba = round(survival_proba * 100, 2)

    # return probability to survive
    return survival_proba
