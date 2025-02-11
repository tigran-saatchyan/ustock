import json
import math
import numpy as np
import pandas as pd
from rest_framework.renderers import JSONRenderer

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSONEncoder that replaces NaN values with None and converts pandas.Timestamp objects to strings.

    This encoder overrides the default method to handle specific data types:
      - Converts pandas.Timestamp objects to their string representation.
      - Replaces NaN values (for both float and numpy.floating types) with None.

    Args:
        obj (Any): The object to be encoded.

    Returns:
        A JSON-serializable representation of the object.
    """
    def default(self, obj):
        if isinstance(obj, pd.Timestamp):
            return str(obj)
        if isinstance(obj, (float, np.floating)):
            if math.isnan(obj):
                return None
        return super().default(obj)


class CustomJSONRenderer(JSONRenderer):
    """Renderer that uses the CustomJSONEncoder for JSON responses.

    This renderer converts the response data to JSON using the CustomJSONEncoder.
    By default, no indentation is applied and the output is encoded in UTF-8.

    Attributes:
        encoder_class (Type[json.JSONEncoder]): The JSON encoder class to use.
        indent (Optional[int]): Indentation level for the JSON output (default is None).
        charset (str): The output character set (default is 'utf-8').
    """
    encoder_class = CustomJSONEncoder
    indent = None  # Indentation is not used by default.
    charset = 'utf-8'  # The output charset is set to 'utf-8'.

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """Render `data` into JSON, returning a bytes object.

        Args:
            data (Any): The data to render. If None, returns an empty bytes object.
            accepted_media_type (Optional[str]): The accepted media type (not used).
            renderer_context (Optional[dict]): Additional context for rendering (not used).

        Returns:
            bytes: The JSON representation of `data`, encoded with the specified charset.
        """
        if data is None:
            return bytes()
        return json.dumps(
            data,
            cls=self.encoder_class,
            ensure_ascii=self.ensure_ascii,
            indent=self.indent
        ).encode(self.charset)
