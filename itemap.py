import folium
from folium import plugins
import os
import webbrowser

def generate_global_view(campuses):
    """Creates a high-level Singapore map showing all three ITE campuses."""
    # Center of Singapore
    m = folium.Map(location=[1.3521, 103.8198], zoom_start=12, tiles='cartodbdark_matter')
    
    fg = folium.FeatureGroup(name="ITE Campuses")
    
    for key, c in campuses.items():
        folium.Marker(
            location=c["center"],
            popup=f"<b>{c['name']}</b><br>Click 'Select' in terminal to view details.",
            tooltip=c["name"],
            icon=folium.Icon(color=c["theme"], icon="university", prefix='fa')
        ).add_to(fg)
    
    fg.add_to(m)
    output = "ITE_Singapore_Global_View.html"
    m.save(output)
    webbrowser.open('file://' + os.path.realpath(output))
    print(f"\n[GLOBAL VIEW] Opened Singapore overview.")

def generate_detailed_map(c):
    """Generates the high-detail interactive map for a specific campus."""
    m = folium.Map(location=c["center"], zoom_start=18, tiles=None)
    
    # Layers
    folium.TileLayer('openstreetmap', name="Light Mode").add_to(m)
    folium.TileLayer('cartodbdark_matter', name="Dark Mode").add_to(m)
    
    # Sidebar HTML
    sidebar_html = f"""
    <div style="position:fixed; top:20px; left:20px; width:220px; background:white; 
         border:2px solid {c['hex']}; z-index:9999; padding:15px; border-radius:10px; font-family:sans-serif;">
        <h4 style="margin:0; color:{c['hex']};">{c['name']}</h4>
        <p style="font-size:12px;">Smart Campus Dashboard</p>
        <hr>
        <div id="clock" style="font-weight:bold;"></div>
        <script>
            setInterval(() => {{ document.getElementById('clock').innerText = new Date().toLocaleTimeString(); }}, 1000);
        </script>
    </div>
    """
    m.get_root().html.add_child(folium.Element(sidebar_html))

    # Add Markers & Features
    fg = folium.FeatureGroup(name="Landmarks")
    for loc in c["landmarks"]:
        folium.Marker(
            loc["pos"], 
            popup=loc["name"],
            icon=folium.Icon(color=c["theme"], icon=loc["ico"], prefix='fa')
        ).add_to(fg)
    
    fg.add_to(m)
    folium.LayerControl().add_to(m)
    
    file_name = f"{c['name'].replace(' ', '_')}_Detail.html"
    m.save(file_name)
    webbrowser.open('file://' + os.path.realpath(file_name))
    print(f"[DETAIL VIEW] Opened {c['name']} detailed dashboard.")

# --- DATA REPOSITORY ---
campuses = {
    "1": {
        "name": "ITE College West", "theme": "red", "hex": "#CC0000",
        "center": [1.3768, 103.7518],
        "landmarks": [{"name": "School of ICT", "pos": [1.3765, 103.7511], "ico": "laptop"}]
    },
    "2": {
        "name": "ITE College Central", "theme": "blue", "hex": "#0000FF",
        "center": [1.3705, 103.8596],
        "landmarks": [{"name": "Aero Hub", "pos": [1.3698, 103.8595], "ico": "plane"}]
    },
    "3": {
        "name": "ITE College East", "theme": "green", "hex": "#008000",
        "center": [1.3415, 103.9530],
        "landmarks": [{"name": "Cyber Security Centre", "pos": [1.3408, 103.9532], "ico": "shield"}]
    }
}

# --- MAIN INTERFACE ---
while True:
    print("\n" + "="*40)
    print("   ITE SMART CAMPUS MASTER NAVIGATOR")
    print("="*40)
    print("0. Show Global Singapore View")
    print("1. ITE College West (Choa Chu Kang)")
    print("2. ITE College Central (Ang Mo Kio)")
    print("3. ITE College East (Simei)")
    print("4. Exit")
    
    choice = input("\nSelect Option (0-4): ")
    
    if choice == "0":
        generate_global_view(campuses)
    elif choice in campuses:
        generate_detailed_map(campuses[choice])
    elif choice == "4":
        print("Closing Navigator. Good luck for your interview!")
        break
    else:
        print("Invalid Choice.")
