from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

FONT_REGULAR = "C:/Windows/Fonts/msyh.ttc"
FONT_BOLD = "C:/Windows/Fonts/msyhbd.ttc"


PALETTES = {
    "light": {
        "bg_a": (237, 247, 242),
        "bg_b": (226, 239, 236),
        "rail": (12, 96, 84),
        "ink": (15, 23, 42),
        "muted": (58, 73, 96),
        "soft": (91, 112, 135),
        "primary": (15, 118, 110),
        "primary_2": (14, 116, 144),
        "line": (97, 161, 151),
        "card": (248, 250, 247),
        "card_2": (241, 247, 244),
        "accent": (202, 124, 26),
        "accent_soft": (244, 203, 133),
        "wash_primary": (221, 239, 232),
        "wash_accent": (244, 229, 198),
        "white": (255, 255, 255),
    },
    "dark": {
        "bg_a": (5, 18, 15),
        "bg_b": (9, 30, 31),
        "rail": (32, 188, 170),
        "ink": (241, 245, 249),
        "muted": (190, 202, 215),
        "soft": (140, 158, 176),
        "primary": (45, 212, 191),
        "primary_2": (56, 189, 248),
        "line": (67, 170, 160),
        "card": (13, 27, 30),
        "card_2": (16, 34, 38),
        "accent": (245, 158, 11),
        "accent_soft": (124, 81, 20),
        "wash_primary": (8, 44, 41),
        "wash_accent": (45, 35, 18),
        "white": (15, 23, 42),
    },
}


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size=size)


def lerp(a, b, t):
    return int(a + (b - a) * t)


def gradient(size, a, b):
    width, height = size
    img = Image.new("RGBA", size)
    pix = img.load()
    for y in range(height):
        for x in range(width):
            t = (x / max(1, width - 1)) * 0.72 + (y / max(1, height - 1)) * 0.28
            pix[x, y] = tuple(lerp(a[i], b[i], t) for i in range(3)) + (255,)
    return img


def text(draw, xy, value, fill, size, bold=False, anchor=None):
    draw.text(xy, value, fill=fill, font=font(size, bold), anchor=anchor)


def rule(draw, xy, width, color, accent, thickness=2):
    x, y = xy
    draw.line((x, y, x + width, y), fill=color, width=thickness)
    draw.line((x, y, x + 70, y), fill=accent, width=thickness + 1)


def card(draw, box, palette, radius=8, fill_key="card", outline_key="line", width=2):
    draw.rounded_rectangle(
        box,
        radius=radius,
        fill=palette[fill_key],
        outline=palette[outline_key],
        width=width,
    )


def draw_hero(mode):
    p = PALETTES[mode]
    img = gradient((1280, 340), p["bg_a"], p["bg_b"])
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 0, 16, 340), fill=p["rail"])
    draw.rectangle((16, 0, 28, 340), fill=p["wash_primary"])
    draw.polygon([(1110, 0), (1280, 0), (1280, 118)], fill=p["wash_accent"])
    draw.polygon([(1118, 340), (1280, 244), (1280, 340)], fill=p["wash_primary"])

    left = 64
    right = 1218
    rule(draw, (left, 64), right - left, p["line"], p["accent"], 2)

    text(draw, (78, 92), "AI Native R&D Profile", p["primary_2"], 15, True)
    text(draw, (78, 130), "南橘 / Suzike", p["ink"], 42, True)
    text(draw, (79, 185), "汽车热管理应用层软件 · 智慧空调 Agent · MATLAB/Simulink MBD", p["muted"], 19)
    text(draw, (79, 219), "从 PRD / SOR 到 SWRS、Architecture、Model、Test、Calibration 与 Knowledge Base", p["soft"], 15)

    card(draw, (888, 92, 1196, 230), p, 8, "card", "line", 2)
    text(draw, (916, 123), "Engineering Loop", p["primary_2"], 15, True)
    items = ["Requirement", "Design", "Model", "MIL / HIL", "Evidence"]
    for idx, item in enumerate(items):
        y = 155 + idx * 16
        draw.rectangle((918, y - 3, 928, y - 1), fill=p["accent" if idx in (0, 4) else "primary_2"])
        text(draw, (940, y - 9), item, p["muted"], 12)

    draw.line((64, 276, 1218, 276), fill=p["line"], width=2)
    cells = [
        ("01", "Thermal ASW", "热管理控制算法"),
        ("02", "Smart HVAC Agent", "热舒适与个性化控制"),
        ("03", "MBD Toolchain", "MATLAB / Simulink"),
        ("04", "AI Native Platform", "Agent · MCP · Tool"),
    ]
    cell_w = (1218 - 64) / 4
    for idx, (num, title, sub) in enumerate(cells):
        x = int(64 + idx * cell_w)
        if idx:
            draw.line((x, 292, x, 327), fill=p["line"], width=1)
        text(draw, (x + 14, 302), num, p["primary_2"], 13, True)
        text(draw, (x + 48, 294), title, p["ink"], 15, True)
        text(draw, (x + 48, 318), sub, p["soft"], 11)
        if idx == 0:
            draw.rectangle((x + 14, 334, x + 110, 337), fill=p["accent"])

    img.save(ASSETS / f"profile-hero-{mode}.png")


def arrow(draw, start, end, p, down=False):
    color = p["primary_2"]
    draw.line((*start, *end), fill=color, width=2)
    ex, ey = end
    if down:
        draw.polygon([(ex - 6, ey - 2), (ex + 6, ey - 2), (ex, ey + 8)], fill=color)
    else:
        draw.polygon([(ex - 2, ey - 6), (ex - 2, ey + 6), (ex + 8, ey)], fill=color)


def node(draw, box, number, title, sub, p):
    card(draw, box, p, 7, "card", "line", 2)
    x1, y1, _, _ = box
    text(draw, (x1 + 18, y1 + 20), number, p["primary_2"], 13, True)
    text(draw, (x1 + 58, y1 + 18), title, p["ink"], 15, True)
    text(draw, (x1 + 58, y1 + 46), sub, p["muted"], 12)


def draw_platform(mode):
    p = PALETTES[mode]
    img = gradient((1280, 450), p["bg_a"], p["bg_b"])
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 0, 14, 450), fill=p["rail"])
    draw.polygon([(14, 0), (330, 0), (14, 120)], fill=p["wash_primary"])
    draw.polygon([(1195, 0), (1280, 0), (1280, 450), (1235, 450)], fill=p["wash_accent"])

    text(draw, (64, 50), "AI Native 研发闭环", p["ink"], 29, True)
    text(draw, (64, 88), "用 Agent、MCP、Tool、Skill 和 Knowledge Base 连接汽车热管理软件从需求到交付的工程路径。", p["muted"], 14)
    rule(draw, (64, 112), 1153, p["line"], p["accent"], 2)

    top = [
        ("01", "PRD / SOR", "场景、边界与输入"),
        ("02", "Functional Requirement", "功能拆解与约束"),
        ("03", "SWRS", "软件需求分析"),
        ("04", "Architecture / SWDD", "接口、状态与数据流"),
    ]
    bottom = [
        ("05", "Simulink Model", "Model Dev / Check"),
        ("06", "MIL / HIL Test", "Test Case / Evidence"),
        ("07", "Calibration Evidence", "参数策略与发布证据"),
        ("08", "Knowledge Base", "复用、沉淀与改进"),
    ]
    xs = [64, 358, 652, 946]
    w, h = 267, 73
    for idx, item in enumerate(top):
        node(draw, (xs[idx], 132, xs[idx] + w, 205), *item, p)
        if idx < 3:
            arrow(draw, (xs[idx] + w + 8, 168), (xs[idx + 1] - 14, 168), p)
    arrow(draw, (1096, 205), (1096, 222), p, down=True)

    card(draw, (64, 224, 1217, 261), p, 7, "card_2", "line", 2)
    text(draw, (86, 240), "Agent Loop Engineering（智能体的循环工程）", p["primary_2"], 14, True)
    text(draw, (420, 240), "Plan → Act → Check → Learn → Reuse", p["muted"], 14)
    draw.rectangle((86, 257, 386, 260), fill=p["accent"])
    arrow(draw, (196, 261), (196, 279), p, down=True)

    for idx, item in enumerate(bottom):
        node(draw, (xs[idx], 282, xs[idx] + w, 355), *item, p)
        if idx < 3:
            arrow(draw, (xs[idx] + w + 8, 319), (xs[idx + 1] - 14, 319), p)

    card(draw, (64, 387, 1217, 428), p, 7, "card_2", "line", 2)
    text(draw, (86, 403), "Runtime Layer", p["primary_2"], 14, True)
    text(draw, (220, 403), "LLM Runtime · Agent · MCP · Tool · Skill · Harness Engineering · Knowledge Base", p["muted"], 13)
    draw.rectangle((86, 424, 187, 427), fill=p["accent"])

    img.save(ASSETS / f"platform-loop-{mode}.png")


def main():
    ASSETS.mkdir(exist_ok=True)
    for mode in ("light", "dark"):
        draw_hero(mode)
        draw_platform(mode)


if __name__ == "__main__":
    main()
