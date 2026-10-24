import os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip

def generate_video():
    print("Initializing Quran video generation...")
    
    # Create a 9:16 vertical video clip (dark indigo theme)
    width, height = 1080, 1920
    duration = 5 # seconds for testing
    
    # Background color (Dark Indigo / Midnight Blue)
    bg_clip = ColorClip(size=(width, height), color=(15, 15, 30), duration=duration)
    
    # Save a placeholder frame to test rendering
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "quran_reel.mp4")
    
    # Write the video file using MoviePy
    bg_clip.write_videofile(output_path, fps=24, codec="libx264", audio=False)
    print(f"Video successfully generated at: {output_path}")

if __name__ == "__main__":
    generate_video()
  
