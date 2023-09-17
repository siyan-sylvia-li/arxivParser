"""
\\
arXiv:2309.02553
Date: Tue, 5 Sep 2023 19:40:45 GMT   (1295kb,D)

Title: Automating Behavioral Testing in Machine Translation
Authors: Javier Ferrando, Matthias Sperber, Hendra Setiawan, Dominic Telaar,
  Sa\v{s}a Hasan
Categories: cs.CL cs.AI
\\
  Behavioral testing in NLP allows fine-grained evaluation of systems by
examining their linguistic capabilities through ...
\\ ( https://arxiv.org/abs/2309.02553 ,  1295kb)
"""

import re

class ArxivPassage:
    def __init__(self, date="", title="", authors="", category="", abstract="", link="https://arxiv.org/"):
        self.date = date
        self.title = title
        self.authors = authors
        self.category = category
        self.abstract = abstract
        self.link = link

    def __str__(self):
        return f"ArxivPassage with Title={self.title}; Authors={self.authors}; Category={self.category}; Abstract={self.abstract}; at Link {self.link}"

    def to_dict(self):
        return {
            "Title": self.title,
            "Date": self.date,
            "Authors": self.authors,
            "Category": self.category,
            "Abstract": self.abstract,
            "Link": self.link
        }


def parse_arxiv(arxiv_text: str, final_obj: ArxivPassage):
    arxiv_lines = arxiv_text.split("\n")
    for i in range(len(arxiv_lines)):
        arxiv_lines[i] = arxiv_lines[i].strip()
        if len(arxiv_lines[i]) == 0 or arxiv_lines[i].startswith("arXiv:"):
            continue
        elif arxiv_lines[i].startswith("Date: "):
            date_data = arxiv_lines[i][4:].strip()
            if "(" in date_data:
                date_data = date_data[:date_data.index("(")].strip()
            final_obj.date = date_data
        elif arxiv_lines[i].startswith("Title:"):
            final_obj.title = arxiv_lines[i].replace("Title: ", "")
        elif arxiv_lines[i - 1].startswith("Title:") and not arxiv_lines[i].startswith("Authors: "):
            final_obj.title += " " + arxiv_lines[i]
        elif arxiv_lines[i].startswith("Authors: "):
            authors = arxiv_lines[i].replace("Authors: ", "")
            final_obj.authors = authors
        elif arxiv_lines[i - 1].startswith("Authors:") and not arxiv_lines[i].startswith("Categories:"):
            final_obj.authors += " " + arxiv_lines[i]
        elif arxiv_lines[i].startswith("Categories: "):
            final_obj.category = arxiv_lines[i].replace("Categories: ", "")
    return final_obj


def parse_abstract(abstract_text: str, final_obj: ArxivPassage):
    abstract_ts = abstract_text.replace("\n", " ")
    final_obj.abstract = abstract_ts
    return final_obj


def parse_link(link_text: str, final_obj: ArxivPassage):
    start_ind = link_text.index("(") + 1
    end_ind = link_text.index(",")
    link_text = link_text[start_ind: end_ind].strip()
    final_obj.link = link_text
    return final_obj


def parse_passage(full_text):
    all_lines = full_text.split("\\\\")
    while "\n" in all_lines:
        all_lines.remove("\n")
    while "" in all_lines:
        all_lines.remove("")
    while " " in all_lines:
        all_lines.remove(" ")
    all_lines = [x.lstrip("\n") for x in all_lines]
    # if there are two of such segments, then it is an update, else a full passage
    final_passage = ArxivPassage()
    if len(all_lines) == 3:
        final_passage = parse_arxiv(all_lines[0], final_passage)
        final_passage = parse_abstract(all_lines[1], final_passage)
        final_passage = parse_link(all_lines[2], final_passage)
    final_passage.title = final_passage.title.strip()
    final_passage.abstract = final_passage.abstract.strip()
    final_passage.date = final_passage.date.strip()
    return final_passage


def split_into_articles(full_text_all):
    all_arxiv_chunks = re.split(r"---(-)+", full_text_all)
    all_passages = []
    for a in all_arxiv_chunks:
        if re.match(r"^(-)+", a):
            pass
        parsed_pass = parse_passage(a)
        if parsed_pass.title != "":
            all_passages.append(parsed_pass)
    return all_passages


