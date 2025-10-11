import random
from itertools import groupby
from pathlib import Path
from string import printable
from typing import Any, Generator, Literal, Never

import pandas as pd


def get_cah_cards() -> dict[str, pd.DataFrame]:
    path = Path(__file__).parent.parent.joinpath('static/cards.ods')
    xl = pd.ExcelFile(path)
    return {str(sheet): xl.parse(sheet) for sheet in xl.sheet_names}


def get_lang_pack(lang: str) -> dict[str, pd.Series]:
    dfs = [cards[pack] for pack in packs[lang]]
    lang_pack = pd.concat(dfs, ignore_index=True)
    black = lang_pack['black'].dropna().reset_index(drop=True)
    white = lang_pack['white']
    return {'black': black, 'white': white}


def get_card_generator(
    language: str,
    b_or_w: Literal['black', 'white'],
) -> dict[str, Generator[str, Any, Never]]:
    lang_pack = lang_packs[language][b_or_w]
    return {b_or_w: shuffler(lang_pack)}


def shuffler(sequence: pd.Series) -> Generator[str, Any, Never]:
    seq = list(range(len(sequence)))
    offset: int = len(seq) - 1
    while True:
        i = random.randint(0, offset)
        card = seq[i]
        seq[i], seq[offset] = seq[offset], seq[i]
        offset += -1 if offset > 0 else len(seq) - 1
        yield sequence[card]


cards = get_cah_cards()
packs = {k: list(g) for k, g in groupby(cards.keys(), key=lambda x: x[:2])}
lang_packs = {k: get_lang_pack(k) for k in packs}


if __name__ == '__main__':
    gen = get_card_generator('PL', 'white')['white']
    print(list(next(gen) for _ in range(10)))
