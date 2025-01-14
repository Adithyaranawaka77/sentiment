from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
from textblob import TextBlob, Word
import random
import time

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyse', methods=['POST'])  # Corrected spelling of the route
def analyse():
    start = time.time()
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        blob = TextBlob(rawtext)
        received_text = str(blob)
        blob_sentiment, blob_subjectivity = blob.sentiment.polarity, blob.sentiment.subjectivity
        number_of_tokens = len(list(blob.words))
        
        nouns = []
        for word, tag in blob.tags:
            if tag == 'NN':  # Corrected equality comparison
                nouns.append(word.lemmatize())  # Fixed the misspelled 'lemmatize'

        len_of_words = len(nouns)
        rand_words = random.sample(nouns, len_of_words) if len_of_words > 0 else []
        final_word = [Word(item).pluralize() for item in rand_words]

        summary = final_word
        end = time.time()
        final_time = end - start

        # Render results in 'index.html'
        return render_template(
            'index.html',
            received_text=received_text,
            number_of_tokens=number_of_tokens,
            blob_sentiment=blob_sentiment,
            blob_subjectivity=blob_subjectivity,
            summary=summary,
            final_time=final_time
        )