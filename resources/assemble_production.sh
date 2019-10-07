#!/bin/bash

cd ..
if [ -d "tmp/" ]; then
  echo "Clearing previous assembly."
  rm -r tmp/
fi
mkdir tmp/

# Copy python files
cp __init__.py tmp/
cp collect_info.py tmp/
cp get_beers.py tmp/
cp scrape_data.py tmp/
cp -r utilities tmp/
echo "All core files copied."

# Copy depepndancies
cp -r venv/Lib/site-packages/* tmp/
echo "All dependancies copied."

cd tmp/
zip -rq production_files.zip *
echo "Files compressed."

mv production_files.zip ..
cd ..
rm -r tmp/
echo "Temporary files cleaned up"

