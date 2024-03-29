"""
Validates whether the incoming data has an acceptable type and structure.

Edit this file to verify data expected by you module.
"""

import os
import re
from logging import getLogger

log = getLogger("validator")

REQUIRED_LABELS = []
if os.getenv("FORMULA"):
    for label in [x[2:-2] for x in re.findall("{{.*?}}", os.getenv("FORMULA"))]:
        REQUIRED_LABELS.append(label)
log.debug(f"Required labels: {REQUIRED_LABELS}")

def data_validation(data: any) -> str:
    """
    Validate incoming data i.e. by checking if it is of type dict or list.
    Function description should not be modified.

    Args:
        data (any): Data to validate.

    Returns:
        str: Error message if error is encountered. Otherwise returns None.

    """

    log.debug("Validating ...")

    try:
        allowed_data_types = [dict, list]

        if not type(data) in allowed_data_types:
            return f"Detected type: {type(data)} | Supported types: {allowed_data_types} | invalid!"

        if type(data) == list:
            for d in data:
                # check if all labels required in FORMULA are present in the received data
                missing_labels = set(REQUIRED_LABELS) - set(d.keys())
                if missing_labels:
                    return f"The following data labels included in mathematics FORMULA were not found in received data: {missing_labels}"


        else:
            # check if all labels required in FORMULA are present in the received data
            missing_labels = set(REQUIRED_LABELS) - set(data.keys())
            if missing_labels:
                return f"The following data labels included in mathematics FORMULA were not found in received data: {missing_labels}"

        return None

    except Exception as e:
        return f"Exception when validating module input data: {e}"
