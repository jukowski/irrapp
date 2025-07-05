import re
import pandas as pd

def clean_column_names(df):
    """
    Renames DataFrame columns to lowercase and removes special characters.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame
    
    Returns:
    pd.DataFrame: DataFrame with cleaned column names
    """
    df = df.copy()
    new_columns = []
    for col in df.columns:
        # Convert to lowercase
        new_col = col.lower()
        # Replace spaces and special characters with underscores
        new_col = re.sub(r'\W+', '_', new_col)
        # Remove leading/trailing underscores
        new_col = new_col.strip('_')
        new_columns.append(new_col)
    df.columns = new_columns
    return df

def disassemble_json(p):
    keys = ['Genre', 'MediaType', 'Artist', 'Album', 'Track', 'Employee',
            'Customer', 'Invoice', 'InvoiceLine', 'Playlist', 'PlaylistTrack']
    return [
        pd.DataFrame(p[k])
        for k in keys
    ]
