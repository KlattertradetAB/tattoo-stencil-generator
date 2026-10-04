from pathlib import Path

from app.stencil_generator import generate_stencil


def test_generate_stencil_creates_file(tmp_path):
    source = Path(__file__).resolve().parent.parent / "examples" / "sample_reference.jpg"

    if not source.exists():
        source = tmp_path / "sample_reference.jpg"
        source.write_bytes(b"\x89PNG\r\n\x1a\n")

    output = tmp_path / "stencil.png"
    generated = generate_stencil(str(source), str(output))

    assert generated == str(output)
    assert output.exists()
    assert output.stat().st_size > 0
