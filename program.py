import sys
import time
from tkinter import *
from tkinter import filedialog, messagebox, ttk, PhotoImage, FLAT
import threading
import subprocess
import minecraft_launcher_lib
import zipfile
import os
import shutil
from PIL import Image, ImageTk
from os import system

# Define paths
current_user = os.environ['USERNAME']
app_data_directory = f"C://Users//{current_user}//AppData//Roaming//"
minecraft_folder = os.path.join(app_data_directory, ".snLauncher")
username_file_path = f"C://Users//{current_user}//username.txt"

# Creation of the mail folder for the launcher
def create_folder_if_not_exists(folder_path):
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
    print(f"Folder created at: {folder_path}")


create_folder_if_not_exists(minecraft_folder)
if not os.path.exists(username_file_path):
    with open(username_file_path, 'w') as f:
        f.write("Username")

# Get the path of the zip file with or the files for the download
if getattr(sys, 'frozen', False):
    # When running as a PyInstaller executable
    base_path = sys._MEIPASS
else:
    # When running as a normal script
    base_path = os.path.abspath(os.path.dirname(__file__))

mods_zip_path = os.path.join(base_path, "mods.zip")


def unzip_file(zip_path, extract_to_directory):
    if not os.path.exists(zip_path):
        print(f"The file {zip_path} does not exist.")
        return

    # Ensure the extraction directory exists
    os.makedirs(extract_to_directory, exist_ok=True)

    # Open the zip file and extract its contents
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        total_members = len(zip_ref.infolist())
        # Extract all members, overwriting files if necessary
        for member in zip_ref.infolist():
            zip_ref.extract(member, extract_to_directory)
            extracted_file_path = os.path.join(extract_to_directory, member.filename)
            if os.path.exists(extracted_file_path):
                print(f"Overwritten: {extracted_file_path}")
            app_window.update_idletasks()


# Global variable to store the selected memory value
global_memory_value = 7


def update_memory_label(value):
    global global_memory_value
    global_memory_value = round(float(value))
    memory_label.config(text=f'Memory (GB): {global_memory_value}')
    return global_memory_value


def create_custom_scale(panel):
    # Create a custom style for the Scale widget
    style = ttk.Style()

    # Configure the style of the trough and slider
    style.configure('Custom.Horizontal.TScale',
                    troughcolor='#f0f0f0',  # Trough color
                    background='#ffffff',  # Slider background color
                    sliderlength=20)  # Slider length

    # Create the Scale widget with the custom style
    memory_scale = ttk.Scale(panel, orient='horizontal', style='Custom.Horizontal.TScale', length=175, from_=7, to=20,
                             command=update_memory_label)
    memory_scale.pack(pady=5, padx=5)


def play_game():
    username = username_entry.get()
    memory = global_memory_value
    min_memory = global_memory_value - 1

    def run_minecraft():
        print(username)
        print(memory)
        # Save username to file
        with open(username_file_path, 'w') as file:
            file.write(username)

        # Minecraft launch options
        options = {
            'username': username,
            'uuid': '',
            'token': '',
            "jvmArguments": [f"-Xmx{memory}G", f"-Xms{min_memory}G"],
            "launcherVersion": "0.0.1",
        }

        # Get Minecraft command
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(
            "1.12.2-forge-14.23.5.2860", minecraft_folder, options)

        # Close the tkinter window
        app_window.destroy()

        # Run Minecraft
        subprocess.run(minecraft_command)

    # Check if selected memory is sufficient
    if memory <= 8:
        response = messagebox.askokcancel("Warning",
                                          "The selected memory is low and may cause performance issues on big modpacks. It's recommended to use at least 9GB. Do you want to continue?")
        if response:
            run_minecraft()
        else:
            print("Cancelled")
    else:
        run_minecraft()


def download_files():
    disable_reset_button()
    show_progress_bar()
    disable_download_button()

    # Initialize progress bar
    for progress in range(25):
        progress_var.set(progress)
        app_window.update_idletasks()
        app_window.after(50)
    print("Download started, please wait")

    def run_download_process():
        forge_version = minecraft_launcher_lib.forge.find_forge_version('1.12.2')
        # Forge is included on the zip file. The commented command is for the installation of forge.
        # minecraft_launcher_lib.forge.install_forge_version(forge_version, minecraft_folder)

        # Update progress bar for unzipping process
        for progress in range(26, 51):
            progress_var.set(progress)
            app_window.update_idletasks()
            app_window.after(10)
        print("Unzipping files")
        unzip_file(mods_zip_path, minecraft_folder)
        progress_var.set(75)
        app_window.update_idletasks()

        enable_play_button()
        for progress in range(76, 101):
            progress_var.set(progress)
            app_window.update_idletasks()
            app_window.after(10)
        enable_reset_button()
        print("Completed")

    # Start the thread for the download process
    threading.Thread(target=run_download_process).start()


def enable_play_button():
    if os.path.exists(minecraft_folder) and os.listdir(minecraft_folder):
        play_button.config(state='normal')
    else:
        play_button.config(state='disabled')


def disable_download_button():
    download_button.config(state='disabled')


def initialize_download_button_state():
    if os.path.exists(minecraft_folder) and os.listdir(minecraft_folder):
        download_button.config(state='disabled')
    else:
        download_button.config(state='normal')


def show_progress_bar():
    progress_bar = ttk.Progressbar(progress_panel, orient="horizontal", length=320, mode="determinate",
                                   variable=progress_var)
    progress_bar.grid(row=0, column=0)


def read_file_content(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    else:
        return None


def reset_game():
    def reinstall():
        with open(username_file_path, 'w') as file:
            file.write("Username")
        shutil.rmtree(minecraft_folder)
        print("Launcher directory has been deleted")
        print("Restarting the program in 5s")
        time.sleep(5)
        app_window.destroy()

    response = messagebox.askokcancel("Warning",
                                      "If you reinstall Minecraft, all config data will be lost. To keep it, just copy and paste the necessary files from .snlauncher directory. (Click Cancel to avoid reinstalling Minecraft).")
    if response:
        reinstall()
    else:
        print("Cancelled")


def disable_reset_button():
    reset_button.config(state='disabled')


def enable_reset_button():
    reset_button.config(state='normal')

#=========================
#GUI WITH TKINTER
#=========================

# Initialize tkinter application
app_window = Tk()

# Set window size
app_window.geometry('1020x630+0+0')

# Prevent window resizing
app_window.resizable(0, 0)

# Set window title and icon
app_window.title("Olivgard - Launcher")
icon_path = os.path.join(base_path, "multimedia//img.ico")
app_window.iconbitmap(icon_path)

# Set background image
background_img_path = os.path.join(base_path, "multimedia//background.png")
background_img = Image.open(background_img_path)
background_img_tk = ImageTk.PhotoImage(background_img)

canvas = Canvas(app_window)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_img_tk, anchor="nw")
app_window.config(bg='sea green')

# Top panel
top_panel = Frame(app_window, bd=1, relief=FLAT, bg='SkyBlue4')
top_panel.place(relx=0.5, y=10, anchor='n')  # Centered at the top

# Load title image
title_img_path = os.path.join(base_path, "multimedia//title.png")
title_image = Image.open(title_img_path)
new_width = 500
new_height = int((new_width / 1024) * 273)
title_image = title_image.resize((new_width, new_height))
title_img_tk = ImageTk.PhotoImage(title_image)

# Title label as an image
title_label = Label(top_panel, image=title_img_tk, bg='SkyBlue4')
title_label.grid(row=0, column=0)

# Panel for username entry
username_panel = Frame(app_window, bd=1, relief=FLAT)
username_panel.place(relx=0.5, y=160, anchor='n')

# Username entry
username_entry = Entry(username_panel, font=("Dosis", 12, "bold"))
username_entry.grid(row=0, column=0)
file_content = read_file_content(username_file_path)
if file_content is not None:
    username_entry.insert(0, file_content)

# Panel for memory slider
slider_panel = Frame(app_window)
slider_panel.place(relx=0.5, y=195, anchor='n')

# Memory slider
create_custom_scale(slider_panel)

# Panel for memory label
memory_label_panel = Frame(app_window)
memory_label_panel.place(relx=0.5, y=235, anchor='n')

# Memory label
memory_label = Label(memory_label_panel, text="Memory (GB): 7")
memory_label.grid(row=0, column=0)

# Panel for play button
play_panel = Frame(app_window, bd=1, relief=FLAT)
play_panel.place(relx=0.5, y=260, anchor='n')

# Load play button image
play_img_path = os.path.join(base_path, "multimedia//play.png")
play_img_tk = PhotoImage(file=play_img_path)

# Play button
play_button = Button(play_panel, image=play_img_tk, width=500)
play_button.grid(row=0, column=0)
play_button.config(command=play_game)

# Panel for download button
download_panel = Frame(app_window, bd=1, relief=FLAT)
download_panel.place(relx=0.5, y=330, anchor='n')

# Load download button image
download_img_path = os.path.join(base_path, "multimedia//download.png")
download_img_tk = PhotoImage(file=download_img_path)

# Download button
download_button = Button(download_panel, image=download_img_tk, width=500)
download_button.grid(row=0, column=0)
download_button.config(command=download_files)

# Progress bar panel
progress_panel = Frame(app_window, bd=1, relief=FLAT)
progress_panel.place(relx=0.5, y=480, anchor='n')

progress_var = DoubleVar()
progress_bar = ttk.Progressbar(progress_panel, orient="horizontal", length=320, mode="determinate",
                               variable=progress_var)
progress_bar.grid(row=0, column=0)

progress_bar.grid_remove()

# Update the state of the play button
enable_play_button()

# Initialize the state of the download button
initialize_download_button_state()

# Panel for reset button
reset_panel = Frame(app_window, bd=1, relief=FLAT)
reset_panel.place(relx=0.5, y=400, anchor='n')

# Load reset button image
reset_img_path = os.path.join(base_path, "multimedia//reinstall.png")
reset_img_tk = PhotoImage(file=reset_img_path)

# Reset button
reset_button = Button(reset_panel, image=reset_img_tk, width=500)
reset_button.grid(row=0, column=0)
reset_button.config(command=reset_game)

# Prevent the window from closing immediately
app_window.mainloop()
