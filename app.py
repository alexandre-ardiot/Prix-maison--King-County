import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import pydeck as pdk

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


df = pd.read_csv("donnees_map.csv")

st.title("Maison")

#df_map = pd.DataFrame(columns=["lat", "long"])

midpoint = (np.average(df["lat"]), np.average(df["lon"]))

st.pydeck_chart(pdk.Deck(
    map_style = None,
    initial_view_state = pdk.ViewState(
        latitude = midpoint[0],
        longitude = midpoint[1],
        zoom = 11,
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

#st.map(df)
#