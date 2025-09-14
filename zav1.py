import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import numpy as np

current_image = None
image_array = None
current_feature_vector = None
current_normalized_vector = None

def load_img():
    global current_image, image_array

    file_path = filedialog.askopenfilename(filetypes=[("BMP files", "*.bmp")])
    if file_path:
        img = Image.open(file_path).convert('L')
        image_array = np.array(img)

        current_image = ImageTk.PhotoImage(img)
        image_canvas.delete("all")
        canvas_w = int(image_canvas.cget("width"))
        canvas_h = int(image_canvas.cget("height"))
        img_w, img_h = img.size
        x = (canvas_w - img_w) // 2
        y = (canvas_h - img_h) // 2
        image_canvas.create_image(x, y, anchor="nw", image=current_image)

        feature_vector_text.delete(1.0, tk.END)
        normalized_vector_text.delete(1.0, tk.END)

def segment_image(image_arr, rows, cols):
    height, width = image_arr.shape
    segments = []
    row_size = height // rows
    col_size = width // cols

    for i in range(rows):
        for j in range(cols):
            start_row = i * row_size
            end_row = (i + 1) * row_size if i < rows - 1 else height
            start_col = j * col_size
            end_col = (j + 1) * col_size if j < cols - 1 else width
            segment = image_arr[start_row:end_row, start_col:end_col]
            segments.append(segment)
    return segments

def calculate_feature_vector(segments, threshold=128):
    return np.array([np.sum(seg < threshold) for seg in segments])

def normalize_vector(vector):
    total = np.sum(vector)
    return vector / total if total > 0 else vector

def calculate_features():
    global current_feature_vector, current_normalized_vector
    if image_array is None:
        messagebox.showwarning("Увага", "Спочатку завантажте зображення")
        return

    rows = int(rows_entry.get())
    cols = int(cols_entry.get())
    threshold = int(threshold_entry.get())

    segments = segment_image(image_array, rows, cols)
    current_feature_vector = calculate_feature_vector(segments, threshold)
    current_normalized_vector = normalize_vector(current_feature_vector)

    display_results()

def display_results():
    feature_vector_text.delete(1.0, tk.END)
    normalized_vector_text.delete(1.0, tk.END)

    feature_str = "X = (" + "; ".join(map(str, current_feature_vector)) + ")\n\n"
    feature_vector_text.insert(tk.END, feature_str)

    normalized_formatted = [f"{x:.4f}" for x in current_normalized_vector]
    normalized_str = "X_norm = (" + "; ".join(normalized_formatted) + ")\n\n"
    normalized_vector_text.insert(tk.END, normalized_str)

# GUI
root = tk.Tk()
root.title("Вектор ознак графічних зображень")
root.geometry("700x500")

# --- Зображення ---
image_frame = ttk.LabelFrame(root, text="Зображення", padding="10")
image_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

canvas_width, canvas_height = 200, 200
image_canvas = tk.Canvas(image_frame, width=canvas_width, height=canvas_height, bg="white", relief="sunken")
image_canvas.pack(pady=10)

load_button = ttk.Button(image_frame, text="Завантажити", command=load_img)
load_button.pack(pady=5)

# --- Налаштування ---
settings_frame = ttk.LabelFrame(root, text="Налаштування", padding="10")
settings_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

# Параметри сегментації
ttk.Label(settings_frame, text="Рядки:").grid(row=0, column=0, sticky="w", pady=5)
rows_entry = ttk.Entry(settings_frame, width=5)
rows_entry.insert(0, "5")
rows_entry.grid(row=0, column=1, padx=5)

ttk.Label(settings_frame, text="Стовпці:").grid(row=1, column=0, sticky="w", pady=5)
cols_entry = ttk.Entry(settings_frame, width=5)
cols_entry.insert(0, "5")
cols_entry.grid(row=1, column=1, padx=5)

ttk.Label(settings_frame, text="Поріг:").grid(row=2, column=0, sticky="w", pady=5)
threshold_entry = ttk.Entry(settings_frame, width=5)
threshold_entry.insert(0, "128")
threshold_entry.grid(row=2, column=1, padx=5)

ttk.Button(settings_frame, text="Обчислити", command=calculate_features)\
    .grid(row=3, column=0, columnspan=2, pady=10)

# --- Результати ---
results_frame = ttk.Frame(root)
results_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

feature_frame = ttk.LabelFrame(results_frame, text="Абсолютний вектор", padding="5")
feature_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
feature_vector_text = scrolledtext.ScrolledText(feature_frame, height=10, width=40)
feature_vector_text.pack(fill="both", expand=True)

normalized_frame = ttk.LabelFrame(results_frame, text="Нормований вектор", padding="5")
normalized_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
normalized_vector_text = scrolledtext.ScrolledText(normalized_frame, height=10, width=40)
normalized_vector_text.pack(fill="both", expand=True)

# --- Розтягування ---
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)
results_frame.columnconfigure(0, weight=1)
results_frame.columnconfigure(1, weight=1)

root.mainloop()
