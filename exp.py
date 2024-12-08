import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.font import Font
from PIL import Image, ImageTk
import os
import fitz  # PyMuPDF

# Function to create the static directory if it doesn't exist
def create_static_directory():
    directory = 'static/'
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created")
    else:
        print(f"Directory '{directory}' already exists")

# Call the function to create the static directory
create_static_directory()

# Defining globally accessible variables
pdf_writer = fitz.open()
window = tk.Tk()

# Function for removing widgets
def remove_elements(split_button, merge_button, add_button, i2p_button, header, text):
    split_button.destroy()
    merge_button.destroy()
    add_button.destroy()
    i2p_button.destroy()
    header.destroy()
    if text == "split_pdf":
        split_pdf()
    elif text == "i2p":
        pass
    elif text == "merge_pdf":
        pass
    elif text == "add_pages":
        pass

# Function for selecting multiple files
def select_multiple_file():
    file_path = list(filedialog.askopenfilenames())
    return file_path

# Function for selecting a single file
def select_file():
    file_path = filedialog.askopenfilename()
    return file_path

# Function for saving the output file
def save_file():
    file_path = filedialog.asksaveasfilename(
        title="Save As",
        defaultextension=".pdf",
        filetypes=[("PDF Files", ".pdf"), ("All Files", ".*")]
    )
    return file_path

def savefile():
    with open(save_file(), 'wb') as output_file:
        pdf_writer.save(output_file)

def show_preview(file, button):
    button.destroy()
    # Create a frame for the content
    frame = tk.Frame(window, bg="black")
    frame.pack(fill=BOTH, expand=True)
    # Add a canvas for scrolling
    canvas = tk.Canvas(frame, bg="black")
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    # Add a scrollbar
    scrollbar = tk.Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    # Configure the canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    # Create a frame inside the canvas
    image_frame = tk.Frame(canvas, bg="black")
    canvas.create_window((0, 0), window=image_frame, anchor="nw")
    # Add a label
    label = tk.Label(image_frame, text="No files selected", background="black", fg="white", font=("Helvetica", 12))
    label.grid(row=0, column=0, columnspan=5, pady=10)
    row, col = 1, 0
    for file_path in file:
        try:
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image = Image.open(file_path)
                image = image.resize((100, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(image_frame, image=photo, bg="black")
                image_label.image = photo
                image_label.grid(row=row, column=col, padx=5, pady=5)
                file_name_label = tk.Label(image_frame, text=os.path.basename(file_path), font=("Helvetica", 10), bg="black", fg="white")
                file_name_label.grid(row=row+1, column=col, padx=5, pady=5)
            elif file_path.lower().endswith('.pdf'):
                pdf_document = fitz.open(file_path)
                for page_num in range(len(pdf_document)):
                    page = pdf_document.load_page(page_num)
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    img = img.resize((100, 100), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    image_label = tk.Label(image_frame, image=photo, bg="black")
                    image_label.image = photo
                    image_label.grid(row=row, column=col, padx=5, pady=5)
                    file_name_label = tk.Label(image_frame, text=f"{os.path.basename(file_path)} - Page {page_num+1}", font=("Helvetica", 10), bg="black", fg="white")
                    file_name_label.grid(row=row+1, column=col, padx=5, pady=5)
                    col += 1
                    if col >= 5:  # Change this value to adjust the number of columns
                        col = 0
                        row += 2
        except Exception as e:
            label.config(text=f"Error loading file: {e}")

# Function for splitting PDF files
def split_pdf():
    def split_selection(button):
        file = select_file()
        show_preview([file], button)
    def split_pdf_main_window():
        Header_font = Font(size=22, weight='bold')
        Header = tk.Label(window, text="SPLIT PDF", fg="aqua", background="black", font=Header_font)
        Header.pack()
        button_font = Font(size=10, weight='bold')
        Button_select_file = Button(window, text="Select PDF", fg="aqua", background="black", bd=3, relief="groove", font=button_font, width=20, height=2, command=lambda: split_selection(Button_select_file))
        Button_select_file.pack(pady=20)
    def operations(input_pdf, start_page, end_page):
        pdf_reader = fitz.open(input_pdf)
        for page_num in range(start_page - 1, end_page):
            page = pdf_reader.load_page(page_num)
            pdf_writer.insert_pdf(pdf_reader, from_page=page_num, to_page=page_num)
        savefile()
    split_pdf_main_window()

# Function to create the main window to display all functionalities
def main_window(Name_app, author_name):
    Name_app.place_forget()
    author_name.place_forget()
    window.geometry("600x400")
    window.configure(bg="black")
    def main_window_elements():
        Header_font = Font(size=22, weight='bold')
        Header = tk.Label(window, text="PDF EDITOR", fg="aqua", background="black", font=Header_font)
        Header.pack()
        button_font = Font(size=10, weight='bold')
        Button_split = Button(window, text="Split PDF", fg="aqua", background="black", bd=3, relief="groove", font=button_font, width=20, height=2, command=lambda: remove_elements(Button_split, Button_merge, Button_add_pages, Button_i2p, Header, "split_pdf"))
        Button_split.pack(pady=20)
        Button_i2p = Button(window, text="Image to PDF", fg="aqua", background="black", bd=3, relief="groove", font=button_font, width=20, height=2, command=lambda: remove_elements(Button_split, Button_merge, Button_add_pages, Button_i2p, Header, "i2p"))
        Button_i2p.pack(pady=20)
        Button_merge = Button(window, text="Merge PDF", fg="aqua", background="black", bd=3, relief="groove", font=button_font, width=20, height=2, command=lambda: remove_elements(Button_split, Button_merge, Button_add_pages, Button_i2p, Header, "merge_pdf"))
        Button_merge.pack(pady=20)
        Button_add_pages = Button(window, text="Add PDF", fg="aqua", background="black", bd=3, relief="groove", font=button_font, width=20, height=2, command=lambda: remove_elements(Button_split, Button_merge, Button_add_pages, Button_i2p, Header, "add_pages"))
        Button_add_pages.pack(pady=20)
    main_window_elements()

# Function for loading window
def loading_window():
    window.geometry("400x200")
    window.configure(bg="black")
    window.title("PDF-EDITOR")
    App_name_font = Font(size=30, weight='bold')
    App_name = tk.Label(window, text="PDF-EDITOR", fg="aqua", background="black", font=App_name_font)
    App_name.place(x=110, y=65)
    Author_name_font = Font(size=10, weight='bold')
    author_name = tk.Label(window, text="by SAKTHI-STARK", background="black", fg="aqua", font=Author_name_font)
    author_name.place(x=230, y=110)
    window.after(700, lambda: main_window(App_name, author_name))
    window.mainloop()

loading_window()
