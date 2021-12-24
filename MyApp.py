from tkinter import *
from tkinter import filedialog
from cartoonize import Cartoonize
from ffmpegOperations import convert_mov_to_seq
from ffmpegOperations import convert_seq_to_mov
from cv2 import cv2
import os
import ntpath
import threading
import moviepy.editor as mp


def open_photo_file(cartoonize):
    load_path = filedialog.askopenfilename(initialdir="C:\\Users\\Vanja\\Desktop",
                                           title="Choose photo",
                                           filetypes=[("image", "*.jpg")])
    if len(load_path) != 0:
        name = ntpath.basename(load_path)
        cartoonize.cartoonize(load_path, name, 'cartoonized_images')


def open_video_file(cartoonize):
    load_path = filedialog.askopenfilename(initialdir="C:\\Users\\Vanja\\Desktop",
                                           title="Choose video",
                                           filetypes=[("video", "*.mp4")])

    if len(load_path) != 0:
        output_test_folder = 'test_images'
        output_cartoonized_folder = 'cartoonized_video_images'
        save_folder = 'cartoonized_images'
        removing_old_files(output_test_folder)
        removing_old_files(output_cartoonized_folder)
        name = ntpath.basename(load_path)
        convert_mov_to_seq(load_path, output_test_folder)
        cartoonize_iterate(cartoonize, output_test_folder, output_cartoonized_folder)
        cap = cv2.VideoCapture(load_path)
        frame_rate = cap.get(cv2.CAP_PROP_FPS)

        new_clip_dir = os.path.join(save_folder, name)

        files = []
        name_list = os.listdir(output_cartoonized_folder)
        for name in name_list:
            temp = f"{output_cartoonized_folder}\{name}"
            files.append(temp)

        removing_old_files("audio")

        my_clip = mp.VideoFileClip(load_path)
        my_clip.audio.write_audiofile(r"audio/my_result.mp3")
        new_audio_dir = r"audio/my_result.mp3"
        new_audio = mp.AudioFileClip(new_audio_dir)

        convert_seq_to_mov(new_clip_dir, files, frame_rate, new_audio)


def cartoonize_iterate(cartoon, load_folder='test_images', cartoonized_folder='cartoonized_video_images'):
    name_list = os.listdir(load_folder)
    for name in name_list:
        load_path = os.path.join(load_folder, name)
        cartoon.cartoonize(load_path, name, cartoonized_folder)


def removing_old_files(load_folder):
    list_dir = os.listdir(load_folder)
    for filename in list_dir:
        remove_path = os.path.join(load_folder, filename)
        os.unlink(remove_path)


def start_photo_process_thread(cartoonize):
    t1 = threading.Thread(target=open_photo_file, args=(cartoonize,))
    t1.start()


def start_video_process_thread(cartoonize):
    t2 = threading.Thread(target=open_video_file, args=(cartoonize,))
    t2.start()


window = Tk()
window.title("White-box cartoonization")
window.minsize(721, 480)
window.config(bg="#765898")
window.iconbitmap("dummy_photos/icon.ico")

# cartoon = Cartoonize('saved_models')


# button_photo_cartoon.pack()
# button_video_cartoon.pack()

left_frame = Frame(window, width=400, height=480, bg='#090314')
left_frame.grid(row=0, column=0, padx=10, pady=5)
right_frame = Frame(window, width=550, height=480, bg='#090314')
right_frame.grid(row=0, column=1, padx=10, pady=5)
tool_bar = Frame(left_frame, width=180, height=300, bg='#090314')
tool_bar.grid(row=2, column=0, padx=5, pady=5)
left_image = PhotoImage(file="dummy_photos/real life.png")
original_image = left_image.subsample(2, 2)  # resize image using subsample
left_img_lbl = Label(left_frame, image=original_image)
left_img_lbl.grid(row=1, column=0, padx=5, pady=5)

right_image = PhotoImage(file="dummy_photos/cartoon.png")
right_image_lbl = Label(right_frame, image=right_image)
right_image_lbl.grid(row=0, column=0, padx=5, pady=5)

# , command=lambda: start_photo_process_thread(cartoon)
# , command=lambda: start_video_process_thread(cartoon)
button_photo_cartoon = Button(tool_bar, text='Cartoonize photo')
button_video_cartoon = Button(tool_bar, text='Cartoonize video')

Label(left_frame, text="Original Image", background="#090314", foreground='white').grid(row=0, column=0, padx=5, pady=5)

button_photo_cartoon.grid(row=3, column=0, padx=7, pady=150)
button_video_cartoon.grid(row=3, column=1, padx=7, pady=150)

window.mainloop()
