import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

WHITE = (255, 255, 255)
OUTLINE_COLOR = (18, 18, 26)
HATCH_COLOR = (120, 140, 255)
GUIDE_BG = (239, 243, 255)
GUIDE_BORDER = (84, 96, 166)


def _resize_for_processing(img: Image.Image, max_size: int = 1800) -> Image.Image:
    if max(img.size) > max_size:
        img.thumbnail((max_size, max_size))
    return img


def _center_subject(img: Image.Image) -> Image.Image:
    rgb = np.array(img.convert("RGB"))
    mask = np.any(rgb < 245, axis=2)
    ys, xs = np.where(mask)
    if xs.size == 0 or ys.size == 0:
        return img

    x0 = max(0, int(xs.min()) - 30)
    x1 = min(img.width, int(xs.max()) + 30)
    y0 = max(0, int(ys.min()) - 30)
    y1 = min(img.height, int(ys.max()) + 30)
    return img.crop((x0, y0, x1, y1))


def _subject_mask(img: Image.Image) -> np.ndarray:
    rgb = np.array(img.convert("RGB"), dtype=np.uint8)
    mask = np.any(rgb < 245, axis=2).astype(np.uint8) * 255
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        filled = np.zeros_like(mask)
        cv2.drawContours(filled, [largest], -1, 255, thickness=-1)
        mask = filled

    return mask


def _edge_map(img: Image.Image, mask: np.ndarray) -> np.ndarray:
    gray = ImageOps.grayscale(img)
    gray = ImageEnhance.Contrast(gray).enhance(1.8)
    edges = cv2.Canny(np.asarray(gray), 60, 150)
    return cv2.bitwise_and(edges, mask)


def _apply_outline(img: Image.Image, edges: np.ndarray, line_weight: int = 1) -> Image.Image:
    overlay = Image.new("RGB", img.size, WHITE)
    draw = ImageDraw.Draw(overlay)

    for y, x in np.argwhere(edges > 0):
        for dx in range(-line_weight, line_weight + 1):
            for dy in range(-line_weight, line_weight + 1):
                xx = x + dx
                yy = y + dy
                if 0 <= xx < img.width and 0 <= yy < img.height:
                    draw.point((xx, yy), fill=OUTLINE_COLOR)

    overlay = overlay.filter(ImageFilter.MaxFilter(3))
    return overlay


def _hatch_density(value: int) -> int:
    return max(1, min(7, int((255 - value) / 35)))


def _hatch_shading(img: Image.Image, mask: np.ndarray, spacing: int = 8) -> Image.Image:
    hatch = Image.new("RGB", img.size, WHITE)
    draw = ImageDraw.Draw(hatch)
    gray = ImageOps.grayscale(img)
    arr = np.asarray(gray)

    for y in range(0, img.height, spacing):
        for x in range(0, img.width, spacing):
            if mask[y, x] == 0:
                continue

            darkness = 255 - arr[y, x]
            if darkness < 18:
                continue

            density = _hatch_density(arr[y, x])
            step = 6 + density * 2

            for offset in range(density):
                sx = x + offset * 2
                sy = y + offset * 2
                ex = min(img.width - 1, sx + step)
                ey = min(img.height - 1, sy + step)
                draw.line((sx, sy, ex, ey), fill=HATCH_COLOR, width=1)
                draw.line((x, y + offset * 2, x + step, y + offset * 2 + step), fill=HATCH_COLOR, width=1)

    return hatch


def _add_guide_box(img: Image.Image) -> Image.Image:
    result = img.copy()
    draw = ImageDraw.Draw(result)

    box_w = max(150, int(result.width * 0.22))
    box_h = max(42, int(result.height * 0.075))
    x0, y0 = 18, 18
    x1, y1 = x0 + box_w, y0 + box_h

    draw.rounded_rectangle((x0, y0, x1, y1), radius=8, fill=GUIDE_BG, outline=GUIDE_BORDER, width=2)
    font = ImageFont.load_default()

    text = "SHADING GUIDE"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]
    text_x = x0 + (box_w - text_w) // 2
    text_y = y0 + (box_h - text_h) // 2
    draw.text((text_x, text_y), text, fill=GUIDE_BORDER, font=font)

    density_y = y0 + box_h - 10
    draw.line((x0 + 12, density_y, x1 - 12, density_y), fill=GUIDE_BORDER, width=2)
    for step in range(5):
        sx = x0 + 18 + step * 22
        ex = sx + 11
        draw.line((sx, density_y - 2, ex, density_y + 2), fill=GUIDE_BORDER, width=1)

    return result


def generate_stencil(input_path: str, output_path: str, line_weight: int = 1, hatch_spacing: int = 8) -> str:
    if not input_path:
        raise ValueError("Input path is required.")

    original = Image.open(input_path).convert("RGB")
    original = _resize_for_processing(original)
    original = _center_subject(original)

    mask = _subject_mask(original)
    edges = _edge_map(original, mask)
    outline = _apply_outline(original, edges, line_weight=line_weight)
    hatch = _hatch_shading(original, mask, spacing=hatch_spacing)

    result = Image.new("RGB", original.size, WHITE)
    result.paste(outline, (0, 0))
    result = Image.blend(result, hatch, alpha=0.6)
    result = _add_guide_box(result)

    directory = os.path.dirname(output_path) or "."
    os.makedirs(directory, exist_ok=True)
    result.save(output_path, format="PNG")
    return output_path


if __name__ == "__main__":
    generate_stencil("input.jpg", "output/stencil.png")
