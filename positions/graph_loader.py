"""Load position graphs from JSON files and build SpritePosition objects."""
import json
import os

from positions.SpritePosition import SpritePosition

LINK_ATTRS = ["next_move", "left_move", "right_move", "up_move", "down_move", "jump_move"]


def load_position_graph(actor_type):
    """Load a position graph from JSON and return {name: SpritePosition}.

    Each position in the JSON may have:
      - Link attributes (next_move, left_move, etc.) referencing other position names
      - eater_name: cross-type collision reference (not validated here)
      - sprite_name: override for the image file name (e.g. K02b uses K02 sprite)
    """
    json_path = os.path.join("positions", "graphs", f"{actor_type}.json")
    with open(json_path, "r") as f:
        data = json.load(f)

    graph_actor_type = data["actor_type"]

    # Phase 1: Create all SpritePosition objects
    positions = {}
    for name, links in data["positions"].items():
        sprite_name = links.get("sprite_name", name)
        positions[name] = SpritePosition(sprite_name, graph_actor_type)

    # Phase 2: Wire graph links
    for name, links in data["positions"].items():
        sp = positions[name]
        for attr in LINK_ATTRS:
            target = links.get(attr)
            if target is not None:
                if target not in positions:
                    raise ValueError(
                        f"{actor_type}: {name}.{attr} references unknown position '{target}'"
                    )
                setattr(sp, attr, target)
        if "eater_name" in links:
            sp.eater_name = links["eater_name"]

    return positions
