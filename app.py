from flask import Flask, render_template, request, redirect, url_for
import wikipedia

app = Flask(__name__)

SUPPORTED_LANGUAGES = ['en', 'ru']


@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search']
        language = request.form.get('language', 'en')

        if language not in SUPPORTED_LANGUAGES:
            return "Неподдерживаемый язык"

        wikipedia.set_lang(language)

        try:
            suggestions = wikipedia.suggest(search_term)
            if suggestions:
                search_term = suggestions[0]

            results = wikipedia.search(search_term)
            summary = wikipedia.summary(results[0], sentences=2)
            return render_template('results.html', results=results, summary=summary, language=language)

        except wikipedia.exceptions.DisambiguationError as e:
            return render_template('disambiguation.html', options=e.options, search_term=search_term, language=language)
        except wikipedia.exceptions.PageError:
            return render_template('results.html', error="Статья не найдена", language=language)

    return render_template('search.html')


@app.route('/language/<lang>')
def set_language(lang):
    if lang in SUPPORTED_LANGUAGES:
        return redirect(url_for('search', language=lang))
    return "Неподдерживаемый язык"


if __name__ == '__main__':
    app.run(debug=True)