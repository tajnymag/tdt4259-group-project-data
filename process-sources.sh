#!/usr/bin/bash

# load common helpers
source common.sh

# setup variables
INPUT_DIR=raw
OUTPUT_DIR=processed

# setup output directory
mkdir -p "$OUTPUT_DIR"

# prepare datasets
for dataset_path in $(find "$INPUT_DIR" -mindepth 1 -maxdepth 2 -type d); do
    dataset_name=$(basename "$dataset_path")

    echo "processing dataset $dataset_path"

    mkdir -p "$OUTPUT_DIR/$dataset_name"

    # convert to csv
    libreoffice --convert-to csv --outdir "$OUTPUT_DIR/$dataset_name" "$dataset_path"/*.xls

    # merge csv files
    concat_csv "$OUTPUT_DIR/$dataset_name"/*.csv > "$OUTPUT_DIR/$dataset_name.csv"
done
