import os

from extract_text import get_highlighted_text
from pdf_to_card import extract_questions
from text_to_anki import write_to_anki
from write_to_txt import write_to_txt
from flask import Flask, request, render_template, session
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp'

app = Flask(__name__)
app.secret_key = 'any random string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze_pdf', methods=['POST'])
def analyze_pdf():
    pdf_file = request.files['pdf_file']
    filename = secure_filename(request.files['pdf_file'].filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(file_path)

    extracted_text = get_highlighted_text(file_path)
    print('extracted text is ', extracted_text)

    result_list = []

    for item in extracted_text:
        questions = extract_questions(item)
        questions_iterator = questions.split('\n')
        # print(f'the result for {item} is {questions_iterator}')

        current_qa = {}

        for line in questions_iterator:
            response = line.split(';')
            if len(response) == 2:
                current_qa['question'] = response[0].strip()
                current_qa['answer'] = response[1].strip()
                result_list.append([item, current_qa['question'], current_qa['answer']])
                current_qa = {}
            else:
                print('Trouble with this pair : ')
                print(response)

    # print('result list is ', result_list)
    session['num_rows'] = len(result_list)
    session['result_list'] = result_list

    return render_template('index.html', data=result_list)

def analyze_pdf_file(pdf_file):
    # Do your processing on the PDF file here and return the results as a string and a list of strings
    # For example, you could use the PyPDF2 library to extract text from the PDF
    result_str = "PDF file uploaded and analyzed"
    result_list = ["string1", "string2", "string3"]
    
    return result_str, result_list

@app.route('/upload_to_anki', methods=['POST'])
def upload_to_anki():
    # TODO(ev) this is not efficient
    checkbox_values = []
    cards_to_write = []
    for i in range(session['num_rows']):
        print(f'should upload {i} has value', request.form.get(f'should_upload_{i}', '0'))
        checkbox_value = request.form.get(f'should_upload_{i}', '0')
        checkbox_values.append(checkbox_value)
        if checkbox_value == '1':
            cards_to_write.append([request.form.get(f'item_{i}_1'), request.form.get(f'item_{i}_2')])
    # data = request.get_json()
    # text = data['text']
    # result = upload_to_anki(text)
    write_to_anki(cards_to_write)
    return render_template('index.html')

@app.route('/upload_to_txt', methods=['POST'])
def upload_to_txt():
    # TODO(ev) this is not efficient
    checkbox_values = []
    cards_to_write = []
    for i in range(session['num_rows']):
        print(f'should upload {i} has value', request.form.get(f'should_upload_{i}', '0'))
        checkbox_value = request.form.get(f'should_upload_{i}', '0')
        checkbox_values.append(checkbox_value)
        if checkbox_value == '1':
            cards_to_write.append([request.form.get(f'item_{i}_1'), request.form.get(f'item_{i}_2')])

    print(cards_to_write)

    write_to_txt(cards_to_write)
    return render_template('index.html')

    # write_to_anki(cards_to_write)

# def upload_to_anki(text):
#     # Do your processing on the text here and return the results as a string
#     # For example, you could use the AnkiConnect API to create a new note in Anki
    
#     return "Text uploaded to Anki!"

if __name__ == '__main__':
    app.run(debug=True)