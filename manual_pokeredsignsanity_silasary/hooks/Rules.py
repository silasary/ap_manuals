from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value
from BaseClasses import MultiWorld, CollectionState

import re

def MainGameCanReachRegion(world: World, state: CollectionState, region_name: str) -> bool:
    return state.can_reach_region(region_name, world.attached_slot)

def MainGameCanReachLocation(world: World, state: CollectionState, location_name: str) -> bool:
    return state.can_reach_location(location_name, world.attached_slot)

def MainGameHas(world: World, state: CollectionState, item_name: str, count: Optional[int] = None) -> bool:
    if not count:
        count = 1

    return state.has(item_name, world.attached_slot, count)
