import cv2
import pytesseract


def run_ocr(image_path, output_file):

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError(
            f"Could not load image: {image_path}"
        )

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    gray = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2
    )

    text = pytesseract.image_to_string(
        gray,
        config="--psm 6"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(text)

    return text