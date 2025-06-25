#This file turns a csv into a latex table. 

# prints the table in stdout.

import csv
import os
import sys

def csv_to_latex(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        
        # Read the header
        headers = next(reader)
        
        # LaTeX table setup
        column_format = ' | '.join(['c' for _ in headers])
        latex_table = "\\begin{table}[h!]\n\\centering\n"
        latex_table += "\\begin{tabular}{| " + column_format + "| p{6cm}|}\n"

        latex_table += "\\hline\n"
        # Add the header to the LaTeX table
        header_row = ' & '.join(headers) + " \\\\"
        latex_table += header_row + "\n"
        latex_table += "\\hline\n"
        
        # Add the data rows to the LaTeX table
        for row in reader:
            latex_row = ' & '.join(row) + " \\\\"
            latex_table += latex_row + "\n"
            latex_table += "\\hline\n"
        latex_table += "\\end{tabular}"
        latex_table += "\\caption{placeholder}\n"
        latex_table += "\\label{tab:placeholder}\n"
        latex_table += "\\end{table}"

        # Print the resulting LaTeX table
        print(latex_table)
        print("\n\n")  # Add some space between tables

def process_csv_files(path):
    if os.path.isfile(path) and path.endswith('.csv'):
        csv_to_latex(path)
    elif os.path.isdir(path):
        for filename in os.listdir(path):
            if filename.endswith('.csv'):
                csv_to_latex(os.path.join(path, filename))
    else:
        print("Invalid file or directory. Please provide a valid CSV file or directory containing CSV files.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python csv_to_latex.py <csv_file_or_directory>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    process_csv_files(input_path)