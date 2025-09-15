from typing import List, Optional

VIALRGB_EFFECT_SKIP = 0xFFFF

vial_effects: List[List[str]] = [
    ["VIALRGB_EFFECT_OFF", "OFF"],
    ["VIALRGB_EFFECT_DIRECT", "Direct"],
    ["VIALRGB_EFFECT_SOLID_COLOR", "Solid Color"],
    ["VIALRGB_EFFECT_ALPHAS_MODS", "Alphas Mods"],
    ["VIALRGB_EFFECT_GRADIENT_UP_DOWN", "Gradient Up Down"],
    ["VIALRGB_EFFECT_GRADIENT_LEFT_RIGHT", "Gradient Left Right"],
    ["VIALRGB_EFFECT_BREATHING", "Breathing"],
    ["VIALRGB_EFFECT_BAND_SAT", "Band Sat"],
    ["VIALRGB_EFFECT_BAND_VAL", "Band Val"],
    ["VIALRGB_EFFECT_BAND_PINWHEEL_SAT", "Band Pinwheel Sat"],
    ["VIALRGB_EFFECT_BAND_PINWHEEL_VAL", "Band Pinwheel Val"],
    ["VIALRGB_EFFECT_BAND_SPIRAL_SAT", "Band Spiral Sat"],
    ["VIALRGB_EFFECT_BAND_SPIRAL_VAL", "Band Spiral Val"],
    ["VIALRGB_EFFECT_CYCLE_ALL", "Cycle All"],
    ["VIALRGB_EFFECT_CYCLE_LEFT_RIGHT", "Cycle Left Right"],
    ["VIALRGB_EFFECT_CYCLE_UP_DOWN", "Cycle Up Down"],
    ["VIALRGB_EFFECT_RAINBOW_MOVING_CHEVRON", "Rainbow Moving Chevron"],
    ["VIALRGB_EFFECT_CYCLE_OUT_IN", "Cycle Out In"],
    ["VIALRGB_EFFECT_CYCLE_OUT_IN_DUAL", "Cycle Out In Dual"],
    ["VIALRGB_EFFECT_CYCLE_PINWHEEL", "Cycle Pinwheel"],
    ["VIALRGB_EFFECT_CYCLE_SPIRAL", "Cycle Spiral"],
    ["VIALRGB_EFFECT_DUAL_BEACON", "Dual Beacon"],
    ["VIALRGB_EFFECT_RAINBOW_BEACON", "Rainbow Beacon"],
    ["VIALRGB_EFFECT_RAINBOW_PINWHEELS", "Rainbow Pinwheels"],
    ["VIALRGB_EFFECT_RAINDROPS", "Raindrops"],
    ["VIALRGB_EFFECT_JELLYBEAN_RAINDROPS", "Jellybean Raindrops"],
    ["VIALRGB_EFFECT_HUE_BREATHING", "Hue Breathing"],
    ["VIALRGB_EFFECT_HUE_PENDULUM", "Hue Pendulum"],
    ["VIALRGB_EFFECT_HUE_WAVE", "Hue Wave"],
    ["VIALRGB_EFFECT_TYPING_HEATMAP", "Typing Heatmap"],
    ["VIALRGB_EFFECT_DIGITAL_RAIN", "Digital Rain"],
    ["VIALRGB_EFFECT_SOLID_REACTIVE_SIMPLE", "Solid Reactive Simple"],
    ["VIALRGB_EFFECT_SOLID_REACTIVE", "Solid Reactive"],
    ["VIALRGB_EFFECT_SOLID_REACTIVE_WIDE", "Solid Reactive Wide"],
    ["VIALRGB_EFFECT_SOLID_REACTIVE_MULTIWIDE", "Solid Reactive Multiwide"],
    ["VIALRGB_EFFECT_SOLID_REACTIVE_CROSS", "Solid Reactive Cross"],
    ["VIALRGB_EFFECT_SOLID_REACTIVE_MULTICROSS", "Solid Reactive Multicross"],
    ["VIALRGB_EFFECT_SOLID_REACTIVE_NEXUS", "Solid Reactive Nexus"],
    ["VIALRGB_EFFECT_SOLID_REACTIVE_MULTINEXUS", "Solid Reactive Multinexus"],
    ["VIALRGB_EFFECT_SPLASH", "Splash"],
    ["VIALRGB_EFFECT_MULTISPLASH", "Multisplash"],
    ["VIALRGB_EFFECT_SOLID_SPLASH", "Solid Splash"],
    ["VIALRGB_EFFECT_SOLID_MULTISPLASH", "Solid Multisplash"],
    ["VIALRGB_EFFECT_PIXEL_RAIN", "Pixel Rain"],
    ["VIALRGB_EFFECT_PIXEL_FRACTAL", "Pixel Fractal"]
]

def get_vial_effect_id(effect_name: str) -> Optional[int]:
    """Get the Vial effect ID for a given effect name.
    
    Args:
        effect_name: Effect name to search for (case-insensitive)
        
    Returns:
        Effect ID (integer) if found, None if not found
    """
    effect_simple_name = effect_name.strip().lower().replace("_", " ")
    for idx, effect_strs in enumerate(vial_effects):
        if effect_simple_name in [
            e.lower().replace("_", " ") for e in effect_strs
        ]:
            return idx
    if effect_simple_name in ["vialrgb effect skip","skip"]:
        return VIALRGB_EFFECT_SKIP
    return None

def get_vial_effect_name(effect_id: int, pretty_name: bool = True) -> Optional[str]:
    """Get the Vial effect name for a given effect id.
    
    Args:
        effect_id: Effect ID to look up
        pretty_name: If True, return human-readable name; 
                    if False, return internal constant name
                    
    Returns:
        Effect name string if valid ID, None if invalid
    """
    if effect_id < len(vial_effects):
        if pretty_name == True:
            return vial_effects[effect_id][1]
        else:
            return vial_effects[effect_id][0]
    else:
        return None

def all_vial_effects() -> List[str]:
    """Get a list of all Vial effect names.
    
    Returns:
        List of effect names
    """
    return vial_effects.append(["VIALRGB_EFFECT_SKIP","Skip"])