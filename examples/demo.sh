#!/bin/bash
# Demo script for AntPorter CLI

echo "==================================="
echo "AntPorter CLI Demo"
echo "==================================="
echo ""

# Create test file (10MB)
echo "1. Creating test file (10MB)..."
dd if=/dev/urandom of=test_file.bin bs=1M count=10 2>/dev/null
echo "✓ Test file created"
echo ""

# Split the file
echo "2. Splitting file into 3MB chunks..."
antporter split test_file.bin --chunk-size 3MB --output-dir ./chunks
echo ""

# Show info
echo "3. Showing metadata information..."
antporter info ./chunks/test_file.bin.meta.json
echo ""

# Merge the file
echo "4. Merging chunks..."
antporter merge ./chunks/test_file.bin.meta.json --output-dir ./output
echo ""

# Verify
echo "5. Verifying integrity..."
original_md5=$(md5sum test_file.bin | cut -d' ' -f1)
merged_md5=$(md5sum ./output/test_file.bin | cut -d' ' -f1)

if [ "$original_md5" == "$merged_md5" ]; then
    echo "✓ Verification successful!"
    echo "  MD5: $original_md5"
else
    echo "✗ Verification failed!"
fi
echo ""

# Cleanup
echo "6. Cleaning up..."
rm -rf test_file.bin ./chunks ./output
echo "✓ Cleanup complete"
echo ""

echo "==================================="
echo "Demo completed!"
echo "==================================="
