import os
import shutil
from PIL import Image, ImageDraw, ImageFont
import subprocess

def create_complex_coding_video(steps, output_path):
    frames_dir = "/tmp/complex_coding_frames"
    if os.path.exists(frames_dir):
        shutil.rmtree(frames_dir)
    os.makedirs(frames_dir, exist_ok=True)
    
    bg_color = (13, 17, 23)
    header_color = (30, 35, 45)
    text_color = (200, 200, 200)
    cursor_color = (0, 150, 136)
    
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
        font = ImageFont.truetype(font_path, 30)
        header_font = ImageFont.truetype(font_path, 28)
    except:
        font = ImageFont.load_default()
        header_font = ImageFont.load_default()

    frame_count = 0
    chars_per_frame = 3 # Fast-paced for complex look
    
    for filename, code in steps:
        print(f"Generating frames for {filename}...")
        total_chars = len(code)
        
        for i in range(0, total_chars + 1, chars_per_frame):
            visible_text = code[:i]
            
            img = Image.new('RGB', (1080, 1920), color=bg_color)
            draw = ImageDraw.Draw(img)
            
            # Header
            draw.rectangle([0, 0, 1080, 100], fill=header_color)
            draw.text((40, 35), f"Project: SENTINEL-XDR | File: {filename}", font=header_font, fill=(150, 150, 150))
            
            # MacOS Window Controls
            draw.ellipse([900, 35, 930, 65], fill=(255, 95, 87))
            draw.ellipse([940, 35, 970, 65], fill=(255, 189, 46))
            draw.ellipse([980, 35, 1010, 65], fill=(39, 201, 63))

            # Code window area
            # Handle long code by showing the "tail" if it exceeds screen height
            lines = visible_text.split('\n')
            max_lines = 45
            if len(lines) > max_lines:
                display_lines = lines[-max_lines:]
            else:
                display_lines = lines
            
            display_text = "\n".join(display_lines)
            draw.text((50, 150), display_text, font=font, fill=text_color)
            
            # Cursor
            if frame_count % 4 < 2:
                last_line = display_lines[-1] if display_lines else ""
                y_pos = 150 + (len(display_lines) - 1) * 38
                x_pos = 50 + len(last_line) * 18
                draw.rectangle([x_pos, y_pos, x_pos + 18, y_pos + 32], fill=cursor_color)

            frame_path = os.path.join(frames_dir, f"frame_{frame_count:04d}.png")
            img.save(frame_path)
            frame_count += 1
            
        # Add a "Saved" flicker
        for _ in range(10):
            img = Image.new('RGB', (1080, 1920), color=bg_color)
            draw = ImageDraw.Draw(img)
            draw.rectangle([0, 0, 1080, 100], fill=(0, 100, 80)) # Green flash
            draw.text((40, 35), f"FILE SAVED: {filename}", font=header_font, fill=(255, 255, 255))
            draw.text((50, 150), display_text, font=font, fill=text_color)
            frame_path = os.path.join(frames_dir, f"frame_{frame_count:04d}.png")
            img.save(frame_path)
            frame_count += 1

    print("Encoding master video...")
    subprocess.run([
        "ffmpeg", "-y", "-framerate", "30", "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-profile:v", "high", "-level:v", "4.0", 
        "-pix_fmt", "yuv420p", "-crf", "23", output_path
    ])
    print(f"Complex system build saved to {output_path}")

if __name__ == "__main__":
    build_steps = [
        ("sentinel.h", """
#ifndef SENTINEL_H
#define SENTINEL_H

typedef struct {
    int pid;
    char proc_name[256];
    double cpu_usage;
    long mem_usage;
} ProcessNode;

void init_engine();
void scan_network_layer();
void resolve_threat(int threat_id);

#endif
        """),
        ("engine.c", """
#include "sentinel.h"
#include <stdio.h>

void init_engine() {
    printf("[*] Initializing XDR Engine v4.2...\\n");
    // Allocate memory for detection matrix
    // Bind kernel hooks
}

void scan_network_layer() {
    printf("[!] Inbound traffic check...\\n");
    for(int i=0; i<1024; i++) {
        // Deep Packet Inspection logic
    }
}
        """),
        ("terminal", """
$ gcc -c engine.c -o engine.o
$ gcc -c network.c -o network.o
$ gcc main.o engine.o network.o -o sentinel_xdr
$ ./sentinel_xdr --stealth --aggressive

[SYSTEM] Sentinel XDR Online.
[SYSTEM] Listening on interfaces: eth0, tun0
[SYSTEM] Deep Reasoning Core: ACTIVE
---------------------------------------
THREAT DETECTED: UNKNOWN_BOT_ACCESS
ACTION: ISOLATING...
RESULT: THREAT NEUTRALIZED.
        """)
    ]
    create_complex_coding_video(build_steps, "/root/clawd/complex_system_build.mp4")
