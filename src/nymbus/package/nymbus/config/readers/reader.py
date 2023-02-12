from pathlib import Path

import yaml


def read_yml(path: Path) -> dict:
    # Read the bag file
    with open(path) as f:
        return yaml.load(f, Loader=yaml.SafeLoader) or {}


def merge_dictionaries(main_dict, new_dict, merging_lists=False):
    """ Merge two dictionaries prioritizing the second one """

    # Copy the dict
    main_dict = main_dict.copy()

    # Get all the keys
    main_keys = main_dict.keys()
    new_keys = new_dict.keys()
    keys = set(main_keys).union(new_keys)

    # For each key, merge the dict
    for key in keys:
        # If key is just in new, add it to main
        if key not in main_keys:
            main_dict[key] = new_dict[key]
        # If key is in both dicts, and...
        elif key in new_keys:
            # ...the values are dicts, merge them recursively
            if isinstance(main_dict[key], dict) and isinstance(new_dict[key], dict):
                main_dict[key] = merge_dictionaries(main_dict[key], new_dict[key], merging_lists=merging_lists)
            # ...the value is NOT a dict in both cases, override the main value
            else:
                # If merging lists is True, and values are lists, concatenate the elements
                if merging_lists and isinstance(main_dict[key], list) and isinstance(new_dict[key], list):
                    main_dict[key] = main_dict[key] + new_dict[key]
                # Override them otherwise
                else:
                    main_dict[key] = new_dict[key]
        # If key is just in main, nothing to do: just keep main_dict as it is

    return main_dict
