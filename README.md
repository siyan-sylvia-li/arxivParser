# arxivParser
This tool is completely customizable for converting the arxiv email you receive daily to a list of relevant papers, and then reading the abstracts out loud using Google Text-to-speech!! It is for academics / paper-readers who work better with audio.

Your arxiv email usually looks like this:
![image](https://github.com/siyan-sylvia-li/arxivParser/assets/32021903/db75e295-1270-434e-8df6-000175668a1c)

But what if it can now look like this?
![image](https://github.com/siyan-sylvia-li/arxivParser/assets/32021903/eb748bc1-609d-46eb-a7d8-52b40682352c)

Complete with keyword specification? That sure sounds nice!

Here are the steps you need to get the parser kicking and working locally. I am not yet hosting it on a public site, so you would need to set up Google text-to-speech yourself, which should just be about setting up Google Cloud Platform, then creating a project and adding Google Text-to-speech to it. 

## Setting Up
1. If you don't have daily arxiv emails and want to sign up for one, please follow [this link](https://info.arxiv.org/help/subscribe.html)
2. You should also sign up for Google Cloud Platform if you haven't already, and then make a project specifically for arxivParser, and then add [Google Text-to-Speech](https://cloud.google.com/text-to-speech)
3. Create a conda environment using the `environment.yml` file attached
```bash
conda env create -f environment.yml
```
4. Run the flask app; there will likely be some error if this is your first time. If you haven't yet, you should run `gcloud auth login` to log in as your GCP user. Make sure your default project is the project for arxivParser.
```bash
python3 app.py
```

## Tool Workflow
1. Download your .eml file. You can download this by downloading your arxiv email message directly.
2. Specify the keyword / key phrase you want to look up papers about; SentenceTransformer would then be used to match individual articles to the keyword you specify.
3. Convert the relevant papers to audio; this may take a hot second.
4. Play individual audios or play all audio clips! These audio clips will be stored in `static/audio` folder in case you want to go find them. You can specify the voice used by Google text-to-speech in `helpers/read_to_audio.py`.

### Direct Reading-Out-Loud
If you just want something read out loud to you, you can copy and paste the content directly into the "Raw Text" text box and continue with the workflow.
