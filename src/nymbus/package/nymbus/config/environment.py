import logging
import os
import re

logger = logging.getLogger(__name__)

DEFAULT_ENVIRONMENT = "default"
NYMBUS_FOLDER = ".nymbus"
NYMBUS_OUTPUT_FOLDER = f"{NYMBUS_FOLDER}/output"
DEFAULT_NYMBUS_EXTENSION = ".nymbus.yml"
DEFAULT_ENVIRONMENT_FILE = f"{DEFAULT_ENVIRONMENT}{DEFAULT_NYMBUS_EXTENSION}"
VARIABLE_EXPANSION = re.compile(r"^\$\{([^}]+)}$")


def expand_variable(value: str):

    # Check if the value is in the form ${<name>}
    match = VARIABLE_EXPANSION.match(value)
    if not match:
        return value
    else:
        # Get the value corresponding to the variable with name <name>
        variable_name = match.group(1)
        variable_value = os.environ.get(variable_name, None)
        if variable_value is None:
            logger.warning(f"Variable {variable_name} is not set.")
            variable_value = ""
        return variable_value
