import os
import io
import csv
import fitz
from google.cloud import vision
from google.cloud.vision_v1 import types


client = vision.ImageAnnotatorClient()

# Initialize an empty list to store the highlighted text
highlighted_text = []

doc = fitz.open('Naked Money.epub')

for page in doc:
    annots = page.annots()
    for annot in annots:
        if annot.type[0] == 8:
            rect = annot.rect
            pix = page.get_pixmap(clip=rect)
            pix.save('highlight.png')

            with io.open('highlight.png', 'rb') as image_file:
                content = image_file.read()

            image = vision.Image(content=content)

            response = client.text_detection(image=image)
            ocr_text = response.text_annotations[0].description

            highlighted_text.append(ocr_text)

doc.close()

print(highlighted_text)