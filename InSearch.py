import customtkinter as ctk
from tkinter import END, messagebox, filedialog, Listbox
from datetime import datetime
from app_logic import create_database, reindex_files, index_files, update_index, search_documents, search_documents_by_metadata, save_search_results, open_file, get_indexed_folders, delete_index
import os

# Set the appearance mode to dark
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Function to Open Indexed Folders Sidebar
def toggle_indexed_folders_sidebar():
    if hasattr(toggle_indexed_folders_sidebar, "sidebar") and toggle_indexed_folders_sidebar.sidebar.winfo_exists():
        toggle_indexed_folders_sidebar.sidebar.destroy()
        del toggle_indexed_folders_sidebar.sidebar
    else:
        open_indexed_folders_sidebar()

def open_indexed_folders_sidebar():
    indexed_folders = get_indexed_folders()
    
    sidebar = ctk.CTkFrame(root, width=200)
    sidebar.grid(row=0, column=3, rowspan=11, padx=10, pady=5, sticky="ns")
    toggle_indexed_folders_sidebar.sidebar = sidebar
    
    listbox = Listbox(sidebar, width=30, height=20, bg="#2e2e2e", fg="white", selectbackground="#4a4a4a")
    listbox.pack(padx=10, pady=10)
    
    for folder, path, timestamp in indexed_folders:
        listbox.insert(END, f"{folder} - Last Indexed: {datetime.fromtimestamp(float(timestamp))}")

    def start_updating_index():
        selected = listbox.curselection()
        if selected:
            folder_info = listbox.get(selected[0]).split(" - ")
            folder_name = folder_info[0]
            folder_path = folder_info[1]
            update_index(folder_path)
            messagebox.showinfo("Success", f"Index updated for {folder_name}!")

    def start_deleting_index():
        selected = listbox.curselection()
        if selected:
            folder_info = listbox.get(selected[0]).split(" - ")
            folder_name = folder_info[0]
            folder_path = folder_info[1]
            delete_index(folder_path)
            listbox.delete(selected[0])
            messagebox.showinfo("Success", f"Index deleted for {folder_name}!")

    update_button = ctk.CTkButton(sidebar, text="Update Index", command=start_updating_index)
    update_button.pack(pady=5)

    delete_button = ctk.CTkButton(sidebar, text="Delete Index", command=start_deleting_index)
    delete_button.pack(pady=5)

    close_button = ctk.CTkButton(sidebar, text="Close", command=sidebar.destroy)
    close_button.pack(pady=5)

# GUI Application
def run_gui():
    def start_indexing():
        folder_path = filedialog.askdirectory(title="Select Folder to Index")
        if folder_path and os.path.isdir(folder_path):
            index_files(folder_path)
            status_label.configure(text="Indexing complete!", text_color="green")
            open_indexed_folders_sidebar()  # Refresh the sidebar
        else:
            status_label.configure(text="Invalid folder path!", text_color="red")

    def search():
        keywords = search_entry.get().split()
        results = search_documents(keywords)
        results_listbox.delete(0, END)
        for result in results:
            results_listbox.insert(END, f"{result[0]} - {result[1]}")

    def open_selected_file():
        selected = results_listbox.curselection()
        if selected:
            index = selected[0]
            filepath = results_listbox.get(index).split(" - ")[1]
            open_file(filepath)

    def save_results():
        results = [results_listbox.get(i) for i in range(results_listbox.size())]
        save_search_results(results)

    # GUI Layout
    global root
    root = ctk.CTk()
    root.title("InSearch Beta 0.1") 
    # root.geometry("800x600")
    root.maxsize(1024, 768)

    # Indexing Frame
    indexing_frame = ctk.CTkFrame(root, border_width=1)
    indexing_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    ctk.CTkLabel(indexing_frame, text="Folder Path:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    folder_entry = ctk.CTkEntry(indexing_frame, width=300)
    folder_entry.grid(row=0, column=1, padx=10, pady=5)
    ctk.CTkButton(indexing_frame, text="Index Files", command=start_indexing).grid(row=0, column=2, padx=10, pady=5)
    ctk.CTkButton(indexing_frame, text="Show Indexed Folders", command=toggle_indexed_folders_sidebar).grid(row=0, column=3, padx=10, pady=5)

    # Keyword Search Frame
    keyword_search_frame = ctk.CTkFrame(root, border_width=1, width=1000)
    keyword_search_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="w")

    ctk.CTkLabel(keyword_search_frame, text="Search Keyword(s):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    search_entry = ctk.CTkEntry(keyword_search_frame, width=255)
    search_entry.grid(row=0, column=1, padx=10, pady=5)
    ctk.CTkButton(keyword_search_frame, text="Search", command=search,width=300).grid(row=0, column=2, padx=10, pady=5)

    results_listbox = Listbox(keyword_search_frame, width=80, height=23, bg="#2e2e2e", fg="white", selectbackground="#4a4a4a")
    results_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    ctk.CTkButton(keyword_search_frame, text="Open Selected File", command=open_selected_file).grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="e")
    ctk.CTkButton(keyword_search_frame, text="Save Results", command=save_results).grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="e")

    status_label = ctk.CTkLabel(keyword_search_frame, text="")
    status_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

    root.mainloop()

# Main Function
if __name__ == "__main__":
    create_database()
    reindex_files()
    run_gui()
