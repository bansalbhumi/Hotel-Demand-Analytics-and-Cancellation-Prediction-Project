import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path: str) -> pd.DataFrame:
    """Loads the dataset from a given path."""
    logging.info(f"Loading data from {file_path}")
    return pd.read_csv(file_path)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the hotel bookings dataframe by handling missing values
    and removing invalid rows.
    """
    logging.info(f"Initial shape: {df.shape}")
    
    # 1. Handle missing values
    df['children'] = df['children'].fillna(0)
    df['country'] = df['country'].fillna('Unknown')
    df['agent'] = df['agent'].fillna(0)
    df['company'] = df['company'].fillna(0)
    
    # 2. Remove invalid rows
    # A booking must have at least 1 guest
    zero_guests = (df['adults'] + df['children'] + df['babies']) == 0
    df = df[~zero_guests].copy()
    
    logging.info(f"Shape after cleaning: {df.shape}")
    return df

def save_data(df: pd.DataFrame, output_path: str):
    """Saves the cleaned dataset to a given path."""
    logging.info(f"Saving cleaned data to {output_path}")
    df.to_csv(output_path, index=False)

import os

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_dir, "..", "data", "raw", "hotel_bookings.csv")
    output_path = os.path.join(current_dir, "..", "data", "processed", "hotel_bookings_cleaned.csv")
    
    df_raw = load_data(input_path)
    df_clean = clean_data(df_raw)
    save_data(df_clean, output_path)
    logging.info("Data cleaning completed successfully.")
