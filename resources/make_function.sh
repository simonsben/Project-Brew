#!/bin/bash

build_directory="tmp/"

# Start clean with a build directory
if [ -d "$build_directory" ]; then
  echo "Clearing previous assembly."
  rm -r "$build_directory"
fi
mkdir "$build_directory"

# Copy python files
cp *.py "$build_directory"
cp -r "utilities/" "$build_directory"
echo "All core files copied."

# Compress files
(
  cd "$build_directory" || exit
  zip -rq "../deployment_function.zip" *
)
echo "Files compressed."

# Clear build directory
rm -r "$build_directory"
echo "Temporary files cleaned up"
