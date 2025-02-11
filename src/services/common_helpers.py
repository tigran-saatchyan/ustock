import math
import numpy as np

def format_currency(value):
    """
    Форматирует число в валютный формат.
    """
    try:
        return "${:,.2f}".format(value)
    except (TypeError, ValueError):
        return value


def convert_keys_to_str(obj):
    """
    Рекурсивно преобразует ключи в словарях в строки и заменяет числовые значения nan (как float, так и numpy.floating)
    на None. Если встречается numpy-массив, он преобразуется в список.
    """
    if isinstance(obj, dict):
        return {str(k): convert_keys_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_keys_to_str(item) for item in obj]
    elif isinstance(obj, np.ndarray):
        # Преобразуем массив в список и обрабатываем его
        return convert_keys_to_str(obj.tolist())
    elif isinstance(obj, (float, np.floating)):
        # Если значение nan, возвращаем None, иначе само значение
        return None if math.isnan(obj) else obj
    else:
        return obj