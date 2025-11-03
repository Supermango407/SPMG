def lerp(a:float, b:float, v:float) -> float:
    """linear interpolation between `a`, and `b`, given `v`."""
    return a + (b - a) * v