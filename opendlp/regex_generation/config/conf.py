from enum import Enum,unique

@unique
class RegexFlavour(Enum):
    Java = 'Java'
    Python = 'Python'

BPE_PAIR_PERCENT_THRESHOLD = 0.2
BPE_CHAR_PERCENT_THRESHOLD = 0.75

MAX_DEPTH = 7