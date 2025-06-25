import pandas as pd
import argparse
import os


# USE=======================
# python anovaProcess.py directory_with_anova_csvs
#              OR
# python anovaProcess.py csvFile.csv

# Prints Latex tables for each csv in the directory, or the single csv anova








# Here's some example R code to generate a CSV from an anova
# CT_ANOVA <- ezANOVA(
#   data = success_trials,
#   dv = completionTime,
#   wid = pID,
#   within = .(interaction, block),
#   between = .(device),
#   type = 3,
#   #detailed = TRUE,
#   ##return_aov = TRUE
# )
# CT_ANOVA
# write.csv(CT_ANOVA["ANOVA"],
#           paste0(directory, "ANOVAS/CT_ANOVA.csv"),
#           row.names = TRUE)





def format_scientific(x):
    try:
        return "{:.2e}".format(float(x))
    except ValueError:
        return x
    
def round_scientific_to_decimal(x):
    try:
        # Convert the input to a float
        num = float(x)
        # Convert the number to scientific notation
        sci_not = "{:.2e}".format(num)
        # Check the exponent part of the scientific notation
        base, exponent = sci_not.split('e')
        exponent = int(exponent)
        
        # Round if the exponent is -01 or -02
        if exponent == -1 or exponent == -2:
            # Convert to decimal notation with 2 significant figures
            rounded_num = "{:.2f}".format(num)
            return rounded_num
        else:
            return sci_not
    except ValueError:
        # Return the original value if it cannot be converted to a float
        return x


def processRow(row):
    value = round_scientific_to_decimal(row["p"])

    if row["p < 0.05"] != "*":
        row["Eta Squared"] = ""
        row["p"] = value
    else:
        row["p"] = "\\textbf{" + value + "}"
    return row

def generate_latex_table(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Drop the first unnamed column if it exists
    if df.columns[0].startswith('Unnamed'):
        df = df.drop(columns=[df.columns[0]])

    # Replace ":" with " x " in the 'Effect' column
    df['ANOVA.Effect'] = df['ANOVA.Effect'].str.replace(':', ' $\\times$ ')

    # Combine 'DFn' and 'DFd' into a single column
    df['DF (n,d)'] = df.apply(lambda row: f"{row['ANOVA.DFn']}, {row['ANOVA.DFd']}", axis=1)

    # Use the 'ANOVA.ges' column as the 'Eta Squared' value and format it to 2 decimal places
    df['Eta Squared'] = df['ANOVA.ges'].apply(lambda x: "{:.2f}".format(float(x)) if x != '' else '')

    # Select and reorder columns
    df = df[['ANOVA.Effect', 'DF (n,d)', 'ANOVA.F', 'ANOVA.p', 'ANOVA.p..05', 'Eta Squared']]
    df.columns = ['Effect', 'DF (n,d)', 'F', 'p', 'p < 0.05', 'Eta Squared']

    # Replace NaN values with empty strings
    df = df.fillna('')

    # Convert p-values to scientific notation
    df['p'] = df['p'].apply(format_scientific)
    df['p < 0.05'] = df['p < 0.05'].apply(format_scientific)


    # Round F statistics to 2 decimal points
    df['F'] = df['F'].apply(lambda x: "{:.2f}".format(float(x)) if x != '' else '')

    # Add an empty column for 'Pairwise Contrasts (mean), t-test result'
    df['Pairwise Contrasts (mean), t-test result'] = ''

    # Prepare LaTeX table content
    latex_content = []
    
    # Define header
    latex_content.append(
        "\\begin{table}\n"
        "\\centering\n"
        "\\begin{tabular}{|c|c|c|c|c|c|p{6cm}|}\n"
        "\\hline\n"
        "\\textbf{Factor} & \\textbf{DF (n,d)} & \\textbf{F} & \\textbf{p} & \\textbf{$\\eta^2$} & \\textbf{Pairwise Contrasts (mean), t-test result} \\\\\n"
        "\\hline\n"
    )
    
    # Insert data with horizontal lines between different factors
    prev_factor_count = None
    for idx, row in df.iterrows():
        # Determine the number of factors
        effect = row['Effect']

        if(effect != "(Intercept)"):
            effect = row['Effect']
            factor_count = effect.count(' x ') + 1
            
            # Add a horizontal line if the number of factors changes
            if prev_factor_count is not None and factor_count != prev_factor_count:
                latex_content.append("\\hline\n")
            
            row = processRow(row)

            # Append the row content
            latex_content.append(
                f"{row['Effect']} & {row['DF (n,d)']} & {row['F']} & {row['p']} & {row['Eta Squared']} & {row['Pairwise Contrasts (mean), t-test result']} \\\\\n"
            )
            
            # Update the previous factor count
            prev_factor_count = factor_count

    # Add the footer
    # latex_content.append(
    #     "\\hline\n"
    #     "\\end{tabular}\n"
    #     "\\caption{ANOVA Results}\n"
    #     "\\label{tab:anova_results}\n"
    #     "\\end{table}"
    # )
    base_name = os.path.splitext(os.path.basename(csv_file))[0]
    baseNameString = base_name.replace("_", " ")
    latex_content.append(
        "\\hline\n"
        "\\end{tabular}\n"
        f"\\caption{{ANOVA Results from {baseNameString}}}\n"
        f"\\label{{tab:{base_name}_anova_results}}\n"
        "\\end{table}"
    )

        
    
    # Join all parts and print
    full_latex_table = ''.join(latex_content)
    print(full_latex_table)
    print()
    print()
    print()

# if __name__ == "__main__":
#     # Set up command-line argument parsing
#     parser = argparse.ArgumentParser(description="Generate a LaTeX table from an ANOVA CSV file.")
#     parser.add_argument('csv_file', type=str, help="Path to the CSV file containing ANOVA results.")
    
#     args = parser.parse_args()
    
#     # Generate and print the LaTeX table
#     generate_latex_table(args.csv_file)

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Generate LaTeX tables from an ANOVA CSV file or all CSV files in a directory.")
    parser.add_argument('path', type=str, help="Path to the CSV file or directory containing ANOVA CSV files.")
    
    args = parser.parse_args()
    
    # Check if the path is a directory or a file
    if os.path.isdir(args.path):
        # Process all CSV files in the directory
        for filename in os.listdir(args.path):
            if filename.endswith(".csv"):
                csv_file_path = os.path.join(args.path, filename)
                generate_latex_table(csv_file_path)
    elif os.path.isfile(args.path) and args.path.endswith(".csv"):
        # Process the single CSV file
        generate_latex_table(args.path)
    else:
        print("The provided path is neither a CSV file nor a directory containing CSV files.")