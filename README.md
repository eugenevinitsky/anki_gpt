![output](https://github.com/eugenevinitsky/anki_gpt/assets/7660397/5efd5ce4-81bf-4cca-8bea-00bc1fad7c3d)

# Why?
Both of us are big Anki users but often find that writing the cards can be fairly dull. We built this to make it easy to convert PDFs into Anki cards.

Lowering the energy barrier to using Anki and making it more broadly accessible seems important. However, **getting practice writing your own cards is important for learning what type of cards do / don't work so don't just rely on this!**

# Installation
We're too lazy to host this for you so we've set this up as a locally hosted thing. 
There's a few things you need to install.

## Setting up your python environment
Make sure you have conda and then run
```
conda env create -f environment.yml
source activate anki_proj
```

## Setting up Google Cloud for Vision
We use Google Cloud to extract the highlighted segments before passing them into a PDF reader as we found that PDF readers were no good at getting highlighted chunks. Follow the instructions at the [Google Cloud API](https://pypi.org/project/google-cloud-vision/).

## Setting up OpenAI.
We create the cards using OpenAI's GPT. You need to have a key in your environment
called OPENAI_API_KEY. You can do this by either by pasting in your command line
```
export OPENAI_API_KEY="<YOUR SECRET KEY>"
```
or opening your shell configuration file (most often `~/.bashrc`) and pasting the export
line into there.

## Setting up the direct connection to Anki.
To make life easier, we have two convenience modes for exporting your anki cards.
First of all, we have two buttons at the bottom of the flask webpage. One 
`export to txt` writes the results to a line-separated file called `results.txt`.
The other uses the [Anki Connect](https://ankiweb.net/shared/info/2055492159) app. To set 
this up, follow the link, then go into the `text_to_anki.py` file, change the `DECK_NAME`
variable to your desired deck and run it.

# Running the app.
To run this app, simply run
```
flask --app app run
```
which will host the app locally. Then open http://127.0.0.1:5000.

For testing it out, we provide a convenient pdf called `test_pdf.pdf`. It's a fairly big PDF, so it'll take about 30s to a minute to run. Enjoy learning about Passover!

# How do I use this well?
We provide some example demos in the demo_pdfs folder. Take a look at the highlighting pattern there and mess around with it!

## Highlight intelligently
Keep in mind, when you highlight a section of text, you bring a lot of context into it. GPT does not have this context! It's **best if you highlight one or two sentences that have very clear, unambiguous meaning.**
### Don't highlight huge chunks of text
If you highlight an entire page, I have no idea what it'll do. Probably something dumb.
### Don't highlight half of a line or an incomplete sentence.
If you highlight just a few words, GPT decides to fill things in for you. For example, passing the single line **kill the kernel and rerun all cells** will inexplicably generate 20 cards about machine learning. Maybe a better prompt would fix this but we haven't found it yet.

## Watch out for math results
You probably have to correct the extracted outputs from equations. PDF readers don't always extract math correctly.
