from tkinter import *
from tkinter import filedialog, ttk
from cartoonize import Cartoonize
from ffmpegOperations import convert_mov_to_seq
from ffmpegOperations import convert_seq_to_mov
from PIL import ImageTk, Image
from cv2 import cv2
import os
import ntpath
import threading
import moviepy.editor as mp


def open_photo_file(cartoonize):
    load_path = filedialog.askopenfilename(initialdir="C:\\Users\\Vanja\\Desktop",
                                           title="Choose photo",
                                           filetypes=[("image", "*.jpg"), ("image", "*jpeg")])

    global left_img_lbl
    global right_image_lbl
    global left_frame
    global right_frame
    global left_image
    global right_image

    if len(load_path) != 0:
        name = ntpath.basename(load_path)
        cartoonize.cartoonize(load_path, name, 'cartoonized_images')

        img = Image.open(load_path)

        if img.width > left_frame.winfo_width() or img.height > left_frame.winfo_height():
            resized = img.resize((left_frame.winfo_width(), int(left_frame.winfo_width() * img.height / img.width)),
                                 Image.ANTIALIAS)
        else:
            resized = img.resize((int(img.width / 2), int(img.height / 2)), Image.ANTIALIAS)
        left_img_lbl.grid_forget()
        left_image = ImageTk.PhotoImage(resized)
        left_img_lbl = Label(left_frame, image=left_image, borderwidth=0)
        left_img_lbl.grid(row=1, column=0, padx=5, pady=5)

        relative_path = os.path.join('cartoonized_images', name)
        img2 = Image.open(relative_path)

        if img2.width > right_frame.winfo_width() or img2.height > right_frame.winfo_height():
            resized2 = img2.resize((right_frame.winfo_width(), int(right_frame.winfo_width() * img2.height / img2.width)),
                                 Image.ANTIALIAS)
        else:
            resized2 = img2.resize((int(img2.width / 2), int(img2.height / 2)), Image.ANTIALIAS)
        right_image_lbl.grid_forget()
        right_image = ImageTk.PhotoImage(resized2)
        right_image_lbl = Label(right_frame, image=right_image, borderwidth=0)
        right_image_lbl.grid(row=1, column=0, padx=5, pady=5)


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


cartoon = Cartoonize('saved_models')
window = Tk()
window.title("White-box Cartoonization")
window.minsize(1025, 500)
window.geometry("1025x500")
window.iconbitmap("dummy_photos/icon.ico")

darker_color = '#090314'
lighter_color = "#765898"
window.config(bg=lighter_color)


left_frame = Frame(window, width=window.winfo_width() / 2 - 150, height=window.winfo_height() - 10, bg=darker_color)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nswe')
right_frame = Frame(window, width=window.winfo_width() / 2 + 80, height=window.winfo_height() - 10, bg=darker_color)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nswe')
tool_bar = Frame(left_frame, width=180, height=50, bg=darker_color)
tool_bar.grid(row=2, column=0, padx=5, pady=5)
left_image = PhotoImage(file="dummy_photos/real life.png")
original_image = left_image.subsample(2, 2)  # resize image using subsample
left_img_lbl = Label(left_frame, image=original_image, borderwidth=0)
left_img_lbl.grid(row=1, column=0, padx=5, pady=5)
right_image = PhotoImage(file="dummy_photos/cartoon.png")
right_image_lbl = Label(right_frame, image=right_image, borderwidth=0)
right_image_lbl.grid(row=1, column=0, padx=5, pady=5)

button_photo_cartoon = Button(tool_bar, background=lighter_color, highlightcolor=lighter_color, text='Cartoonize photo',
                              command=lambda: start_photo_process_thread(cartoon))
button_video_cartoon = Button(tool_bar, text='Cartoonize video', command=lambda: start_video_process_thread(cartoon))

original_txt = Label(left_frame, text="Original Image", background="#090314", foreground='white', height=3)
original_txt.grid(row=0, column=0, padx=5, pady=5)

cartoon_txt = Label(right_frame, text="Cartoon Image", background="#090314", foreground='white', height=3)
cartoon_txt.grid(row=0, column=0, padx=5, pady=5)

button_photo_cartoon.grid(row=0, column=0, padx=7, pady=150)
button_video_cartoon.grid(row=0, column=1, padx=7, pady=150)
window.grid_columnconfigure('all', weight=1)
window.grid_rowconfigure('all', weight=1)
left_frame.grid_columnconfigure('all', weight=1)
left_frame.grid_rowconfigure('all', weight=1)
right_frame.grid_rowconfigure('all', weight=1)
right_frame.grid_columnconfigure('all', weight=1)

window.mainloop()
