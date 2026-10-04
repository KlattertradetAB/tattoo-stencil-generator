from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFilter
import cv2
import numpy as np

WHITE = (255, 255, 255)
OUTLINE = (22, 22, 30)
SHADING_BLUE = (103, 141, 255)
GUIDE_BG = (236, 240, 255)
GUIDE_BORDER = (80, 96, 160)


def _load_image(path: str) -> Image.Image:
    image = Image.open(path).convert("RGBA")

    background = Image.new("RGBA", image.size, WHITE + (255,))
    image = Image.alpha_composite(background, image)
    image = image.convert("RGB")
    return image


def _center_subject(img: Image.Image) -> Image.Image:
    gray = ImageOps.grayscale(img)
    arr = np.array(gray)
    mask = arr < 245
    ys, xs = np.where(mask)

    if xs.size == 0 or ys.size == 0:
        return img

    x0, x1 = xs.min(), xs.max()
    y0, y1 = ys.min(), ys.max()
    margin = 40
    x0 = max(0, x0 - margin)
    y0 = max(0, y0 - margin)
    x1 = min(img.width, x1 + margin)
    y1 = min(img.height, y1 + margin)
    cropped = img.crop((x0, y0, x1, y1))
    return cropped


def _resize_for_processing(img: Image.Image, max_size: int = 1800) -> Image.Image:
    if max(img.size) > max_size:
        img.thumbnail((max_size, max_size))
    return img


def _edge_map(img: Image.Image) -> np.ndarray:
    gray = ImageOps.grayscale(img)
    gray = ImageEnhance.Contrast(gray).enhance(1.8)
    arr = np.array(gray)
    edges = cv2.Canny(arr, 40, 120)
    return edges


def _apply_outline(img: Image.Image, edges: np.ndarray) -> Image.Image:
    overlay = Image.new("RGB", img.size, WHITE)
    pix = overlay.load()

    for y in range(img.height):
        for x in range(img.width):
            if edges[y, x] > 0:
                pix[x, y] = OUTLINE

    # Add a subtle cleanup pass to keep the linework crisp.
    overlay = overlay.filter(ImageFilter.MaxFilter(3))
    return overlay


def _hatch_shading(img: Image.Image, hatch_spacing: int = 8) -> Image.Image:
    hatch = Image.new("RGB", img.size, WHITE)
    draw = ImageDraw.Draw(hatch)
    gray = ImageOps.grayscale(img)
    arr = np.array(gray)

    for y in range(0, img.height, hatch_spacing):
        for x in range(0, img.width, hatch_spacing):
            val = arr[y, x] if 0 <= y < arr.shape[0] and 0 <= x < arr.shape[1] else 255
            darkness = max(0, 255 - val)

            if darkness < 20:
                continue

            density = max(1, int((darkness / 255) * 4))
            length = 8 + density * 2
            for i in range(density):
                offset = i * 2
                draw.line(
                    (x + offset, y, x + offset + length, y + length),
                    fill=(
                        120 + int(darkness * 0.15),
                        140 + int(darkness * 0.20),
                        255,
                    ),
                    width=1,
                )

    return hatch


def _add_guide_box(img: Image.Image) -> Image.Image:
    result = img.copy()
    draw = ImageDraw.Draw(result)

    box_w = int(result.width * 0.26)
    box_h = int(result.height * 0.08)
    padding = 18
    x0 = padding
    y0 = padding
    x1 = x0 + box_w
    y1 = y0 + box_h

    draw.rounded_rectangle((x0, y0, x1, y1), radius=8, fill=GUIDE_BG, outline=GUIDE_BORDER, width=2)

    try:
        import PIL.ImageFont as ImageFont
        font = ImageFont.load_default()
    except Exception:
        font = None

    text = "SHADING GUIDE"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]
    text_x = x0 + (box_w - text_w) // 2
    text_y = y0 + (box_h - text_h) // 2
    draw.text((text_x, text_y), text, fill=GUIDE_BORDER, font=font)

    # Add a small reference strip inside the box to show hatch density.
    density_y = y0 + box_h - 12
    draw.line((x0 + 12, density_y, x1 - 12, density_y), fill=GUIDE_BORDER, width=2)
    for step in range(5):
        sx = x0 + 18 + step * 24
        ex = sx + 10
        draw.line((sx, density_y - 2, ex, density_y + 2), fill=GUIDE_BORDER, width=1)

    return result


def generate_stencil(input_path: str, output_path: str, line_weight: int = 1) -> str:
    if not input_path:
        raise ValueError("Input path is required.")

    original = _load_image(input_path)
    original = _resize_for_processing(original)
    original = _center_subject(original)

    gray = ImageOps.grayscale(original)
    edges = _edge_map(gray)
    outline = _apply_outline(original, edges)

    hatching = _hatch_shading(original)

    # Compose the final stencil on a white background.
    base = Image.new("RGB", original.size, WHITE)
    base.paste(outline, (0, 0))
    base = Image.blend(base, hatching, alpha=0.55)

    # Keep outlines readable and ensure shading is technical rather than soft.
    result = Image.new("RGB", base.size, WHITE)
    result.paste(base, (0, 0))
    result = _add_guide_box(result)

    output_dir = output_path.rsplit("/", 1)[0] if "/" in output_path else "."
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    result.save(output_path, format="PNG")
    return output_path


import os
