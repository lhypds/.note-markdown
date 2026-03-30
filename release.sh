#!/bin/bash

set -euo pipefail

rm -rf release/

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
RELEASE_DIR="$ROOT_DIR/release"

# Create release folders
mkdir -p "$RELEASE_DIR/python"
mkdir -p "$RELEASE_DIR/rust"

# Build Python binaries and move to release/python
echo "Building Python..."
"$ROOT_DIR/build_py.sh"
mv "$ROOT_DIR/note" "$RELEASE_DIR/python/note"
if [ -d "$ROOT_DIR/_internal_note" ]; then
	mv "$ROOT_DIR/_internal_note" "$RELEASE_DIR/python/_internal_note"
fi
echo "Python binaries moved to $RELEASE_DIR/python"

# Build Rust binaries and move to release/rust
echo "Building Rust..."
"$ROOT_DIR/build_rs.sh"
mv "$ROOT_DIR/note" "$RELEASE_DIR/rust/note"
echo "Rust binaries moved to $RELEASE_DIR/rust"

echo "Release complete: $RELEASE_DIR"

ZIP_NAME="dot_note.zip"
ZIP_PATH="$RELEASE_DIR/$ZIP_NAME"
TMP_ZIP_PATH="$ROOT_DIR/$ZIP_NAME"

if [ -f "$ZIP_PATH" ]; then
	rm -f "$ZIP_PATH"
fi
if [ -f "$TMP_ZIP_PATH" ]; then
	rm -f "$TMP_ZIP_PATH"
fi

# Copy install/uninstall scripts to release
cp "$ROOT_DIR/install.sh" "$RELEASE_DIR/install.sh"
cp "$ROOT_DIR/uninstall.sh" "$RELEASE_DIR/uninstall.sh"
chmod +x "$RELEASE_DIR/install.sh" "$RELEASE_DIR/uninstall.sh"
echo "Copied install.sh and uninstall.sh to $RELEASE_DIR"

cd "$RELEASE_DIR"
zip -r -9 "$TMP_ZIP_PATH" "python" "rust" "install.sh" "uninstall.sh"
mv "$TMP_ZIP_PATH" "$ZIP_PATH"
echo "Created archive: $ZIP_PATH"
