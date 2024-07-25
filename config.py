from yaml import safe_load

try:
    with open("config.yml", "r") as f:
        d = safe_load(f)
except FileNotFoundError:
    with open("example.config.yml", "r") as f:  # Fail safe
        d = safe_load(f)

config = d
