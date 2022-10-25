#!/usr/bin/bash

# load common helpers
source common.sh

# setup variables
INPUT_DIR=processed
OUTPUT_DIR=datasets

# setup output directory
mkdir -p "$OUTPUT_DIR"

# process sources
for source_path in $(find "$INPUT_DIR" -mindepth 1 -maxdepth 1 -type f); do
    source_name=$(basename "$source_path")

    echo "preparing dataset $source_name"

    # convert strings to floats where applicable
    cat "$source_path" | sed -E 's/\"(-?[0-9]+),([0-9]+)\"/\1.\2/g' > "$OUTPUT_DIR/$source_name"
done

# merge primary reserves
echo "merging primaryreservesday and primaryreservesdaytwo"
concat_csv "$OUTPUT_DIR"/primaryreservesday{.csv,two.csv} > "$OUTPUT_DIR/primaryreservesday.csv.tmp"
rm "$OUTPUT_DIR"/primaryreservesday{.csv,two.csv}
mv "$OUTPUT_DIR/primaryreservesday.csv.tmp" "$OUTPUT_DIR/primaryreservesday.csv"