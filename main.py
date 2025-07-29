from pyproj import Transformer

# Μετατροπέας από ΕΓΣΑ87 (EPSG:2100) σε WGS84 (EPSG:4326)
transformer = Transformer.from_crs("EPSG:2100", "EPSG:4326", always_xy=True)

x, y = 714242, 4341841  # Παράδειγμα ΕΓΣΑ87 συντεταγμένες
lon, lat = transformer.transform(x, y)

print(f"Γεωγραφικό πλάτος: {lat}, Γεωγραφικό μήκος: {lon}")
