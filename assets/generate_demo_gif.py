"""
Generates an animated terminal-demo GIF for the README, simulating a run of
`docker compose up --build` followed by the CLI generating a report.

This is a one-off asset-generation script (not part of the package itself),
kept here for reproducibility in case the demo needs to be regenerated.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 900, 320
BG = (10, 22, 38)          # matches the report's navy cover
BAR_BG = (16, 34, 54)
BORDER = (30, 50, 72)
TEXT_MAIN = (223, 230, 237)
TEXT_MUTED = (110, 130, 150)
PROMPT_COLOR = (94, 176, 214)
SUCCESS = (110, 200, 120)
WARN = (216, 160, 74)
CRIT = (214, 92, 92)
TITLE = (150, 170, 190)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
font = ImageFont.truetype(FONT_PATH, 16)
font_bold = ImageFont.truetype(FONT_BOLD_PATH, 16)
font_title = ImageFont.truetype(FONT_PATH, 13)

PAD_X = 28
PAD_TOP = 56
LINE_H = 24


def base_canvas():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    # Title bar
    draw.rectangle([0, 0, W, 40], fill=BAR_BG)
    draw.rectangle([0, 40, W, 41], fill=BORDER)
    for i, color in enumerate([CRIT, WARN, SUCCESS]):
        cx = 22 + i * 22
        draw.ellipse([cx, 15, cx + 12, 27], fill=color)
    draw.text((W / 2, 20), "cyberreport-pro — zsh", font=font_title, fill=TITLE, anchor="mm")
    return img, draw


# Each entry: (text, color, font, pause_after_frames)
# type=True -> revealed character by character; type=False -> appears whole
SCRIPT = [
    ("$ docker compose up --build", PROMPT_COLOR, font_bold, True, 6),
    ("[+] Building 1.0s (17/17) FINISHED", TEXT_MUTED, font, False, 3),
    ("✔ cyberreport-pro:local   Built", SUCCESS, font, False, 3),
    ("✔ Container cyberreport-pro-1   Created", SUCCESS, font, False, 3),
    ("cyberreport-pro-1  | Loaded 5 finding(s). Generating report...", TEXT_MAIN, font, False, 5),
    ("cyberreport-pro-1  | ✔ Report generated at: output/report.pdf", SUCCESS, font_bold, False, 5),
    ("cyberreport-pro-1  |   Critical: 2  High: 1  Medium: 1  Low: 1", TEXT_MUTED, font, False, 8),
    ("", TEXT_MAIN, font, False, 2),
    ("$ ", PROMPT_COLOR, font_bold, False, 10),
]

frames = []
durations = []

lines_committed = []  # list of (text, color, font) already fully shown


def render(lines, cursor_visible, partial_text=None, partial_color=None, partial_font=None):
    img, draw = base_canvas()
    y = PAD_TOP
    for text, color, fnt in lines:
        draw.text((PAD_X, y), text, font=fnt, fill=color)
        y += LINE_H
    if partial_text is not None:
        draw.text((PAD_X, y), partial_text, font=partial_font, fill=partial_color)
        if cursor_visible:
            w = draw.textlength(partial_text, font=partial_font)
            draw.rectangle([PAD_X + w + 2, y + 2, PAD_X + w + 10, y + 18], fill=partial_color)
    elif cursor_visible:
        draw.rectangle([PAD_X, y + 2, PAD_X + 8, y + 18], fill=PROMPT_COLOR)
    return img


for text, color, fnt, do_type, hold_frames in SCRIPT:
    if do_type:
        step = max(1, len(text) // 18)
        for i in range(0, len(text) + 1, step):
            partial = text[:i]
            img = render(lines_committed, True, partial, color, fnt)
            frames.append(img)
            durations.append(45)
        lines_committed.append((text, color, fnt))
        img = render(lines_committed, False)
        frames.append(img)
        durations.append(200)
    else:
        lines_committed.append((text, color, fnt))
        img = render(lines_committed, False)
        frames.append(img)
        durations.append(120)
        for _ in range(hold_frames):
            frames.append(img)
            durations.append(120)

# Final blinking cursor hold (loop-friendly ending)
final_static = render(lines_committed, False)
for blink in range(6):
    frames.append(render(lines_committed, blink % 2 == 0))
    durations.append(400)

frames[0].save(
    "/home/claude/cyberreport-pro/assets/demo.gif",
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    optimize=True,
)
print(f"Generated {len(frames)} frames")
