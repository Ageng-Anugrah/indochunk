from enum import Enum


class Token:
    def __init__(self, token, pos_tag=None, chunk_tag=None, pos_tag_bio=None):
        self.token = token
        self.pos_tag = pos_tag
        self.chunk_tag = chunk_tag
        self.pos_tag_bio = pos_tag_bio

    def __str__(self):
        if self.pos_tag_bio != "O":
            return f"{self.token} {self.pos_tag} {self.pos_tag_bio}-{self.chunk_tag}"
        return f"{self.token} {self.pos_tag} {self.pos_tag_bio}"

    def __repr__(self):
        return self.__str__()


class ChunkType(Enum):
    NP = 1
    VP = 2
    ADVP = 3
    ADJP = 4
    PP = 5
    SBAR = 6
    CONJP = 7
    PRT = 8
    INTJ = 9
    LST = 10
    UCP = 11
    O = 12
