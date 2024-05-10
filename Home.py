import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

# Customize the sidebar




# Customize page title
st.title("Aplicacion Geolocalizacion hecha by Juan Quintero Colombia Comunidad Latinos")

st.markdown(
    """
    En esta aplicacion Consumo distintas APIS Y repositorios para realizar la Aplicacion De Geolocaliacion
    """
)




mapa = leafmap.Map(minimap_control=True)
mapa.add_basemap("OpenTopoMap")
mapa.to_streamlit(height=500)
