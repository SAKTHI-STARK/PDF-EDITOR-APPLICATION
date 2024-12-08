import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.font import Font
from PIL import Image, ImageTk
import os
import fitz  # PyMuPDF
from tkinter import messagebox
import PyPDF2
# Function to create the static directory if it doesn't exist
def create_static_directory():
    directory = 'static/'
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created")
    else:
        print(f"Directory '{directory}' already exists")
create_static_directory()
# Defining globally accessible variables
window = tk.Tk()
global App_name
global author_name
# Function for removing widgets and entering into specific action
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
def destroy_fun():
    for widget in window.winfo_children():
                widget.destroy()
    pass
# Function for select the directory
def save_file():
    file_path = filedialog.asksaveasfilename(
        title="Save As",
        defaultextension=".pdf",
        filetypes=[("PDF Files", ".pdf"), ("All Files", ".*")]
    )
    return file_path
#function to save the output file
def savefile(pdf_writer): 
    output_path = save_file() 
    if output_path: 
        with open(output_path, 'wb') as output_file: 
            pdf_writer.write(output_file)
            destroy_fun()
            Header_font = Font(size=22, weight='bold')
            Header = tk.Label(window, text="SPLIT PDF", fg="aqua", background="black", font=Header_font)
            Header.pack()
            file_saved= tk.Label(window, text="SUCCESFULLY SPLIT FILE", background="black", fg="yellow",font=Header_font)
            file_saved.pack()
#function for showing the preview pages of the df file and images
def show_preview(file, button):
    button.destroy()
    # Create a frame for the content
    frame = tk.Frame(window, background="black", bd=0) 
    frame.pack(fill=BOTH, expand=True) 
    # Add a canvas for scrolling 
    canvas = tk.Canvas(frame, background="black", bd=0, highlightthickness=0) 
    canvas.pack(side=LEFT, fill=BOTH, expand=True) 
    # Add a scrollbar 
    scrollbar = tk.Scrollbar(frame, orient=VERTICAL, command=canvas.yview, background="black", bd=0, highlightthickness=0) 
    scrollbar.pack(side=RIGHT, fill=Y) 
    # Configure the canvas 
    canvas.configure(yscrollcommand=scrollbar.set) 
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all"))) 
    # Create a frame inside the canvas 
    image_frame = tk.Frame(canvas, background="black", bd=0, highlightthickness=0) 
    canvas.create_window((0, 0), window=image_frame, anchor="nw") 
    # Add a label
    label = tk.Label(image_frame, text="No files selected", background="black", fg="white", font=("Helvetica", 12))
    label.grid(row=0, column=5, columnspan=4, pady=10)
    row, col = 1, 0
    for file_path in file:
        try:
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image = Image.open(file_path)
                image = image.resize((100, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(image_frame, image=photo, background="black")
                image_label.image = photo
                image_label.grid(row=row, column=col, padx=5, pady=5)
                file_name_label = tk.Label(image_frame, text=os.path.basename(file_path), font=("Helvetica", 10), background="black", fg="aqua")
                file_name_label.grid(row=row+1, column=col, padx=5, pady=5)
            elif file_path.lower().endswith('.pdf'):
                pdf_document = fitz.open(file_path)
                label.config(text=f"{os.path.basename(file_path)}", background="black", fg="aqua")
                for page_num in range(len(pdf_document)):
                    page = pdf_document.load_page(page_num)
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    img = img.resize((100, 100), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    image_label = tk.Label(image_frame, image=photo, background="black")
                    image_label.image = photo
                    image_label.grid(row=row, column=col, padx=5, pady=5)
                    file_name_label = tk.Label(image_frame, text=f"Page {page_num+1}", background="black", fg="aqua", font=("Helvetica", 10))
                    file_name_label.grid(row=row+1, column=col, padx=5, pady=5)
                    col += 1
                    if col >= 13:  # Change this value to adjust the number of columns
                        col = 0
                        row += 2
                return len(pdf_document)
        except Exception as e:
            label.config(text=f"Error loading file: {e}")
# Function for splitting PDF files
def split_pdf():
    def split_selection(button):
        file = select_file()
        num_pages = show_preview([file], button)
        get_page_vals(file, num_pages)
    #function that used to get the spliting page values
    def get_page_vals(file, num_pages):
        Start_page = tk.Label(window, text="Start Pg No:", background="black", fg="aqua")
        Start_page.pack()
        start_page_val = tk.Entry(window,background="black",fg="aqua",bd=2,relief="groove",insertbackground="grey")
        start_page_val.pack()
        End_page = tk.Label(window, text="End Page No:", background="black", fg="aqua")
        End_page.pack()
        End_page_val = tk.Entry(window,background="black",fg="aqua",bd=2,relief="groove",insertbackground="grey")
        End_page_val.pack()
        button_font = Font(size=10, weight='bold')
        button_convert = Button(window, text="Split File", fg="aqua", background="black", bd=3, relief="groove", font=button_font, width=20, height=2, command=lambda: split_pdf_command(file, start_page_val, End_page_val, num_pages))
        button_convert.pack(pady=20)
    #function that get the values from the split file page
    def split_pdf_command(file, start_page_val, End_page_val, num_pages):
        try:
            st_pg_val = int(start_page_val.get())
            end_pg_val = int(End_page_val.get())
            if end_pg_val <= num_pages:
                    operations(file, st_pg_val, end_pg_val)
            else:
                messagebox.showwarning("Invalid Input", "Enter a valid range")
        except:
            messagebox.showwarning("invalid input","Enter valid type-int")
    #function that run for selecting split pdf button from the home menu
    def split_pdf_main_window():
        Header_font = Font(size=22, weight='bold')
        Header = tk.Label(window, text="SPLIT PDF", fg="aqua", background="black", font=Header_font)
        Header.pack()
        button_font = Font(size=10, weight='bold')
        Button_select_file = Button(window, text="Select PDF", fg="aqua", background="black", bd=3, relief="groove", font=button_font, width=20, height=2, command=lambda: split_selection(Button_select_file))
        Button_select_file.pack(pady=20)
    #function contains operations for split the pdf file
    def operations(input_pdf, start_page, end_page):
        pdf_writer = PyPDF2.PdfWriter()
        # Ensure input_pdf is a file path or file-like object
        if isinstance(input_pdf, str):
            pdf_reader = PyPDF2.PdfReader(input_pdf)
        elif hasattr(input_pdf, 'read'):
            pdf_reader = PyPDF2.PdfReader(input_pdf)
        else:
            raise ValueError("input_pdf should be a file path or file-like object")
        # For loop for adding the certain range pages from the PDF
        for page_num in range(start_page - 1, end_page):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)
        # Save the newly created PDF file
        savefile(pdf_writer)
    split_pdf_main_window()
# Function to create the main window to display all functionalities
def main_window(Name_app, author_name):
    Name_app.place_forget()
    author_name.place_forget()
    window.geometry("600x400")
    window.configure(bg="black")
    def back():
        destroy_fun()
        main_window_elements()

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
        button_home = Button(window, text="Home", fg="aqua", background="black", bd=3, relief="groove", font=button_font, width=5, height=1, command=back)
        button_home.place(x=10,y=5)
    main_window_elements()
# Function for loading window
def loading_window():
    global App_name
    global author_name
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
