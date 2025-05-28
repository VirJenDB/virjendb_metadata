import pandas as pd
import os

INPUT_XLSX = "metadata.xlsx"  # Replace with your actual XLSX file name
OUTPUT_DIR = "raw_files"  # This should match the INPUT_DIR in your existing script

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Define a dictionary where keys are sheet names and values are column indexes (starting from 0)
WANTED_FILES = [
    {"sheet_name": "VJDBCore", "cols": ["vjdbv0.3_field_id",	"vjdbv0.3_name",	"vjdbv0.3_description",	"vjdbv0.3_fields_type",	"vjdbv0.3_privacy"], "filename": "VJDBCore"},
    {"sheet_name": "VJDBCore", "cols": ["vjdbv0.3_field_id",	"vjdbv0.3_name",	"vjdbv0.3_tags"], "filename": "Tags"},
    {"sheet_name": "VJDBCore", "cols": ["vjdbv0.3_field_id",	"vjdbv0.3_name",	"vjdbv0.3_description", "vjdbv0.3_tags", "vjdbv0.3_privacy"], "filename": "Frontend"},
    {"sheet_name": "VJDBCore", "cols": ["vjdbv0.3_field_id",	"vjdbv0.3_name",	"vjdbv0.3_description", "vjdbv0.3_tags", "vjdbv0.3_privacy", "ena_submission_fieldtype", "vjdb_submission_requiredness", "ena_submission_validation"], "filename": "Submission"},
    {"sheet_name": "VJDBCore", "cols": ["vjdbv0.3_field_id",    "vjdbv0.3_fields_type", "vjdbv0.3_input_source", "ncbi_virus_n_nucleotide_field_id", "bv-brc_b_field_name", "ictv40_i_field_name", "vjdbv0.3_field_index"], "filename": "DB_Scheme"},
    ]


# Load the Excel file
xlsx = pd.ExcelFile(INPUT_XLSX)

# Convert each sheet to a TSV file with specified columns

for wanted_file in WANTED_FILES:
    print(wanted_file)
    if wanted_file["sheet_name"] in xlsx.sheet_names:
        df = pd.read_excel(xlsx, sheet_name=wanted_file["sheet_name"], usecols=lambda x: x in wanted_file["cols"], skiprows=3)
        tsv_path = os.path.join(OUTPUT_DIR, f"{wanted_file['filename']}.tsv")
        df.to_csv(tsv_path, sep="\t", index=False)
    else: 
        print("No such sheet: ", wanted_file.sheet_name)
        

# ➕ Export full sheet as "VJDB_catalogue.tsv"
if "VJDBCore" in xlsx.sheet_names:
    full_df = pd.read_excel(xlsx, sheet_name="VJDBCore", skiprows=3)
    full_tsv_path = os.path.join(OUTPUT_DIR, "VJDB_catalogue.tsv")
    full_df.to_csv(full_tsv_path, sep="\t", index=False)
    print("Full sheet saved as VJDB_catalogue.tsv")
else:
    print("No such sheet: VJDBCore")


print("TSV files have been generated!")
