import argparse
from .stencil_generator import generate_stencil


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a tattoo stencil from a reference image.")
    parser.add_argument("--input", required=True, help="Path to the reference image")
    parser.add_argument("--output", required=True, help="Path to save the stencil PNG")
    args = parser.parse_args()

    result = generate_stencil(args.input, args.output)
    print(f"Stencil generated at: {result}")


if __name__ == "__main__":
    main()
