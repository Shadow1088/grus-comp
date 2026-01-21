from io import BytesIO
from PIL import Image

def compress_image(data: bytes, max_bytes: int = 8_000_000) -> bytes:
    if len(data) <= max_bytes:
        return data

    img = Image.open(BytesIO(data))
    # Convert to RGB if it's RGBA (JPEGs don't support alpha)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Strategy: Start with a significant resize if the file is massive
    # This prevents the loop from running 100 times
    quality = 85
    proportion = 0.9
    
    output = BytesIO()
    img.save(output, format='JPEG', quality=quality)
    
    while len(output.getvalue()) > max_bytes:
        output = BytesIO()
        width, height = img.size
        # Shrink dimensions dynamically based on how far over the limit we are
        img = img.resize((int(width * proportion), int(height * proportion)), Image.Resampling.LANCZOS)
        img.save(output, format='JPEG', quality=quality)
        
        # If still too big, drop quality slightly
        if quality > 40:
            quality -= 5
            
    return output.getvalue()


import ffmpeg
import os
import tempfile
import json

def compress_video(data: bytes, filename: str, max_bytes: int = 8_000_000):
    if len(data) <= max_bytes:
        return data

    # 1. Create temp files for input and output
    suffix = os.path.splitext(filename)[-1] or ".mp4"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as in_file:
        in_file.write(data)
        in_path = in_file.name
    
    out_path = tempfile.mktemp(suffix=".mp4")

    try:
        # 2. Get duration using ffprobe
        probe = ffmpeg.probe(in_path)
        duration = float(probe['format']['duration'])
        
        # 3. Calculate target bitrate (90% of max to allow for muxing overhead)
        # target_bitrate = (total_bits / duration)
        target_total_bits = (max_bytes * 8) * 0.9
        audio_bitrate = 128_000 # 128k for audio
        video_bitrate = (target_total_bits / duration) - audio_bitrate
        
        # Guard against negative bitrate for very long videos
        video_bitrate = max(video_bitrate, 150_000) 

        # 4. Run FFmpeg compression
        # We use a single pass here for speed, but constrained by the calculated bitrate
        (
            ffmpeg
            .input(in_path)
            .output(out_path, 
                    **{
                        'c:v': 'libx264',
                        'b:v': int(video_bitrate),
                        'maxrate': int(video_bitrate * 1.5),
                        'bufsize': int(video_bitrate * 2),
                        'pix_fmt': 'yuv420p', # Ensures compatibility
                        'preset': 'faster',
                        'c:a': 'aac',
                        'b:a': '128k',
                        'vf': 'scale=iw*min(1\,720/ih):ih*min(1\,720/ih)' # Scale to 720p max
                    })
            .overwrite_output()
            .run(quiet=True)
        )

        with open(out_path, "rb") as f:
            return f.read()

    finally:
        if os.path.exists(in_path): os.remove(in_path)
        if os.path.exists(out_path): os.remove(out_path)