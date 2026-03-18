import folium
from folium import plugins
import os
import webbrowser

# 1. CAMPUS COORDINATES & DATA
ite_west_coords = [1.3768, 103.7518]

# Boundary for the ITE CW Perimeter
boundary = [[1.37804, 103.7515], [1.3779, 103.75235], [1.37715, 103.7528], 
            [1.3762, 103.7526], [1.3755, 103.7522], [1.3755, 103.7514], 
            [1.3762, 103.7508], [1.3772, 103.7509]]

# Landmarks with Metadata (Name, Position, Category, Color, Icon, Image)
landmarks = [
    {"name": "School of ICT", "pos": [1.37650, 103.75110], "cat": "School", "clr": "green", "ico": "laptop", "img": "https://www.ite.edu.sg/images/default-source/college-west/cw-ict-building.jpg"},
    {"name": "School of Business", "pos": [1.37730, 103.75140], "cat": "School", "clr": "blue", "ico": "briefcase", "img": "https://www.ite.edu.sg/images/default-source/college-west/cw-business.jpg"},
    {"name": "Student Cafeteria", "pos": [1.37660, 103.75150], "cat": "Facility", "clr": "orange", "ico": "utensils", "img": "https://www.ite.edu.sg/images/default-source/college-west/cw-amenities.jpg"},
    {"name": "Main Entrance", "pos": [1.37775, 103.75185], "cat": "Facility", "clr": "black", "ico": "door-open", "img": "https://www.ite.edu.sg/images/default-source/college-west/cw-entrance.jpg"}
]

# 2. INITIALIZE MAP & TILES
m = folium.Map(location=ite_west_coords, zoom_start=18, tiles=None)
folium.TileLayer('openstreetmap', name="Light Mode").add_to(m)
folium.TileLayer('cartodbdark_matter', name="Dark Mode").add_to(m)
folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', 
                 name="Satellite", attr="Esri").add_to(m)

# 3. CREATE FEATURE GROUPS
fg_markers = folium.FeatureGroup(name="Locations")
fg_heat = folium.FeatureGroup(name="Crowd Density (Heatmap)", show=False)
fg_routes = folium.FeatureGroup(name="Walking Routes")

# 4. ADD SIDEBAR & LIVE CLOCK (HTML/JS Injection)
sidebar_html = f"""
<div id="sidebar" style="position:fixed; top:20px; left:20px; width:240px; background:rgba(255,255,255,0.9); 
     border:2px solid #CC0000; z-index:9999; padding:15px; border-radius:12px; font-family:sans-serif; box-shadow:2px 2px 10px rgba(0,0,0,0.2);">
    <h3 style="margin:0; color:#CC0000;">ITE College West</h3>
    <div style="font-size:18px; margin:10px 0; font-weight:bold;" id="clock">--:--:--</div>
    <ul style="list-style:none; padding:0; font-size:13px;">
        {"".join([f"<li style='margin-bottom:5px;'><i class='fa fa-map-marker' style='color:{l['clr']}'></i> {l['name']}</li>" for l in landmarks])}
    </ul>
    <script>
        function updateClock() {{ document.getElementById('clock').innerText = new Date().toLocaleTimeString(); }}
        setInterval(updateClock, 1000); updateClock();
    </script>
</div>
"""
m.get_root().html.add_child(folium.Element(sidebar_html))

# 5. ADD LAYERS (Polygon, Markers, Heatmap, Routes)
folium.Polygon(boundary, color="#CC0000", fill=True, fill_opacity=0.1, popup="ITE CW Perimeter").add_to(m)

for loc in landmarks:
    popup_html = f'<div style="width:200px"><h4>{loc["name"]}</h4><img src="{loc["img"]}" style="width:100%; border-radius:5px;"><br><small>ITE CW {loc["cat"]}</small></div>'
    folium.Marker(loc["pos"], name=loc["name"], popup=folium.Popup(folium.IFrame(popup_html, width=220, height=180)),
                  icon=folium.Icon(color=loc["clr"], icon=loc["ico"], prefix='fa')).add_to(fg_markers)

plugins.HeatMap([[1.3766, 103.7515, 0.9], [1.3768, 103.7518, 0.7]], radius=25).add_to(fg_heat)
plugins.AntPath([[1.37775, 103.75185], [1.3774, 103.75185], [1.3765, 103.7511]], color="blue", weight=5).add_to(fg_routes)

# 6. INTEGRATE & SAVE
fg_markers.add_to(m); fg_heat.add_to(m); fg_routes.add_to(m)
folium.LayerControl(collapsed=False).add_to(m)
plugins.Search(layer=fg_markers, search_label='name', placeholder="Find building...", collapsed=False).add_to(m)
plugins.LocateControl().add_to(m)
plugins.Fullscreen().add_to(m)
m.add_child(folium.LatLngPopup())

output = "ITE_CW_Smart_App.html"
m.save(output)
webbrowser.open('file://' + os.path.realpath(output))
print(f"Deployment Successful: {output}")