import pandas as pd
import os

VERSION = "v1.0"

INPUT_XLSX = "metadata.xlsx"  # Replace with your actual XLSX file name
OUTPUT_DIR = "raw_files"  # This should match the INPUT_DIR in your existing script

os.makedirs(OUTPUT_DIR, exist_ok=True)

WANTED_FILES = [
    {
        "sheet_name": "VJDBCore",
        "cols": [
            f"vjdb{VERSION}_field_index",
            f"vjdb{VERSION}_field_id",
            f"vjdb{VERSION}_name",
            f"vjdb{VERSION}_fields_type",
            f"vjdb{VERSION}_input_source",
            "ncbi_virus_n_nucleotide_field_id",
            "bv-brc_b_field_name",
            "ictv40_i_field_name",
            f"vjdb{VERSION}_privacy",
            f"vjdb{VERSION}_index",
            f"vjdb{VERSION}_search_method",
            f"vjdb{VERSION}_default_search"
        ],
        "filename": "DB_Scheme"
    },
    {
        "sheet_name": "VJDBCore",
        "cols": [
            f"vjdb{VERSION}_field_id",
            f"vjdb{VERSION}_name",
            f"vjdb{VERSION}_description",
            f"vjdb{VERSION}_tags",
            f"vjdb{VERSION}_privacy",
            "ena_submission_fieldtype",
            "vjdb_submission_requiredness",
            "ena_submission_validation",
            "vjdb_example",
            "vjdb_validation_rules"
        ],
        "filename": "Frontend"
    },
    {
        "sheet_name": "VJDBCore",
        "cols": [
            f"vjdb{VERSION}_field_id",
            f"vjdb{VERSION}_name",
            f"vjdb{VERSION}_description",
            f"vjdb{VERSION}_fields_type",
            f"vjdb{VERSION}_tags",
            f"vjdb{VERSION}_input_source",
            f"vjdb{VERSION}_notes",
            f"vjdb{VERSION}_changes",
            "vjdb_example",
            "ictv40_i_field_name"
        ],
        "filename": f"vjdb{VERSION}_metadata_schema_main"
    }
    ,
    {
        "sheet_name": "VJDBCore",
        "cols": [
            f"vjdb{VERSION}_field_id",
            f"vjdb{VERSION}_name",
            f"vjdb{VERSION}_description",
            f"vjdb{VERSION}_fields_type",
            f"vjdb{VERSION}_tags",
            f"vjdb{VERSION}_input_source",
            f"vjdb{VERSION}_notes",
            f"vjdb{VERSION}_changes",
            "vjdb_example",
            "ictv40_i_field_name",
            "rki_field_id",
            "migs-vi_field_id",
            "migs-uvig_field_id",
            "ncbi_virus_n_nucleotide_field_id",
            "bv-brc_b_field_name",
            "ena_erc32_field_name",
            "ena_erc33_field_name",
            "img/vr_field_name",
            "phd_field_name",
            "phispy_field_name",
            "gtdb_field_name",
            "ncbi_virus_n_field_description",
            "ncbi_virus_n_type",
            "ncbi_virus_n_curation_notes",
            "bv-brc_b_category",
            "bv-brc_b_schema_category",
            "bv-brc_b_field_id",
            "bv-brc_b_field_type",
            "bv-brc_b_type",
            "bv-brc_b_curation_notes",
            "ena_erc32_field_description",
            "ena_erc32_controlled_vocabulary",
            "ena_erc32_field_type",
            "ena_erc33_field_description",
            "ena_erc33_controlled_vocabulary",
            "ena_erc33_field_type",

        ],
        "filename": f"vjdb{VERSION}_metadata_schema_main_and_maps"
    }
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
    full_tsv_path = os.path.join(OUTPUT_DIR, f"vjdb{VERSION}_metadata_schema_all.tsv")
    full_df.to_csv(full_tsv_path, sep="\t", index=False)
    print("Full sheet saved")
else:
    print("No such sheet: VJDBCore")


print("TSV files have been generated!")
