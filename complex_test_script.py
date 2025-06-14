import math
import json
import numpy as np
import os
import pandas as pd

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def describe(self):
        return f"A circle with radius {self.radius} has area {self.area():.2f}"

def main():
    arr = np.array([1,2,3])
    array = np.arange(10)
    squared = array ** 2
    stats = {
        "mean": float(np.mean(squared)),
        "sum": int(np.sum(squared))
    }
    print("Array!")
    return {
        "arr_sum": int(np.sum(arr)),
        "squared_sum": int(np.sum(squared)),
        "squared_mean": float(np.mean(squared)),
        "df_rows": 3,
        "df_cols": 1
    }
