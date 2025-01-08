import os
import sqlite3
from datetime import datetime
from PyPDF2 import PdfReader
from tkinter import END, messagebox, filedialog, Listbox
import webbrowser

# Database Setup
DB_NAME = "documents.db"

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            filename TEXT,
            filepath TEXT,
            folder_name TEXT,
            folder_path TEXT,
            content TEXT,
            last_modified TEXT
        )
    """)
    conn.commit()
    conn.close()

def reindex_files():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='documents'")
    if cursor.fetchone():
        cursor.execute("PRAGMA table_info(documents)")
        columns = [info[1] for info in cursor.fetchall()]
        if 'folder_name' not in columns:
            cursor.execute("ALTER TABLE documents ADD COLUMN folder_name TEXT")
        if 'folder_path' not in columns:
            cursor.execute("ALTER TABLE documents ADD COLUMN folder_path TEXT")
        if 'last_modified' not in columns:
            cursor.execute("ALTER TABLE documents ADD COLUMN last_modified TEXT")
    conn.commit()
    conn.close()

# Function to Index Files
def index_files(folder_path):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Clear existing index
    cursor.execute("DELETE FROM documents")

    for root, _, files in os.walk(folder_path):
        folder_name = os.path.basename(root)
        for file in files:
            filepath = os.path.join(root, file)
            try:
                if file.endswith(".txt"):
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            content = f.read()
                    except UnicodeDecodeError:
                        with open(filepath, "r", encoding="latin-1") as f:
                            content = f.read()
                elif file.endswith(".pdf"):
                    content = ""
                    pdf = PdfReader(filepath)
                    for page in pdf.pages:
                        content += page.extract_text()
                else:
                    continue  # Skip unsupported file types

                last_modified = os.path.getmtime(filepath)
                cursor.execute("""
                    INSERT INTO documents (filename, filepath, folder_name, folder_path, content, last_modified)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (file, filepath, folder_name, folder_path, content, last_modified))
                print(f"Indexed: {file}")
            except Exception as e:
                print(f"Failed to index {file}: {e}")

    conn.commit()
    conn.close()
    print("Indexing complete!")

# Function to Update Index
def update_index(folder_path):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Get all indexed files
    cursor.execute("SELECT filepath, last_modified FROM documents")
    indexed_files = {row[0]: row[1] for row in cursor.fetchall()}

    for root, _, files in os.walk(folder_path):
        folder_name = os.path.basename(root)
        for file in files:
            filepath = os.path.join(root, file)
            last_modified = os.path.getmtime(filepath)  # Last modified timestamp

            # If file is not indexed or has been updated
            if filepath not in indexed_files or indexed_files[filepath] != str(last_modified):
                try:
                    if file.endswith(".txt"):
                        with open(filepath, "r", encoding="utf-8") as f:
                            content = f.read()
                    elif file.endswith(".pdf"):
                        content = ""
                        pdf = PdfReader(filepath)
                        for page in pdf.pages:
                            content += page.extract_text()
                    else:
                        continue  # Skip unsupported file types

                    if filepath in indexed_files:
                        # Update existing document
                        cursor.execute("""
                            UPDATE documents
                            SET filename = ?, content = ?, last_modified = ?, folder_name = ?, folder_path = ?
                            WHERE filepath = ?
                        """, (file, content, last_modified, folder_name, folder_path, filepath))
                        print(f"Updated: {file}")
                    else:
                        # Add new document
                        cursor.execute("""
                            INSERT INTO documents (filename, filepath, folder_name, folder_path, content, last_modified)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (file, filepath, folder_name, folder_path, content, last_modified))
                        print(f"Indexed: {file}")
                except Exception as e:
                    print(f"Failed to index {file}: {e}")

    # Delete documents that no longer exist in the folder
    for filepath in indexed_files:
        if not os.path.exists(filepath):
            cursor.execute("DELETE FROM documents WHERE filepath = ?", (filepath,))
            print(f"Deleted: {filepath}")

    conn.commit()
    conn.close()
    print("Index updated!")

# Function to Search Documents
def search_documents(keywords):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = "SELECT filename, filepath FROM documents WHERE " + " AND ".join(["content LIKE ?"] * len(keywords))
    cursor.execute(query, [f"%{keyword}%" for keyword in keywords])
    results = cursor.fetchall()
    conn.close()
    return results

# Function to Search Documents by Metadata
def search_documents_by_metadata(filename=None, filetype=None, min_size=None, max_size=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = "SELECT filename, filepath FROM documents WHERE 1=1"
    params = []
    if filename:
        query += " AND filename LIKE ?"
        params.append(f"%{filename}%")
    if filetype:
        query += " AND filename LIKE ?"
        params.append(f"%.{filetype}")
    if min_size:
        query += " AND LENGTH(content) >= ?"
        params.append(min_size)
    if max_size:
        query += " AND LENGTH(content) <= ?"
        params.append(max_size)
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

# Function to Save Search Results
def save_search_results(results):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
    if file_path:
        with open(file_path, 'w') as file:
            for result in results:
                file.write(f"{result[0]} - {result[1]}\n")
        messagebox.showinfo("Success", "Search results saved successfully!")

# Function to Open File
def open_file(filepath):
    try:
        webbrowser.open(filepath)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file: {e}")

# Function to Get Indexed Folders
def get_indexed_folders():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT folder_name, folder_path, MAX(last_modified) FROM documents GROUP BY folder_name, folder_path")
    results = cursor.fetchall()
    conn.close()
    return results

# Function to Delete Index of a Folder
def delete_index(folder_path):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM documents WHERE folder_path = ?", (folder_path,))
    conn.commit()
    conn.close()
    print(f"Index deleted for folder: {folder_path}")
