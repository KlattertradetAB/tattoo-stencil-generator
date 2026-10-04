import argparse

from app.stencil_generator import generate_stencil
from app.styles import STYLES, parse_color


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a tattoo stencil from a reference image.")
    parser.add_argument("--input", required=True, help="Path to the reference image")
    parser.add_argument("--output", required=True, help="Path to save the stencil PNG")
    parser.add_argument("--style", choices=sorted(STYLES), default="medium", help="Preset shading style")
    parser.add_argument("--line-weight", type=int, default=None, help="Override line weight")
    parser.add_argument("--hatch-spacing", type=int, default=None, help="Override hatch spacing")
    parser.add_argument("--outline-color", default=None, help="Optional outline color as r,g,b")
    parser.add_argument("--hatch-color", default=None, help="Optional hatch color as r,g,b")
    parser.add_argument("--guide-bg", default=None, help="Optional guide box background color as r,g,b")
    parser.add_argument("--guide-border", default=None, help="Optional guide box border color as r,g,b")
    args = parser.parse_args()

    generate_stencil(
        args.input,
        args.output,
        style=args.style,
        line_weight=args.line_weight,
        hatch_spacing=args.hatch_spacing,
        outline_color=parse_color(args.outline_color) if args.outline_color else None,
        hatch_color=parse_color(args.hatch_color) if args.hatch_color else None,
        guide_bg=parse_color(args.guide_bg) if args.guide_bg else None,
        guide_border=parse_color(args.guide_border) if args.guide_border else None,
    )
    print(f"Stencil generated at: {args.output}")


if __name__ == "__main__":
    main()
