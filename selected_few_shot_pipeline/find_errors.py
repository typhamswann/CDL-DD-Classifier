import pandas as pd

def filter_incorrect_claims(input_csv_path: str, output_csv_path: str) -> None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv_path)

    # Filter rows where human_label does not match llm_label
    incorrect_claims_df = df[df['human_label'] != df['llm_label']]

    # Save the filtered DataFrame to a new CSV file
    incorrect_claims_df.to_csv(output_csv_path, index=False)

filter_incorrect_claims('selected_few_shot_pipeline/results.csv', 'selected_few_shot_pipeline/errors.csv')
