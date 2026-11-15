# ETS2 – No Damage + No Passenger Dissatisfaction

**[Get it on the Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=3840637172)** (easiest way to install and stay updated)

A Euro Truck Simulator 2 mod for **1.62** that:

- keeps truck and trailer damage at **0%** (collision damage, mileage wear, cargo damage all zeroed, plus used-truck dealer offers spawn with no unfixable wear)
- keeps **bus passenger satisfaction** from ever dropping (every penalty zeroed: harsh acceleration, crashes, speeding, part wear, lateness, traffic offences; new passengers start at max; acceleration job-failure disabled). Requires the Bus DLC for the bus part.

## Install

Easiest: subscribe on the [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=3840637172).

Manual install:

1. Download [`dist/zzz_no_damage_no_dissatisfaction.scs`](dist/zzz_no_damage_no_dissatisfaction.scs)
2. Put it in `Documents/Euro Truck Simulator 2/mod/`
3. In-game: Mod Manager → enable **No Damage + No Passenger Dissatisfaction** and keep it at the top of the load order.
4. Repair your truck once at a service station: wear already in your save is not reset.

Don't enable other "No Damage" mods at the same time (they override the same `def/damage_data.sii`).

## Steam Workshop upload

`workshop/no_damage_bus_satisfaction/` is ready for the **SCS Workshop Uploader**
(`versions.sii` and a `content_162` package; `preview.jpg` sits next to the folder). Point the uploader at that folder and use `preview.jpg` as the preview image. Don't run the local `.scs` and the Workshop copy at the same time.

## What it changes

| File | Change |
|---|---|
| `def/damage_data.sii` | all damage coefficients and wear rates set to 0.0 |
| `def/bus_economy_data.sii` | all `satisfaction_*penalt*` set to 0, new-passenger satisfaction (1.0, 1.0), failure acceleration limit 999 |
| `def/used_vehicle_config.sii` | `truck_*_wear_unfixable_max` set to 0.0 |

Only the value fields changed; everything else matches the stock 1.62.3.3 files. Hired AI drivers' cargo damage is untouched.

## Rebuilding

`tools/build_mod.py` regenerates the mod from game definitions extracted with the official SCS extractor (paths inside the script are specific to my setup, so adjust them).

Compatible with game version `1.62.*`. Not affiliated with SCS Software.

## License

MIT for the build script and packaging. The `.sii` files are minimally edited copies of SCS Software game data.
