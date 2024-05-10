import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")



st.title("Marcadores")

with st.expander("Aqui esta el Codigo"):
    with st.echo():

        mapa = leafmap.Map(center=[40, -100], zoom=4)
        ciudades = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_cities.csv"
        regiones = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_regions.geojson"

        mapa.add_geojson(regiones, layer_name="US Regions")
        mapa.add_points_from_xy(
            ciudades,
            x="longitude",
            y="latitude",
            color_column="region",
            icon_names=["gear", "map", "leaf", "globe"],
            spin=True,
            add_legend=True,
        )

mapa.to_streamlit(height=700)
