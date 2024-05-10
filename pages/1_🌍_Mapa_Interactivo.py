import streamlit as st
import leafmap.foliumap as leafmap



st.title(" Mapa Interactivo")

col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:

    basemap = st.selectbox("Selecciona Una  a base Del Mapa:", options, index)


with col1:

    mapa = leafmap.Map(
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
    )
    mapa.add_basemap(basemap)
    mapa.to_streamlit(height=700)
