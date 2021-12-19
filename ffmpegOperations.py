import ntpath
import os
import subprocess
import moviepy.editor as mp




def convert_mov_to_seq(video_path, output_folder):
    video_input = f"{video_path}"
    output_name = os.path.join(output_folder, "out")
    sequence_output = f"{output_name}.%03d.png"
    cmd = f'ffmpeg  -i "{video_input}" "{sequence_output}"'
    subprocess.check_output(cmd, shell=True)

def convert_seq_to_mov(name, files, frame_rate, audio_clip):
    clip = mp.ImageSequenceClip(files,fps=frame_rate)
    clip.audio = audio_clip
    clip.write_videofile(name, fps = frame_rate)

