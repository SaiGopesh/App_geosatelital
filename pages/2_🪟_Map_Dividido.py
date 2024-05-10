import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")


st.title("Amigos, Divido El mapa En dos Partes Para ANIMARLO MUCHO MEJOR")

with st.expander("El Codigo Fuente Que se Uso"):
    with st.echo():
        m = leafmap.Map()
        m.split_map(
            left_layer="ESA WorldCover 2020 S2 FCC", right_layer="ESA WorldCover 2020"
        )
        m.add_legend(title="Cobertura terrestre", builtin_legend="ESA_WorldCover")

m.to_streamlit(height=700)
