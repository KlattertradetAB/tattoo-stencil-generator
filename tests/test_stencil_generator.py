from pathlib import Path

from PIL import Image, ImageDraw

from app.stencil_generator import generate_stencil


def _make_test_image(path: Path) -> None:
    image = Image.new("RGB", (500, 500), "white")
    draw = ImageDraw.Draw(image)
    draw.ellipse((120, 90, 380, 420), fill=(130, 150, 180))
    draw.rectangle((200, 220, 300, 360), fill=(90, 120, 150))
    image.save(path)


def test_generate_stencil_creates_file(tmp_path):
    source = tmp_path / "sample_reference.png"
    _make_test_image(source)

    output = tmp_path / "stencil.png"
    generated = generate_stencil(str(source), str(output))

    assert generated == str(output)
    assert output.exists()
    assert output.stat().st_size > 0
