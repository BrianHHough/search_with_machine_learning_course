import pandas as pd

def count_category_query_pairs(file_path, output_file, threshold):
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

        # Count unique categories (labels)
        num_unique_categories = data['label'].nunique()
        print(f"Number of unique categories before pruning: {num_unique_categories}")

        # Group by label and query and count occurrences
        category_query_counts = data.groupby(['label', 'query']).size().reset_index(name='counts')
        
        # Prune the data by removing categories with counts below the threshold
        pruned_data = category_query_counts.groupby('label').filter(lambda x: x['counts'].sum() >= threshold)

        # Count unique categories after pruning
        num_unique_categories_after_pruning = pruned_data['label'].nunique()
        print(f"Number of unique categories after pruning: {num_unique_categories_after_pruning}")

        # Save to CSV
        pruned_data.to_csv(output_file, index=False)
        
        return pruned_data
        
    except Exception as e:
        print("Error reading file:", e)
        return None

# Parameters
file_path = '/workspace/datasets/fasttext/labeled_queries.txt'
output_file = '/workspace/datasets/fasttext/labeled_queries.txt'
# Save locally
# output_file = 'outputs/query_counts_pruned.csv'
threshold = 1000
pruned_data = count_category_query_pairs(file_path, output_file, threshold)
print(pruned_data)