from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from cartoonize import Cartoonize


def openPhotoFile(cartoonize):
    # filepath = filedialog.askopenfilename(initialdir="C:\\Users\\Vanja\\Desktop",
    #                                       title="Choose photo",
    #                                       filetypes=[("image", "*.jpg")])
    # print(filepath)

    model_path = 'saved_models'
    load_folder = 'test_images'
    save_folder = 'cartoonized_images'
    cartoonize.cartoonize(load_folder, save_folder, model_path)


def openVideoFile():
    print("Heloo")
    # filepath = filedialog.askopenfilename(initialdir="C:\\Users\\Vanja\\Desktop",
    #                                       title="Choose video",
    #                                       filetypes=[("video", "*.mp4")])
    # print(filepath)


def main():
    window = Tk()
    window.title("White-box cartoonization")
    window.geometry("720x480")

    # left_panel = PanedWindow(bg="black")
    # left_panel.pack(fill=BOTH, expand=True)

    cartoonize = Cartoonize()

    button_photo_cartoon = Button(window, text='Cartoonize photo', command=lambda: openPhotoFile(cartoonize))
    button_video_cartoon = Button(window, text='Cartoonize video', command=lambda: openVideoFile())

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
