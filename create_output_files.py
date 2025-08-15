import os
import pandas as pd
import json
import xml.etree.ElementTree as ET
import logging

VERSION = 'v1.0'

FIELD_ID         = f'vjdb{VERSION}_field_id'
FIELD_BVBRC_CAT  = 'bv-brc_b_category'
FIELD_BVBRC_ID   = 'bv-brc_b_field_id'
FIELD_BVBRC_NAME = 'bv-brc_b_field_name'
FIELD_BVBRC_NOTE = 'bv-brc_b_curation_notes'
FIELD_BVBRC_SHM  = 'bv-brc_b_schema_category'
FIELD_BVBRC_TYPE = 'bv-brc_b_field_type'
FIELD_CHANGES    = f'vjdb{VERSION}_changes'
FIELD_DEF_SEARCH = f'vjdb{VERSION}_default_search'
FIELD_DESCR      = f'vjdb{VERSION}_description'
FIELD_ENA_ID     = 'ena_field_id'
FIELD_ENA32_DESC = 'ena_erc32_field_description'
FIELD_ENA32_NAME = 'ena_erc32_field_name'
FIELD_ENA32_TYPE = 'ena_erc32_field_type'
FIELD_ENA32_VOC  = 'ena_erc32_controlled_vocabulary'

FIELD_ENA33_DESC = 'ena_erc33_field_description'
FIELD_ENA33_NAME = 'ena_erc33_field_name'
FIELD_ENA33_TYPE = 'ena_erc33_field_type'
FIELD_ENA33_VOC  = 'ena_erc33_controlled_vocabulary'
FIELD_ENV_O      = 'env-o_field_id'
FIELD_EXAMPLE    = 'vjdb_example'
FIELD_FIELD      = f'vjdb{VERSION}_field_index'
FIELD_GROUP1     = f'vjdb{VERSION}_group1'
FIELD_GROUP2     = f'vjdb{VERSION}_group2'
FIELD_GROUP3     = f'vjdb{VERSION}_group3'
FIELD_ICTV_NAME  = 'ictv40_i_field_name'
FIELD_INDEX      = f'vjdb{VERSION}_index'
FIELD_INP_SRC    = f'vjdb{VERSION}_input_source'
FIELD_MIGS_VI    = 'migs-vi_field_id'
FIELD_MIGS_UVIG  = 'migs-uvig_field_id'
FIELD_NAME       = f'vjdb{VERSION}_name'
FIELD_NCBI_NAME  = 'ncbi_virus_n_field_name'
FIELD_NCBI_DESCR = 'ncbi_virus_n_field_description'
FIELD_NCBI_NUCL  = 'ncbi_virus_n_nucleotide_field_id'
FIELD_NCBI_TYPE  = 'ncbi_virus_n_type'
FIELD_NCBI_NOTES = 'ncbi_virus_n_curation_notes'
FIELD_NOTES      = f'vjdb{VERSION}_notes'
FIELD_PRIVACY    = f'vjdb{VERSION}_privacy'
FIELD_RKI_ID     = 'rki_field_id'
FIELD_SEARCH_MET = f'vjdb{VERSION}_search_method'
FIELD_TAGS       = f'vjdb{VERSION}_tags'
FIELD_TYPE       = f'vjdb{VERSION}_fields_type'
FIELD_VALIDATION = 'vjdb_validation_rules'
DIR_INPUT        = "raw_files"  # Folder containing TSV files
DIR_DOWNLOAD     = "downloads"  # Folder for files linked from the documentation site

LOG_FORMAT    = '%(asctime)s %(levelname)-7s %(message)s'
logging.basicConfig(format=LOG_FORMAT,level=logging.DEBUG)
logger           = logging.getLogger()


def dict_to_xml(tag, d):
    """Convert a dictionary to an XML element"""
    elem = ET.Element(tag)
    for key, val in d.items():
        child = ET.SubElement(elem, key.replace(" ", "_"))  # Replace spaces with underscores
        child.text = str(val)
    return elem


def create_xml_structure(data):
    """Convert flat data into XML format"""
    root = ET.Element("Root")

    for item in data:
        entry_elem = dict_to_xml("Entry", item)
        root.append(entry_elem)

    return ET.ElementTree(root)

def write_formats():
    # Ensure top-level output directories exist
    for folder in ["json", "csv", "tsv", "xml"]:
        logger.debug("Checking directory %s exists",folder)
        os.makedirs(folder, exist_ok=True)


    for file in os.listdir(DIR_INPUT):
        if file.endswith(".tsv"):
            logger.debug("processing %s/%s:",DIR_INPUT,file)
            input_path = os.path.join(DIR_INPUT, file)
            base_name = os.path.splitext(file)[0]

            # Read TSV file
            df = pd.read_csv(input_path, sep='\t')

            # Handle NaN values before processing
            df = df.fillna('N/A')  # Replace NaN values with "N/A" or another placeholder

            # Ensure we have enough columns
            if df.shape[1] < 3:
                logger.warning(f"Skipping {file} (needs at least 3 columns)")
                continue

            # Check for the column containing the array (adjust column name accordingly)
            if FIELD_TAGS in df.columns:
                # Convert the column containing the string representation of a list into an actual list
                df[FIELD_TAGS] = df[FIELD_TAGS].apply(lambda x: json.loads(x) if isinstance(x, str) else x)

            # Flatten the structure, no hierarchical nesting
            flat_data = []

            for _, row in df.iterrows():
                entry = row.to_dict()  # Flatten the row into a single dictionary
                flat_data.append(entry)

            # Save JSON file

            json_path = os.path.join("json", f"{base_name}.json")
            logger.debug('  creating %s',json_path)
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(flat_data, json_file, indent=4)

            # Save XML file
            xml_path = os.path.join("xml", f"{base_name}.xml")
            logger.debug('  creating %s',xml_path)
            xml_tree = create_xml_structure(flat_data)
            xml_tree.write(xml_path, encoding="utf-8", xml_declaration=True)

            # Save CSV and TSV (no change needed as they are already flat)
            csv_path = os.path.join("csv", f"{base_name}.csv")
            logger.debug('  creating %s',csv_path)
            df.to_csv(csv_path, index=False)

            tsv_path = os.path.join("tsv", f"{base_name}.tsv")
            logger.debug('  creating %s',tsv_path)
            df.to_csv(tsv_path, sep='\t', index=False)

def write_schema(tsv):
    schema_download = tsv[[
        FIELD_ID,
        FIELD_NAME,
        FIELD_DESCR,
        FIELD_TYPE,
        FIELD_GROUP1,
        FIELD_GROUP2,
        FIELD_GROUP3,
        FIELD_TAGS,
        FIELD_INP_SRC,
        FIELD_NOTES,
        FIELD_CHANGES,
        FIELD_EXAMPLE,
        FIELD_VALIDATION,
        FIELD_FIELD,
        FIELD_INDEX,
        FIELD_SEARCH_MET,
        FIELD_DEF_SEARCH
    ]]
    schema_path = os.path.join(DIR_DOWNLOAD,'schema.tsv')
    logger.debug('  writing %s',schema_path)
    os.makedirs(DIR_DOWNLOAD, exist_ok=True)
    schema_download.to_csv(schema_path,sep='\t',index=False)

def write_mapping(tsv):
    maapping_download = tsv[[
        FIELD_ID,
        FIELD_NAME,
        FIELD_DESCR,
        FIELD_ENA_ID,
        FIELD_RKI_ID,
        FIELD_MIGS_VI,
        FIELD_MIGS_UVIG,
        FIELD_ENV_O,
        FIELD_NCBI_NUCL,
        FIELD_BVBRC_NAME,
        FIELD_ENA32_NAME,
        FIELD_ENA33_NAME,
        FIELD_NCBI_NAME,
        FIELD_NCBI_DESCR,
        FIELD_NCBI_TYPE,
        FIELD_NCBI_NOTES,
        FIELD_BVBRC_CAT,
        FIELD_BVBRC_SHM,
        FIELD_BVBRC_ID,
        FIELD_BVBRC_TYPE,
        FIELD_BVBRC_NOTE,
        FIELD_ENA32_DESC,
        FIELD_ENA32_VOC,
        FIELD_ENA32_TYPE,
        FIELD_ENA33_DESC,
        FIELD_ENA33_VOC,
        FIELD_ENA33_TYPE,
        FIELD_ICTV_NAME
    ]]
    mapping_path = os.path.join(DIR_DOWNLOAD,'mapping.tsv')
    logger.debug('  writing %s',mapping_path)
    os.makedirs(DIR_DOWNLOAD, exist_ok=True)
    maapping_download.to_csv(mapping_path,sep='\t',index=False)

def write_compact():
    source = None

    for file in os.listdir(DIR_INPUT):
        if 'vjdbv1.0_metadata_schema_all' in file.lower():
            source = os.path.join(DIR_INPUT, file)
    if not source:
        logger.warning('no schema file found')
    logger.debug('processing %s:',source)
    tsv = pd.read_csv(source,sep='\t')
    public = tsv[tsv[FIELD_PRIVACY] == 'public']
    write_schema(public)
    write_mapping(public)


def main():
    write_formats()
    write_compact()
    logger.info("Conversion complete!")

if __name__ == '__main__':
    main()




