import pandas as pd
import random

def random_sample_csv(input_csv_path, num_lines, output_csv_path):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(input_csv_path)
        
        # Check if the number of lines to sample is greater than the total lines in the CSV
        if num_lines > len(df):
            raise ValueError("The number of lines to sample exceeds the total number of lines in the CSV file.")
        
        # Sample the specified number of lines
        sampled_df = df.sample(n=num_lines, random_state=random.randint(1, 10000))
        
        # Write the sampled lines to a new CSV file
        sampled_df.to_csv(output_csv_path, index=False)
        print(f"Successfully sampled {num_lines} lines from {input_csv_path} and saved to {output_csv_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_csv_path = 'data_labeled/ty_will_data/denial_delay_labels_formatted.csv'
num_lines = 50
output_csv_path = 'data_labeled/ty_will_data/random_clean_50.csv'

random_sample_csv(input_csv_path, num_lines, output_csv_path)
