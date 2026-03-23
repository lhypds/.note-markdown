#!/bin/bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
ENTRY_FILE="$ROOT_DIR/note.py"
BUILD_MODE="onedir"

if [ "${1:-}" = "--onefile" ]; then
	BUILD_MODE="onefile"
elif [ -n "${1:-}" ]; then
	echo "Usage: ./build.sh [--onefile]"
	echo "Default build mode is onedir for faster run speed."
	exit 1
fi

if [ ! -x "$PYTHON_BIN" ]; then
	echo "Error: Python virtual environment not found at $PYTHON_BIN"
	echo "Run ./setup.sh first."
	exit 1
fi

if [ ! -f "$ENTRY_FILE" ]; then
	echo "Error: Entry file not found: $ENTRY_FILE"
	exit 1
fi

echo "Building note.py with PyInstaller ($BUILD_MODE)..."
cd "$ROOT_DIR"

rm -rf build dist note.spec


PYINSTALLER_ARGS=(
	--clean
	--noconfirm
	--name note
	"$ENTRY_FILE"
)

if [ "$BUILD_MODE" = "onefile" ]; then
	PYINSTALLER_ARGS=(--onefile "${PYINSTALLER_ARGS[@]}")
else
	PYINSTALLER_ARGS=(--onedir "${PYINSTALLER_ARGS[@]}")
fi

"$PYTHON_BIN" -m PyInstaller \
	"${PYINSTALLER_ARGS[@]}"

if [ "$BUILD_MODE" = "onefile" ]; then
	OUTPUT_FILE="$ROOT_DIR/dist/note"
	TARGET_FILE="$ROOT_DIR/note"
	echo "Build complete: $ROOT_DIR/dist/note"
else
	OUTPUT_FILE="$ROOT_DIR/dist/note/note"
	OUTPUT_INTERNAL_DIR="$ROOT_DIR/dist/note/_internal"
	TARGET_FILE="$ROOT_DIR/note"
	TARGET_INTERNAL_DIR="$ROOT_DIR/_internal"
	echo "Build complete: $ROOT_DIR/dist/note/note"
fi

cp "$OUTPUT_FILE" "$TARGET_FILE"
chmod +x "$TARGET_FILE"

if [ "$BUILD_MODE" = "onedir" ]; then
	rm -rf "$TARGET_INTERNAL_DIR"
	cp -R "$OUTPUT_INTERNAL_DIR" "$TARGET_INTERNAL_DIR"
else
	rm -rf "$ROOT_DIR/_internal"
fi

echo "Copied executable to: $TARGET_FILE"

echo "Warming up executable..."
"$TARGET_FILE" --help >/dev/null 2>&1 || true
