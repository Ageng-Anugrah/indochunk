from enum import Enum

from nltk import ParentedTree
from nltk.corpus import BracketParseCorpusReader

from utils.chunk_utils import ChunkType, Token

# Constituency Parsing Folde
root_folder = ""
file_name = r""

corpus_root = root_folder
file_pattern = file_name

tb = BracketParseCorpusReader(corpus_root, file_pattern)

import re

np_pattern = r"^NP.*"
sbar_pattern = r"^SBAR.*"
adjp_pattern = r"^ADJP.*"
ucp_pattern = r"^UCP.*"
advp_pattern = r"^ADVP.*|^RB"
pp_pattern = r"^PP.*"
# o_pattern = r"^CC.*"
vp_pattern = r"^VB|^MD"

txt = ""
for tree in tb.parsed_sents():
    tree = ParentedTree.convert(tree)

    # list for tokens
    tokens = []

    # get all leaves(tokens) from the tree
    leaves = [t for t in tree.subtrees(lambda t: t.height() == 2)]
    for idx, leaf in enumerate(leaves):
        # whether it is NP or else
        prev_chunk_tag = None
        try:
            prev_chunk_tag = tokens[-1].chunk_tag
        except IndexError:
            pass

        word = leaf[0]
        if leaf.label() in ["-NONE-", "-LRB-", "-RRB-"]:
            continue
        pos_tag = leaf.label()
        cur_parent = leaf

        while cur_parent != None:
            chunk_label = cur_parent.label()
            if re.search(np_pattern, chunk_label):
                chunk_label = "NP"
            elif re.search(sbar_pattern, chunk_label):
                chunk_label = "SBAR"
            elif re.search(adjp_pattern, chunk_label):
                chunk_label = "ADJP"
            elif re.search(ucp_pattern, chunk_label):
                chunk_label = "UCP"
            elif re.search(advp_pattern, chunk_label):
                chunk_label = "ADVP"
            elif re.search(pp_pattern, chunk_label):
                chunk_label = "PP"
            # elif re.search(o_pattern, chunk_label):
            #     chunk_label = "O"
            elif re.search(vp_pattern, chunk_label):
                chunk_label = "VP"

            if chunk_label in ChunkType._member_names_:
                if chunk_label == "O":
                    state = "O"
                elif prev_chunk_tag == chunk_label:
                    state = "I"
                else:
                    state = "B"

                tokens.append(Token(word, pos_tag, chunk_label, state))
                break
            prev_parent = cur_parent
            cur_parent = cur_parent.parent()
            if cur_parent != None and cur_parent.label() in ["S", "SINV"]:
                if re.match(r"[a-zA-z]+", word):
                    tokens.append(Token(word, pos_tag, "O", "O"))
                else:
                    tokens.append(Token(word, word, "O", "O"))
                break

    for token in tokens:
        txt += token.__str__() + "\n"
    txt += "\n"
