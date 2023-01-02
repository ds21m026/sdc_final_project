from fastapi import FastAPI # import FastAPI class
from pydantic import BaseModel

import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

api = FastAPI()

# using Pydantic models to declare request body
# base data as derived from Streamlit Frontend
class titanicData(BaseModel):
	Age: int
	pclassAux: int
	family_size: int
	sex: str
	embarked: str
	
# preprocessed data as returned from API
class modelData(BaseModel):
	Age: int
	child: int
	family_size: int
	Pclass_1: int
	Pclass_2: int
	Pclass_3: int
	Sex_female: int
	Sex_male: int
	Embarked_C: int
	Embarked_Q: int
	Embarked_S: int


# define post method to preprocess data
# define post method to get prediction from model
@api.post("/predict/")
def predict_proba(data: titanicData):
	
	arr = [0, 0, 0, 0,0,0, 0,0, 0,0,0]
	# child indicator
	arr[1] = int(data.Age <= 16)
	
	# passenger class
	if data.pclassAux==1:
	    arr[3]=1
	if data.pclassAux==2:
	    arr[4]=1
	if data.pclassAux==3:
	    arr[5]=1
	    
	# male/female indicators
	Sex_female = 0
	Sex_male = 0
	if data.sex=="female":
	    arr[6]=1
	else:
	    arr[7]=1
	
	# embarked indicators
	if data.embarked=="Cherbourg":
	    arr[8] = 1
	if data.embarked=="Queenstown":
	    arr[9] = 1
	if data.embarked=="Southampton":
	    arr[10] = 1
	

	
	# load the Random Forest Classifier
	with open("./rfSimple.pkl", 'rb') as file:
    	    rf = pickle.load(file)
    # make predictions
	#SurvivalProba = rf.predict_proba(inputDF)[0,1]
	#test = [[23,0,3,1,0,0,1,0,1,0,0]]
	arr = [arr]
	SurvivalProba = rf.predict_proba(arr)[0,1]
	#survPerc = round(SurvivalProba*100, 1)
	
	return SurvivalProba

