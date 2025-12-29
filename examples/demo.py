#!/usr/bin/env python3
"""
Demo script for AntPorter Python API.

This script demonstrates how to use AntPorter programmatically.
"""

import os
import tempfile
from pathlib import Path
from antporter import FileSplitter, FileMerger, MetadataManager


def main():
    """Run the demo."""
    print("=" * 60)
    print("AntPorter Demo")
    print("=" * 60)
    
    # Create temporary directory
    temp_dir = Path(tempfile.gettempdir()) / "antporter_demo"
    temp_dir.mkdir(exist_ok=True)
    
    # Create test file (10MB)
    print("\n1. Creating test file (10MB)...")
    test_file = temp_dir / "test_data.bin"
    with open(test_file, 'wb') as f:
        f.write(os.urandom(10 * 1024 * 1024))
    print(f"✓ Created: {test_file}")
    
    # Split file
    print("\n2. Splitting file into 3MB chunks...")
    chunks_dir = temp_dir / "chunks"
    chunks_dir.mkdir(exist_ok=True)
    
    splitter = FileSplitter.from_size_string(
        input_file=test_file,
        chunk_size_str="3MB",
        output_dir=chunks_dir
    )
    metadata_path = splitter.split()
    print(f"✓ Split complete: {metadata_path}")
    
    # Show info
    print("\n3. Metadata information:")
    manager = MetadataManager(metadata_path)
    print(f"   File: {manager.data['original_filename']}")
    print(f"   Size: {manager.data['original_size']:,} bytes")
    print(f"   Chunks: {manager.data['chunk_count']}")
    
    # Merge file
    print("\n4. Merging chunks...")
    output_dir = temp_dir / "output"
    output_dir.mkdir(exist_ok=True)
    
    merger = FileMerger(
        metadata_file=metadata_path,
        output_dir=output_dir,
        verify=True
    )
    merged_file = merger.merge()
    print(f"✓ Merge complete: {merged_file}")
    
    # Verify
    print("\n5. Verifying integrity...")
    original_md5 = MetadataManager.calculate_md5(test_file)
    merged_md5 = MetadataManager.calculate_md5(merged_file)
    
    if original_md5 == merged_md5:
        print("✓ Verification successful! Files are identical.")
    else:
        print("✗ Verification failed!")
    
    # Cleanup
    print("\n6. Cleaning up...")
    import shutil
    shutil.rmtree(temp_dir)
    print("✓ Cleanup complete")
    
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
