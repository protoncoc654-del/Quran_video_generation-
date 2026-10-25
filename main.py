import subprocess
from PIL import Image, ImageDraw, ImageFont

W, H = 720, 1280
FPS = 30
DURATION = 4.0
OUT = "intro_4s.mp4"

# Original text and timings (not taken from the reference video)
NOTIFICATIONS = [
    (0.8, "Sam", "Hey, you up?"),
    (1.5, "Weather", "Storm warning for tonight"),
    (2.3, "ALERT", "Stay indoors. Check updates."),
]
CAPTION = [(0.4, "THE"), (0.8, "NIGHT"), (1.2, "GOT"), (1.6, "QUIET")]


def font(size):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default(size=size)


def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def lerp(a, b, t):
    return a + (b - a) * t


def draw_frame(t):
    img = Image.new("RGB", (W, H), (12, 12, 16))
    d = ImageDraw.Draw(img)

    # HUD in the top-left corner
    d.text((40, 60), "SCENE 01", font=font(28), fill=(230, 70, 70))
    d.text((40, 100), f"00:{int(t):02d}", font=font(44), fill=(235, 235, 235))

    # Phone body rises into view
    rise = lerp(320, 0, ease_out(t / 0.6))
    px0, py0, px1, py1 = 140, 260 + rise, 580, 1040 + rise
    d.rounded_rectangle((px0, py0, px1, py1), radius=50,
                        fill=(28, 28, 34), outline=(70, 70, 80), width=4)

    # Lock-screen clock
    clock = "9:41"
    cw = d.textlength(clock, font=font(110))
    d.text(((W - cw) / 2, py0 + 60), clock, font=font(110), fill=(245, 245, 245))

    # Notification cards slide in from the right
    card_y = py0 + 240
    for start, title, body in NOTIFICATIONS:
        p = ease_out((t - start) / 0.4)
        if p <= 0:
            card_y += 120
            continue
        x_off = lerp(200, 0, p)
        x0 = px0 + 30 + x_off
        d.rounded_rectangle((x0, card_y, px1 - 30 + x_off, card_y + 100),
                            radius=24, fill=(45, 45, 55))
        d.text((x0 + 24, card_y + 16), title, font=font(24), fill=(150, 150, 165))
        d.text((x0 + 24, card_y + 50), body, font=font(26), fill=(240, 240, 240))
        card_y += 120

    # Word-by-word caption at the bottom
    shown = [w for start, w in CAPTION if t >= start]
    if shown:
        line = " ".join(shown)
        cap_font = font(64)
        tw = d.textlength(line, font=cap_font)
        d.text(((W - tw) / 2, H - 200), line, font=cap_font, fill=(255, 255, 255))

    return img


def main():
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        OUT,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(int(DURATION * FPS)):
        proc.stdin.write(draw_frame(i / FPS).tobytes())
    proc.stdin.close()
    proc.wait()
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
