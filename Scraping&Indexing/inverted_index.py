import sys
import os
import re
from collections import defaultdict

class InvertedIndex:
    def _init_(self):
        self.input_path = None
        self.output_path = None
        self.word_file_counts = defaultdict(lambda: defaultdict(int))
        
    def set_paths(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
    
    def clean_and_split_word(self, word):
        """Filter out non-alphanumeric chars and split by underscore"""
        # First remove all non-alphanumeric/underscore characters
        cleaned = re.sub(r'[^a-zA-Z0-9_]', '', word)
        # Then split by underscore and filter empty strings
        return [part.lower() for part in cleaned.split('_') if part]
    
    def mapper(self):
        """Process input files and emit word@filename with count 1"""
        for filename in os.listdir(self.input_path):
            filepath = os.path.join(self.input_path, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        for word in line.split():
                            for cleaned_part in self.clean_and_split_word(word):
                                key = f"{cleaned_part}@{os.path.splitext(filename)[0]}"
                                yield (key, 1)
    
    # [Rest of the methods remain the same as previous version...]
    def combiner(self, mapper_output):
        """Combine counts for same word@filename pairs"""
        combined = defaultdict(int)
        for key, count in mapper_output:
            combined[key] += count
        return combined.items()
    
    def reducer(self, combiner_output):
        """Group by word and collect all filename:count pairs"""
        word_index = defaultdict(list)
        for key, count in combiner_output:
            word, filename = key.split('@')
            word_index[word].append(f"{filename}:{count}")
        return word_index
    
    def run(self):
        """Execute the full inverted index pipeline"""
        # Mapper phase
        mapper_out = self.mapper()
        
        # Combiner phase
        combiner_out = self.combiner(mapper_out)
        
        # Reducer phase
        reducer_out = self.reducer(combiner_out)
        
        # Write output
        os.makedirs(self.output_path, exist_ok=True)
        output_file = os.path.join(self.output_path, 'inverted_index.txt')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for word in sorted(reducer_out.keys()):
                files_str = ";".join(sorted(reducer_out[word]))
                f.write(f"{word}\t{files_str}\n")
        
        print(f"Inverted index created at: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python inverted_index.py <input_dir> <output_dir>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    # Verify input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist")
        sys.exit(1)
    
    # Clear output directory if it exists
    if os.path.exists(output_dir):
        for f in os.listdir(output_dir):
            os.remove(os.path.join(output_dir, f))
    else:
        os.makedirs(output_dir)
    
    # Run the inverted index process
    try:
        indexer = InvertedIndex()
        indexer.set_paths(input_dir, output_dir)
        indexer.run()
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        sys.exit(1)