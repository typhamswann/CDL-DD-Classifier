import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, cohen_kappa_score

def calculate_metrics(csv_filepath):
    # Load the CSV file
    df = pd.read_csv(csv_filepath)
    
    # Extract the columns
    human_labels = df['category_2']
    llm_labels = df['llm_label']
    
    # Calculate the metrics
    precision = precision_score(human_labels, llm_labels, average='weighted')
    recall = recall_score(human_labels, llm_labels, average='weighted')
    f1 = f1_score(human_labels, llm_labels, average='weighted')
    accuracy = accuracy_score(human_labels, llm_labels)
    kappa = cohen_kappa_score(human_labels, llm_labels)

    
    # Print the metrics
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1:.2f}")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Intercoder Reliability (Cohen's Kappa): {kappa:.2f}")


# Example usage
csv_filepath = 'selected_few_shot_pipeline/results_split_150.csv'
calculate_metrics(csv_filepath)
