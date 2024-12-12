import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.font import Font
from PIL import Image, ImageTk
import os
import fitz  
from tkinter import messagebox
import PyPDF2
import img2pdf as i2p
# Defining globally accessible variables
window = tk.Tk()
global App_name
global author_name
pdf_writer = PyPDF2.PdfWriter()
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
        convert_img2pdf()
    elif text == "merge_pdf":
        merge_pdf()
    elif text == "add_pages":
        add_pdf()
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
        try:
            button_text = widget.cget("text")
            if button_text == "Home":
                continue
        except tk.TclError:
            # Handle widgets that do not have a 'text' attribute
            pass
        widget.destroy()
#function for showing final window after successfull complete the operation
def final_window():
    destroy_fun()
    Header_font = Font(size=22, weight='bold')
    Header = tk.Label(window, text="THANK YOU", fg="aqua", background="black", font=Header_font)
    Header.pack()
    file_saved= tk.Label(window, text="SUCCESFULLY DONE", background="black", fg="yellow",font=Header_font)
    file_saved.pack()      
# Function for select the directory
def save_file():
    file_path = filedialog.asksaveasfilename(
        title="Save As",
        defaultextension=".pdf",
        filetypes=[("PDF Files", ".pdf"), ("All Files", ".*")]
    )
    return file_path
#function to save the output file
def savefile(): 
    output_path = save_file() 
    if output_path: 
        with open(output_path, 'wb') as output_file: 
            pdf_writer.write(output_file)
            final_window()
def show_front_page():
    # Create a frame to display the PDF front pages
    image_frame = tk.Frame(window,background="black", bd=0)
    image_frame.pack(fill=tk.BOTH, expand=True)
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if file_paths:
        for widget in image_frame.winfo_children():
            widget.destroy()  # Clear previous images
        row, col = 0, 0
        for file_path in file_paths:
            pdf_document = fitz.open(file_path)
            page = pdf_document.load_page(0)  # Load the first page
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img = img.resize((150, 200), Image.LANCZOS)  # Resize the image to fit the window
            photo = ImageTk.PhotoImage(img)
            image_label = tk.Label(image_frame, image=photo)
            image_label.image = photo
            image_label.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col >= 5:  # Adjust the number of columns as needed
                col = 0
                row += 1
    return file_paths
#function for showing the preview pages of the df file and images
def show_preview(files, button):
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
    for file_path in files:
        try:
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                label.config(text="Selected images", background="black", fg="aqua")
                image = Image.open(file_path)
                image = image.resize((100, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(image_frame, image=photo, background="black", bd=0, highlightthickness=0)
                image_label.image = photo
                image_label.grid(row=row, column=col, padx=5, pady=5)
                file_name_label = tk.Label(image_frame, text=os.path.basename(file_path), font=("Helvetica", 4), background="black", fg="aqua", bd=0, highlightthickness=0)
                file_name_label.grid(row=row+1, column=col, padx=5, pady=5)
                col += 1
                if col >= 13:  
                    col = 0
                    row += 2
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
                    if col >= 13:  
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
                def new_window():
                    destroy_fun()
                    Header_font = Font(size=22, weight='bold')
                    Header = tk.Label(window, text="Split Pdf", fg="aqua", background="black", font=Header_font)
                    Header.pack()
                    button_font = Font(size=10, weight='bold')
                    Button_select_file = Button(window, text="Save Pdf", fg="aqua", background="black", bd=3, relief="groove", font=button_font, width=20, height=2,command=lambda:operations(file, st_pg_val, end_pg_val))
                    Button_select_file.pack(pady=20)
                new_window()
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
        savefile()
    split_pdf_main_window()
#main function for image to pdf convertioin
def convert_img2pdf():
    #contain the operation to convert image
    def operations(file):
        save_dir=save_file()
        with open(save_dir,'ab') as f:
            page_size = (595, 842)
            f.write(i2p.convert(file,page_size=page_size))
            final_window()
    #contain the preview window of image to pdf
    def image_selection(button):
        file = select_multiple_file()
        show_preview(file,button)
        def new_window():
            destroy_fun()
            Header_font = Font(size=22, weight='bold')
            Header = tk.Label(window, text="Image to Pdf", fg="aqua", background="black", font=Header_font)
            Header.pack()
            button_font = Font(size=10, weight='bold')
            Button_select_file = Button(window, text="Save Pdf", fg="aqua", background="black", bd=3, relief="groove", font=button_font, width=20, height=2,command=lambda:operations(file))
            Button_select_file.pack(pady=20)
        button_font = Font(size=10, weight='bold')
        button_convert = Button(window, text="CONVERT TO PDF", fg="aqua", background="black", bd=3, relief="groove", font=button_font, width=20, height=2, command=new_window)
        button_convert.pack(pady=20)
    #contain the window of image to pdf
    def img_select_main_window():
        Header_font = Font(size=22, weight='bold')
        Header = tk.Label(window, text="IMAGE TO PDF", fg="aqua", background="black", font=Header_font)
        Header.pack()
        button_font = Font(size=10, weight='bold')
        Button_select_file = Button(window, text="Select images", fg="aqua", background="black", bd=3, relief="groove", font=button_font, width=20, height=2,command=lambda:image_selection(Button_select_file))
        Button_select_file.pack(pady=20)
    img_select_main_window()
#function for creating merge pdf documents
def merge_pdf():
    #functionalities for merging document
    def operations(pdf_list):
        print(pdf_list)
        pdf_merger = PyPDF2.PdfMerger()
        for pdf in pdf_list:
            pdf_merger.append(pdf)
        with open(save_file(), 'wb') as output_file:
            pdf_merger.write(output_file)
        final_window()
    #function for selecting pdf documents
    def pdf_selection(button):
        button.destroy()
        file=show_front_page()
        def new_window():
            destroy_fun()
            Header_font = Font(size=22, weight='bold')
            Header = tk.Label(window, text="Merge Pdf", fg="aqua", background="black", font=Header_font)
            Header.pack()
            button_font = Font(size=10, weight='bold')
            Button_select_file = Button(window, text="Save Pdf", fg="aqua", background="black", bd=3, relief="groove", font=button_font, width=20, height=2,command=lambda:operations(file))
            Button_select_file.pack(pady=20)
        button_font = Font(size=10, weight='bold')
        button_convert = Button(window, text="MERGE PDF", fg="aqua", background="black", bd=3, relief="groove", font=button_font, width=20, height=2, command=new_window)
        button_convert.pack(pady=20)
    #function containing the main merge pdf window elements
    def pdf_select_main_window():
        Header_font = Font(size=22, weight='bold')
        Header = tk.Label(window, text="MERGE PDF", fg="aqua", background="black", font=Header_font)
        Header.pack()
        button_font = Font(size=10, weight='bold')
        Button_select_file = Button(window, text="Select PDF's", fg="aqua", background="black", bd=3, relief="groove", font=button_font, width=20, height=2,command=lambda:pdf_selection(Button_select_file))
        Button_select_file.pack(pady=20)
    pdf_select_main_window()
def add_pdf():
    global file
    def operations(file,insert_pdf,position):
        # Open the source PDF
        with open(file, 'rb') as source_file:
            source_reader = PyPDF2.PdfReader(source_file)
            source_writer = PyPDF2.PdfWriter()
            # Open the PDF to be inserted
            with open(insert_pdf, 'rb') as insert_file:
                insert_reader = PyPDF2.PdfReader(insert_file)
                # Add pages from the source PDF up to the specified position
                for i in range(position-1):
                    source_writer.add_page(source_reader.pages[i])
                # Add all pages from the insert PDF
                for page in insert_reader.pages:
                    source_writer.add_page(page)
                # Add the remaining pages from the source PDF
                for i in range(position, len(source_reader.pages)):
                    source_writer.add_page(source_reader.pages[i])
            with open(save_file(), 'wb') as output_file:
                source_writer.write(output_file)
        final_window()
    def add_file(file,add_page_val):
        insert_pdf=select_file()
        position=int(add_page_val.get())
        def new_window():
            destroy_fun()
            Header_font = Font(size=22, weight='bold')
            Header = tk.Label(window, text="ADD PAGES", fg="aqua", background="black", font=Header_font)
            Header.pack()
            button_font = Font(size=10, weight='bold')
            Button_select_file = Button(window, text="Save Pdf", fg="aqua", background="black", bd=3, relief="groove", font=button_font, width=20, height=2,command=lambda:operations(file,insert_pdf,position))
            Button_select_file.pack(pady=20)
        new_window()   
    def pdf_selection(button):
        file=select_file()
        show_preview([file],button)
        add_page = tk.Label(window, text=" Where to Add file", background="black", fg="aqua")
        add_page.pack()
        add_page_val = tk.Entry(window,background="black",fg="aqua",bd=2,relief="groove",insertbackground="grey",)
        add_page_val.pack()
        button_font = Font(size=10, weight='bold')
        button_convert = Button(window, text="ADD PDF", fg="aqua", background="black", bd=3, relief="groove", font=button_font, width=20, height=2, command=lambda:add_file(file,add_page_val))
        button_convert.pack(pady=20)
    def pdf_select_main_window():
        Header_font = Font(size=22, weight='bold')
        Header = tk.Label(window, text="ADD PAGES", fg="aqua", background="black", font=Header_font)
        Header.pack()
        button_font = Font(size=10, weight='bold')
        Button_select_file = Button(window, text="Select PDF", fg="aqua", background="black", bd=3, relief="groove", font=button_font, width=20, height=2,command=lambda:pdf_selection(Button_select_file))
        Button_select_file.pack(pady=20)
    pdf_select_main_window()
# Function to create the main window to display all functionalities
def main_window(Name_app, author_name):
    Name_app.place_forget()
    author_name.place_forget()
    window.geometry("600x400")
    window.configure(bg="black")
    #function for the home button
    def back():
        destroy_fun()
        main_window_elements()
    #function for creating main window elements like split pdf,merge pdf
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