#!/usr/bin/env python3

import subprocess
import re
import argparse

def run_silence_detect(input_file):
    ffmpeg_cmd = [
        "ffmpeg", "-i", input_file,
        "-hide_banner",
        "-af", "silencedetect=n=-50dB:d=1",
        "-f", "null", "-"
    ]
    result = subprocess.run(ffmpeg_cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
    return result.stderr

def parse_silence_and_generate_command(ffmpeg_log, input_file):
    selectionsList = []
    timeSelection = "between(t,0,"
    start = end = None

    for line in ffmpeg_log.splitlines():
        end_match = re.search(r"silence_start: (\d+\.?\d+)", line)
        if end_match:
            end = end_match.group(1)

        start_match = re.search(r"silence_end: (\d+\.?\d+)", line)
        if start_match:
            start = start_match.group(1)
            timeSelection = f"between(t,{start},"

        if end:
            timeSelection += f"{end})"
            selectionsList.append(timeSelection)
            timeSelection = "between(t,0,"
            end = None

    if not selectionsList:
        raise RuntimeError("No silence regions detected or parsed.")

    selectionFilter = "+".join(selectionsList)
    vfilter = f"select='{selectionFilter}',setpts=N/FRAME_RATE/TB"
    afilter = f"aselect='{selectionFilter}',asetpts=N/SR/TB"

    output_file = f"outfile_{input_file}"
    ffmpeg_args = [
        "ffmpeg", "-i", input_file,
        "-vf", vfilter,
        "-af", afilter,
        output_file
    ]
    return ffmpeg_args

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove silent parts from a video using ffmpeg.")
    parser.add_argument("input_file", help="Path to the input video file")
    args = parser.parse_args()

    ffmpeg_output = run_silence_detect(args.input_file)
    ffmpeg_command = parse_silence_and_generate_command(ffmpeg_output, args.input_file)

    print("Running:", " ".join(ffmpeg_command))
    subprocess.run(ffmpeg_command)
