import streamlit as st
import leafmap.foliumap as leafmap



st.title("Buscando Mapas Bases")
st.markdown(
    """

Amigos, Esta aplicación la he desarollado como  una demostración de cómo buscar y cargar mapas base desde [xyzservices]
"""
)



row1_col1, row1_col2 = st.columns([3, 1])
width = None
height = 800
tiles = None

with row1_col2:

    checkbox = st.checkbox("Buscar servicios de mapas rápidos (QMS)")
    keyword = st.text_input("Ingrese una palabra clave para buscar y presione Enter (x,y,z):")
    empty = st.empty()

    if keyword:
        options = leafmap.search_xyz_services(keyword=keyword)
        if checkbox:
            options = options + leafmap.search_qms(keyword=keyword)

        tiles = empty.multiselect("Selecciona mosaicos XYZ para agregarlos al mapa:", options)

    with row1_col1:
        m = leafmap.Map()

        if tiles is not None:
            for tile in tiles:
                m.add_xyz_service(tile)

        m.to_streamlit(width, height)
