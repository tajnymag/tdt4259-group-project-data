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

# filter out empty rkom data
echo "filtering out empty rkom data"
awk -F, 'BEGIN { FPAT = "([^, ]+)|(\\"[^\\"]+\\")" } { sum=0; for (i=6;i<=NF;i++) sum+=$i; if (sum > 0) print $0 }' "$OUTPUT_DIR/rkom.csv" > "$OUTPUT_DIR/rkom.csv.tmp"
mv "$OUTPUT_DIR/rkom.csv.tmp" "$OUTPUT_DIR/rkom.csv"