import math
import json
import numpy as np

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def describe(self):
        return f"A circle with radius {self.radius} has area {self.area():.2f}"

def main():
    c = Circle(5)
    print(c.describe())

    array = np.arange(10)
    squared = array ** 2
    stats = {
        "mean": np.mean(squared).item(),
        "sum": np.sum(squared).item()
    }

    data = {
        "description": c.describe(),
        "stats": stats,
        "squared_list": squared.tolist()
    }

    return data
