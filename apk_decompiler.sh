#!/bin/bash

INPUT_DIR="/apks"
OUTPUT_DIR="/path/to/decompiled_apps"

mkdir -p "$OUTPUT_DIR"

for apk in "$INPUT_DIR"/*.apk; do
    app_name=$(basename "$apk" .apk)
    echo "Decompiling $app_name..."
    apktool d "$apk" -o "$OUTPUT_DIR/$app_name" -f
done
