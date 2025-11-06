import tkinter as tk
import random
import time

# ===============================
# Global variables
# ===============================
worker = None
data = []

# ===============================
# Sorting Algorithm Generators
# ===============================

def bubble_sort():
    global data
    n = len(data)
    for i in range(n - 1):
        for j in range(n - i - 1):
            color_array = ["red" if x == j or x == j + 1 else "yellow" for x in range(n)]
            draw_data(data, color_array)
            yield
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    draw_data(data, ["green" for _ in range(n)])


def selection_sort():
    global data
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            color_array = ["red" if x == j or x == min_idx else "yellow" for x in range(n)]
            draw_data(data, color_array)
            yield
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
    draw_data(data, ["green" for _ in range(n)])


def insertion_sort():
    global data
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j] > key:
            color_array = ["red" if x == j or x == j + 1 else "yellow" for x in range(len(data))]
            draw_data(data, color_array)
            yield
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
    draw_data(data, ["green" for _ in range(len(data))])


def merge_sort(start, end):
    if end <= start:
        return
    mid = (start + end) // 2
    yield from merge_sort(start, mid)
    yield from merge_sort(mid + 1, end)
    yield from merge(start, mid, end)
    draw_data(data, ["green" for _ in range(len(data))])


def merge(start, mid, end):
    global data
    left = data[start:mid + 1]
    right = data[mid + 1:end + 1]
    i = j = 0
    k = start

    while i < len(left) and j < len(right):
        color_array = ["red" if x == k else "yellow" for x in range(len(data))]
        draw_data(data, color_array)
        yield
        if left[i] <= right[j]:
            data[k] = left[i]
            i += 1
        else:
            data[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        data[k] = left[i]
        i += 1
        k += 1
        yield
    while j < len(right):
        data[k] = right[j]
        j += 1
        k += 1
        yield


def quick_sort(start, end):
    if start >= end:
        return
    pivot_index = partition(start, end)
    yield from quick_sort(start, pivot_index - 1)
    yield from quick_sort(pivot_index + 1, end)


def partition(start, end):
    global data
    pivot = data[end]
    i = start
    for j in range(start, end):
        color_array = ["red" if x == j or x == end else "yellow" for x in range(len(data))]
        draw_data(data, color_array)
        yield
        if data[j] < pivot:
            data[i], data[j] = data[j], data[i]
            i += 1
    data[i], data[end] = data[end], data[i]
    return i

# ===============================
# UI Helper Functions
# ===============================

def draw_data(data, color_array):
    canvas.delete("all")
    c_height = 380
    c_width = 880
    bar_width = c_width / (len(data) + 1)
    offset = 10
    spacing = 2

    normalized_data = [i / max(data) for i in data]
    for i, height in enumerate(normalized_data):
        x0 = i * bar_width + offset + spacing
        y0 = c_height - height * 350
        x1 = (i + 1) * bar_width + offset
        y1 = c_height
        canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i])
    window.update_idletasks()


def generate_data():
    global data
    data = [random.randint(10, 100) for _ in range(size_var.get())]
    draw_data(data, ["yellow" for _ in range(len(data))])


def start_sort():
    global worker
    if algo_menu.get() == "Bubble Sort":
        worker = bubble_sort()
    elif algo_menu.get() == "Selection Sort":
        worker = selection_sort()
    elif algo_menu.get() == "Insertion Sort":
        worker = insertion_sort()
    elif algo_menu.get() == "Merge Sort":
        worker = merge_sort(0, len(data) - 1)
    elif algo_menu.get() == "Quick Sort":
        worker = quick_sort(0, len(data) - 1)
    animate()


def animate():
    global worker
    if worker is not None:
        try:
            next(worker)
            window.after(speed_var.get(), animate)
        except StopIteration:
            draw_data(data, ["green" for _ in range(len(data))])
            worker = None

# ===============================
# Tkinter UI Setup
# ===============================

window = tk.Tk()
window.title("Sorting Algorithm Visualizer")
window.geometry("900x550")
window.config(bg="#E3F2FD")

# UI Frames
ui_frame = tk.Frame(window, bg="#E3F2FD")
ui_frame.pack(pady=10)

canvas = tk.Canvas(window, width=880, height=380, bg="white", highlightthickness=0)
canvas.pack(pady=20)

# UI Controls
tk.Label(ui_frame, text="Algorithm:", bg="#E3F2FD", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=5, pady=5)
algo_menu = tk.StringVar()
algo_menu.set("Bubble Sort")
tk.OptionMenu(ui_frame, algo_menu, "Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort").grid(row=0, column=1, padx=5, pady=5)

tk.Label(ui_frame, text="Speed (ms):", bg="#E3F2FD", font=("Arial", 11, "bold")).grid(row=0, column=2, padx=5, pady=5)
speed_var = tk.IntVar(value=50)
tk.Scale(ui_frame, from_=1, to=200, orient=tk.HORIZONTAL, variable=speed_var, length=120, bg="#E3F2FD").grid(row=0, column=3, padx=5, pady=5)

tk.Label(ui_frame, text="Size:", bg="#E3F2FD", font=("Arial", 11, "bold")).grid(row=0, column=4, padx=5, pady=5)
size_var = tk.IntVar(value=30)
tk.Scale(ui_frame, from_=5, to=100, orient=tk.HORIZONTAL, variable=size_var, length=120, bg="#E3F2FD").grid(row=0, column=5, padx=5, pady=5)

tk.Button(ui_frame, text="Generate Array", command=generate_data, bg="#1565C0", fg="white", font=("Arial", 10, "bold"), width=14).grid(row=0, column=6, padx=10)
tk.Button(ui_frame, text="Start Sorting", command=start_sort, bg="#43A047", fg="white", font=("Arial", 10, "bold"), width=14).grid(row=0, column=7, padx=10)

generate_data()
window.mainloop()
