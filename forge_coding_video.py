import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
from pygments import highlight
from pygments.lexers import CppLexer
from pygments.formatters import ImageFormatter
import subprocess

def create_coding_video(code, output_path):
    # Setup directories
    frames_dir = "/tmp/coding_frames"
    import shutil
    if os.path.exists(frames_dir):
        shutil.rmtree(frames_dir)
    os.makedirs(frames_dir, exist_ok=True)
    
    # Branded Colors (Terminal style)
    bg_color = (13, 17, 23)
    
    # Font setup
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
        font = ImageFont.truetype(font_path, 32)
    except:
        font = ImageFont.load_default()

    # Generate frames character by character
    print("Generating frames...")
    frame_count = 0
    
    # We'll group characters to speed up (e.g., 1 char per frame for longer video)
    chars_per_frame = 1
    
    total_chars = len(code)
    for i in range(0, total_chars + 1, chars_per_frame):
        # Frame text
        visible_text = code[:i]
        
        # Create image
        img = Image.new('RGB', (1080, 1920), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Draw some "header" UI
        draw.rectangle([0, 0, 1080, 80], fill=(30, 35, 45))
        draw.text((40, 20), "Main.c - Digital Assistant Forge", font=font, fill=(180, 180, 180))
        
        # Draw dots (mac-style buttons)
        draw.ellipse([900, 25, 930, 55], fill=(255, 95, 87))
        draw.ellipse([940, 25, 970, 55], fill=(255, 189, 46))
        draw.ellipse([980, 25, 1010, 55], fill=(39, 201, 63))

        # Draw the text
        draw.text((50, 150), visible_text, font=font, fill=(200, 200, 200))
        
        # Draw cursor
        if frame_count % 4 < 2: # Blink effect
            last_lines = visible_text.split('\n')
            if last_lines:
                last_line = last_lines[-1]
                y_pos = 150 + (len(last_lines) - 1) * 40
                x_pos = 50 + len(last_line) * 19
                draw.rectangle([x_pos, y_pos, x_pos + 20, y_pos + 35], fill=(0, 150, 136))

        frame_path = os.path.join(frames_dir, f"frame_{frame_count:04d}.png")
        img.save(frame_path)
        frame_count += 1

    # Add 5 seconds of pause at the end
    for _ in range(125):
        frame_path = os.path.join(frames_dir, f"frame_{frame_count:04d}.png")
        img.save(frame_path)
        frame_count += 1

    print("Encoding video...")
    subprocess.run([
        "ffmpeg", "-y", "-framerate", "25", "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", output_path
    ])
    print(f"Video saved to {output_path}")

if __name__ == "__main__":
    c_code = """
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/* System Pulse Forge */
void monitor_sys() {
    printf("Initializing Global Monitor...\\n");
    while(1) {
        system("clear");
        printf("[ SYSTEM VITALS ]\\n");
        printf("-----------------\\n");
        printf("CPU Load: ");
        fflush(stdout);
        system("uptime | awk '{print $10}'");
        printf("Memory: ");
        fflush(stdout);
        system("free -h | grep Mem | awk '{print $3}'");
        sleep(1);
    }
}

int main() {
    monitor_sys();
    return 0;
}
    """
    create_coding_video(c_code, "/root/clawd/coding_strike_v2.mp4")
