from datetime import datetime

def split_file_by_pattern(input_file, pattern, output_prefix):
    with open(input_file, 'r') as file:
        file_count = 0
        output_file = None
        for line in file:
            # Check if the line matches the pattern
            if pattern in line:
                # Close the previous file if it's open
                if output_file:
                    output_file.close()

                # Increment file count and create a new file
                current_time = datetime.now()
                timestamp = current_time.strftime('%Y%m%d_%H%M%S_%f')
                output_filename = f"{output_prefix}_{timestamp}.txt"
                output_file = open(output_filename, 'w')
                file_count += 1
                
            # Write the line to the current output file
            if output_file:
                output_file.write(line)

        # Close the last file if it's open
        if output_file:
            output_file.close()

    print(f"Finished splitting {input_file} into {file_count} files.")

# Example usage
input_file = 'Source-Data-Corpus.txt'  # Replace with your input file
pattern = '---SPLIT---'              # Replace with your split pattern
output_prefix = 'tweets/GCC_X_'        # Prefix for the output files
split_file_by_pattern(input_file, pattern, output_prefix)

