import pandas as pd

def detect_separator(file_path: str) -> str:
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("#") == False:
                if "\t" in line:
                    return "\t"
                if "," in line:
                    return ","
                
def validate_dataframe_of_map(df: pd.DataFrame) -> pd.DataFrame:
    new_columns = {"#X": "X", 
                   "Unnamed: 1": "Y",
                   "#Y": "W",
                   "Unnamed: 3": "I"}
    df = df.rename(columns=new_columns)
    return df.dropna(axis=1, how='all')