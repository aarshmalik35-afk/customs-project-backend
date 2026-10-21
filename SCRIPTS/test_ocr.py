import cv2
import pytesseract

img = cv2.imread("UPLOADS/latest_invoice.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray = cv2.resize(gray, None, fx=2, fy=2)

text = pytesseract.image_to_string(
    gray,
    config="--psm 6"
)

with open("OUTPUT/invoice_text.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("OCR completed successfully")
print(text)