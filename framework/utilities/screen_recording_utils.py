import os
import subprocess
import time

_video_process = None
_video_file_path = None

def start_video_recording(test_name, screen_size="1920x1080", framerate=15):
    """Start ffmpeg screen recording for the given test."""
    global _video_process, _video_file_path
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    video_dir = os.path.join(os.getcwd(), 'output', 'videos')
    os.makedirs(video_dir, exist_ok=True)
    safe_name = test_name.replace(' ', '_')
    _video_file_path = os.path.join(video_dir, f"test_{safe_name}_{timestamp}.mp4")
    ffmpeg_cmd = [
        'ffmpeg', '-y', '-f', 'gdigrab', '-framerate', str(framerate), '-video_size', screen_size, '-i', 'desktop',
        '-vcodec', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', _video_file_path
    ]
    _video_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return _video_file_path


def stop_video_recording():
    """Stop ffmpeg screen recording gracefully."""
    global _video_process, _video_file_path
    if _video_process:
        try:
            _video_process.communicate(input=b'q', timeout=5)
        except Exception:
            _video_process.terminate()
            _video_process.wait()
        _video_process = None
    return _video_file_path
