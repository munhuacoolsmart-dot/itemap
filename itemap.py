import folium
from folium import plugins
import os
import webbrowser

def generate_global_view(campuses):
    """Creates a high-level overview of ITE's presence across Singapore."""
    # Center of Singapore
    m = folium.Map(location=[1.3521, 103.8198], zoom_start=12, tiles='openstreetmap')
    
    fg = folium.FeatureGroup(name="ITE Campus Locations")
    for key, c in campuses.items():
        folium.Marker(
            location=c["center"],
            popup=f"<b>{c['name']}</b><br>Select from terminal for 3D details.",
            tooltip=f"Click for {c['name']}",
            icon=folium.Icon(color=c["theme"], icon="university", prefix='fa')
        ).add_to(fg)
    
    fg.add_to(m)
    plugins.Fullscreen().add_to(m)
    
    output = "ITE_Singapore_Global_Overview.html"
    m.save(output)
    webbrowser.open('file://' + os.path.realpath(output))
    print(f"\n[SUCCESS] Global Overview launched. Returning to menu...")

def generate_detailed_map(c):
    """Detailed campus map: Defaults to Satellite imagery with Light/Dark support."""
    # Satellite URL for default start
    sat_url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
    
    # Initialize with Satellite View
    m = folium.Map(location=c["center"], zoom_start=18, tiles=sat_url, attr='Esri')
    
    # Add Toggles (Light Mode is the first fallback)
    folium.TileLayer('openstreetmap', name="Light Mode").add_to(m)
    folium.TileLayer('cartodbdark_matter', name="Dark Mode").add_to(m)
    folium.TileLayer(sat_url, name="Satellite View", attr="Esri").add_to(m)
    
    # Sidebar with Live Clock
    sidebar_html = f"""
    <div style="position:fixed; top:20px; left:20px; width:220px; background:rgba(255,255,255,0.9); 
         border:2px solid {c['hex']}; z-index:9999; padding:15px; border-radius:10px; font-family:sans-serif; box-shadow: 2px 2px 10px rgba(0,0,0,0.2);">
        <h4 style="margin:0; color:{c['hex']};">{c['name']}</h4>
        <p style="font-size:12px; margin:5px 0;">Smart Campus Navigator</p>
        <hr>
        <div id="clock" style="font-weight:bold; font-size:16px;">--:--:--</div>
        <script>
            setInterval(() => {{ document.getElementById('clock').innerText = new Date().toLocaleTimeString(); }}, 1000);
        </script>
    </div>
    """
    m.get_root().html.add_child(folium.Element(sidebar_html))

    # Landmarks & Search
    fg_landmarks = folium.FeatureGroup(name="Campus Landmarks")
    for loc in c["landmarks"]:
        folium.Marker(
            loc["pos"], 
            name=loc["name"],
            popup=loc["name"],
            icon=folium.Icon(color=c["theme"], icon=loc["ico"], prefix='fa')
        ).add_to(fg_landmarks)
    
    fg_landmarks.add_to(m)

    # UI Controls
    plugins.Search(layer=fg_landmarks, search_label='name', placeholder="Find building...", collapsed=False).add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    plugins.Fullscreen().add_to(m)
    plugins.LocateControl().add_to(m)
    
    file_name = f"{c['name'].replace(' ', '_')}_Dashboard.html"
    m.save(file_name)
    webbrowser.open('file://' + os.path.realpath(file_name))
    print(f"\n[SUCCESS] {c['name']} Detailed Dashboard launched. Returning to menu...")

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
            {"name": "First Avenue (Food Court)", "pos": [1.3705, 103.8598], "ico": "utensils"}
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

# --- MAIN INTERFACE ---
while True:
    print("\n" + "="*50)
    print("      ITE SMART CAMPUS GEOSPATIAL INTERFACE")
    print("="*50)
    print("0. View National Campus Distribution (Global Overview)")
    print("1. Analyze ITE College West (Choa Chu Kang)")
    print("2. Analyze ITE College Central (Ang Mo Kio)")
    print("3. Analyze ITE College East (Simei)")
    print("4. Terminate Program")
    
    choice = input("\nEnter selection (0-4): ")
    
    if choice == "0":
        generate_global_view(campuses)
    elif choice in campuses:
        generate_detailed_map(campuses[choice])
    elif choice == "4":
        print("\nExiting.")
        break
    else:
        print("\n[!] Entry not recognized. Please choose 0, 1, 2, 3, or 4.")
