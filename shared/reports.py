import requests
from typing import Union, Dict, List, Any


def get_report(url: str, params: dict = None) -> Union[Dict[str, Any], List[Any]]:
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()