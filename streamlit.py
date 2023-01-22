# import python modules
import pandas as pd
import numpy as np
import requests
import json
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Titanic Dashboard & Predictions",
                   page_icon=":chart_with_upwards_trend:",
                   layout="wide"
                   )

@st.cache
def get_data_and_transform():
    df = pd.read_csv(
        "data/train.csv",
        delimiter=","
    )
    return df

df = get_data_and_transform()

# -----SIDEBAR-----

st.sidebar.header("Filter:")
city = st.sidebar.multiselect(
    "Embarkation Point:",
    options=df["Embarked"].unique(),
    default=df["Embarked"].unique()
)
gender = st.sidebar.multiselect(
    "Gender:",
    options=df["Sex"].unique(),
    default=df["Sex"].unique()
)
pclass = st.sidebar.multiselect(
    "Passenger class:",
    options=df["Pclass"].unique(),
    default=df["Pclass"].unique()
)
parch1, parch2 = st.sidebar.select_slider(
    "Number of Parents/Children:",
    options=list(set(df['Parch'])),
    value=(0, 6)
)
sibsp1, sibsp2 = st.sidebar.select_slider(
    "Number of Siblings/Spouses:",
    options=list(set(df['SibSp'])),
    value=(0, 8)
)
survived = st.sidebar.multiselect(
    "Survived:",
    options=df["Survived"].unique(),
    default=df["Survived"].unique()
)

df_selection = df.query(
    "Embarked == @city & Sex == @gender & Pclass == @pclass & Parch >= @parch1 & Parch <= @parch2 & SibSp >= @sibsp1 "
    "& SibSp <= @sibsp2 & Survived == @survived"
)

# -----MAINPAGE-----

st.title(":ship: Titanic Dashboard and Survival Predictor")
st.markdown("##")

# INDICATORS
number_passengers = len(df_selection.index)
total_casualties = len(df_selection.loc[df['Survived'] == 0])
total_survivers = len(df_selection.loc[df['Survived'] == 1])

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Number of Passengers:")
    st.subheader(number_passengers)
with middle_column:
    st.subheader("Number of casualties:")
    st.subheader(total_casualties)
with right_column:
    st.subheader("Number of survivors:")
    st.subheader(total_survivers)


sns.set(rc={'axes.facecolor':'none', 'figure.facecolor':'none'})
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 4))
sns.kdeplot(
    data=df_selection[df_selection['Pclass'] == 1], x = 'Age', cut=0, fill=True, hue="Survived", ax = ax1, multiple = 'stack', palette='PuBu'
)
sns.kdeplot(
    data=df_selection[df_selection['Pclass'] == 2], x = 'Age', cut=0, fill=True, hue="Survived", ax = ax2, multiple = 'stack', palette='PuBu'
)
sns.kdeplot(
    data=df_selection[df_selection['Pclass'] == 3], x = 'Age', cut=0, fill=True, hue="Survived", ax = ax3, multiple = "stack", palette='PuBu'
)
st.pyplot(fig)


st.header("Would you survive the Titanic?")

# get input data from different parameters in streamlit frontend
age = st.number_input("How old are you?", 0, 100, 30)
family_size = st.number_input("How many family members are on board (including yourself)?", 1, 20, 1)
pclassAux = st.selectbox("In which passenger class are you traveling?", (1, 2, 3))
sex = st.selectbox("Are you male or female?", ("male", "female"), index=1)
embarked = st.selectbox("What is your port of embarkation?", ("Cherbourg", "Queenstown", "Southampton"))

# combine input to dictionary
data = {"age": age,
        "family_size": family_size,
        "pclassAux": pclassAux,
        "sex": sex,
        "embarked": embarked}

# create json object from dict	
dataJSON = json.dumps(data)

# button to show json object
if st.button("Show inputs as json"):
    st.write(dataJSON)

# button to call the api
if st.button("Get prediction"):
    # post request to the API
    r = requests.post(url="http://localhost:8000/predict/", data=dataJSON)

    # get result from api
    st.write("Your chance to survive based on the information in %: ", r.text)
