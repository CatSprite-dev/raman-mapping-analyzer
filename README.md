# raman-mapping-analyzer

## Description

A CLI tool for automated mineral identification from Raman mapping data. For each point in the map, the script removes the baseline, normalizes and smooths the spectrum, then compares it against a library of reference mineral spectra using Pearson correlation. The result is a summary of how many points match each mineral.

I’m specifically referring to minerals because I use the script to analyze heavy-fraction minerals, but in reality, it can be used to analyze the mapping of any materials. All that’s required is the map itself and the corresponding library of reference spectra.

## Motivation

Manual processing of large Raman maps is extremely time-consuming — a single map can contain thousands of spectra. This tool automates the entire pipeline so that analysis which would take hours by hand is done in seconds.

## Quick Start

1. Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/CatSprite-dev/raman-mapping-analyzer.git
cd raman-mapping-analyzer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Create a `.env` file in the project root:

```
MAP_PATH=path/to/your/map.txt
LIBRARY_PATH=path/to/your/library/folder
```

3. Run:

```bash
python3 main.py
```

## Usage

### Input

- **Map file** — a CSV or TSV file with columns `#X`, `Y`, `#Y` (wavenumber), `I` (intensity)
- **Library folder** — a directory containing reference spectrum files against which comparisons will be made, with one file per mineral. The name of each file must begin with the name of the mineral to which the spectrum in that file corresponds, for example, Quartz__R050125-3__Raman__514__.txt.

### Output

```
===| path/to/map.txt |===

Total spectra = 1640
Epidote - 113
Hematite - 207
Quartz - 4
...
```

### Matching threshold

A mineral is assigned to a point if the Pearson correlation coefficient with its reference spectrum exceeds **0.50**. If multiple minerals match, the one with the highest correlation is selected.