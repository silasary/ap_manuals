import json
import os

files = ["frankston_line.json",
         "geelong_line.json",
         "hurstbridge_line.json",
         "lilydale,_belgrave,_alamein_and_glen_waverley_lines.json",
         "mernda_line.json",
         "pakenham_and_cranbourne_lines.json",
         "sandringham_line.json",
         "sunbury_line.json",
         "upfield_line.json"]


def convert(filename: str):
    with open(os.path.join(os.path.split(__file__)[0], filename)) as f:
        blob = json.load(f)
    output = [{"name":blob[0]["name"]}]
    children = blob[0]["children"]
    new_children = []
    for child in children:
        access = child["access_rules"]
        map_coords = child["map_locations"]
        map_coords.append({
                        "map": f'{filename.split(".")[0]}_map',
                        "x": 12,
                        "y": 12,
                        "size": 24
                    })
        stations = child["sections"]
        for station in stations:
            new_children.append([{"name": station["name"], "access_rules": access, "sections": [{"name": station["name"], "item_count": 1}], "map_locations": map_coords}])
    output[0]["children"] = new_children
    with open(os.path.join(os.path.split(__file__)[0], f'output/{filename}'), 'w') as f:
        json.dump(obj=output, fp=f)

convert("werribee_and_williamstown_lines.json")
    