"""Evolution chain data models."""
from dataclasses import dataclass, field


@dataclass(slots=True)
class EvolutionTrigger:
    """How a Pokemon evolves."""
    trigger: str
    min_level: int | None
    item: str | None
    held_item: str | None
    min_happiness: int | None
    time_of_day: str | None
    known_move: str | None
    location: str | None

    def display_text(self) -> str:
        """Human-readable evolution condition."""
        if self.min_level:
            return f"Lv.{self.min_level}"
        if self.item:
            return self.item.replace("-", " ").title()
        if self.min_happiness:
            tod = f" ({self.time_of_day})" if self.time_of_day else ""
            return f"Happiness {self.min_happiness}{tod}"
        if self.trigger == "trade":
            if self.held_item:
                return f"Trade ({self.held_item.replace('-', ' ').title()})"
            return "Trade"
        if self.known_move:
            return f"Know {self.known_move.replace('-', ' ').title()}"
        if self.location:
            return f"At {self.location.replace('-', ' ').title()}"
        if self.time_of_day:
            return f"Level up ({self.time_of_day})"
        return self.trigger.replace("-", " ").title()


@dataclass(slots=True)
class EvolutionNode:
    """A node in the evolution tree."""
    species_name: str
    species_id: int
    triggers: list[EvolutionTrigger] = field(default_factory=list)
    evolves_to: list["EvolutionNode"] = field(default_factory=list)


@dataclass(slots=True)
class EvolutionChain:
    """Full evolution chain."""
    id: int
    root: EvolutionNode
