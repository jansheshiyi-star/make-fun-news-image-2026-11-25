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


def wrap(draw, text, font, width):
    """Wrap at whole-word boundaries using measured glyph widths."""
    lines = []
    line = ""
    for word in text.split():
        candidate = f"{line} {word}" if line else word
        if line and draw.textlength(candidate, font=font) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    lines.append(line)
    return lines


def main():
    # Pillow embeds the scalable Aileron TrueType font in its Python module.
    title_font = ImageFont.load_default(size=76)
    headline_font = ImageFont.load_default(size=36)
    summary_font = ImageFont.load_default(size=26)
    small_font = ImageFont.load_default(size=20)
    image = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, SIZE - 1, 149), fill=NAVY)
    draw.text((LEFT, 85), "WORLD NEWS", font=title_font, fill=PAPER,
              stroke_width=2, anchor="ls")
    draw.text((LEFT, 127), "Wednesday, 25 November 2026",
              font=summary_font, fill=PAPER, anchor="ls")
    draw.rectangle((0, 150, SIZE - 1, 153), fill=ACCENT)
    for number, (headline, summary) in enumerate(STORIES, start=1):
        top = 169 + (number - 1) * 131
        center = top + 38
        draw.ellipse((LEFT, center - 20, LEFT + 40, center + 20), fill=NAVY)
        draw.text((LEFT + 20, center), str(number), font=small_font,
                  fill=PAPER, stroke_width=1, anchor="mm")
        headlines = wrap(draw, headline, headline_font, RIGHT - TEXT_LEFT - 4)
        summaries = wrap(draw, summary, summary_font, RIGHT - TEXT_LEFT - 4)
        headline_baseline = top + 44
        baseline = headline_baseline + 35 + 40 * (len(headlines) - 1)
        if len(headlines) > 2 or len(summaries) > 2 or baseline + 32 * (len(summaries) - 1) > top + 120:
            raise ValueError(f"Story {number} exceeds its row")
        for index, line in enumerate(headlines):
            draw.text((TEXT_LEFT, headline_baseline + index * 40), line,
                      font=headline_font, fill=INK, stroke_width=1, anchor="ls")
        for index, line in enumerate(summaries):
            draw.text((TEXT_LEFT, baseline + index * 32), line,
                      font=summary_font, fill=GREY, anchor="ls")
        draw.line((LEFT, top + 130, RIGHT, top + 130), fill=RULE)
    draw.text((LEFT, 992), "Compiled from major news coverage · 25 November 2026",
              font=small_font, fill=GREY, anchor="ls")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, format="PNG", compress_level=9)


if __name__ == "__main__":
    main()
