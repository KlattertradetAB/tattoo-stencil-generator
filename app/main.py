from __future__ import annotations

STYLES = {
    "fine": {
        "line_weight": 1,
        "hatch_spacing": 10,
        "outline_color": (18, 18, 26),
        "hatch_color": (120, 140, 255),
        "guide_bg": (239, 243, 255),
        "guide_border": (84, 96, 166),
    },
    "medium": {
        "line_weight": 1,
        "hatch_spacing": 8,
        "outline_color": (18, 18, 26),
        "hatch_color": (120, 140, 255),
        "guide_bg": (239, 243, 255),
        "guide_border": (84, 96, 166),
    },
    "bold": {
        "line_weight": 2,
        "hatch_spacing": 6,
        "outline_color": (18, 18, 26),
        "hatch_color": (90, 110, 220),
        "guide_bg": (233, 238, 255),
        "guide_border": (70, 82, 150),
    },
}


def parse_color(value: str | None) -> tuple[int, int, int] | None:
    if value is None:
        return None
    try:
        parts = [int(part.strip()) for part in value.split(",")]
        if len(parts) != 3:
            raise ValueError
        return tuple(parts)
    except ValueError as exc:
        raise ValueError(f"Invalid color format: {value}. Use r,g,b") from exc


def resolve_style(
    style_name: str = "medium",
    line_weight: int | None = None,
    hatch_spacing: int | None = None,
    outline_color: tuple[int, int, int] | str | None = None,
    hatch_color: tuple[int, int, int] | str | None = None,
    guide_bg: tuple[int, int, int] | str | None = None,
    guide_border: tuple[int, int, int] | str | None = None,
) -> dict:
    style_key = (style_name or "medium").lower()
    if style_key not in STYLES:
        raise ValueError(f"Unknown style: {style_name}. Available styles: {sorted(STYLES)}")

    cfg = STYLES[style_key].copy()

    if line_weight is not None:
        cfg["line_weight"] = line_weight
    if hatch_spacing is not None:
        cfg["hatch_spacing"] = hatch_spacing

    if isinstance(outline_color, str):
        outline_color = parse_color(outline_color)
    if isinstance(hatch_color, str):
        hatch_color = parse_color(hatch_color)
    if isinstance(guide_bg, str):
        guide_bg = parse_color(guide_bg)
    if isinstance(guide_border, str):
        guide_border = parse_color(guide_border)

    if outline_color is not None:
        cfg["outline_color"] = tuple(outline_color)
    if hatch_color is not None:
        cfg["hatch_color"] = tuple(hatch_color)
    if guide_bg is not None:
        cfg["guide_bg"] = tuple(guide_bg)
    if guide_border is not None:
        cfg["guide_border"] = tuple(guide_border)

    return cfg


__all__ = ["STYLES", "parse_color", "resolve_style"]
