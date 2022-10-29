"""
This file implements module's main logic.
Data processing should happen here.

Edit this file to implement your module.
"""

import os
import re
from logging import getLogger
from .tokens import generateTokens
from .calculate import evaluateRPN

log = getLogger("module")

__RESULT_LABEL__ = os.getenv("RESULT_LABEL", "defaultLabel")
__NEW_RESULT__ = os.getenv("NEW_RESULT", "stand-alone")

TOKENS, tokensError = generateTokens()
if tokensError:
    log.error(tokensError)

def module_main(received_data: any) -> [any, str]:
    """
    Process received data by implementing module's main logic.
    Function description should not be modified.

    Args:
        received_data (any): Data received by module and validated.

    Returns:
        any: Processed data that are ready to be sent to the next module or None if error occurs.
        str: Error message if error occurred, otherwise None.

    """

    log.debug("Processing ...")

    try:
        global TOKENS

        # find labeled data in TOKENS and emplace their values from received_data
        for i in range(len(TOKENS)):
            if re.search("{{.*?}}", TOKENS[i]):
                # its a label so emplace value
                TOKENS[i] = received_data[TOKENS[i][2:-2]]

        calculation_result = evaluateRPN(TOKENS)

        if __NEW_RESULT__ == "update" or __NEW_RESULT__ == "append":
            received_data[__RESULT_LABEL__] = calculation_result
        elif __NEW_RESULT__ == "stand-alone":
            received_data = {
                __RESULT_LABEL__: calculation_result
            }

        return received_data, None

    except Exception as e:
        return None, f"Exception in the module business logic: {e}"
