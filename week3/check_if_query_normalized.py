import pandas as pd
import re
import nltk
stemmer = nltk.stem.PorterStemmer()

# Function to normalize a query
def normalize_query(query):
    if query is None:
        return ''
    query = query.lower()
    query = re.sub('[^a-z0-9]', ' ', query)
    query = re.sub(' +', ' ', query)
    query = ' '.join([stemmer.stem(word) for word in query.split()])
    return query

# Load and process the output file
output_df = pd.read_csv('/workspace/datasets/fasttext/labeled_queries.txt', sep='\|', engine='python', names=['label_query'], header=None)
output_df['label_query'] = output_df['label_query'].str.strip()  # Remove any leading/trailing whitespace
output_df[['label', 'query']] = output_df['label_query'].str.split(' ', n=1, expand=True)

# Define the original and expected normalized query
original_query = "Beats By Dr. Dre- Monster Pro Over-the-Ear Headphones -"
normalized_original_query = normalize_query(original_query)

# Check if the specific query is normalized correctly
contains_query = output_df['query'].apply(lambda x: normalize_query(x) if pd.notnull(x) else '').str.contains(normalized_original_query, regex=False)
is_normalized = contains_query.any()

print("Query normalized correctly in labeled_queries.txt:", is_normalized)
print("Original Query:", original_query)
print("Normalized Query:", normalized_original_query)