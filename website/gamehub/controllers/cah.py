from collections.abc import Iterator
from itertools import groupby
from pathlib import Path

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


def get_cards_generators(lang: str) -> dict[str, Iterator[str]]:
    lang_pack = lang_packs[lang]
    return {
        'black': iter(lang_pack['black'].sample(frac=1)),
        'white': iter(lang_pack['white'].sample(frac=1)),
    }


cards = get_cah_cards()
packs = {k: list(g) for k, g in groupby(cards.keys(), key=lambda x: x[:2])}
lang_packs = {k: get_lang_pack(k) for k in packs.keys()}


if __name__ == '__main__':
    gens = get_cards_generators('PL')
    print(gens)
    black = gens['black']
    print(next(black), next(gens['white']))
