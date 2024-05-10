'''import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

st.set_page_config(layout="wide")

st.title("Mapa DE CALOR")

# Cargar los límites de los países
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Encuentra el polígono de Colombia
colombia = world[world['name'] == 'Colombia']

with st.expander("MIRA EL CODIGO"):
    with st.echo():
        url_path = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_cities.csv"
        mapa = leafmap.Map(center=[4, -74], zoom=5)  # Ajustar centro y zoom para Colombia
        
        # Añadir mapa de calor
        mapa.add_heatmap(
            url_path,
            latitude="latitude",
            longitude="longitude",
            value="pop_max",
            name="Heat map",
            radius=20,
        )
        
        # Añadir capa de límites de países después del mapa de calor
        mapa.add_gdf(world, layer_name='World Borders')
        
        # Añadir polígono de Colombia después de la capa de límites de países
        mapa.add_gdf(colombia, layer_name='Colombia', fill_color='red', fill_opacity=0.5)
        
mapa.to_streamlit(height=700)

import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

st.set_page_config(layout="wide")

st.title("Mapa DE CALOR")

# Cargar los límites de los países
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Encuentra el polígono de Colombia
colombia = world[world['name'] == 'Colombia']

with st.expander("MIRA EL CODIGO"):
    with st.echo():
        url_path = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_cities.csv"
        mapa = leafmap.Map(center=[4, -74], zoom=5)  # Ajustar centro y zoom para Colombia
        
        # Añadir mapa de calor
        mapa.add_heatmap(
            url_path,
            latitude="latitude",
            longitude="longitude",
            value="pop_max",
            name="Heat map",
            radius=20,
        )
        
        # Añadir polígono de Colombia al mapa
        mapa.add_gdf(colombia, layer_name='Colombia', fill_color='red', fill_opacity=0.5)
        # Añadir etiqueta al país de Colombia
        mapa.add_marker(location=[4, -74], popup="¡Bienvenido a Colombia!", tooltip="Mi bello Pais Colombia", layer_name="Colombia Label")

        
mapa.to_streamlit(height=700)
'''
import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

st.set_page_config(layout="wide")

st.title("Mapa DE CALOR")

# Cargar los límites de los países
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Encuentra el polígono de Colombia
colombia = world[world['name'] == 'Colombia']

with st.expander("MIRA EL CODIGO"):
    with st.echo():
        url_path = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_cities.csv"
        mapa = leafmap.Map(center=[4, -74], zoom=5)  # Ajustar centro y zoom para Colombia
        
        # Añadir mapa de calor
        mapa.add_heatmap(
            url_path,
            latitude="latitude",
            longitude="longitude",
            value="pop_max",
            name="Heat map",
            radius=20,
        )
        
        # Añadir polígono de Colombia al mapa
        colombia_layer = mapa.add_gdf(colombia, layer_name='Colombia', fill_color='red', fill_opacity=0.5)
        
        # Añadir etiqueta al país de Colombia
        colombia_label = mapa.add_marker(location=[4, -74], popup="¡Bienvenido a Colombia!", tooltip="Colombia", layer_name="Colombia Label")
        
        # JavaScript para cambiar el color de fondo del polígono al hacer clic en la etiqueta
        html = """
        <script>
        var colombiaLabel = document.querySelector('[title="Colombia"]');
        colombiaLabel.addEventListener('click', function() {
            var colombiaLayer = leafmap.map.getLayer('Colombia');
            if (colombiaLayer.options.fillColor == 'red') {
                colombiaLayer.setStyle({fillColor: 'blue'});
            } else {
                colombiaLayer.setStyle({fillColor: 'red'});
            }
        });
        </script>
        """
        st.markdown(html, unsafe_allow_html=True)
        
mapa.to_streamlit(height=700)
