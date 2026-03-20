# VirJenDB Metadata

This repository serves as the ground truth for the metadata schema of the VirJenDB

**CURRENT VERSION 1.0 RELEASE METADATA ON [BRANCH `v1.0`](https://github.com/VirJenDB/virjendb_metadata/tree/v1.0)**\
They are available for download in `.json`, `.tsv`, `.csv` and `.xml` format in the corresponding folders.

Files:

- `vjdbv1.0_metadata_schema_main` most relevant file, contains information like ids, names, descriptions, tags, examples and more.
- `vjdbv1.0_metadata_schema_main_and_maps` containt all information from the file above plus mapping information
- `vjdbv1.0_metadata_schema_all.csv` complete rundown from the source metadata.xlsx

The complete metadata catalogue can be explored in the `metadata.xlsx` on `main` branch or via our [_Metadata Explorer_](https://virjendb.org/MetadataTemplates) for public metadata. It also allows you to build and download custom lists of metadata fields.

## How to contribute

If you want to propose changes to the metadata schema you can create an issue to this repository stating the following information:

- **What** should be changed? Give a comparison of the current value and the new value.
- **Why** should this be changed? State the reasons on why the changes should be applied. Describe what are advantages and disadvantages.

You can bundle multiple changes into one issue.

## Metadata.xlsx

This is the working file of the repository. All information for all the metadata fields will be collected in there.

Once changed github actions runs the `convert_xlsx_to_tsv.py` script and builds a trackable tsv version of the schema. Once finished github actions runs `create_output_files.py` and pushes the newly build file formats to the corresponding branch.

### **Attenion!**

Only open tile file via `Excel`! There are build in formulas, to keep them intact please refrain from using Google Sheets or Libre Office Calc. For none windows users, there is an online version of [Excel](https://excel.cloud.microsoft/).

For working within the file please stick to the following guidelines:

- `Row 1` - describes the object the information of the columns is derived from or that it adresses, e.g. `ENA`, `VJDBv0.3`
- `Row 2` - describes the purpose or meaning of the column information, e.g. `description`, `field id`
- `Row 3` - **DONT CHANGE THIS ROW** - Helper to construct the naming of a columns from `Row 1` and `Row 2`. When a new columns is created drag the formula from the previous columns to populate the field.
- `Row 4` - **DONT CHANGE THIS ROW** - Contains the real name of the column. This field is created by formulas using `Row 3`. When a new columns is created drag the formula from the previous columns to populate the field.
- `vjdbv0.3_tags` - **DONT CHANGE THIS COLUMN** - This column constructs the tags for a metadata field from other columns (H - U). For columns H - P it inserts the naming of `Row 1` if the cell of the columns is filled, for the other columns is inserts the value of the field if there is one in the column. For new rows the formula is to be extended. Should a new tag be introduced by a new column the formula needs to be adjusted.

### **Important Notice on vjdbv0.3_field_index Column**

- The `vjdbv0.3_field_index` column must remain unchanged and persist across all updates.
- When adding new records, always append them to the end of the dataset. Do not insert rows between existing records.
- Avoid deleting any rows from this index. Instead, if a record is no longer in use, tag it as "not used" in `vjdbv0.3_fields_type` rather than removing it.
- Deleting rows can disrupt the automated processes relying on this index, causing new fields to fail to map correctly.
- Cleanup or reorganization of this index should be done manually and carefully, not through automated procedures.

### **Important Notice on vjdbv0.3_tags Column**

- when new rows are inserted make sure the the formula generating the tags is applied to the new fields, empty tag fiels crash the 2. conversion script!

### convert_xlsx_to_tsv.py

This script converts the xlsx file into tsv files that can be tracked. It is run everytime a push to main happens that changes `metadata.xlsx`. The number of output files is determined by

```python
WANTED_FILES = [
    {"sheet_name": "VJDBCore", "cols": ["vjdbv0.3_field_id", "vjdbv0.3_name", "vjdbv0.3_description", "vjdbv0.3_fields_type", "vjdbv0.3_privacy"], "filename": "VJDBCore"},
    {"sheet_name": "VJDBCore", "cols": ["vjdbv0.3_field_id", "vjdbv0.3_name", "vjdbv0.3_tags"], "filename": "Tags"},
    {"sheet_name": "VJDBCore", "cols": ["vjdbv0.3_field_id", "vjdbv0.3_name", "vjdbv0.3_description", "vjdbv0.3_tags", "vjdbv0.3_privacy"], "filename": "Frontend"},
    {"sheet_name": "VJDBCore", "cols": ["vjdbv0.3_field_id", "vjdbv0.3_name", "vjdbv0.3_description", "vjdbv0.3_tags", "vjdbv0.3_privacy", "ena_submission_fieldtype", "vjdb_submission_requiredness", "ena_submission_validation"], "filename": "Submission"},
    {"sheet_name": "VJDBCore", "cols": ["vjdbv0.3_field_index", "vjdbv0.3_field_id", "vjdbv0.3_name", "vjdbv0.3_fields_type", "vjdbv0.3_input_source", "ncbi_virus_n_nucleotide_field_id", "bv-brc_b_field_name", "ictv40_i_field_name", "vjdbv0.3_privacy", "vjdbv0.3_index", "vjdbv0.3_search_method", "vjdbv0.3_default_search" ], "filename": "DB_Scheme"},
,
    ]
```

- `sheet_name` - describes the name of the excel sheet that should be converted
- `cols` - describes a list of the columns name the should be included in the newly generated tsv file. Column names are taken from row 4 of `metadata.xlsx`.
- `filename` - describes the name of the output file

To create a new file add an dictionary containing the above information to the array of `WANTED_FILES`. An tsv files will be created for every element in the array. The output tsv files will be used by `create_output_files.py` to generated json, xml and csv files of it.\
Additionally one file with all columns will be created called `VJDB_catalogue`.

- Note: The first three rows of the excel will be skipped `usecols=lambda x: x in wanted_file["cols"], skiprows=3)`

### On VirJenDB Release Change

Update the name of the new branch in the `.github/workflow/file_publication.yaml`

```yaml
# Step 6: Create a new branch and remove all existing files
- name: Commit converted files
  env:
    OUTPUT_BRANCH: "v0.3" # Define your branch name
```

## Webhooks

The connection between the metadata repository and the website is handled by Webhooks. Each Webhook calls an API endpoint on the backend, which downloads the corresponding JSON file into a backend folder. These JSON files are then used to provide field names to the website and to support query functionality.

There are four Webhooks in total:

- Two pointing to the development services (api2.virjendb.org)

- Two pointing to the production services (api.virjendb.org)

As described above, whenever the `XLSX` file is modified, a new set of files (including `DB_Scheme.json` and `Frontend.json`) is generated in the `dev` branch. Files in other branches remain unchanged.

To select which branch the Webhooks should use, no changes are needed in GitHub. Instead, update the backend configuration file to reference the raw URL of the JSON file in the desired branch, for example:
`https://raw.githubusercontent.com/VirJenDB/virjendb_metadata/refs/heads/v1.0/json/Frontend.json`

## 

And the documentation ;)
