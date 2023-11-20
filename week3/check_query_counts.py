import pandas as pd

def count_category_query_pairs(file_path, output_file):
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

        # Group by label and query and count occurrences
        category_query_counts = data.groupby(['label', 'query']).size().reset_index(name='counts')
        
        # Save to CSV
        category_query_counts.to_csv(output_file, index=False)
        
        return category_query_counts
        
    except Exception as e:
        print("Error reading file:", e)
        return None

# Parameters
file_path = '/workspace/datasets/fasttext/labeled_queries.txt'
output_file = 'query_counts.csv'
category_query_counts = count_category_query_pairs(file_path, output_file)
print(category_query_counts)
