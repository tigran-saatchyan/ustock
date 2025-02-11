import math
import numpy as np

def format_currency(value):
    """Formats a number into a currency string.

    Args:
        value (float): The numeric value to format.

    Returns:
        str: A string representing the value in US dollar format (e.g. "$1,234.56").
             If the value cannot be formatted due to a type or value error, returns the original value.
    """
    try:
        return "${:,.2f}".format(value)
    except (TypeError, ValueError):
        return value


def convert_keys_to_str(obj):
    """Recursively converts dictionary keys to strings and replaces NaN values with None.

    This function traverses the input object and:
      - If the object is a dictionary, converts its keys to strings and processes its values recursively.
      - If the object is a list, processes each element recursively.
      - If the object is a numpy array, converts it to a list and processes it recursively.
      - If the object is a float (or numpy floating), returns None if it is NaN, otherwise returns the value.
      - Otherwise, returns the object unchanged.

    Args:
        obj (Any): The input object (can be a dict, list, numpy array, or numeric value).

    Returns:
        Any: The transformed object with keys as strings and NaN values replaced by None.
    """
    if isinstance(obj, dict):
        return {str(k): convert_keys_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_keys_to_str(item) for item in obj]
    elif isinstance(obj, np.ndarray):
        # Convert numpy array to list and process it
        return convert_keys_to_str(obj.tolist())
    elif isinstance(obj, (float, np.floating)):
        # Return None if the value is NaN, otherwise return the value
        return None if math.isnan(obj) else obj
    else:
        return obj
