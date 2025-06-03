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
    silence_periods = []
    
    # Parse silence start and end times
    for line in ffmpeg_log.splitlines():
        silence_start_match = re.search(r"silence_start: (\d+\.?\d+)", line)
        if silence_start_match:
            silence_start = float(silence_start_match.group(1))
            
        silence_end_match = re.search(r"silence_end: (\d+\.?\d+)", line)
        if silence_end_match:
            silence_end = float(silence_end_match.group(1))
            if 'silence_start' in locals():
                silence_periods.append((silence_start, silence_end))
    
    if not silence_periods:
        print("No silence regions detected. The video will be copied as-is.")
        return ["ffmpeg", "-i", input_file, "-c", "copy", f"outfile_{input_file}"]
    
    # Get video duration
    duration_cmd = ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", input_file]
    duration_result = subprocess.run(duration_cmd, capture_output=True, text=True)
    total_duration = float(duration_result.stdout.strip())
    
    # Create segments to keep (non-silent parts)
    segments_to_keep = []
    current_time = 0.0
    
    for silence_start, silence_end in silence_periods:
        # Add the segment before this silence (if it exists and is meaningful)
        if silence_start > current_time:
            segments_to_keep.append(f"between(t,{current_time},{silence_start})")
        current_time = silence_end
    
    # Add the final segment after the last silence
    if current_time < total_duration:
        segments_to_keep.append(f"between(t,{current_time},{total_duration})")
    
    if not segments_to_keep:
        raise RuntimeError("All content would be removed. Check silence detection parameters.")
    
    selectionFilter = "+".join(segments_to_keep)
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
