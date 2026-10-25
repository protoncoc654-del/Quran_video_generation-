import os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import TextClip, ColorClip, CompositeVideoClip

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Reel Dimensions (1080x1920 for 9:16 Shorts/Reels)
width, height = 1080, 1920
fps = 30
duration = 7  # seconds

# Create base background color (Dark Aesthetic Theme)
bg_clip = ColorClip(size=(width, height), color=(15, 23, 42), duration=duration)

# Arabic Verse & Translation Text
arabic_text = "فَبِأَيِّ آلَاءِ رَبِّكُمَا تُكَذِّبَانِ"
translation_text = "So which of the favors of your Lord will you deny?"
surah_ref = "Surah Ar-Rahman [55:13]"

# Create Text Overlay (MoviePy TextClip)
# Uses default font, styled for mobile screens
txt_arabic = TextClip(
    arabic_text,
    fontsize=60,
    color='gold',
    size=(width - 100, None),
    method='caption'
).set_position(('center', height * 0.35)).set_duration(duration)

txt_trans = TextClip(
    translation_text,
    fontsize=40,
    color='white',
    size=(width - 120, None),
    method='caption'
).set_position(('center', height * 0.52)).set_duration(duration)

txt_ref = TextClip(
    surah_ref,
    fontsize=30,
    color='lightgray',
    method='caption'
).set_position(('center', height * 0.65)).set_duration(duration)

# Composite all elements together
final_video = CompositeVideoClip([bg_clip, txt_arabic, txt_trans, txt_ref])

# Export video file
final_video.write_videofile(
    "output/quran_reel.mp4",
    fps=fps,
    codec="libx264",
    audio=False
)
print("Video successfully generated!")
