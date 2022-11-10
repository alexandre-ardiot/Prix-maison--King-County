import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import pydeck as pdk
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.pipeline import make_pipeline

import folium as fl
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

def get_pos(lat,lng):
    return lat,lng

m = fl.Map()

#m.add_child(fl.LatLngPopup())

map = st_folium(m, height=350, width=700)


data = get_pos(map['last_clicked']['lat'],map['last_clicked']['lng'])

st.write(data)


df = pd.read_csv("kc_house_data.modelisation.csv")
map = pd.read_csv("donnees_map.csv")

pickle_in = open("Model.pkl", "rb")
model = pickle.load(pickle_in)

colT1,colT2 = st.columns([4,6])

with colT2:
    st.title("Maison")

midpoint = (np.average(map["lat"]), np.average(map["lon"]))

LAND_COVER = [[[-123.0, 49.196], [-123.0, 49.324], [-123.306, 49.324], [-123.306, 49.196]]]

st.pydeck_chart(pdk.Deck(
    map_style = None,
    initial_view_state = pdk.ViewState(
        latitude = midpoint[0],
        longitude = midpoint[1],
        zoom = 11,
        max_zoom = 30,
        pitch = 50,
        bearing=0
    ),
    layers=[
        pdk.Layer(
            'PolygonLayer',
            LAND_COVER,
            stroked=False,
            # processes the data as a flat longitude-latitude pair
            get_polygon='-',
            get_fill_color=[0, 0, 0, 20]
        ),
        pdk.Layer(
            'GeoJsonLayer',
            data=df,
            opacity=0.8,
            stroked=False,
            filled=True,
            extruded=True,
            wireframe=True,
            get_line_color=[255, 255, 255],
            pickable=True
        ),
    ],
))

#st.map(df)


colT3,colT4 = st.columns([4,6])

with colT4:
    st.write("Choisissez votre configuration :")

col1, col2 = st.columns(2)

with col1:
    m2_habitable = st.text_input("Nombre de m2 habitable (34 - 1 258)", 34)
    m2_etage = st.text_input("Nombre de m2 à l'étage (34 - 874)", 34)
    chambres = st.selectbox("Nombre de chambre :", ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"))
    condition = st.selectbox("Condition de la maison :", ("1", "2", "3", "4", "5"))
    salle_de_bain = st.slider("Nombre de salle de bain :", 0.25, 8.0, step=0.25)

with col2:
    m2_parcelle = st.text_input("Nombre de m2 de parcelle (48 - 1 000)", 48)
    m2_cave = st.text_input("Nombre de m2 à la cave (0 - 448)", 0)
    etages = st.selectbox("Nombre d'étages :", ("1.0", "1.5", "2.0", "2.5", "3.0", "3.5"))
    code_postal = st.selectbox("Code postal souhaité :", ("98001", "98002", "98003", "98004", "98005", "98006", "98007", "98008",
            "98010", "98011", "98014", "98019", "98022", "98023", "98024", "98027", "98028", "98029", "98030", "98031", "98032",
            "98033", "98034", "98038", "98039", "98040", "98042", "98045", "98052", "98053", "98055", "98056", "98058", "98059",
            "98065", "98070", "98072", "98074", "98075", "98077", "98092", "98102", "98103", "98105", "98106", "98107", "98108",
            "98109", "98112", "98115", "98116", "98117", "98118", "98119", "98122", "98125", "98126", "98133", "98136", "98144",
            "98146", "98148", "98155", "98166", "98168", "98177", "98178", "98188", "98198", "98199"))
    vue_mer = st.radio("Vue sur la mer ? :", ("Non", "Oui"))

if vue_mer == "Oui":
    vue_mer = int(1)
else:
    vue_mer = int(0)


df_user = df.loc[len(df)-1:].apply(lambda x: 0.0)
df_user = df_user.drop(["id", "date", "prix"])
df_user["m2_habitable"] = m2_habitable
df_user["m2_parcelle"] = m2_parcelle
df_user["m2_etage"] = m2_etage
df_user["m2_cave"] = m2_cave
df_user["salle_de_bain"] = salle_de_bain
df_user["chambres"] = chambres
df_user["etages"] = etages
df_user["condition"] = condition
df_user["vue_mer"] = vue_mer
df_user[code_postal] = 1

df_user["lat"] = 47.7210
df_user["lon"] = -122.319
df_user["annee_construction"] = 1951
df_user["annee_renovation"] = 1991
df_user["note"] = 7
df_user["m2_habitable15"] = 157.0
df_user["m2_parcelle15"] = 710.0
df_user["vue"] = 0

prix_utilisateur = model.predict([df_user])
resultat = [f"{int(val):,}".replace(",", " ") for val in prix_utilisateur]



#Affichage du bouton, puis de l'espèce et des 2 graph sur les sépales et pétales
colT5,colT6 = st.columns([4,6])

with colT6:
    st.write("Le prix estimé est de : {} $".format(resultat[0]))