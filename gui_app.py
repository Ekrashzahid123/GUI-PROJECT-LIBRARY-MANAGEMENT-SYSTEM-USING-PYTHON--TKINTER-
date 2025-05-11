import tkinter as tk
from tkinter import messagebox, simpledialog
from book_library import Book, EBook, Library, BookNotAvailableError

library = Library()

root  = tk.Tk()
root.title("Library Management System")
root.geometry("600x600")

# ====================== Function Definitions ======================

def validate_numeric_input(new_value):
    """Allow only numeric input for download size."""
    return new_value == "" or new_value.isdigit()

def add_book():
    title = title_entry.get()
    author = author_entry.get()
    isbn = isbn_entry.get()
    is_ebook = ebook_var.get()
    size = size_entry.get()

    if not title or not author or not isbn:
        messagebox.showerror("Error", "Title, Author, and ISBN are required.")
        return

    if is_ebook and not size:
        messagebox.showerror("Error", "Download size required for eBooks.")
        return

    if is_ebook:
        book = EBook(title, author, isbn, size)
    else:
        book = Book(title, author, isbn)

    library.add_book(book)
    messagebox.showinfo("Success", f"Book '{title}' added to the library.")
    update_book_list()

def lend_book():
    isbn = simpledialog.askstring("Lend Book", "Enter ISBN of the book to lend:")
    if isbn:
        try:
            library.lend_book(isbn)
            messagebox.showinfo("Success", "Book lent successfully.")
            update_book_list()
        except BookNotAvailableError as e:
            messagebox.showerror("Error", str(e))

def return_book():
    isbn = simpledialog.askstring("Return Book", "Enter ISBN of the book to return:")
    if isbn:
        try:
            library.return_book(isbn)
            messagebox.showinfo("Success", "Book returned successfully.")
            update_book_list()
        except BookNotAvailableError as e:
            messagebox.showerror("Error", str(e))

def remove_book():
    isbn = simpledialog.askstring("Remove Book", "Enter ISBN of the book to remove:")
    if isbn:
        library.remove_book(isbn)
        messagebox.showinfo("Success", "Book removed from library.")
        update_book_list()

def view_books_by_author():
    author = simpledialog.askstring("Search by Author", "Enter author's name:")
    if author:
        books = list(library.books_by_author(author))
        if books:
            listbox.delete(0, tk.END)
            listbox.insert(tk.END, f"Books by {author}:")
            for book in books:
                listbox.insert(tk.END, str(book))
        else:
            messagebox.showinfo("Not Found", "No books by this author.")

def update_book_list():
    listbox.delete(0, tk.END)
    listbox.insert(tk.END, "Available Books:")
    for book in library:
        listbox.insert(tk.END, str(book))

# ====================== GUI Widgets ======================

# Validation command registration
vcmd = (root.register(validate_numeric_input), '%P')

# Title
tk.Label(root, text="Title:").pack()
title_entry = tk.Entry(root)
title_entry.pack()

# Author
tk.Label(root, text="Author:").pack()
author_entry = tk.Entry(root)
author_entry.pack()

# ISBN
tk.Label(root, text="ISBN:").pack()
isbn_entry = tk.Entry(root)
isbn_entry.pack()

# eBook checkbox with inline logic
ebook_var = tk.BooleanVar()

def ebook_checkbox_changed():
    if ebook_var.get():
        size_entry.config(state='normal')
    else:
        size_entry.delete(0, tk.END)
        size_entry.config(state='disabled')

tk.Checkbutton(
    root,
    text="eBook?",
    variable=ebook_var,
    command=ebook_checkbox_changed
).pack()

# Download Size
tk.Label(root, text="Download Size (MB):").pack()
size_entry = tk.Entry(root, validate='key', validatecommand=vcmd, state='disabled')
size_entry.pack()

# Buttons
tk.Button(root, text="Add Book", command=add_book).pack(pady=5)
tk.Button(root, text="Lend Book", command=lend_book).pack(pady=5)
tk.Button(root, text="Return Book", command=return_book).pack(pady=5)
tk.Button(root, text="Remove Book", command=remove_book).pack(pady=5)
tk.Button(root, text="View Books by Author", command=view_books_by_author).pack(pady=5)

# Inventory
tk.Label(root, text="Library Inventory:").pack()
listbox = tk.Listbox(root, width=70)
listbox.pack(pady=10)

update_book_list()
root.mainloop()
