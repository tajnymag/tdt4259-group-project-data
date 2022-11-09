#!/usr/bin/bash
set -euo pipefail
shopt -s inherit_errexit

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
    datasets_by_year=("$OUTPUT_DIR/$dataset_name"/*.csv)
    last_valid_year=$(basename "${datasets_by_year[0]}" .csv | tail -c 5)
    last_valid_header=$(head -n 1 "${datasets_by_year[0]}")
    previous_year=$last_valid_year
    first_year=$last_valid_year
    last_year=$(basename "${datasets_by_year[-1]}" .csv | tail -c 5)

    for dataset_by_year_path in "${datasets_by_year[@]}"; do
        current_year=$(basename "$dataset_by_year_path" .csv | tail -c 5)
        current_header=$(head -n 1 "$dataset_by_year_path")

        if [[ "$current_header" != "$last_valid_header" ]]; then
            echo "merging $dataset_name from $last_valid_year to $previous_year"
            concat_csv "$OUTPUT_DIR/$dataset_name/"*_{$last_valid_year,$previous_year}.csv > "$OUTPUT_DIR/${dataset_name}_${last_valid_year}_${previous_year}.csv"

            last_valid_year="$current_year"
            last_valid_header=$(head -n 1 "$dataset_by_year_path")
        elif [[ "$current_year" == "$last_year" ]]; then
            echo "merging $dataset_name from $last_valid_year to $current_year"
            concat_csv "$OUTPUT_DIR/$dataset_name/"*_{$last_valid_year,$current_year}.csv > "$OUTPUT_DIR/${dataset_name}_${last_valid_year}_${current_year}.csv"
        fi

        previous_year="$current_year"
    done


    if [[ -f "$OUTPUT_DIR/${dataset_name}_${first_year}_${last_year}.csv" ]]; then
        echo "merging whole $dataset_name"
        mv "$OUTPUT_DIR/${dataset_name}_${first_year}_${last_year}.csv" "$OUTPUT_DIR/${dataset_name}.csv"
    fi
done
