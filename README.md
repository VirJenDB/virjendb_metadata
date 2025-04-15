# VirJenDB Metadata

This repository serves as the ground truth for the metadata schema of the VirJenDB

**Find our current metadata schema and expansions on the branch `v0.3`** \
They are available for download in `.json`, `.tsv`, `.csv` and `.xml` format in the corresponding folders.

Alternatively you can download a custom metadata template (incorporating the core model and custom expansions) using our [_template creator_](https://virjendb.org/MetadataTemplates).

## Metadata Update Process

- create a new branch
- edit the `metadata.xlsx` file
- commit your changes to your branch
- create a merge request with the main branch

Once the merge was approved github actions runs the `convert_xlsx_to_tsv.py` script and builds trackable tsv version of the schema. Once finished github actions runs `create_output_files.py` and pushes the newly build file formats to the corresponding branch.

## On VirJenDB Release Change

Update the name of the new branch in the `.github/workflow/file_publication.yaml`

```yaml
# Step 6: Create a new branch and remove all existing files
- name: Commit converted files
  env:
    OUTPUT_BRANCH: "v0.3" # Define your branch name
```

And the documentation ;)
