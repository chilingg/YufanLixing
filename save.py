import json

def loadJson(file):
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

def saveJson(obj, file):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, sort_keys=True, indent=2)

if __name__ == "__main__":
    file = "yufanlixing.fas.json"
    configFile = "data/config.json"
    componentsPath = "data/components/"

    source = loadJson(file)

    components = source['components']
    source['components'] = {}

    for key in components:
        saveJson(components[key], componentsPath + key + '.json')

    otherConfigList = [
        "interval",
        "place_replace",
        "reduce_replace",
        "supplement",
        "type_replace"
    ]
    for key in otherConfigList:
        data = source['config'][key]
        source['config'][key] = {}
        saveJson(data, 'data/' + key + '.json')

    saveJson(source, configFile)