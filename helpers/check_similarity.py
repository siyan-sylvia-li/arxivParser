from sentence_transformers import SentenceTransformer, util
from nltk import sent_tokenize
from .arxiv_passage import ArxivPassage
from typing import List


sentence_bert = SentenceTransformer("all-mpnet-base-v2")


def find_similarity(word, abstract, title):
    # First split into individual sentences
    abs_sentences = sent_tokenize(abstract)
    key_word_vec = sentence_bert.encode([word])[0]
    all_rel_vecs = sentence_bert.encode(abs_sentences + [title])
    # find the top three items with high similarity
    all_sims = [util.cos_sim(key_word_vec, sv) for sv in all_rel_vecs]
    all_sims.sort(reverse=True)
    return sum(all_sims[:3])


def sort_list_of_passage(kw: str, arxiv_list: List[ArxivPassage]):
    sim_list = []
    for x in arxiv_list:
        score = find_similarity(kw, x.abstract, x.title)
        if score > 1:
            sim_list.append((score, x))
    sim_list.sort(reverse=True, key=lambda a: a[0])
    return [a[1] for a in sim_list]


