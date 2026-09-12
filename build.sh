#!/data/data/com.termux/files/usr/bin/bash
# E.L.V ROOT ENGINE - Build Release Package

VERSION="1.0.0"
NAME="elv-root-engine"
OUT="${NAME}-v${VERSION}.zip"
BUILD_DIR="build/${NAME}-v${VERSION}"

GREEN='\033[92m'
RED='\033[91m'
END='\033[0m'

echo -e "${GREEN}[+] Building E.L.V ROOT ENGINE v${VERSION}${END}"

for f in elv.py elv.sh README.md LICENSE; do
    if [ ! -f "$f" ]; then
        echo -e "${RED}[!] File '$f' missing. Create it first.${END}"
        exit 1
    fi
done

if ! command -v zip &>/dev/null; then
    echo -e "${RED}[!] 'zip' not installed. Run: pkg install zip${END}"
    exit 1
fi

rm -rf build
mkdir -p "$BUILD_DIR"

cp elv.py "$BUILD_DIR/"
cp elv.sh "$BUILD_DIR/"
cp README.md "$BUILD_DIR/"
cp LICENSE "$BUILD_DIR/"

chmod +x "$BUILD_DIR/elv.py"
chmod +x "$BUILD_DIR/elv.sh"

cd build
zip -r "../$OUT" "${NAME}-v${VERSION}" > /dev/null
cd ..

echo -e "${GREEN}[+] Done: $OUT${END}"
ls -lh "$OUT"