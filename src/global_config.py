import json

config_path = "src/config.json"
with open(config_path) as file:
    config = json.load(file)