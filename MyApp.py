from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from shutil import copy2
from cartoonize import Cartoonize
import os
import ntpath
import threading


def open_photo_file(cartoonize):
    loadpath = filedialog.askopenfilename(initialdir="C:\\Users\\Vanja\\Desktop",
                                          title="Choose photo",
                                          filetypes=[("image", "*.jpg")])

    load_folder = 'test_images'
    name = ntpath.basename(loadpath)

    print(loadpath)
    print(name)

    # removing_old_photos(load_folder)
    #
    # copy2(loadpath, load_folder)
    #
    cartoonize.cartoonize(loadpath, name)


def open_video_file():
    print("Heloo")
    # filepath = filedialog.askopenfilename(initialdir="C:\\Users\\Vanja\\Desktop",
    #                                       title="Choose video",
    #                                       filetypes=[("video", "*.mp4")])
    # print(filepath)


def removing_old_photos(load_folder):
    list_dir = os.listdir(load_folder)
    for filename in list_dir:
        remove_path = os.path.join(load_folder, filename)
        print("Deleting file: ", remove_path)
        os.unlink(remove_path)


def start_photo_process_thread(cartoonize):
    t1 = threading.Thread(target=open_photo_file, args=(cartoonize,))
    t1.start()

def main():
    window = Tk()
    window.title("White-box cartoonization")
    window.geometry("720x480")

    # left_panel = PanedWindow(bg="black")
    # left_panel.pack(fill=BOTH, expand=True)

    # model_path = 'saved_models'
    # save_folder = 'cartoonized_images'
    # cartoonize = Cartoonize(model_path, save_folder)
    cartoon = Cartoonize('saved_models', 'cartoonized_images')

    button_photo_cartoon = Button(window, text='Cartoonize photo', command=lambda: start_photo_process_thread(cartoon))
    button_video_cartoon = Button(window, text='Cartoonize video', command=lambda: open_video_file())

    button_photo_cartoon.pack()
    button_video_cartoon.pack()

    # right_panel = PanedWindow(bg="white")
    # right_panel.pack()

    # left_panel.add(buttonPhotoCartoon)
    # left_panel.add(buttonVideoCartoon)
    # left_panel.add(right_panel)

    window.mainloop()


if __name__ == '__main__':
    main()
