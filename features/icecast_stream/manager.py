import subprocess
import signal
from .state import STREAM_STATE

ICECAST_URL = "icecast://source:mksheela@127.0.0.1:8000/radio.mp3"

def start_stream(source: str):
    if STREAM_STATE["playing"]:
        raise RuntimeError("Stream already running")

    cmd = [
        "ffmpeg",
        "-re",
        "-i", source,
        "-vn",
        "-c:a", "libmp3lame",
        "-b:a", "128k",
        "-f", "mp3",
        ICECAST_URL,
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    STREAM_STATE.update({
        "playing": True,
        "paused": False,
        "source": source,
        "process": process,
    })


def stop_stream():
    process = STREAM_STATE.get("process")
    if process:
        process.kill()

    STREAM_STATE.update({
        "playing": False,
        "paused": False,
        "source": None,
        "process": None,
    })


def pause_stream():
    process = STREAM_STATE.get("process")
    if process and not STREAM_STATE["paused"]:
        process.send_signal(signal.SIGSTOP)
        STREAM_STATE["paused"] = True


def resume_stream():
    process = STREAM_STATE.get("process")
    if process and STREAM_STATE["paused"]:
        process.send_signal(signal.SIGCONT)
        STREAM_STATE["paused"] = False