from typing import Any, Dict, List


def flatten_json(nested_json: Dict[str, Any], separator: str = '.') -> Dict[str, Any]:
    """
    Flatten a nested JSON object while keeping keys in camelCase and using a distinct separator for nested keys.
    
    Parameters:
        nested_json (Dict[str, Any]): The JSON object to flatten.
        separator (str): The separator used to denote nesting in the keys.
    
    Returns:
        Dict[str, Any]: A dictionary with flattened keys.
    """
    flattened_dict = {}

    def flatten(current_element: Any, key_prefix: str = '') -> None:
        """
        Recursively flattens the JSON object.
        
        Parameters:
            current_element (Any): Current element to be flattened.
            key_prefix (str): Accumulated key formed from nested dictionary keys.
        """
        if isinstance(current_element, dict):
            for key, value in current_element.items():
                flatten(value, key_prefix + key + separator)
        elif isinstance(current_element, list):
            for index, item in enumerate(current_element):
                flatten(item, key_prefix + str(index) + separator)
        else:
            flattened_dict[key_prefix.rstrip(separator)] = current_element

    flatten(nested_json)
    return flattened_dict


def flatten_list_of_dicts(list_of_dicts: List[Dict[str, Any]], separator: str = '.') -> List[Dict[str, Any]]:
    """
    Flattens a list of nested JSON-like dictionaries, applying the flatten_json function to each dictionary.

    Parameters:
        list_of_dicts (List[Dict[str, Any]]): A list of dictionaries to be flattened.
        separator (str): The separator used to denote nesting in the keys, passed to flatten_json.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries where each dictionary has been flattened.
    """
    flattened_dicts = []
    for nested_dict in list_of_dicts:
        flattened_dict = flatten_json(nested_dict, separator)
        flattened_dicts.append(flattened_dict)
    return flattened_dicts


def add_key_value_to_dicts(dicts_list: List[Dict[str, Any]], key: str, value: Any) -> List[Dict[str, Any]]:
    """
    Adds a key-value pair to each dictionary in the list at the first level.

    :param dicts_list: List of dictionaries to update.
    :param key: The key to add to each dictionary.
    :param value: The value to associate with the key.
    :return: The list of updated dictionaries.
    """
    if not isinstance(dicts_list, list):
        raise ValueError("The first argument must be a list of dictionaries.")
    
    for dictionary in dicts_list:
        if not isinstance(dictionary, dict):
            raise ValueError("All elements in the list must be dictionaries.")
        dictionary[key] = value

    return dicts_list


def flatten_graphql_fields(field_str: str, parent_key: str = '', separator: str = '.') -> List[str]:
    """
    Recursively flattens a nested GraphQL fields string into a list of dot-separated field paths.

    Parameters:
        field_str (str): The string representing nested GraphQL fields.
        parent_key (str): The base path for the current level of fields. Used during recursion.
        separator (str): The separator used to denote nesting in the field paths.

    Returns:
        List[str]: A list of flattened field paths.

    Raises:
        ValueError: If there are unbalanced braces in the input string.
    """
    flattened_fields = []

    def recurse(fields: str, parent_key: str) -> None:
        """
        Helper function to recursively flatten the nested fields.

        Parameters:
            fields (str): The string of fields to process.
            parent_key (str): The base path for the current level of fields.

        Raises:
            ValueError: If there are unbalanced braces in the input string.
        """
        i = 0
        n = len(fields)
        while i < n:
            if fields[i] == '{':
                i += 1
                nested_fields = ""
                brace_count = 1

                # Collect nested fields.
                while i < n and brace_count > 0:
                    if fields[i] == '{':
                        brace_count += 1
                    elif fields[i] == '}':
                        brace_count -= 1
                    if brace_count > 0:
                        nested_fields += fields[i]
                    i += 1

                if brace_count != 0:
                    raise ValueError("Unbalanced braces in input string")

                # Recurse into nested fields.
                recurse(nested_fields, parent_key)
            else:
                # Collect field name.
                field_name = ""
                while i < n and fields[i] not in ('{', '}'):
                    field_name += fields[i]
                    i += 1
                field_name = field_name.strip()

                if field_name:
                    key = f"{parent_key}{separator}{field_name}" if parent_key else field_name
                    flattened_fields.append(key)

    recurse(field_str, parent_key)
    return flattened_fields