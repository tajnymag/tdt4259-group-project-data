#!/usr/bin/bash

# setup variables
INPUT_DIR=raw
OUTPUT_DIR=processed

# setup output directory
mkdir -p "$OUTPUT_DIR"

# process sources
for source_path in $(find "$INPUT_DIR" -mindepth 1 -maxdepth 2 -type d); do
    echo "processing source $source_path"

    source_name=$(basename "$source_path")
    
    cp -r "$source_path" "$OUTPUT_DIR"
done
