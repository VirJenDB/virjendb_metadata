import pandas as pd
import json
import os

VERSION = "v1.0"

# Constants
INPUT_XLSX = "metadata.xlsx"  # Replace with actual file
OUTPUT_JSON = "metadata_summary.json"
FIELD_ID_COLUMN = f"vjdb{VERSION}_field_id"  # Column that must not be empty
TAG_COLUMN = f"vjdb{VERSION}_tags"  # Column with tags
SHEETS_TO_PROCESS = ["VJDBCore"]  # Modify as needed

summary = {}

# Load Excel file
xlsx = pd.ExcelFile(INPUT_XLSX)

# Process each sheet
for sheet_name in (SHEETS_TO_PROCESS or xlsx.sheet_names):
    df = pd.read_excel(xlsx, sheet_name=sheet_name, skiprows=3)  # Skip first 3 rows

    # Remove rows where vjdbv0.3_field_id is empty
    df = df.dropna(subset=[FIELD_ID_COLUMN])

    tag_counts = {}
    if TAG_COLUMN in df.columns:
        # Convert stringified lists into actual lists
        df[TAG_COLUMN] = df[TAG_COLUMN].apply(lambda x: json.loads(x) if isinstance(x, str) and x.startswith("[") else x)

        # Flatten all tags into a single list
        all_tags = df[TAG_COLUMN].dropna().explode().astype(str)  # Handle NaN values and split lists

        for tag in all_tags:
            tag = tag.strip()  # Remove extra spaces
            tag_counts[tag] = tag_counts.get(tag, 0) + 1  # Count occurrences

        summary[sheet_name] = {
            "num_fields": len(df),  # Number of valid rows after filtering
            "unique_tags": list(tag_counts.keys()),
            "tag_counts": tag_counts
        }
    else:
        summary[sheet_name] = {
            "num_fields": len(df),
            "unique_tags": [],
            "tag_counts": {}
        }

# Save JSON
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=4, ensure_ascii=False)

print(f"Summary JSON generated: {OUTPUT_JSON}")
