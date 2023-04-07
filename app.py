import streamlit as st
import ee
import geemap
import folium
from folium.plugins import DualMap
from streamlit_folium import folium_static
from datetime import date
import datetime
from RadGEEToolbox import LandsatCollection, CollectionStitch, LandsatCollection2

#os.environ["EARTHENGINE_TOKEN"] == st.secrets["EARTHENGINE_TOKEN"]

st.set_page_config(layout="wide")

st.title("Utah Remote Sensing Interface | Static Snow Comparisons | 2022 vs 2023")

ee.Initialize()
today = datetime.datetime.today()
start_date = '2022-04-07' #today - datetime.timedelta(days=365)
end_date = '2023-04-10' #today.strftime('%Y-%m-%d')

# Function to generate the satellite imagery
@st.cache_resource(show_spinner="Fetching map data...")
def generate_satellite_imagery():
    lcol_S = LandsatCollection2(start_date, end_date, 32, 38, 30)
    lcol_N = LandsatCollection2(start_date, end_date, 31, 38, 30)
    lcol = lcol_S.CollectionStitch(lcol_N)
    vis_params = {
        'bands':['SR_B4', 'SR_B3', 'SR_B2'],
        'min':0,
        'max':35000,
        'gamma':0.9,
    }
    # Your Earth Engine layers
    left_tile_url = lcol.image_grab(-1).getMapId(vis_params)['tile_fetcher'].url_format
    right_tile_url = lcol.image_grab(0).getMapId(vis_params)['tile_fetcher'].url_format

    # Create the folium map
    map_center = (40.874741, -111.902031)
    map_zoom = 10

    # Create the DualMap
    m = DualMap(location=map_center, zoom_start=map_zoom, tiles=None, control_scale=True, attr="id=dual_map")

    folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m.m1)
    folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m.m2)

    # Create the Earth Engine layers
    left_layer = folium.TileLayer(
        tiles=left_tile_url, 
        attr='Map Data &copy; <font size="4"> <a href="https://earthengine.google.com/">Google Earth Engine</a> | Landsat Imagery'
    )
    right_layer = folium.TileLayer(
        tiles=right_tile_url, 
        attr='Map Data &copy; <font size="4"> <a href="https://earthengine.google.com/">Google Earth Engine</a> | Landsat Imagery'
    )
    # Add layers to the maps
    left_layer.add_to(m.m1)
    right_layer.add_to(m.m2)
    # Add streets layer on top of the GEE imagery
    folium.TileLayer(
        tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lines/{z}/{x}/{y}{r}.png',
        attr='Street tiles by <font size="1"> <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.',
        name='Streets',
        opacity=1
    ).add_to(m.m1)

    folium.TileLayer(
        tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lines/{z}/{x}/{y}{r}.png',
        attr='Street tiles by <font size="1"> <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.',
        name='Streets',
        opacity=1
    ).add_to(m.m2)


    return m, lcol.image_grab(-1).getInfo().get('properties')['Date_Filter'], lcol.image_grab(0).getInfo().get('properties')['Date_Filter']

# Function to generate the satellite imagery
@st.cache_resource(show_spinner="Fetching map data...")
def generate_satellite_imagery_23():
    lcol_S = LandsatCollection2(start_date, end_date, 32, 38, 30)
    lcol_N = LandsatCollection2(start_date, end_date, 31, 38, 30)
    lcol = lcol_S.CollectionStitch(lcol_N)
    vis_params = {
        'bands':['SR_B4', 'SR_B3', 'SR_B2'],
        'min':0,
        'max':35000,
        'gamma':0.9,
    }
    # Your Earth Engine layers
    left_tile_url = lcol.image_grab(-2).getMapId(vis_params)['tile_fetcher'].url_format
    right_tile_url = lcol.image_grab(-3).getMapId(vis_params)['tile_fetcher'].url_format

    # Create the folium map
    map_center = (40.874741, -111.902031)
    map_zoom = 10

    # Create the DualMap
    m = DualMap(location=map_center, zoom_start=map_zoom, tiles=None, control_scale=True, attr="id=dual_map")

    folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m.m1)
    folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m.m2)

    # Create the Earth Engine layers
    left_layer = folium.TileLayer(
        tiles=left_tile_url, 
        attr='Map Data &copy; <font size="4"> <a href="https://earthengine.google.com/">Google Earth Engine</a> | Landsat Imagery'
    )
    right_layer = folium.TileLayer(
        tiles=right_tile_url, 
        attr='Map Data &copy; <font size="4"> <a href="https://earthengine.google.com/">Google Earth Engine</a> | Landsat Imagery'
    )
    # Add layers to the maps
    left_layer.add_to(m.m1)
    right_layer.add_to(m.m2)
    # Add streets layer on top of the GEE imagery
    folium.TileLayer(
        tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lines/{z}/{x}/{y}{r}.png',
        attr='Street tiles by <font size="1"> <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.',
        name='Streets',
        opacity=1
    ).add_to(m.m1)

    folium.TileLayer(
        tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lines/{z}/{x}/{y}{r}.png',
        attr='Street tiles by <font size="1"> <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.',
        name='Streets',
        opacity=1
    ).add_to(m.m2)


    return m, lcol.image_grab(-2).getInfo().get('properties')['Date_Filter'], lcol.image_grab(-3).getInfo().get('properties')['Date_Filter']

# Function to generate the satellite imagery
@st.cache_resource(show_spinner="Fetching map data...")
def generate_satellite_imagery_22_23():
    lcol_S = LandsatCollection2(start_date, end_date, 32, 38, 30)
    lcol_N = LandsatCollection2(start_date, end_date, 31, 38, 30)
    lcol = lcol_S.CollectionStitch(lcol_N)
    vis_params = {
        'bands':['SR_B4', 'SR_B3', 'SR_B2'],
        'min':0,
        'max':35000,
        'gamma':0.9,
    }
    # Your Earth Engine layers
    left_tile_url = lcol.image_grab(-4).getMapId(vis_params)['tile_fetcher'].url_format
    right_tile_url = lcol.image_grab(-5).getMapId(vis_params)['tile_fetcher'].url_format

    # Create the folium map
    map_center = (40.874741, -111.902031)
    map_zoom = 10

    # Create the DualMap
    m = DualMap(location=map_center, zoom_start=map_zoom, tiles=None, control_scale=True, attr="id=dual_map")

    folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m.m1)
    folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m.m2)

    # Create the Earth Engine layers
    left_layer = folium.TileLayer(
        tiles=left_tile_url, 
        attr='Map Data &copy; <font size="4"> <a href="https://earthengine.google.com/">Google Earth Engine</a> | Landsat Imagery'
    )
    right_layer = folium.TileLayer(
        tiles=right_tile_url, 
        attr='Map Data &copy; <font size="4"> <a href="https://earthengine.google.com/">Google Earth Engine</a> | Landsat Imagery'
    )
    # Add layers to the maps
    left_layer.add_to(m.m1)
    right_layer.add_to(m.m2)
    # Add streets layer on top of the GEE imagery
    folium.TileLayer(
        tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lines/{z}/{x}/{y}{r}.png',
        attr='Street tiles by <font size="1"> <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.',
        name='Streets',
        opacity=1
    ).add_to(m.m1)

    folium.TileLayer(
        tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lines/{z}/{x}/{y}{r}.png',
        attr='Street tiles by <font size="1"> <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.',
        name='Streets',
        opacity=1
    ).add_to(m.m2)


    return m, lcol.image_grab(-4).getInfo().get('properties')['Date_Filter'], lcol.image_grab(-5).getInfo().get('properties')['Date_Filter']

# def main():
#     st.title("My Snow Extent Map")
#     map_width = st.slider("Map Width (adjust to fit your device)", min_value=400, max_value=2000, value=1200, step=10)
#     # Call the cached function to get the satellite imagery
#     map, date1, date2 = generate_satellite_imagery()
#     st.header("Left image: "+str(date1)+" | Right image: "+str(date2))
#     map2, date3, date4 = generate_satellite_imagery_23()
#     folium_static(map, width=map_width, height=600)
#     new_dates = 'Left: '+str(date3)+' | Right: '+str(date4)
#     st.header(new_dates)
#     folium_static(map2, width=map_width, height=600)
#     map3, date5, date6 = generate_satellite_imagery_22_23()
#     st.header("Left image: "+str(date5)+" | Right image: "+str(date6))
#     folium_static(map3, width=map_width, height=600)

def main():
    st.title("My Snow Extent Map")
    
    # Custom CSS for centering the content
    custom_css = """
    <style>
        .centered {
            display: flex;
            justify-content: center;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    
    map_width = st.slider("Map Width (adjust to fit your device)", min_value=400, max_value=2000, value=1200, step=10)
    map_height = st.slider("Map Width (adjust to fit your device)", min_value=200, max_value=1500, value=600, step=10)

    with st.expander("Map 1 - 2022 vs 2023", expanded=True):
        map, date1, date2 = generate_satellite_imagery()
        st.header("Left image: "+str(date1)+" | Right image: "+str(date2))
        container1 = st.container()
        with container1:
            st.markdown('<div class="centered">', unsafe_allow_html=True)
            folium_static(map, width=map_width, height=map_height)
            st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("Map 2 - Early 2023"):
        map2, date3, date4 = generate_satellite_imagery_23()
        st.header("Left image: "+str(date3)+" | Right image: "+str(date4))
        container2 = st.container()
        with container2:
            st.markdown('<div class="centered">', unsafe_allow_html=True)
            folium_static(map2, width=map_width, height=map_height)
            st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("Map 3 - Late 2022 vs Early 2023"):
        map3, date5, date6 = generate_satellite_imagery_22_23()
        st.header("Left image: "+str(date5)+" | Right image: "+str(date6))
        container3 = st.container()
        with container3:
            st.markdown('<div class="centered">', unsafe_allow_html=True)
            folium_static(map3, width=map_width, height=map_height)
            st.markdown('</div>', unsafe_allow_html=True)

st.write('*Contact: markradwin@gmail.com* | Earth Observations Geoscientist')
st.write('*Affiliation: University of Utah - Geology & Geophysics Dept.*')    

if __name__ == "__main__":
    main()
