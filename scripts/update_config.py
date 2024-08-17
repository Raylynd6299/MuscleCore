import json
import os

def update_config():
    with open('.chalice/config.json', 'r') as f:
        config = json.load(f)

    for stage in config['stages']:
        for key, value in config['stages'][stage]['environment_variables'].items():
            if value == "":
                config['stages'][stage]['environment_variables'][key] = os.getenv(key)

    with open('.chalice/config.json', 'w') as f:
        json.dump(config, f, indent=2)

if __name__ == "__main__":
    update_config()
