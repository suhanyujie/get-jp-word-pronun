import toml


def get_config():
    config = toml.load("./.env.toml")
    collect_map = config["moji"]["collection_dict"]
    print(collect_map)
    pass


get_config()
