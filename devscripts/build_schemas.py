import json
import tessera.models.v1.schemas as sch

with open("schemas.json", "w") as f:
    jsn = {}
    for name in sch.__dict__.items():
        if isinstance(name[1], dict) and not name[0].startswith("__"):
            jsn[name[0]] = name[1]

    f.write(json.dumps(jsn, sort_keys=True, indent=4))
