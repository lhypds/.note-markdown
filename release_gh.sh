#!/bin/bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
RELEASE_DIR="$ROOT_DIR/release"

# Accept VERSION and BUILD_ZIP as arguments, or derive them
if [ $# -ge 2 ]; then
	VERSION="$1"
	ZIP_PATH="$2"
else
	VERSION_FILE="$ROOT_DIR/VERSION"
	if [ ! -f "$VERSION_FILE" ]; then
		echo "Error: VERSION file not found."
		exit 1
	fi
	VERSION="v$(cat "$VERSION_FILE" | tr -d '[:space:]')"
	ZIP_PATH="$RELEASE_DIR/dot_note_${VERSION}.zip"
fi

# Check zip exists
if [ ! -f "$ZIP_PATH" ]; then
	echo "Error: $ZIP_PATH not found. Run release.sh first."
	exit 1
fi

# Check gh is available
if ! command -v gh &>/dev/null; then
	echo "Error: GitHub CLI (gh) is not installed. Install it from https://cli.github.com"
	exit 1
fi

echo "Ready to publish release:"
echo "  Tag:    $VERSION"
echo "  Asset:  $ZIP_PATH"
echo ""
read -r -p "Release notes (leave blank for default): " RELEASE_NOTES
if [ -z "$RELEASE_NOTES" ]; then
	RELEASE_NOTES="Release $VERSION"
fi
echo ""
read -r -p "Publish to GitHub? [Y/n]: " CONFIRM
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
	echo "Aborted."
	exit 0
fi

# Create tag and GitHub release, upload zip
gh release create "$VERSION" "$ZIP_PATH" \
	--title "$VERSION" \
	--notes "$RELEASE_NOTES"

echo "Published release $VERSION with $ZIP_PATH"
