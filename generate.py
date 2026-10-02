
import os
import random
import argparse
import textwrap

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance


 

WIDTH = 1600
HEIGHT = 1000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE_DIR, "fonts")
TEXT_DIR = os.path.join(BASE_DIR, "texts")

FONT_PATHS = {
    "devanagari": os.path.join(
        FONT_DIR, "NotoSansDevanagari-Regular.ttf"
    ),
    "modi": os.path.join(
        FONT_DIR, "NotoSansModi-Regular.ttf"
    ),
    "sharada": os.path.join(
        FONT_DIR, "NotoSansSharada-Regular.ttf"
    ),
}


 

def load_text(script):
    """Load source text for the selected script."""

    path = os.path.join(TEXT_DIR, f"{script}.txt")

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Text file not found: {path}"
        )

    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        raise ValueError(
            f"Text file is empty: {path}"
        )

    return text


 

def create_aged_paper():
    """Create an aged handmade-paper background."""

    arr = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)

    base = np.array([214, 190, 145], dtype=np.float32)

    noise = np.random.normal(
        0, 9, (HEIGHT, WIDTH, 1)
    )

    arr[:] = base
    arr += noise

    # subtle paper fibers
    for _ in range(2500):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)

        length = random.randint(2, 20)

        arr[
            y:min(y + 1, HEIGHT),
            x:min(x + length, WIDTH)
        ] -= random.randint(2, 12)

    arr = np.clip(arr, 0, 255).astype(np.uint8)

    image = Image.fromarray(arr)

    return image


def create_palm_leaf():
    """Create a palm-leaf inspired manuscript background."""

    arr = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)

    base = np.array([170, 145, 85], dtype=np.float32)

    noise = np.random.normal(
        0, 7, (HEIGHT, WIDTH, 1)
    )

    arr[:] = base
    arr += noise

    image = Image.fromarray(
        np.clip(arr, 0, 255).astype(np.uint8)
    )

    draw = ImageDraw.Draw(image, "RGBA")

    # longitudinal palm-leaf fibers
    for y in range(20, HEIGHT, random.randint(12, 20)):
        draw.line(
            [(0, y), (WIDTH, y + random.randint(-5, 5))],
            fill=(95, 70, 35, 45),
            width=1
        )

    # irregular fibers
    for _ in range(900):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)

        draw.line(
            [(x, y), (x + random.randint(5, 30), y)],
            fill=(80, 60, 30, random.randint(15, 40)),
            width=1
        )

    return image


def create_background(material=None):
    """Create either aged paper or palm-leaf material."""

    if material is None:
        material = random.choice([
            "aged_paper",
            "palm_leaf"
        ])

    if material == "palm_leaf":
        image = create_palm_leaf()
    else:
        image = create_aged_paper()

    return image, material


 

def add_aging(image):
    """Add stains, faded edges and age variation."""

    overlay = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(overlay)

    # stains
    for _ in range(35):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)

        radius = random.randint(15, 80)

        draw.ellipse(
            [
                x - radius,
                y - radius,
                x + radius,
                y + radius
            ],
            fill=(
                75,
                45,
                20,
                random.randint(8, 25)
            )
        )

    # darkened borders
    border = 100

    for i in range(border):
        alpha = int(
            40 * (1 - i / border)
        )

        draw.rectangle(
            [
                i,
                i,
                WIDTH - i,
                HEIGHT - i
            ],
            outline=(50, 30, 10, alpha)
        )

    overlay = overlay.filter(
        ImageFilter.GaussianBlur(12)
    )

    image = Image.alpha_composite(
        image.convert("RGBA"),
        overlay
    )

    return image


def add_folds(image):
    """Add subtle manuscript folds and creases."""

    overlay = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(overlay)

    for _ in range(random.randint(2, 5)):
        x = random.randint(100, WIDTH - 100)

        draw.line(
            [
                (x, 0),
                (
                    x + random.randint(-30, 30),
                    HEIGHT
                )
            ],
            fill=(70, 45, 20, random.randint(20, 45)),
            width=random.randint(2, 5)
        )

    for _ in range(random.randint(1, 3)):
        y = random.randint(100, HEIGHT - 100)

        draw.line(
            [
                (0, y),
                (
                    WIDTH,
                    y + random.randint(-20, 20)
                )
            ],
            fill=(255, 245, 210, random.randint(15, 35)),
            width=random.randint(2, 4)
        )

    overlay = overlay.filter(
        ImageFilter.GaussianBlur(2)
    )

    return Image.alpha_composite(
        image,
        overlay
    )


def add_surface_warp(image):
    """Create a subtle uneven surface effect."""

    image = image.filter(
        ImageFilter.GaussianBlur(0.35)
    )

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(
        random.uniform(0.92, 1.05)
    )

    return image

 

def get_font(script, size=52):
    path = FONT_PATHS[script]

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Font not found: {path}"
        )

    return ImageFont.truetype(path, size)


def prepare_lines(text, font, max_width):
    """Wrap text according to rendered width."""

    words = text.replace("\n", " ").split()

    lines = []
    current = ""

    dummy = Image.new("RGB", (10, 10))
    draw = ImageDraw.Draw(dummy)

    for word in words:

        candidate = (
            word
            if not current
            else current + " " + word
        )

        bbox = draw.textbbox(
            (0, 0),
            candidate,
            font=font
        )

        width = bbox[2] - bbox[0]

        if width <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)

            current = word

    if current:
        lines.append(current)

    return lines


 

def render_text(image, script):
    """Render handwritten-style manuscript text."""

    text = load_text(script)

    font_size = random.randint(42, 55)

    font = get_font(
        script,
        font_size
    )

    margin_left = 210
    margin_right = 180
    margin_top = 150
    margin_bottom = 130

    max_width = (
        WIDTH
        - margin_left
        - margin_right
    )

    lines = prepare_lines(
        text,
        font,
        max_width
    )

    max_lines = 11
    lines = lines[:max_lines]

    transcription = "\n".join(lines)

 

    highlight_layer = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    highlight_draw = ImageDraw.Draw(
        highlight_layer
    )

    highlight_line = random.randint(
        1,
        max(1, len(lines))
    )

    line_height = font_size + 30

    for index, line in enumerate(lines):

        if index == highlight_line:

            y = (
                margin_top
                + index * line_height
            )

            highlight_draw.rounded_rectangle(
                [
                    margin_left - 10,
                    y - 5,
                    WIDTH - margin_right + 10,
                    y + line_height
                ],
                radius=8,
                fill=(
                    175,
                    135,
                    45,
                    35
                )
            )

    image = Image.alpha_composite(
        image,
        highlight_layer
    )

 

    text_layer = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(text_layer)

    y = margin_top

    for index, line in enumerate(lines):

        x = margin_left

        # Slight handwriting irregularity
        y_offset = random.randint(-4, 4)

        for char in line:

            bbox = draw.textbbox(
                (0, 0),
                char,
                font=font
            )

            char_width = bbox[2] - bbox[0]

            # Natural ink variation
            ink = random.choice([
                (55, 39, 24, 220),
                (65, 43, 25, 205),
                (45, 35, 25, 230),
                (80, 55, 30, 190)
            ])

            draw.text(
                (
                    x + random.randint(-2, 2),
                    y + y_offset
                ),
                char,
                font=font,
                fill=ink
            )

            x += (
                char_width
                + random.randint(0, 3)
            )

            if x > WIDTH - margin_right:
                break

        y += line_height

    # slight softness
    text_layer = text_layer.filter(
        ImageFilter.GaussianBlur(0.35)
    )

    image = Image.alpha_composite(
        image,
        text_layer
    )

    return image, transcription


 

def add_marginal_text(image, script):
    """Add small side annotations."""

    text = load_text(script)

    font = get_font(
        script,
        random.randint(22, 30)
    )

    words = text.split()

    side_text = " ".join(words[:8])

    layer = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(layer)

    draw.text(
        (
            65,
            random.randint(250, 450)
        ),
        side_text,
        font=font,
        fill=(60, 42, 25, 155)
    )

    layer = layer.rotate(
        90,
        expand=False
    )

    return Image.alpha_composite(
        image,
        layer
    )


 

def add_ink_bleed(image):
    """Simulate faded and bleeding ink."""

    overlay = image.copy()

    overlay = overlay.filter(
        ImageFilter.GaussianBlur(
            random.uniform(0.3, 0.8)
        )
    )

    image = Image.blend(
        image,
        overlay,
        random.uniform(0.03, 0.10)
    )

    return image


def add_smudges(image):
    """Add small ink smudges."""

    overlay = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(overlay)

    for _ in range(random.randint(10, 25)):

        x = random.randint(
            150,
            WIDTH - 150
        )

        y = random.randint(
            100,
            HEIGHT - 100
        )

        radius = random.randint(2, 8)

        draw.ellipse(
            [
                x - radius,
                y - radius,
                x + radius,
                y + radius
            ],
            fill=(
                50,
                35,
                20,
                random.randint(20, 80)
            )
        )

    overlay = overlay.filter(
        ImageFilter.GaussianBlur(2)
    )

    return Image.alpha_composite(
        image,
        overlay
    )


 

def create_annotation(
    image_name,
    script,
    material,
    transcription
):
    """Create synchronized Markdown ground truth."""

    return f"""# Ground Truth

- image: {image_name}
- script: {script}
- material: {material}
- image_width: {WIDTH}
- image_height: {HEIGHT}

## Transcription

{transcription}

## Generation Metadata

- handwritten_style: true
- marginal_annotations: true
- highlighted_text: true
- ink_variation: true
- ink_bleeding: true
- folds: true
- surface_warping: true
"""


 

def generate_image(
    script,
    output_dir,
    index=1,
    material=None
):
    """Generate one synthetic manuscript folio."""

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    # Background
    image, material = create_background(
        material
    )

    # Aging
    image = add_aging(image)

    # Folds
    image = add_folds(image)

    # Surface variation
    image = add_surface_warp(image)

    # Main manuscript text
    image, transcription = render_text(
        image,
        script
    )

    # Marginal annotations
    image = add_marginal_text(
        image,
        script
    )

    # Ink effects
    image = add_ink_bleed(image)
    image = add_smudges(image)

    # Final slight texture
    image = image.convert("RGB")

    image_name = f"manuscript_{index:04d}.png"

    image_path = os.path.join(
        output_dir,
        image_name
    )

    image.save(
        image_path,
        quality=95
    )

    # Markdown annotation
    annotation = create_annotation(
        image_name,
        script,
        material,
        transcription
    )

    md_path = os.path.join(
        output_dir,
        f"manuscript_{index:04d}.md"
    )

    with open(
        md_path,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(annotation)

    return image_path, md_path

 
def main():

    parser = argparse.ArgumentParser(
        description="Synthetic Manuscript Generator"
    )

    parser.add_argument(
        "--script",
        choices=[
            "devanagari",
            "modi",
            "sharada"
        ],
        default="devanagari",
        help="Manuscript script"
    )

    parser.add_argument(
        "--output",
        default="generated_output",
        help="Output directory"
    )

    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of folios to generate"
    )

    parser.add_argument(
        "--material",
        choices=[
            "aged_paper",
            "palm_leaf",
            "random"
        ],
        default="random",
        help="Background material"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("SYNTHETIC MANUSCRIPT GENERATOR")
    print("=" * 60)

    print(f"Script   : {args.script}")
    print(f"Count    : {args.count}")
    print(f"Output   : {args.output}")
    print(f"Material : {args.material}")
    print()

    for i in range(1, args.count + 1):

        if args.material == "random":
            material = None
        else:
            material = args.material

        image_path, md_path = generate_image(
            script=args.script,
            output_dir=args.output,
            index=i,
            material=material
        )

        print(
            f"[{i}/{args.count}] "
            f"Generated: {image_path}"
        )

    print()
    print("Generation completed successfully.")


if __name__ == "__main__":
    main()
