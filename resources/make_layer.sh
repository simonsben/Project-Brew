#!/bin/bash

echo "Making layer with dependencies"

build_directory="python/"
layer="deployment_layer.zip"

# Delete and remake build directory if present
if [ -d "$build_directory" ]; then
    rm -r "$build_directory"
fi
mkdir "$build_directory"

# Only the requests library is required
pip3 install -q --target="$build_directory" "requests"

echo "Installed dependencies."
tree -L 1 "$build_directory"

# Zip layer and cleanup build
zip -qr "$layer" "$build_directory"
rm -r "$build_directory"

echo "Zipped layer and cleaned up build, layer is $layer"
