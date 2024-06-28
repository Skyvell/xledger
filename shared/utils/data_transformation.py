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


def flatten_graphql_fields(input: str, separator: str = ".") -> List[str]:
    """
    Extracts hierarchical field names from a structured string input.

    Args:
        input (str): The structured string input containing fields and braces to denote hierarchy.
        separator (str): The custom separator to use for nested fields. Defaults to ".".

    Returns:
        list: A list of extracted field names with hierarchy indicated by the custom separator.

    Example:
        input = '''
        user {
            id
            name {
                first
                last
            }
            email
        }
        '''
        flatten_graphql_fields(input) returns:
        ['user.id', 'user.name.first', 'user.name.last', 'user.email']

        flatten_graphql_fields(input, separator="/") returns:
        ['user/id', 'user/name/first', 'user/name/last', 'user/email']

    Limitations:
        - Does only support node structure in its most simple form. Only fields and nested fields are supported.
        - Must follow the exaxt formatting shown in the example.
        - Empty lines are supported.
    """
    # Split the input string into lines and strip any leading/trailing whitespace.
    lines = input.strip().split("\n")

    fields = []
    stack = []

    for line in lines:
        line = line.strip()
        if not line:
            # Skip empty lines.
            continue
        if line.endswith("{"):
            # If the line ends with '{', it's a base for nested fields.
            base = line.split("{")[0].strip()
            if stack:
                # If there's an existing hierarchy, prepend it to the base.
                base = f"{stack[-1]}{separator}{base}"
            stack.append(base)
        elif line == "}":
            # If the line is '}', it indicates the end of a nested block.
            stack.pop()
        else:
            # Otherwise, it's a field name.
            field = line.split()[0]
            if stack:
                # If there's an existing hierarchy, prepend it to the field.
                fields.append(f"{stack[-1]}{separator}{field}")
            else:
                fields.append(field)

    return fields