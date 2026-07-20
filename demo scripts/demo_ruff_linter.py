import os, sys
import math
from pathlib import Path


def greet(name:str="world"):
    message =  f"Hello, {name}"
    unused_value = 123
    print(message )


def compute_total(items):
    total=0
    for item in items:
        total += item
    return total


def read_config():
    config_path = Path("config.json")
    if config_path.exists():
        return config_path.read_text()
    return None


def show_result():
    values = [1,2,3]
    result = compute_total(values)
    print(  "Total:", result)
    print(missing_name)


if __name__=="__main__":
    greet("Fedora")
    show_result()
    