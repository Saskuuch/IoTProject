from flask import Flask, render_template
import folium
#import jinja2

app = Flask(__name__)

def map_create():
    lat = 50.676109
    lon = -120.340836
    zoom = 11

    # dfAreas = getAreas()

    map = folium.Map(location=[lat, lon],
                     zoom_start=zoom, control_scale=True)

    folium.Marker(
        [50.667, -120.367],
        popup=folium.Popup("<div style='width:500px;height:400px; background-color:white'><iframe id='popup' width='100%' height='100%' src='http://127.0.0.1:8000/dashboard'></iframe></div>", max_width=500),
        tooltip="TRU",
    ).add_to(map)

    map.get_root().width = "100%"
    map.get_root().height = "700px"

    return map

@app.route("/")
def initialLanding():
    map = map_create()
    html = map._repr_html_()
    return render_template("testhome.html", map_html = html)

@app.route("/dashboard", methods=['GET', 'POST'])
def dashBoard():
    return render_template("dashboard.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

