import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from roboflow import Roboflow
from PIL import Image
import tempfile
import os
from collections import defaultdict
from geopy.geocoders import Nominatim
import plotly.express as px

# Initialize session state
if "locations" not in st.session_state:
    st.session_state.locations = defaultdict(lambda: {"latitude": None, "longitude": None, "animals": defaultdict(int)})

# Initialize the Roboflow model
rf = Roboflow(api_key="YjMxjvei1qSX2MwmTqkv")  # Replace with your actual API key
project = rf.workspace("ttu-py3sj").project("animal-classification-rextd")  
model = project.version(1).model  

# Geolocator for converting place names to coordinates
geolocator = Nominatim(user_agent="geo_app")

# Sidebar for navigation
st.sidebar.title("🌍 Wildlife Tracking App")
page = st.sidebar.radio("Select a Page", ["Home", "📷 Upload & Classify", "📊 Analytics"])

# -------------------------------------- HOME PAGE --------------------------------------
if page == "Home":
    st.title("🌍 Wildlife Map")
    st.write("Hover over markers to see data. Click to open analytics sidebar.")

    # Create the map
    map_center = [20.0, 0.0]  # Center of the world
    m = folium.Map(location=map_center, zoom_start=2)

    # Add markers
    for place, data in st.session_state.locations.items():
        popup_info = f"**{place}**<br>Animals: {sum(data['animals'].values())}"
        marker = folium.Marker(
            location=[data["latitude"], data["longitude"]],
            popup=popup_info,
            tooltip=place
        )
        marker.add_to(m)

    # Render the map
    folium_static(m)

    # Sidebar pops up when a marker is clicked
    st.sidebar.title("📊 Location Analytics")
    selected_location = st.sidebar.selectbox("Select Location", list(st.session_state.locations.keys()), index=0 if st.session_state.locations else None)

    if selected_location:
        data = st.session_state.locations[selected_location]
        total_animals = sum(data["animals"].values())
        num_species = len(data["animals"])
        species_list = ", ".join(data["animals"].keys())

        st.sidebar.write(f"**📍 Location:** {selected_location}")
        st.sidebar.write(f"**🐾 Total Animals Recorded:** {total_animals}")
        st.sidebar.write(f"**🔬 Number of Species:** {num_species}")
        st.sidebar.write(f"**🦁 Species Found:** {species_list}")

# -------------------------------------- IMAGE UPLOAD & CLASSIFICATION --------------------------------------
elif page == "📷 Upload & Classify":
    st.title("📷 Upload Image for Animal Classification")

    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        max_size = (800, 800)
        image.thumbnail(max_size)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmpfile:
            image.save(tmpfile, format="JPEG")
            tmpfile_path = tmpfile.name
        
        # Predict the animal in the image
        prediction = model.predict(tmpfile_path)
        predicted_label = prediction.predictions[0]['class']
        st.write(f"Prediction: **{predicted_label}**")
        
        # User inputs place name
        place_name = st.text_input("📍 Enter Place Name (e.g., City, Landmark)", key="place_input")

        if st.button("Save Location and Animal Data"):
            if place_name:
                location = geolocator.geocode(place_name)

                if location:
                    if place_name not in st.session_state.locations:
                        st.session_state.locations[place_name]["latitude"] = location.latitude
                        st.session_state.locations[place_name]["longitude"] = location.longitude

                    st.session_state.locations[place_name]["animals"][predicted_label] += 1
                    st.success(f"✅ Data saved for {place_name}!")

                    # Instead of using st.experimental_rerun(), you can simply update session state here
                    # You can force page to refresh using another widget or actions as per need
                    st.session_state.refresh = True

                else:
                    st.warning("⚠️ Location not found. Please enter a valid place name.")

# -------------------------------------- ANALYTICS PAGE --------------------------------------
elif page == "📊 Analytics":
    st.title("📊 Wildlife Analytics Dashboard")

    # Dropdowns for filtering
    selected_location = st.selectbox("📍 Select Location", ["All"] + list(st.session_state.locations.keys()))
    selected_animal = st.selectbox("🐾 Select Animal", ["All"] + list(set(animal for loc in st.session_state.locations.values() for animal in loc["animals"])))
    selected_chart = st.selectbox("📈 Select Chart Type", ["Bar Chart", "Pie Chart", "Line Chart"])

    # Prepare data
    data = []
    for place, info in st.session_state.locations.items():
        for animal, count in info["animals"].items():
            data.append({"Place": place, "Animal": animal, "Count": count})

    df = pd.DataFrame(data)

    if selected_location != "All":
        df = df[df["Place"] == selected_location]

    if selected_animal != "All":
        df = df[df["Animal"] == selected_animal]

    # Display chart
    if not df.empty:
        if selected_chart == "Bar Chart":
            fig = px.bar(df, x="Animal", y="Count", color="Place", title="Animal Count per Location")
        elif selected_chart == "Pie Chart":
            fig = px.pie(df, names="Animal", values="Count", title="Distribution of Animals")
        elif selected_chart == "Line Chart":
            fig = px.line(df, x="Animal", y="Count", color="Place", title="Trend of Animal Sightings")

        st.plotly_chart(fig)
    else:
        st.write("⚠️ No data available for the selected filters.")

    # Interactive Map Analytics
    st.write("### 📌 Click on the Map to View Analytics")
    map_center = [20.0, 0.0]
    m = folium.Map(location=map_center, zoom_start=2)

    def on_click_callback(e):
        st.session_state.clicked_location = e.latlng

    for place, info in st.session_state.locations.items():
        marker = folium.Marker(
            location=[info["latitude"], info["longitude"]],
            tooltip=f"Click for details",
            popup=f"📍 {place}<br>🦁 Animals: {sum(info['animals'].values())}"
        )
        marker.add_to(m)

    folium_static(m)

    if "clicked_location" in st.session_state:
        lat, lon = st.session_state.clicked_location
        clicked_place = None

        for place, info in st.session_state.locations.items():
            if abs(info["latitude"] - lat) < 0.1 and abs(info["longitude"] - lon) < 0.1:
                clicked_place = place
                break

        if clicked_place:
            st.sidebar.write(f"📍 **Location:** {clicked_place}")
            st.sidebar.write(f"🐾 **Animals Found:** {st.session_state.locations[clicked_place]['animals']}")
