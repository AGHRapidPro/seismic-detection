import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import math
import numpy as np
import obspy
# Version 1.7: Moved value reading inside the button functions to capture input only when buttons are pressed.

# Create the root window
root = tk.Tk()
root.title("Rapid Seismic App")  # Change window name
root.geometry("600x600")

# Set modern theme colors
bg_color = "#1F1F1F"  # Dark background color
primary_color = "#007ACC"  # Blue for buttons and active elements
text_color = "#FFFFFF"  # White text color
accent_color = "#3B3B3B"  # Darker accent

# Configure root window with dark background
root.configure(bg=bg_color)

# Global variables to store the paths of the selected files
selected_csv_path = None
# Static PNG file path (set to "test.png")
static_png_path = "test.png"  # Update to your actual PNG file path if necessary
original_img = None
fhd_img = None
def load_mseed_file(filepath):
    st = obspy.read(filepath)
    trace = st.traces[0].copy()

    times = trace.times()
    data = trace.data
    stats = trace.stats

    return times, data, stats
# Placeholder function 1 (now handles loading/resizing the .png file)
def func1():
    value = int(func1_entry.get())  # Get the value from the input field for func1 when the button is pressed
    print(f"Function 1 input value: {value}")
    global original_img, fhd_img

    xaxis = []
    yaxis = []
    stats = []
    xaxis,yaxis,stats = load_mseed_file("code\XB.ELYSE.02.BHV.2021-05-02HR01_evid0017.mseed")
    #for x in dataraw:
    #    data.append(x.split(','))
    #for x in data[1:]:
    #    xaxis.append(float(x[1]))
    #    yaxis.append(float(x[2]))
    fig, axs = plt.subplots(2,figsize=(19,5))
    axs[0].plot(xaxis, yaxis)
    axs[0].set(xlabel='time (s)', ylabel='amplitude (m/s)',title='original_data') #c/s or m/s
    axs[0].grid()
    axs[0].axhline(y = value, color = 'r', linestyle = '-')
    for i in range(len(xaxis)):
        if yaxis[i]>=value:
            axs[0].axvline(x = xaxis[i],color = 'g', linestyle = '-')
    #dodać zapis do .csv
    fig.savefig("test.png",dpi = 300)
    try:
        # Load the static .png file and store the original image
        original_img = Image.open(static_png_path)

        # Compress the image to FHD and store it
        fhd_img = compress_to_fhd(original_img)

        # Display the compressed image, resized to fit the window
        resize_image()

        label.config(text=f"Function 1 executed: Loaded and resized the image with input {value}")
        print(f"Function 1 executed: Loaded and resized the image with input {value}")

    except Exception as e:
        label.config(text=f"Error loading image in func1: {e}")
        print(f"Error loading image in func1: {e}")

# Placeholder function 2 (also handles loading/resizing the .png file)
def func2():
    value = func2_entry.get()  # Get the value from the input field for func2 when the button is pressed
    print(f"Function 2 input value: {value}")
    global original_img, fhd_img

    try:
        # Load the static .png file and store the original image
        original_img = Image.open(static_png_path)

        # Compress the image to FHD and store it
        fhd_img = compress_to_fhd(original_img)

        # Display the compressed image, resized to fit the window
        resize_image()

        label.config(text=f"Function 2 executed: Loaded and resized the image with input {value}")
        print(f"Function 2 executed: Loaded and resized the image with input {value}")

    except Exception as e:
        label.config(text=f"Error loading image in func2: {e}")
        print(f"Error loading image in func2: {e}")

# Function to open file explorer and get CSV file path
def open_csv_explorer():
    value = csv_entry.get()  # Get the value from the CSV input field when the button is pressed
    print(f"CSV file input value: {value}")
    global selected_csv_path
    selected_csv_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])  # Open file dialog for .csv files

    if selected_csv_path:
        label.config(text=f"Selected CSV File: {selected_csv_path} with input {value}")  # Display selected file
        print(f"Selected CSV File: {selected_csv_path} with input {value}")
    else:
        label.config(text="No CSV file selected")
        print("No CSV file selected")

# Function to compress image to FHD (1920x1080) while maintaining aspect ratio
def compress_to_fhd(image):
    max_width, max_height = 1920, 1080
    width, height = image.size

    # If the image is larger than FHD, compress it while maintaining aspect ratio
    if width > max_width or height > max_height:
        ratio = min(max_width / width, max_height / height)
        new_size = (int(width * ratio), int(height * ratio))
        return image.resize(new_size, Image.Resampling.LANCZOS)

    # If the image is already within FHD, return it unchanged
    return image

# Function to resize image dynamically based on window size while maintaining aspect ratio
def resize_image(event=None):
    if fhd_img:
        # Get the current window size
        window_width = root.winfo_width()
        window_height = root.winfo_height()

        # Get the original size of the FHD image
        img_width, img_height = fhd_img.size

        # Calculate the appropriate ratio to fit the image into the window, preserving aspect ratio
        ratio = min((window_width - 100) / img_width, (window_height - 200) / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)

        # Resize the image based on the calculated size while maintaining the aspect ratio
        resized_img = fhd_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(resized_img)  # Convert to Tkinter-compatible image

        # Set the image to the label
        image_label.config(image=img_tk)
        image_label.image = img_tk  # Keep a reference to avoid garbage collection

    # Update the size label with the current window dimensions
    update_size_label()

# Function to update size label
def update_size_label():
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    size_label.config(text=f"[{window_width}] x [{window_height}]")

# Create a frame for the main content
main_frame = tk.Frame(root, bg=bg_color)
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Frame to hold the buttons in a horizontal line
button_frame = tk.Frame(main_frame, bg=bg_color)  # Set background color for frame
button_frame.pack(pady=10)

# Button to trigger CSV file explorer
btn_csv = tk.Button(button_frame, text="Choose CSV File", command=open_csv_explorer, bg=primary_color, fg=text_color, font=("Helvetica", 12), relief=tk.FLAT)
btn_csv.pack(side=tk.LEFT, padx=10)

# Entry field for CSV input value
csv_entry = tk.Entry(button_frame, bg=accent_color, fg=text_color, font=("Helvetica", 12), width=10, relief=tk.FLAT)
csv_entry.pack(side=tk.LEFT, padx=10)

# Button to execute func1 (now loads and resizes the .png)
btn_func1 = tk.Button(button_frame, text="Execute Function 1", command=func1, bg=primary_color, fg=text_color, font=("Helvetica", 12), relief=tk.FLAT)
btn_func1.pack(side=tk.LEFT, padx=10)

# Entry field for Function 1 input value
func1_entry = tk.Entry(button_frame, bg=accent_color, fg=text_color, font=("Helvetica", 12), width=10, relief=tk.FLAT)
func1_entry.pack(side=tk.LEFT, padx=10)

# Button to execute func2 (now loads and resizes the .png)
btn_func2 = tk.Button(button_frame, text="Execute Function 2", command=func2, bg=primary_color, fg=text_color, font=("Helvetica", 12), relief=tk.FLAT)
btn_func2.pack(side=tk.LEFT, padx=10)

# Entry field for Function 2 input value
func2_entry = tk.Entry(button_frame, bg=accent_color, fg=text_color, font=("Helvetica", 12), width=10, relief=tk.FLAT)
func2_entry.pack(side=tk.LEFT, padx=10)

# Label to show selected file
label = tk.Label(main_frame, text="No file selected", bg=bg_color, fg=text_color, font=("Helvetica", 14))
label.pack(pady=20)

# Label to display image (initially empty)
image_label = tk.Label(main_frame, bg=bg_color)
image_label.pack(pady=20)

# Label to show current window size
size_label = tk.Label(main_frame, text="[600] x [600]", bg=bg_color, fg=text_color, font=("Helvetica", 12))
size_label.pack(pady=10)

# Bind the window resize event to the resize_image function
root.bind("<Configure>", lambda event: [resize_image(event), update_size_label()])

# Run the application
root.mainloop()
