import folium
from folium import plugins
import os
import webbrowser

def generate_global_view(campuses):
    """High-level Singapore map showing all three ITE campuses."""
    m = folium.Map(location=[1.3521, 103.8198], zoom_start=11, tiles='openstreetmap')
    
    fg = folium.FeatureGroup(name="ITE Campuses")
    for key, c in campuses.items():
        folium.Marker(
            location=c["center"],
            popup=f"<b>{c['name']}</b>",
            tooltip=c["name"],
            icon=folium.Icon(color=c["theme"], icon="university", prefix='fa')
        ).add_to(fg)
    
    fg.add_to(m)
    output = "ITE_Global_Overview.html"
    m.save(output)
    webbrowser.open('file://' + os.path.realpath(output))

def generate_detailed_map(c):
    """Detailed campus map with Search, Satellite Start, and Light/Dark toggles."""
    # Start with Satellite View
    sat_url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
    m = folium.Map(location=c["center"], zoom_start=18, tiles=sat_url, attr='Esri')
    
    # Add Layer Toggles
    folium.TileLayer('openstreetmap', name="Light Mode").add_to(m)
    folium.TileLayer('cartodbdark_matter', name="Dark Mode").add_to(m)
    folium.TileLayer(sat_url, name="Satellite View", attr="Esri").add_to(m)
    
    # Sidebar with Live Clock
    sidebar_html = f"""
    <div style="position:fixed; top:20px; left:20px; width:220px; background:rgba(255,255,255,0.9); 
         border:2px solid {c['hex']}; z-index:9999; padding:15px; border-radius:10px; font-family:sans-serif; box-shadow: 2px 2px 10px rgba(0,0,0,0.2);">
        <h4 style="margin:0; color:{c['hex']};">{c['name']}</h4>
        <hr>
        <div id="clock" style="font-weight:bold; font-size:16px;">--:--:--</div>
        <script>
            setInterval(() => {{ document.getElementById('clock').innerText = new Date().toLocaleTimeString(); }}, 1000);
        </script>
    </div>
    """
    m.get_root().html.add_child(folium.Element(sidebar_html))

    # Markers Feature Group (REQUIRED for Search Plugin)
    fg_landmarks = folium.FeatureGroup(name="Campus Landmarks")
    for loc in c["landmarks"]:
        folium.Marker(
            loc["pos"], 
            name=loc["name"], # The 'name' attribute is what the Search bar looks for
            popup=loc["name"],
            icon=folium.Icon(color=c["theme"], icon=loc["ico"], prefix='fa')
        ).add_to(fg_landmarks)
    
    fg_landmarks.add_to(m)

    # 1. ADD SEARCH BAR
    plugins.Search(
        layer=fg_landmarks,
        search_label='name',
        placeholder="Search landmark (e.g. ICT, Aero)",
        collapsed=False,
        position='topright'
    ).add_to(m)
    
    # 2. ADD EXTRA CONTROLS
    folium.LayerControl(collapsed=False).add_to(m)
    plugins.Fullscreen().add_to(m)
    plugins.LocateControl().add_to(m)
    
    file_name = f"{c['name'].replace(' ', '_')}_Dashboard.html"
    m.save(file_name)
    webbrowser.open('file://' + os.path.realpath(file_name))
    print(f"[SUCCESS] {c['name']} Dashboard Launched.")

# --- DATA REPOSITORY ---
campuses = {
    "1": {
        "name": "ITE College West", "theme": "red", "hex": "#CC0000",
        "center": [1.3768, 103.7518],
        "landmarks": [
            {"name": "School of ICT", "pos": [1.3765, 103.7511], "ico": "laptop"},
            {"name": "Student Cafeteria", "pos": [1.3766, 103.7515], "ico": "utensils"}
        ]
    },
    "2": {
        "name": "ITE College Central", "theme": "blue", "hex": "#0000FF",
        "center": [1.3705, 103.8596],
        "landmarks": [
            {"name": "Aero Hub", "pos": [1.3698, 103.8595], "ico": "plane"},
            {"name": "First Avenue (Food)", "pos": [1.3705, 103.8598], "ico": "utensils"}
        ]
    },
    "3": {
        "name": "ITE College East", "theme": "green", "hex": "#008000",
        "center": [1.3415, 103.9530],
        "landmarks": [
            {"name": "Cyber Security Centre", "pos": [1.3408, 103.9532], "ico": "shield"},
            {"name": "College Hub", "pos": [1.3415, 103.9530], "ico": "users"}
        ]
    }
}

# --- MENU LOOP ---
while True:
    print("\n" + "="*45)
    print("   ITE SMART CAMPUS MASTER NAVIGATOR")
    print("="*45)
    print("0. Show Global Singapore View")
    print("1. ITE College West")
    print("2. ITE College Central")
    print("3. ITE College East")
    print("4. Exit")
    
    choice = input("\nSelect Option (0-4): ")
    if choice == "0":
        generate_global_view(campuses)
    elif choice in campuses:
        generate_detailed_map(campuses[choice])
    elif choice == "4":
        print("Closing System. Good luck tomorrow!")
        break
