# import python modules
import streamlit as st
import pandas as pd
import requests
import json

st.header("placeholder visualization")

st.write("tbd")

st.header("prediction via fastapi")

# get input data from different parameters in streamlit frontend
age = st.number_input("How old are you?", 0, 100, 30)
family_size = st.number_input("How many family members are on board (including yourself)?", 1, 20, 1)
pclassAux = st.selectbox("In which passenger class are you traveling?", (1,2,3))
sex = st.selectbox("Are you male or female?", ("male", "female"), index=1)
embarked = st.selectbox("Which is your port of embarkation?", ("Cherbourg", "Queenstown", "Southampton"))

# combine input to dictionary
data = {"age": age,
	"family_size": family_size,
	"pclassAux": pclassAux,
	"sex": sex,
	"embarked": embarked}

# create json object from dict	
dataJSON = json.dumps(data)

# button to show json object
if st.button("show inputs as json"):
	st.write(dataJSON)

# button to call the api
if st.button("get prediction"):
	# post request to the API
	r = requests.post(url = "http://localhost:8000/predict/", data=dataJSON)

	# get result from api
	st.write("Your chance to survive based on the information in %: ", r.text)