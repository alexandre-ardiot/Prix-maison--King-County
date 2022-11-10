import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import pickle


#Import du csv et du model via pickle
df = pd.read_csv("kc_house_data.modelisation.csv")

pickle_in = open("Model.pkl", "rb")
model = pickle.load(pickle_in)

#Création du dataframe utilisateur avec toutes les colonnes à 0.0
df_user = df.loc[len(df)-1:].apply(lambda x: 0.0)
df_user = df_user.drop(["id", "date", "prix", "m2_habitable15", "m2_parcelle15"])

#Config Streamlit
st.set_page_config(layout="wide")


#Titre
colT1,colT2 = st.columns([7,9])

with colT2:
    st.title("Maison")


###################################
############### Map ###############
###################################
midpoint = (np.average(df["lat"]), np.average(df["lon"]))

st.pydeck_chart(pdk.Deck(
    map_style = None,
    initial_view_state = pdk.ViewState(
        latitude = midpoint[0],
        longitude = midpoint[1],
        zoom = 10,
        min_zoom = 8,
        max_zoom = 30,
        pitch = 50,
    ),
    layers=[
        pdk.Layer(
           "HexagonLayer",
           data = df,
           get_position = "[lon, lat]",
           radius = 200,
           elevation_scale = 4,
           elevation_range = [0, 1000],
           pickable = True,
           extruded = True,
        ),
        pdk.Layer(
            "ScatterplotLayer",
            data = df,
            get_position = "[lon, lat]",
            get_color = [200, 30, 0, 160],
            get_radius = 200,
        ),
    ],
))


#Choix utilisateur
colT3,colT4 = st.columns([6,8])

with colT4:
    st.write("Choisissez votre configuration :")

col1, col2 = st.columns(2)

with col1:
    df_user["m2_habitable"] = st.text_input("Nombre de m2 habitable (34 - 1 258)", 34)
    df_user["m2_etage"] = st.text_input("Nombre de m2 à l'étage (34 - 874)", 34)
    df_user["annee_construction"] = st.text_input("Année de construction de la maison (1900 - 2015)", 1900)
    df_user["chambres"] = st.selectbox("Nombre de chambre :", ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"))
    df_user["note"] = st.selectbox("État de la maison :", ("3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"))
    code_postal = st.selectbox("Code postal souhaité :", ("98001", "98002", "98003", "98004", "98005", "98006", "98007", "98008",
            "98010", "98011", "98014", "98019", "98022", "98023", "98024", "98027", "98028", "98029", "98030", "98031", "98032",
            "98033", "98034", "98038", "98039", "98040", "98042", "98045", "98052", "98053", "98055", "98056", "98058", "98059",
            "98065", "98070", "98072", "98074", "98075", "98077", "98092", "98102", "98103", "98105", "98106", "98107", "98108",
            "98109", "98112", "98115", "98116", "98117", "98118", "98119", "98122", "98125", "98126", "98133", "98136", "98144",
            "98146", "98148", "98155", "98166", "98168", "98177", "98178", "98188", "98198", "98199"))
    df_user["salle_de_bain"] = st.slider("Nombre de salle de bain :", 0.25, 8.0, step=0.25)

with col2:
    df_user["m2_parcelle"] = st.text_input("Nombre de m2 de parcelle (48 - 1 000)", 48)
    df_user["m2_cave"] = st.text_input("Nombre de m2 à la cave (0 - 448)", 0)
    df_user["annee_renovation"] = st.text_input("Année de rénovation de la maison (1900 - 2015)", 1900)
    df_user["etages"] = st.selectbox("Nombre d'étages :", ("1.0", "1.5", "2.0", "2.5", "3.0", "3.5"))
    df_user["condition"] = st.selectbox("Condition de la maison :", ("1", "2", "3", "4", "5"))
    df_user["vue"] = st.selectbox("Vue de la maison :", ("0", "1", "2", "3", "4"))
    vue_mer = st.radio("Vue sur la mer ? :", ("Non", "Oui"))

if vue_mer == "Oui":
    vue_mer = int(1)
else:
    vue_mer = int(0)


df_user["vue_mer"] = vue_mer
df_user[code_postal] = 1

#Valeur moyenne
df_user["lat"] = 47.571800
df_user["lon"] = -122.230000


#Prédiction du prix, espacement des milliers, et affichage du prix
colT5,colT6 = st.columns([6,8])

with colT6:
    if st.button("Déterminez le prix de la maison"):
        prix_utilisateur = model.predict([df_user])
        resultat = [f"{int(val):,}".replace(",", " ") for val in prix_utilisateur]
        st.write("Le prix estimé est de : {} $".format(resultat[0]))