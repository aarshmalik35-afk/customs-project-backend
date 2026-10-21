import os
import cv2
import pytesseract

# Image path
import sys

if len(sys.argv) < 2:
    print("Usage: py ocr.py <image_path>")
    exit()

image_path = sys.argv[1]

print("=" * 50)
print("CUSTOMS OCR PROCESS")
print("=" * 50)

# Check current working directory
print("Current Folder:", os.getcwd())

# Check if file exists
if not os.path.exists(image_path):
    print(f"ERROR: File not found -> {image_path}")
    exit()

print(f"Found image: {image_path}")

# Read image
img = cv2.imread(image_path)

if img is None:
    print("ERROR: OpenCV could not load the image.")
    exit()

print("Image loaded successfully")

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Resize for better OCR
gray = cv2.resize(gray, None, fx=2, fy=2)

# OCR
text = pytesseract.image_to_string(
    gray,
    config="--psm 6"
)

# Create OUTPUT folder if missing
os.makedirs("OUTPUT", exist_ok=True)

# Save OCR text
output_file = r"OUTPUT\invoice_text.txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(text)

print(f"OCR text saved to: {output_file}")
print("=" * 50)
print("OCR COMPLETED SUCCESSFULLY")
print("=" * 50)

# Preview first 500 chars
print(text[:500])