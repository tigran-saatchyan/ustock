import json
import math
import numpy as np
import pandas as pd
from rest_framework.renderers import JSONRenderer

class CustomJSONEncoder(json.JSONEncoder):
    """
    Кастомный JSONEncoder, который заменяет все значения nan (как float, так и numpy.floating)
    на None и конвертирует pandas.Timestamp в строку.
    """
    def default(self, obj):
        if isinstance(obj, pd.Timestamp):
            return str(obj)
        if isinstance(obj, (float, np.floating)):
            if math.isnan(obj):
                return None
        return super().default(obj)

class CustomJSONRenderer(JSONRenderer):
    """
    Рендерер, использующий кастомный JSONEncoder.
    """
    encoder_class = CustomJSONEncoder
    indent = None  # Отступы не используются по умолчанию
    charset = 'utf-8'  # Обязательно задаём кодировку

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return bytes()
        return json.dumps(
            data,
            cls=self.encoder_class,
            ensure_ascii=self.ensure_ascii,
            indent=self.indent
        ).encode(self.charset)
