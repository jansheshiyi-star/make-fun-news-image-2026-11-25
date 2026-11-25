"""Render the 25 November 2026 world news edition as one PNG."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


STORIES = (
    (
        "China Probes Politburo Member Chen Jining",
        "Beijing opens a corruption investigation into Chen Jining, the Communist Party chief of Shanghai.",
    ),
    (
        "US Jury Convicts Huawei",
        "A US jury finds Huawei guilty of conspiring to steal trade secrets and bank fraud.",
    ),
    (
        "COP31 Climate Summit Collapses",
        "The UN climate summit in Antalya ends with no deal after oil states block fossil-fuel phase-out language.",
    ),
    (
        'Russia Accuses Ukraine of "Terrorism"',
        "Moscow blames Kyiv for drone strikes on a Russian cargo ship in the Baltic Sea and a warship off Libya.",
    ),
    (
        "Tankers Hit Mines in Strait of Hormuz",
        "Iran says three oil tankers struck naval mines and caught fire, and refuses US talks until its conditions are met.",
    ),
    (
        "Gaza Strikes Kill 7 Despite Ceasefire",
        "Israeli airstrikes kill seven people in Gaza, including a senior Hamas security official.",
    ),
)

SIZE = 1024
LEFT = 56
RIGHT = SIZE - LEFT
TEXT_LEFT = 122
NAVY = "#132438"
INK = "#152335"
GREY = "#465462"
PAPER = "#FAFBFC"
RULE = "#CDD5DD"
ACCENT = "#A9D7DE"
OUTPUT = Path("/output/entry.png")
ROW_TOP = 155
ROW_HEIGHT = 133
TEXT_WIDTH = RIGHT - TEXT_LEFT - 4


def wrap(draw, text, font, width):
    """Use one line when possible, otherwise balance two whole-word lines."""
    if draw.textlength(text, font=font) <= width:
        return (text,)

    words = text.split()
    pairs = [
        (" ".join(words[:index]), " ".join(words[index:]))
        for index in range(1, len(words))
    ]
    lines = min(pairs, key=lambda pair: max(
        draw.textlength(line, font=font) for line in pair
    ))
    if any(draw.textlength(line, font=font) > width for line in lines):
        raise ValueError(f"Text exceeds two lines: {text}")
    return lines


def main():
    # Pillow embeds the scalable Aileron TrueType font in its Python module.
    title_font = ImageFont.load_default(size=76)
    headline_font = ImageFont.load_default(size=38)
    summary_font = ImageFont.load_default(size=28)
    small_font = ImageFont.load_default(size=21)
    image = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, SIZE - 1, 149), fill=NAVY)
    draw.text((LEFT, 85), "WORLD NEWS", font=title_font, fill=PAPER,
              stroke_width=2, anchor="ls")
    draw.text((LEFT, 127), "Wednesday, 25 November 2026",
              font=summary_font, fill=PAPER, anchor="ls")
    draw.rectangle((0, 150, SIZE - 1, ROW_TOP - 1), fill=ACCENT)
    for number, (headline, summary) in enumerate(STORIES, start=1):
        top = ROW_TOP + (number - 1) * ROW_HEIGHT
        headlines = wrap(draw, headline, headline_font, TEXT_WIDTH)
        summaries = wrap(draw, summary, summary_font, TEXT_WIDTH)
        headline_text = "\n".join(headlines)
        summary_text = "\n".join(summaries)
        headline_box = draw.multiline_textbbox(
            (0, 0), headline_text, font=headline_font, spacing=3, stroke_width=1
        )
        summary_box = draw.multiline_textbbox(
            (0, 0), summary_text, font=summary_font, spacing=4
        )
        headline_height = headline_box[3] - headline_box[1]
        summary_height = summary_box[3] - summary_box[1]
        gap = 9
        block_height = headline_height + gap + summary_height
        if block_height > ROW_HEIGHT - 12:
            raise ValueError(f"Story {number} exceeds its row")

        block_top = top + (ROW_HEIGHT - block_height) // 2
        center = block_top + 15
        draw.ellipse((LEFT, center - 20, LEFT + 40, center + 20), fill=NAVY)
        draw.text((LEFT + 20, center), str(number), font=small_font,
                  fill=PAPER, stroke_width=1, anchor="mm")
        draw.multiline_text(
            (TEXT_LEFT, block_top - headline_box[1]), headline_text,
            font=headline_font, fill=INK, spacing=3, stroke_width=1,
        )
        draw.multiline_text(
            (TEXT_LEFT, block_top + headline_height + gap - summary_box[1]),
            summary_text, font=summary_font, fill=GREY, spacing=4,
        )
        draw.line((LEFT, top + ROW_HEIGHT - 1, RIGHT, top + ROW_HEIGHT - 1),
                  fill=RULE)
    draw.text((LEFT, 995), "Compiled from major news coverage · 25 November 2026",
              font=small_font, fill=GREY, anchor="ls")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("wb") as output:
        image.save(output, format="PNG", compress_level=9)


if __name__ == "__main__":
    main()
