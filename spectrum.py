import numpy as np
from file_io import detect_separator

class Spectrum():
    def __init__(self, path):
        self.path = path
        delimiter = detect_separator(path)
        self.spectrum = np.genfromtxt(self.path, skip_header=10, delimiter=delimiter)
        self.x = self.spectrum[:, 0]
        self.y = self.spectrum[:, 1]
        self.name = ""

