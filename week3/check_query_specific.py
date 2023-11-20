import pandas as pd

def count_specific_label(file_path, label):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Split each line into label and query
        labels, queries = [], []
        for line in lines:
            split_line = line.strip().split(' ', 1)
            labels.append(split_line[0])
            queries.append(split_line[1] if len(split_line) > 1 else '')

        # Create DataFrame
        data = pd.DataFrame({'label': labels, 'query': queries})

        # Count occurrences of the specific label
        label_count = data[data['label'] == label].shape[0]
        return label_count
    except Exception as e:
        print("Error reading file:", e)
        return None

# Example usage
file_path = '/workspace/datasets/fasttext/labeled_queries.txt'
specific_label = '__label__abcat0701001'  # Label for XBox 360 Consoles
label_count = count_specific_label(file_path, specific_label)
print(f"Count for {specific_label} (XBox 360 Consoles):", label_count)
