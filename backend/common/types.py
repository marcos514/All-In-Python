from dataclasses import dataclass, field
from typing import TypeAlias, Dict

from deep_translator import (GoogleTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator)
from enum import Enum

class Translators:
    GOOGLE = GoogleTranslator
    PONS = PonsTranslator
    LINGUEE = LingueeTranslator
    MYMEMORY= MyMemoryTranslator

# Class to represent text data with coordinates and metadata
@dataclass
class ImageLineTextData:
    x_first: int
    y_first: int
    x_last: int
    y_last: int
    width: int
    height: int
    text: str

# Correct syntax for type alias
TypeSentence: TypeAlias = Dict[str, ImageLineTextData]

# Class with a full text and all sentences in a dictionary
@dataclass
class ImageTextPosition:
    full_text: str
    all_sentences: dict[int, ImageLineTextData] = field(default_factory=dict)


class CloseAppException(Exception):
    pass
