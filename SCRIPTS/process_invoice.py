import subprocess
import sys

if len(sys.argv) < 2:
    print("Usage: py process_invoice.py <image_path>")
    exit()

image_path = sys.argv[1]

print("Running OCR...")
subprocess.run(
    ["py", r"SCRIPTS\ocr.py", image_path],
    check=True
)

print("Running Field Extraction...")
subprocess.run(
    ["py", r"SCRIPTS\extract_fields.py"],
    check=True
)

print("Processing Complete!")