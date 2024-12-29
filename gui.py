import os

os.environ['TCL_LIBRARY'] = r'C:\Users\ACER\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\ACER\AppData\Local\Programs\Python\Python313\tcl\tk8.6'

import pygame
import time
from pygame.locals import QUIT
import tkinter as tk
from tkinter import filedialog, messagebox
from algorithm import create_random_undirected_graph, graph_coloring, visualize_graph



# Đường dẫn đến file nhạc
audio_file = 'D:\WORKING_ON\thisSemester\AI\final\music.mp3'

def play_background_music(audio_file):
    """
    Chơi nhạc nền khi chương trình chạy
    """
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)  # Đường dẫn đến file nhạc nền
    pygame.mixer.music.play(-1)  # Phát nhạc lặp lại liên tục


def play_sound_effect(audio_file_1):
    """
    Phát hiệu ứng âm thanh khi chương trình chạy
    """
    pygame.mixer.Sound(audio_file_1).play()


def setup_gui():
    # Initialize tkinter window
    root = tk.Tk()
    root.title("Graph Visualization with Sound")

    # Create a frame for the graph visualization
    canvas_frame = tk.Frame(root)
    canvas_frame.pack()

    # Khởi tạo Pygame và hiển thị cửa sổ
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Graph Visualization with Sound and Timer')

    def upload_music():
        file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if file_path:
            play_background_music(file_path)

    def upload_sound_effect():
        file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if file_path:
            play_sound_effect(file_path)

    # Button to upload music and sound effect
    upload_music_button = tk.Button(root, text="Upload Music", command=upload_music)
    upload_music_button.pack()

    upload_sound_button = tk.Button(root, text="Upload Sound Effect", command=upload_sound_effect)
    upload_sound_button.pack()

    # Button to play music and sound effect
    play_music_button = tk.Button(root, text="Play Music", command=lambda: play_background_music(audio_file))
    play_music_button.pack()

    play_sound_button = tk.Button(root, text="Play Sound Effect", command=lambda: play_sound_effect(audio_file))
    play_sound_button.pack()

    return root, canvas_frame, 


def main():
    # Set up GUI and get references
    root, canvas_frame, screen = setup_gui()

    # Tạo đồ thị mẫu
    G = create_random_undirected_graph(10, 15)

    # Tô màu đồ thị
    colors = graph_coloring(G)

    # Hiển thị đồ thị
    visualize_graph(G, colors, canvas_frame)

    # Bắt đầu hẹn giờ và hiệu ứng âm thanh
    timer_start = pygame.time.get_ticks()

    # Vòng lặp chính của Pygame
    running = True
    while running:
        screen.fill((255, 255, 255))  # Làm mới màn hình
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Kiểm tra thời gian để dừng nhạc nền sau 30 giây
        if pygame.time.get_ticks() - timer_start > 30000:  # 30 giây
            pygame.mixer.music.stop()

        pygame.display.flip()

    pygame.quit()

    # Start the tkinter main loop
    root.mainloop()


if __name__ == "__main__":
    main()