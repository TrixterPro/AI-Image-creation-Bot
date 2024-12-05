import yaml
import os

CONFIG_PATH = "config.yml"

DEFAULT_CONFIG = {
    "TOKEN": "",
    "PREFIX": "!",
    "IMG_HIPPO_API_KEY": ""  # Add the new key here
}

class basicconfig:

    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as file:
            file.write("# Your discord bot token get it by creating an application at https://discord.com/developers/applications\n")
            yaml.dump({"TOKEN": ""}, file)
            
            file.write("\n# Prefix is for the discord bot prefixed commands (such as !help, '!' is the prefix here)\n")
            yaml.dump({"PREFIX": "!"}, file)
            
            file.write("\n# IMG_HIPPO_API_KEY is for accessing the ImgHippo API. You can get the API key at https://www.imghippo.com/api-info\n")
            yaml.dump({"IMG_HIPPO_API_KEY": ""}, file)

    with open(CONFIG_PATH, "r") as file:
        try:
            _config = yaml.safe_load(file)
            if not isinstance(_config, dict) or set(_config.keys()) != set(DEFAULT_CONFIG.keys()):
                raise ValueError("Invalid configuration structure.")
        except (yaml.YAMLError, ValueError):
            _config = DEFAULT_CONFIG.copy()
            with open(CONFIG_PATH, "w") as reset_file:
                # Manually add comments and the default configuration when resetting
                reset_file.write("# Your discord bot token get it by creating an application at https://discord.com/developers/applications\n")
                yaml.dump({"TOKEN": _config["TOKEN"]}, reset_file)
                
                reset_file.write("\n# Prefix is for the discord bot prefixed commands (such as !help, '!' is the prefix here)\n")
                yaml.dump({"PREFIX": _config["PREFIX"]}, reset_file)
                
                reset_file.write("\n# IMG_HIPPO_API_KEY is for accessing the ImgHippo API. You can get the API key at https://www.imghippo.com/api-info\n")
                yaml.dump({"IMG_HIPPO_API_KEY": _config["IMG_HIPPO_API_KEY"]}, reset_file)

    TOKEN = _config.get("TOKEN", "")
    PREFIX = _config.get("PREFIX", "!")
    IMG_HIPPO_API_KEY = _config.get("IMG_HIPPO_API_KEY", "")
