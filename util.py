def normalize_to_range(x, new_min=0, new_max=10):
    """
    normalized data into rnage 0 to 10
    """
    x_min, x_max = x.min(), x.max()
    return ((x - x_min) / (x_max - x_min)) * (new_max - new_min) + new_min
