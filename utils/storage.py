import os
import json

CONFIG_FILE = "config.json"

DEFAULT_GUILD_CONFIG = {
    "language": "tr",
    "welcome_channel_id": None,
    "goodbye_channel_id": None,
    "log_channel_id": None,
    "autorole_id": None,
    "ticket_category_id": None,
    "support_role_id": None,
    "youtube_channel_url": None,
    "youtube_post_channel_id": None,
    "youtube_last_video_url": None,
    "dm_welcome_enabled": True
}

JSON_FILES = [
    "config.json",
    "youtube.json"
]

def ensure_json_files():
    for filename in JSON_FILES:
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=2, ensure_ascii=False)

def load_json(filename):
    ensure_json_files()
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_config():
    return load_json(CONFIG_FILE)

def save_config(data):
    save_json(CONFIG_FILE, data)

def get_guild_config(guild_id: int):
    data = load_config()
    gid = str(guild_id)

    if gid not in data:
        data[gid] = DEFAULT_GUILD_CONFIG.copy()
        save_config(data)
        return data[gid]

    changed = False
    for key, value in DEFAULT_GUILD_CONFIG.items():
        if key not in data[gid]:
            data[gid][key] = value
            changed = True

    if changed:
        save_config(data)

    return data[gid]

def update_guild_config(guild_id: int, key: str, value):
    data = load_config()
    gid = str(guild_id)

    if gid not in data:
        data[gid] = DEFAULT_GUILD_CONFIG.copy()

    data[gid][key] = value
    save_config(data)
