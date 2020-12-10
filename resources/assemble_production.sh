#!/bin/bash

TMP_DIR="tmp/"

cd ..
if [ ! -d "venv/" ]; then
  echo "No virtual environment present, exiting."
  exit 1;
fi

if [ -d "$TMP_DIR" ]; then
  echo "Clearing previous assembly."
  rm -r "$TMP_DIR"
fi
mkdir "$TMP_DIR"

# Copy python files
cp "__init__.py" "$TMP_DIR"
cp "collect_info.py" "$TMP_DIR"
cp "get_beers.py" "$TMP_DIR"
cp "scrape_data.py" "$TMP_DIR"
cp -r "utilities/" "$TMP_DIR"
echo "All core files copied."

# Copy dependencies
cp -r venv/Lib/site-packages/* "$TMP_DIR"
echo "All dependencies copied."

cd "$TMP_DIR"
zip -rq "production_files.zip" *
echo "Files compressed."

mv "production_files.zip" ..
cd ..
rm -r "$TMP_DIR"
echo "Temporary files cleaned up"
