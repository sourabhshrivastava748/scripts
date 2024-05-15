import csv
import os

def csv_to_html_table(csv_file):
    html_table = "<table style='border-collapse: collapse; border: 1.2px solid black;'>\n"
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        is_heading = True
        for i, row in enumerate(csv_reader):
            if is_heading:
                html_table += "<tr style='font-weight: bold;'>\n"
                is_heading = False
            else:
                if i % 2 == 0:
                    html_table += "<tr style='background-color: #f2f2f2;'>\n"
                else:
                    html_table += "<tr>\n"
            for cell in row:
                html_table += f"<td style='border: 1px solid black; padding: 6px; font-family: Arial;'>{cell}</td>\n"
            html_table += "</tr>\n"
    html_table += "</table>"
    return html_table

def convert_csv_files_to_html():
    all_html_tables = "Please find the attachment. Report prepared by alpha team.<br><br>"
    current_directory = os.getcwd()
    for filename in os.listdir(current_directory):
        if filename.endswith(".csv"):
            table_heading = os.path.splitext(filename)[0]  # Remove extension from filename
            csv_file = os.path.join(current_directory, filename)
            html_table = f"<h3>{table_heading}</h3>\n"
            html_table += csv_to_html_table(csv_file)
            all_html_tables += html_table + "\n"
    return all_html_tables

# Example usage:
html_tables = convert_csv_files_to_html()
print(html_tables)  # Print or write these HTML strings to a file
    