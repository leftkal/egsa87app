from flask import Flask, request, render_template
from pyproj import Transformer
import os

app = Flask(__name__)

# Set up transformers
to_wgs84 = Transformer.from_crs("EPSG:2100", "EPSG:4326", always_xy=True)
to_egsa87 = Transformer.from_crs("EPSG:4326", "EPSG:2100", always_xy=True)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    mode = request.form.get("mode", "egsa_to_wgs")

    if request.method == "POST":
        action = request.form.get("action")

        if action == "convert":
            try:
                val1 = float(request.form.get("val1", "").strip())
                val2 = float(request.form.get("val2", "").strip())

                if mode == "egsa_to_wgs":
                    lon, lat = to_wgs84.transform(val1, val2)
                    result = {
                        "lat": round(lat, 6),
                        "lon": round(lon, 6),
                        "input_x": round(val1, 2),
                        "input_y": round(val2, 2),
                        "mode": mode
                    }
                else:
                    x, y = to_egsa87.transform(val1, val2)
                    result = {
                        "x": round(x, 2),
                        "y": round(y, 2),
                        "input_lat": round(val2, 6),
                        "input_lon": round(val1, 6),
                        "mode": mode
                    }
            except ValueError:
                result = {"error": "Invalid input. Please enter valid numbers.", "mode": mode}

        elif action == "switch":
            mode = "wgs_to_egsa" if mode == "egsa_to_wgs" else "egsa_to_wgs"

    return render_template("index.html", result=result, mode=mode)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)

