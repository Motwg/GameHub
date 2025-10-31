import uuid
from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass, field


@dataclass(slots=True)
class RoomController:
    status: str


@dataclass(slots=True)
class CahController(RoomController):
    queue: deque[tuple[uuid.UUID, str]]
    cah_master: tuple[uuid.UUID, str] = field(init=False)

    black: Iterator[str]
    white: Iterator[str]
    black_card: str = field(init=False)
    gaps: int = field(init=False)

    cards: dict[tuple[uuid.UUID, str], list[str]] = field(init=False, default_factory=dict)
    confirmed_cards: dict[tuple[uuid.UUID, str], list[int]] = field(
        init=False,
        default_factory=dict,
    )

    def __post_init__(self) -> None:
        self.prepare_next_round()

    def _next_master(self) -> None:
        self.cah_master = self.queue.popleft()
        self.queue.append(self.cah_master)

    def _give_cards(self, limit: int = 5) -> None:
        generator = self.white
        for m in self.queue:
            while len(self.cards.setdefault(m, [])) < limit:
                self.cards[m].append(next(generator))

    def prepare_next_round(self) -> None:
        self._give_cards()
        self._next_master()

        black_card = next(self.black)
        gaps = black_card.count('______')
        self.black_card = black_card
        self.gaps = gaps if gaps > 0 else 1

    def end_round(self) -> None:
        pass
