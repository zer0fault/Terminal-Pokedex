"""Type matchup tab showing offensive and defensive effectiveness."""
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static
from rich.text import Text

from src.models.type_info import TypeEffectiveness
from src.models.pokemon import PokemonDetail


class TypeTab(VerticalScroll):
    """Tab content showing type matchups for the Pokemon's types."""

    def compose(self) -> ComposeResult:
        yield Static("Select a Pokemon to view type matchups", id="type-content")

    def load_type_matchups(
        self,
        detail: PokemonDetail,
        type_data: dict[str, TypeEffectiveness],
    ) -> None:
        """Display combined type effectiveness for dual-type Pokemon."""
        content = self.query_one("#type-content", Static)
        text = Text()

        if not type_data:
            text.append("Type data not available", style="dim")
            content.update(text)
            return

        # Calculate combined defensive matchups for dual-type Pokemon
        defensive_matchups = self._calculate_defensive_matchups(type_data)

        # Offensive section
        text.append("OFFENSIVE (Attack Effectiveness)\n", style="bold underline")
        text.append("\n")

        all_super_effective = set()
        all_not_very_effective = set()
        all_no_effect = set()

        for type_name, type_info in type_data.items():
            all_super_effective.update(type_info.double_damage_to)
            all_not_very_effective.update(type_info.half_damage_to)
            all_no_effect.update(type_info.no_damage_to)

        if all_super_effective:
            text.append("  Super Effective (2×): ", style="bold green")
            text.append(", ".join(sorted(t.title() for t in all_super_effective)))
            text.append("\n\n")

        if all_not_very_effective:
            text.append("  Not Very Effective (½×): ", style="bold #FF9800")
            text.append(", ".join(sorted(t.title() for t in all_not_very_effective)))
            text.append("\n\n")

        if all_no_effect:
            text.append("  No Effect (0×): ", style="bold red")
            text.append(", ".join(sorted(t.title() for t in all_no_effect)))
            text.append("\n\n")

        text.append("\n")

        # Defensive section
        text.append("DEFENSIVE (Damage Taken)\n", style="bold underline")
        text.append("\n")

        # Group by multiplier
        for multiplier in [4.0, 2.0, 0.5, 0.25, 0.0]:
            types_at_multiplier = [
                t for t, m in defensive_matchups.items() if m == multiplier
            ]
            if types_at_multiplier:
                if multiplier == 4.0:
                    text.append("  4× Weak to: ", style="bold red")
                    color = "red"
                elif multiplier == 2.0:
                    text.append("  2× Weak to: ", style="bold #FF9800")
                    color = "#FF9800"
                elif multiplier == 0.5:
                    text.append("  ½× Resists: ", style="bold green")
                    color = "green"
                elif multiplier == 0.25:
                    text.append("  ¼× Resists: ", style="bold green")
                    color = "green"
                else:  # 0.0
                    text.append("  Immune to: ", style="bold cyan")
                    color = "cyan"

                text.append(", ".join(sorted(t.title() for t in types_at_multiplier)))
                text.append("\n\n")

        content.update(text)

    def _calculate_defensive_matchups(
        self,
        type_data: dict[str, TypeEffectiveness],
    ) -> dict[str, float]:
        """Calculate combined defensive type matchups."""
        matchups: dict[str, float] = {}

        # Start with all types at 1.0 multiplier
        all_types = set()
        for type_info in type_data.values():
            all_types.update(type_info.double_damage_from)
            all_types.update(type_info.half_damage_from)
            all_types.update(type_info.no_damage_from)

        for attack_type in all_types:
            multiplier = 1.0
            for type_info in type_data.values():
                if attack_type in type_info.double_damage_from:
                    multiplier *= 2.0
                elif attack_type in type_info.half_damage_from:
                    multiplier *= 0.5
                elif attack_type in type_info.no_damage_from:
                    multiplier = 0.0
                    break

            if multiplier != 1.0:
                matchups[attack_type] = multiplier

        return matchups
