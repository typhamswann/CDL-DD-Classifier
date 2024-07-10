import pandas as pd

class DataPrepper:
    def __init__(self):
        pass
    
    
    def mode_count(self, row):
        labels = [row['coder_0'], row['coder_1'], row['coder_2']]
        
        # Count occurrences of each label
        label_counts = pd.Series(labels).value_counts()
        
        # Find the maximum occurrence
        max_count = label_counts.max()
        
        # Find all labels with the maximum occurrence
        common_labels = label_counts[label_counts == max_count].index.tolist()
        
        # Return the mode count and the label(s) if the count is at least 2
        if max_count >= 2:
            return max_count, common_labels[0]  # Assuming you want the first if there are multiple modes
        return max_count, None

def transform_data(input_path: str, output_path: str):
    data_prepper = DataPrepper()
    
    # Load the input data
    tt_original_validation = pd.read_csv(input_path)
    
    # Transform the labels
    tt_original_validation["label"] = tt_original_validation["claim"]
    tt_original_validation = tt_original_validation[["text", "label"]]
    
    # Save the transformed data to the output path
    tt_original_validation.to_csv(output_path, index=False)

transform_data('data_labeled/think_tank/test.csv', 'data_labeled/think_tank/formatted_test.csv')
