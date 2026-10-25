import os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Reel Dimensions (1080x1920 for 9:16 Shorts/Reels)
width, height = 1080, 1920
fps = 30
duration = 7  # seconds

# Create a blank image with a dark aesthetic background color (RGB: 15, 23, 42)
img = Image.new("RGB", (width, height), color=(15, 23, 42))
draw = ImageDraw.Draw(img)

# Load default font (PIL fallback font)
try:
    font_arabic = ImageFont.load_default()
    font_trans = ImageFont.load_default()
except Exception:
    font_arabic = None
    font_trans = None

# Arabic Verse & Translation Text
arabic_text = "فَبِأَيِّ آلَاءِ رَبِّكُمَا تُكَذِّبَانِ"
translation_text = "So which of the favors of your Lord will you deny?"
surah_ref = "Surah Ar-Rahman [55:13]"

# Draw text onto the image canvas
# (Using simple centered coordinates for the test card)
draw.text((100, 700), arabic_text, fill="gold")
draw.text((100, 950), translation_text, fill="white")
draw.text((100, 1150), surah_ref, fill="lightgray")

# Save the generated frame temporarily
temp_image_path = "output/temp_frame.png"
img.save(temp_image_path)

# Convert the image into a MoviePy video clip
video_clip = ImageClip(temp_image_path).set_duration(duration)

# Export final video file
video_clip.write_videofile(
    "output/quran_reel.mp4",
    fps=fps,
    codec="libx264",
    audio=False
)
print("Video successfully generated with Pillow!")
