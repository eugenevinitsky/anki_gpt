import os
import io
import csv
import fitz
from google.cloud import vision
from google.cloud.vision_v1 import types


client = vision.ImageAnnotatorClient()


def get_highlighted_text(filename):
    # Initialize an empty list to store the highlighted text
    highlighted_text = []

    doc = fitz.open(filename)

    for page in doc:
        annots = page.annots()
        for annot in annots:
            if annot.type[0] == 8:
                rect = annot.rect
                pix = page.get_pixmap(clip=rect)  # render page to an image
                pix.save('highlight.png')  # store image as a PNG

                with io.open('highlight.png', 'rb') as image_file:
                    content = image_file.read()

                image = vision.Image(content=content)

                response = client.text_detection(image=image)
                ocr_text = response.text_annotations[0].description
                ocr_text = ocr_text.replace('\n', ' ')

                highlighted_text.append(ocr_text)

    doc.close()

    return highlighted_text

if __name__ == '__main__':
    results = get_highlighted_text('test_pdf.pdf')
    # print(results)