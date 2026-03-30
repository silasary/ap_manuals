# Pokemon Red and Blue Signsanity Sidecar

I was recently asked it if was possible to make a Manual that can be played alongside a full game implementation.

This manual is an example of such a thing.

Right now, it is entirely a proof-of-concept, and does not contain every sign in the game.

## How does it work?

Play this alongside a regular Pokemon Red and Blue slot, and read all the signs as you explore the world.

## Okay, but how does it *work*?

Oh, you want the technical explanation.

We've got a few hooks here.

The most important one* is [Data.after_load_region_file](./hooks/Data.py#L26).  This goes through `worlds.pokemon_rb.regions.map_ids`, and makes a corresponding region for each Pokemon region.  It then sets an access requirement with the custom rule `{MainGameCanReachRegion(region_name)}`.

Which brings us to our requirement functions.

`{MainGameCanReachRegion(region_name)}`, `{MainGameCanReachLocation(location_name)}`, and `{MainGameHas(item_name [,count])}` all do very simple things.

They peek into the slot defined by the `slot:` yaml setting, and check its current accessibility.

## Notes for people adapting this to other games

The region hook is by far the easiest way to clone Pokemon's regions.  But if your games' regions aren't easily introspectable, it's entirely fine to create the file by hand.

Your regions should look like this:
```json
{
    "Pallet Town": {
        "requires": "{MainGameCanReachRegion(Pallet Town)}"
    }
}
```

Because you're leaning on accessibility from the main game, you do not need to worry about connections.  Just leave everything as accessible from the start, and let CanReach do the heavy lifting.

