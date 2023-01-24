import pandas as pd
import requests
import json
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Titanic Dashboard & Predictions",
                   page_icon=":chart_with_upwards_trend:",
                   layout="wide"
                   )


@st.cache
def get_data_and_transform():
    df_titanic = pd.read_csv(
        "data/full_clean2.csv",
        delimiter=","
    )
    return df_titanic


titanic = get_data_and_transform()

# ---------------SIDEBAR---------------

st.sidebar.header("Filter:")
city = st.sidebar.multiselect(
    "Embarkation Point:",
    options=titanic["Boarded"].unique(),
    default=titanic["Boarded"].unique()
)
gender = st.sidebar.multiselect(
    "Gender:",
    options=titanic["Sex"].unique(),
    default=titanic["Sex"].unique()
)
pclass = st.sidebar.multiselect(
    "Passenger class:",
    options=titanic["Pclass"].unique(),
    default=titanic["Pclass"].unique()
)
parch1, parch2 = st.sidebar.select_slider(
    "Number of Parents/Children:",
    options=list(set(titanic['Parch'])),
    value=(0, 9)
)
sibsp1, sibsp2 = st.sidebar.select_slider(
    "Number of Siblings/Spouses:",
    options=list(set(titanic['SibSp'])),
    value=(0, 8)
)
survived = st.sidebar.multiselect(
    "Survived:",
    options=titanic["survived"].unique(),
    default=titanic["survived"].unique()
)

df_selection = titanic.query(
    "Boarded == @city & Sex == @gender & Pclass == @pclass & Parch >= @parch1 & Parch <= @parch2 & SibSp >= @sibsp1 "
    "& SibSp <= @sibsp2 & survived == @survived"
)

# ---------------MAINPAGE---------------

st.title(":ship: Titanic Dashboard and Survival Predictor")
st.markdown("##")

# -----INDICATORS-----
number_passengers = len(df_selection.index)
total_casualties = len(df_selection.loc[titanic['survived'] == 0])
total_survivors = len(df_selection.loc[titanic['survived'] == 1])

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Number of Passengers:")
    st.subheader(number_passengers)
with middle_column:
    st.subheader("Number of casualties:")
    st.subheader(total_casualties)
with right_column:
    st.subheader("Number of survivors:")
    st.subheader(total_survivors)

# ---------------PLOT1---------------

st.markdown("##")
st.markdown("##")

choromap = df_selection.groupby('Country').agg(Survived=('survived', 'sum'),
                                               Passengers=('survived', 'count')).reset_index()

fig_map = px.choropleth(choromap, locations="Country",
                        hover_data=['Survived', 'Passengers'],
                        locationmode='country names',
                        scope='world')
fig_map.update_layout(height=600, margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig_map.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'))

st.plotly_chart(fig_map, use_container_width=True)

# ---------------PLOT2---------------

st.markdown("##")
st.markdown("##")

lifeboat = df_selection.groupby(by=["Lifeboat", 'Sex']).size().reset_index(name='Count')
order = ['7', '5', '3', '8', '1', '6', '16', '14', '12', '9',
         '11', '13', '15', '2', '10', '4', 'C', 'D', 'B', 'A']
lifeboat = lifeboat.reindex(lifeboat['Lifeboat'].map(dict(zip(order, range(len(order))))).sort_values().index)

fig_lifeb = px.bar(lifeboat, x="Lifeboat", y='Count', color='Sex', title="Lifeboats in launch order")
fig_lifeb.update_layout(
    xaxis_title="Lifeboat launch order",
    yaxis_title="Number of people",
    legend_title="Gender",
    xaxis=dict(
        type='category',
    ),
    legend=dict(
        yanchor="top",
        y=0.90,
        xanchor="left",
        x=0.01
    ))

fig_lifeb.update_layout(height=500, margin={"r": 0, "t": 0, "l": 0, "b": 0})

st.plotly_chart(fig_lifeb, use_container_width=True)

# ---------------PLOT3---------------

st.markdown("##")
st.markdown("##")

custom_params = {'axes.grid': False,
                 'figure.facecolor': 'none',
                 'axes.facecolor': 'none',
                 'axes.labelcolor': 'grey',
                 "axes.spines.right": False,
                 "axes.spines.top": False,
                 "axes.spines.left": False,
                 'xtick.color': 'grey',
                 'ytick.color': 'grey',
                 'text.color': 'grey'
                 }

sns.set_theme(style="ticks", rc=custom_params)

plt.figure()
fig_kde1 = sns.kdeplot(
    data=df_selection[df_selection['Pclass'] == 1],
    x='Age', cut=0, fill=True, hue="survived", multiple='stack', palette='PuBu', legend=False
)
fig_kde1.set(xlabel=None)
fig_kde1.set(title='Passenger Class 1')

plt.figure()
fig_kde2 = sns.kdeplot(
    data=df_selection[df_selection['Pclass'] == 2],
    x='Age', cut=0, fill=True, hue="survived", multiple='stack', palette='PuBu'
)
fig_kde2.set(ylabel=None)
fig_kde2.set(title='Passenger Class 2')
sns.move_legend(fig_kde2, 1, fontsize=10, facecolor='none', title='Survived', labelcolor='grey')

plt.figure()
fig_kde3 = sns.kdeplot(
    data=df_selection[df_selection['Pclass'] == 3],
    x='Age', cut=0, fill=True, hue="survived", multiple="stack", palette='PuBu', legend=False
)
fig_kde3.set(ylabel=None)
fig_kde3.set(xlabel=None)
fig_kde3.set(title='Passenger Class 3')

left_column, middle_column, right_column = st.columns(3)
left_column.pyplot(fig_kde1.get_figure())
middle_column.pyplot(fig_kde2.get_figure())
right_column.pyplot(fig_kde3.get_figure())

# ---------------PREDICTIONS---------------

left_column, middle_column, right_column = st.columns(3)

with middle_column:
    st.header("Would you survive the Titanic?")
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
with middle_column:
    if st.button("Show inputs as json"):
        st.write(dataJSON)

    # button to call the api
    if st.button("Get prediction"):
        # post request to the API
        r = requests.post(url="http://localhost:8000/predict/", data=dataJSON)

        # get result from api
        st.write("Your chance to survive based on the information in %: ", r.text)
