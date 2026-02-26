import json
import os
from typing import Union

FixtureDataType = Union[list, dict]


def get_fixture_path(file_name: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(current_dir, "fixtures", file_name)


def read(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        
    return content


def get_fixture_data(file_name: str) -> FixtureDataType:
    content = read(get_fixture_path(file_name))
    
    return json.loads(content)


def get_test_data() -> FixtureDataType:
    return get_fixture_data("test_data.json")
