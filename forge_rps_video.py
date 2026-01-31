import os
import shutil
from PIL import Image, ImageDraw, ImageFont
import subprocess

def create_rps_coding_video(output_path):
    frames_dir = "/tmp/rps_coding_frames"
    if os.path.exists(frames_dir):
        shutil.rmtree(frames_dir)
    os.makedirs(frames_dir, exist_ok=True)
    
    bg_color = (13, 17, 23)
    text_color = (200, 200, 200)
    cursor_color = (0, 150, 136)
    
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
        font = ImageFont.truetype(font_path, 30)
    except:
        font = ImageFont.load_default()

    code_steps = [
        "import random\n",
        "\ndef get_computer_choice():\n    return random.choice(['rock', 'paper', 'scissors'])\n",
        "\ndef determine_winner(user, comp):\n    if user == comp: return 'Tie'\n    if (user == 'rock' and comp == 'scissors') or \\\n       (user == 'paper' and comp == 'rock') or \\\n       (user == 'scissors' and comp == 'paper'):\n        return 'User Wins!'\n    return 'Computer Wins!'\n",
        "\ndef play():\n    user = input('Enter rock, paper, or scissors: ')\n    comp = get_computer_choice()\n    print(f'Comp chose {comp}')\n    print(determine_winner(user, comp))\n\nplay()"
    ]

    frame_count = 0
    full_code = ""
    
    # Total targeted frames for ~20s at 25fps = 500 frames
    for step in code_steps:
        # Type the step
        for i in range(len(step)):
            full_code += step[i]
            img = Image.new('RGB', (1080, 1920), color=bg_color)
            draw = ImageDraw.Draw(img)
            
            # Header
            draw.rectangle([0, 0, 1080, 100], fill=(30, 35, 45))
            draw.text((40, 35), "Project: RockPaperScissors.py", font=font, fill=(150, 150, 150))
            
            # Code
            lines = full_code.split('\n')
            display_text = "\n".join(lines[-45:])
            draw.text((50, 150), display_text, font=font, fill=text_color)
            
            # Cursor
            if frame_count % 4 < 2:
                last_line = lines[-1]
                y_pos = 150 + (len(lines[-45:]) - 1) * 38
                x_pos = 50 + len(last_line) * 18
                draw.rectangle([x_pos, y_pos, x_pos + 18, y_pos + 32], fill=cursor_color)

            frame_path = os.path.join(frames_dir, f"frame_{frame_count:04d}.png")
            img.save(frame_path)
            frame_count += 1
        
        # Pause slightly between functions
        for _ in range(15):
            img.save(os.path.join(frames_dir, f"frame_{frame_count:04d}.png"))
            frame_count += 1

    # Final hold
    for _ in range(100):
        img.save(os.path.join(frames_dir, f"frame_{frame_count:04d}.png"))
        frame_count += 1

    print("Encoding video...")
    subprocess.run([
        "ffmpeg", "-y", "-framerate", "25", "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "/tmp/temp_video.mp4"
    ])

if __name__ == "__main__":
    create_rps_coding_video("/tmp/temp_video.mp4")
