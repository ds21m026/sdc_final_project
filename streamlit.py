import streamlit as st
import pandas as pd
import requests
import json
from pydantic import BaseModel

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


# get input data from streamlit frontend
Age = st.sidebar.number_input("How old are you?", 0, 100, 30)
family_size = st.sidebar.number_input("How many family members are aboard the ship (including yourself)?", 1, 20, 1)
pclassAux = st.sidebar.selectbox("In which passenger class are you traveling?", (1,2,3))
sex = st.sidebar.selectbox("Are you male or female?", ("male", "female"), index=1)
embarked = st.sidebar.selectbox("Which is your port of Embarkation?", ("Cherbourg", "Queenstown", "Southampton"))

# combine input to dict
data = {"Age": Age,
	"family_size": family_size,
	"pclassAux": pclassAux,
	"sex": sex,
	"embarked": embarked}
dataJSON = json.dumps(data) # create json object from dict
st.write(dataJSON)
# preprocess data by making post request to the API
r = requests.post(url = "http://localhost:8000/predict/", data=dataJSON)

st.write("Your chance of Survival based on the information provided is: ", r.text)

	