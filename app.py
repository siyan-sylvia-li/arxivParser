import glob

from flask import Flask, render_template, request, session
from helpers.arxiv_passage import ArxivPassage, split_into_articles
from helpers.check_similarity import sort_list_of_passage
from flask_session import Session
from flask_cors import CORS
from helpers.read_to_audio import text_to_wav
import logging
import sys
sys.path.append("helpers")

# Create the Flask app instance
app = Flask(__name__)

LOGGER = logging.getLogger('gunicorn.error')

SECRET_KEY = 'ArxivParser'
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)

Session(app)
CORS(app)


@app.route('/', methods=["POST"])
def upload_sml():
    data = "Uploaded"
    if request.method == 'POST':
        file = request.files['uploaded-file']
        all_data = b"".join(file.stream.readlines()).decode('utf-8')
        if "\\\\\r\narXiv:" in all_data:
            ind = all_data.index("\\\\\r\narXiv:")
            all_data = all_data[ind:]
        data = all_data.replace("\r", "")

    return render_template("index.html", sml=data)


@app.route("/convert", methods=["POST"])
def convert_arxiv():
    data_request = request.json
    session["sml_content"] = data_request['sml']
    if "\\\\" in session["sml_content"]:
        all_articles = split_into_articles(session["sml_content"])
        session["parsed_articles"] = all_articles
        for x in all_articles[:5]:
            print(x)
        keyword = data_request["keyword"]
        new_list = sort_list_of_passage(keyword, all_articles)
        new_list = [x.to_dict() for x in new_list]
        for it in new_list:
            if len(glob.glob("static/audio/" + it["Link"].replace("https://arxiv.org/abs/", "") + ".wav")) == 0:
                text_to_wav(
                    it["Title"] + "..." + it["Authors"] + "..." + it["Abstract"],
                    "static/audio/" + it["Link"].replace("https://arxiv.org/abs/", "")
                )
        return new_list
    else:
        final_article = ArxivPassage()
        final_article.abstract = session["sml_content"]
        final_article.link = "https://arxiv.org/abs/uploaded"
        text_to_wav(session["sml_content"], "static/audio/uploaded")
        return [final_article.to_dict()]



# Define a route for the root URL
@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")


# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
