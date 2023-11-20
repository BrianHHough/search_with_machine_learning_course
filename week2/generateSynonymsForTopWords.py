import fasttext
import argparse
import csv

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="Generate synonyms for the top words dataset using fastText")
parser.add_argument("--model", default='/workspace/datasets/fasttext/title_model.bin', help="Path to fastText model binary")
parser.add_argument("--input", default='/workspace/datasets/fasttext/top_words.txt', help="Path to list of words for fastText")
parser.add_argument("--output", default='/workspace/datasets/fasttext/synonyms.csv', help="Path to output synonym list for fastText")
parser.add_argument("--threshold", type=float, default=0.8, help="Similarity threshold for considering synonyms with fastText")
args = parser.parse_args()

# Load the FastText model
fasttext.FastText.eprint = lambda x: None
model = fasttext.load_model(args.model)

# Process each word and write synonyms to output file with fastText
with open(args.input, 'r') as infile, open(args.output, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    for word in infile:
        word = word.strip()
        synonyms = [word]  # Start with the word itself
        for similarity, synonym in model.get_nearest_neighbors(word):
            if similarity >= args.threshold:
                synonyms.append(synonym)
        writer.writerow(synonyms)


# WITHOUT ARGUMENTS AS INPUTS:
# Open the file containing the top words
# with open('/workspace/datasets/fasttext/top_words.txt', 'r') as file:
#     top_words = file.readlines()

# Threshold for similarity
# threshold = 0.8 # 0.75

# Open the output file
# with open('/workspace/datasets/fasttext/synonyms.csv', 'w') as output:
#     for word in top_words:
#         word = word.strip()
#         synonyms = model.get_nearest_neighbors(word)
#         # Filter synonyms based on the threshold and write to output
#         filtered_synonyms = [syn for sim, syn in synonyms if sim >= threshold]
#         output.write(f"{word},{' '.join(filtered_synonyms)}\n")
