import json
import os
from copy import deepcopy
from typing import Any

CONFIG_FILE = "config.json"

DEFAULT_GUILD_CONFIG = {
    "language": "en",
    "welcome_channel_id": None,
    "goodbye_channel_id": None,
    "log_channel_id": None,
    "autorole_id": None,
    "ticket_category_id": None,
    "support_role_id": None,
    "youtube_channel_url": None,
    "youtube_post_channel_id": None,
    "youtube_last_video_url": None,
    "dm_welcome_enabled": True,
}

def ensure_file() -> None:
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2, ensure_ascii=False)

def load_config() -> dict[str, Any]:
    ensure_file()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}

def save_config(data: dict[str, Any]) -> None:
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_guild_config(guild_id: int) -> dict[str, Any]:
    data = load_config()
    gid = str(guild_id)

    if gid not in data:
        data[gid] = deepcopy(DEFAULT_GUILD_CONFIG)
        save_config(data)
        return data[gid]

    changed = False
    for key, value in DEFAULT_GUILD_CONFIG.items():
        if key not in data[gid]:
            data[gid][key] = deepcopy(value)
            changed = True

    if changed:
        save_config(data)

    return data[gid]

def update_guild_config(guild_id: int, key: str, value: Any) -> None:
    data = load_config()
    gid = str(guild_id)

    if gid not in data:
        data[gid] = deepcopy(DEFAULT_GUILD_CONFIG)

    data[gid][key] = value
    save_config(data)
