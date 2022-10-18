#!/usr/bin/bash

# setup variables
INPUT_DIR=raw
OUTPUT_DIR=processed

# setup output directory
mkdir -p "$OUTPUT_DIR"

# process datasets
for dataset_path in $(find "$INPUT_DIR" -mindepth 1 -maxdepth 2 -type d); do
    echo "processing dataset $dataset_path"

    dataset_name=$(basename "$dataset_path")
    mkdir -p "$OUTPUT_DIR/$dataset_name"

    # convert to csv
    libreoffice --convert-to csv --outdir "$OUTPUT_DIR/$dataset_name" "$dataset_path"/*.xls

    # merge csv files
    set header_set
    for csv_path in "$OUTPUT_DIR/$dataset_name"/*.csv; do
        if [[ -z "$header_set" ]]; then
            head -n 1 "$csv_path" > "$OUTPUT_DIR/$dataset_name.csv"
            header_set=1
        fi

        tail -n +2 "$csv_path" >> "$OUTPUT_DIR/$dataset_name.csv"
    done
    unset header_set
done
