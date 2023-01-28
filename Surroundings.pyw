#Imports
import tkinter as tk
import json, random, re, datetime, os.path
from tkinter import scrolledtext, font, messagebox
from datetime import datetime
from functools import partial
try:
    from PIL import Image
except:
    tk.messagebox.showerror(title="Error!", message="PIL isn't installed, images won't work!")

#Basic Functions
def error(error_message):
    tk.messagebox.showerror(title="Error!", message = error_message)


def clear(master):
    widgets = master.winfo_children()
    for item in widgets:
        if item.winfo_children():
            widgets.extend(item.winfo_children())
    widget_list = widgets
    for item in widget_list:
        item.pack_forget()


#Load Message Files, Mics Variable Declaration
additional_info = {}
messages = []
cache_search_keyword = []
surroundings_top_bottom = [40,40]
amount_of_texts = 40
file_number = 0
number_of_texts = 0
while True:
    file_number = file_number + 1
    file = "message_" + str(file_number) + ".json"
    try:
        with open(file) as f:
            mess = json.load(f)
            for text in mess["messages"]:
                messages.append(text)
                number_of_texts += 1
    except:
        if number_of_texts <1:
            error("Can't read files")
        break

#Properties
master = tk.Tk()
big_joke = tk.font.Font(family="LilyUPC", size = 35)
joke = tk.font.Font(family="LilyUPC", size = 12)
small_joke = tk.font.Font(family="LilyUPC", size = 7)
master.title("Surroundings")
master.geometry("450x500")
master.resizable(True, True)



#Main Functions
def surroundings_load_more(direction, index_of_text):
    if cache_search_keyword[-1] == [-2]:
        if direction == "up":
            surroundings_top_bottom[0] += 40
        elif direction == "down":
            surroundings_top_bottom[1] += 40
        else:
            pass
        if (index_of_text - surroundings_top_bottom[1]) < 0:
            negative_index = index_of_text - surroundings_top_bottom[1]
            surroundings_top_bottom[1] = surroundings_top_bottom[1] + negative_index
        print(surroundings_top_bottom)
    else:
        surroundings_top_bottom[0] = 40
        surroundings_top_bottom[1] = 40
    surroundings(index_of_text)


def show_image(picture_uri):
    for x in picture_uri:
        if picture_uri.startswith("/photos/"):
            picture_uri = picture_uri.replace("/photos/", "", 1)
            break
        else:
            print(picture_uri)
            picture_uri = picture_uri.replace(picture_uri[0], "", 1)
    picture_uri = os.path.join('photos', picture_uri)
    picture = Image.open(picture_uri)
    picture.show()


def surroundings(index_of_text):
    display_surroundings()
    global delete_surroundings_scroll_frame
    try:
        delete_surroundings_scroll_frame.destroy()
    except:
        pass
    delete_surroundings_scroll_frame = tk.Frame(surroundings_scroll_canvas, bd = 4)
    delete_surroundings_scroll_frame.pack(fill = "both")
    (tk.Button(delete_surroundings_scroll_frame, font=joke, text="Show More", command=lambda: surroundings_load_more("up", index_of_text))).grid(row = 0, column = 0, columnspan = 2)
    cache_search_keyword.append(str(index_of_text))
    surroundings_texts_buttons = []
    surroundings_senders_labels = []
    surroundings_texts_buttons_frames = []
    if (index_of_text + surroundings_top_bottom[0]) > number_of_texts:
        pass
    if (index_of_text - surroundings_top_bottom[1]) < 0:
        negative_index = index_of_text - surroundings_top_bottom[1]
        surroundings_top_bottom[1] = surroundings_top_bottom[1] + negative_index
    for searched_message in messages[index_of_text + surroundings_top_bottom[0] : index_of_text - surroundings_top_bottom[1] : -1]:
            try:
                decoded_search_text = re.sub(r'[\xc2-\xf4][\x80-\xbf]+',lambda m: m.group(0).encode("latin1").decode('utf8'),searched_message["content"])
                text_button_frame = tk.Frame(delete_surroundings_scroll_frame)
                surroundings_texts_buttons_frames.append(text_button_frame)
                if messages[index_of_text]["sender_name"] == searched_message["sender_name"]:
                    text_button_frame.grid(sticky="e", pady=0, column = 1)
                else:
                    text_button_frame.grid(sticky="w", pady=0, column = 0)
                try:
                    if searched_message["sender_name"] == messages[(messages.index(searched_message) + 1)]["sender_name"]:
                        pass
                    else:
                        sender_label = tk.Label(text_button_frame, font=small_joke, text=searched_message["sender_name"] + ":", anchor="sw")
                        surroundings_senders_labels.append(sender_label)
                        sender_label.pack()
                except:
                    pass
                text_button = tk.Button(text_button_frame, font=joke, text=decoded_search_text, justify="left", relief="ridge", wraplength=195)
                surroundings_texts_buttons.append(text_button)
                text_button.pack()
            except:
                    try:
                        text_button_frame = tk.Frame(delete_surroundings_scroll_frame)
                        surroundings_texts_buttons_frames.append(text_button_frame)
                        if messages[index_of_text]["sender_name"] == searched_message["sender_name"]:
                            text_button_frame.grid(sticky="e", pady=0, column=1)
                        else:
                            text_button_frame.grid(sticky="w", pady=0, column=0)
                        try:
                            if searched_message["sender_name"] == messages[(messages.index(searched_message) + 1)]["sender_name"]:
                                pass
                            else:
                                sender_label = tk.Label(text_button_frame, font=small_joke, text=searched_message["sender_name"] + ":", anchor="sw")
                                surroundings_senders_labels.append(sender_label)
                                sender_label.pack()
                        except:
                            pass
                        text_button = tk.Button(text_button_frame, font=joke, justify="left", relief="ridge", wraplength=195)
                        surroundings_texts_buttons.append(text_button)
                        text_button = tk.Button(text_button_frame, font=big_joke, bg ="powder blue", text = "🖼️", justify="center", relief="ridge", wraplength=80, command = partial(show_image, searched_message["photos"][0]["uri"]))
                        text_button.pack()
                    except:
                        pass
    (tk.Button(delete_surroundings_scroll_frame, font=joke, text="Show More", command=lambda: surroundings_load_more("down", index_of_text))).grid(column = 0, columnspan = 2)
    surroundings_scroll_canvas.create_window(0, 0, anchor='nw', window=delete_surroundings_scroll_frame)
    surroundings_scroll_canvas.update_idletasks()
    surroundings_scroll_canvas.configure(scrollregion=surroundings_scroll_canvas.bbox('all'), yscrollcommand=surroundings_scrollbar.set)
    surroundings_scroll_canvas.bind_all('<MouseWheel>', lambda event: surroundings_scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))
    surroundings_scrollbar.config(command = surroundings_scroll_canvas.yview)


def random_text():
    show_time.config(text="")
    count = 0
    while True:
        try:
            random_file = messages[messages.index(random.choice(messages))]
            global file_index
            file_index = messages.index(random_file)
            coded_random_text = random_file["content"]
            decoded_random_text = re.sub(r'[\xc2-\xf4][\x80-\xbf]+', lambda m: m.group(0).decode('utf8'), coded_random_text)
            random_output.delete("1.0", tk.END)
            random_output.insert(tk.INSERT, decoded_random_text)
            break
        except:
            count += 1
            if count > 100:
                error("Can't fetch message")
                break
            pass


def show_context():
    try:
        file = messages[file_index]
        unix_timestamp = (file["timestamp_ms"]) / 1000
        time = datetime.fromtimestamp(unix_timestamp)
        time = time.strftime('%B %d, %Y - %I:%M %p')
        show_time.config(text = file["sender_name"]+" : "+time)
    except:
        pass


def move_text(direction):
    global file_index
    if direction == "left":
        file_index = file_index - 1
        if file_index < 0:
            error("Message out of range")
            file_index = file_index + 1
        else:
            random_output.delete("1.0", tk.END)
            random_output.insert(tk.INSERT, messages[file_index]["content"])
            show_context()
    elif direction == "right":
        file_index = file_index + 1
        if file_index > number_of_texts:
            error("Message out of range")
            file_index = file_index - 1
        else:
            random_output.delete("1.0", tk.END)
            random_output.insert(tk.INSERT, messages[file_index]["content"])
            show_context()


def search_load_more(amount_of_texts):
    global new_amount_of_texts
    try:
        if cache_search_keyword[-1] == cache_search_keyword[-2]:
            new_amount_of_texts += 40
            find_text(amount_of_texts= new_amount_of_texts)
        else:
            new_amount_of_texts = 80
            find_text()
    except:
            new_amount_of_texts = 80
            find_text()


def find_text(amount_of_texts = 800):
    global delete_search_scroll_frame
    try:
        delete_search_scroll_frame.destroy()
    except:
        pass
    delete_search_scroll_frame = tk.Frame(search_scroll_canvas, height = 80000, width = 600)
    delete_search_scroll_frame.pack(fill ="both", expand = 1)
    search_keyword = search_entry_widget.get()
    cache_search_keyword.append(search_keyword)
    results_clock = 0
    search_texts_buttons = []
    search_senders_labels = []
    texts_buttons_frames = []
    for searched_message in messages:
        try:
             if (search_keyword.lower() in (searched_message["content"].lower() or re.sub(r'[\xc2-\xf4][\x80-\xbf]+',lambda m: m.group(0).encode("latin1").decode('utf8'), searched_message["content"]).lower())) and (results_clock < amount_of_texts):
                index_of_search_file = messages.index(searched_message)
                decoded_search_text = re.sub(r'[\xc2-\xf4][\x80-\xbf]+',lambda m: m.group(0).encode("latin1").decode('utf8'), searched_message["content"])
                text_button_frame = tk.Frame(delete_search_scroll_frame)
                texts_buttons_frames.append(text_button_frame)
                sender_label = tk.Label(text_button_frame, font = small_joke, text = searched_message["sender_name"] + ":", anchor = "sw")
                search_senders_labels.append(sender_label)
                text_button = tk.Button(text_button_frame, font = joke, text = decoded_search_text, justify = "left", relief = "ridge", wraplength = 300, command = partial(surroundings, index_of_search_file))
                search_texts_buttons.append(text_button)
                results_clock += 1
        except:
            pass
    for frame in texts_buttons_frames:
        frame.grid(sticky = "w", pady= 6)
    for label in search_senders_labels:
        label.pack()
    for button in search_texts_buttons:
        button.pack()
    tk.Button(delete_search_scroll_frame, font = joke, text ="Show More", command = lambda: search_load_more(amount_of_texts)).grid()
    search_scroll_canvas.create_window(0, 0, anchor='nw', window=delete_search_scroll_frame)
    search_scroll_canvas.update_idletasks()
    search_scroll_canvas.configure(scrollregion=search_scroll_canvas.bbox('all'), yscrollcommand=search_text_scrollbar.set)
    search_scroll_canvas.bind_all('<MouseWheel>', lambda event: search_scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))
    search_text_scrollbar.config(command=search_scroll_canvas.yview)



#Displaying each set of widgets
def display_random():
    clear(master)
    control_frame.pack()
    context_switcher_frame.grid(column = 0, row = 0, padx = 10)
    switch_left_button.grid(column = 0, row = 0)
    context_button.grid(column = 1, row = 0)
    switch_right_button.grid(column = 2, row = 0)
    random_button.grid(column = 1, row = 0, pady = 9, padx = 10)
    show_time.pack(pady = 1)
    random_output.pack(pady=8, padx=10)


def display_find_text():
    clear(master)
    search_entry_widget.pack(side ="left", padx = 3)
    search_entry_widget.delete(0, "end")
    search_entry_widget.insert(tk.INSERT, "Keywords")
    search_button.pack(side = "right")
    search_top_frame.pack(pady = 4)
    search_scroll_frame.pack(fill ="both", expand = 1)
    search_text_scrollbar.pack(side ="right", fill ="y")
    search_scroll_canvas.pack(fill ="y")

def display_surroundings():
    clear(master)
    surroundings_scroll_frame.pack(fill = "both", expand = 1)
    surroundings_scrollbar.pack(side = "right", fill ="y")
    surroundings_scroll_canvas.pack(fill = "both")

def display_info():
    clear(master)



#Main Selector
selector = tk.Menu(master)
master.config(menu = selector)
selector.add_cascade(label = "Random Text", font = joke, command = lambda : display_random())
selector.add_cascade(label = "Find Text", font = joke, command = lambda : display_find_text())
selector.add_cascade(label = "Surroundings", font = joke, command = lambda : surroundings(index_of_text = 0))
selector.add_cascade(label = "Information", font = joke, command = lambda : display_info())


#Random Choice Widgets
control_frame = tk.Frame(master)
context_switcher_frame = tk.Frame(control_frame)
context_button = tk.Button(context_switcher_frame, text = "Context", font = joke, command = lambda: show_context())
switch_left_button =tk.Button(context_switcher_frame, text = "<", font = joke, command = lambda: move_text("right"))
switch_right_button =tk.Button(context_switcher_frame, text = ">", font = joke, command = lambda: move_text("left"))
random_button = tk.Button(control_frame, text="Feeling Lucky?", font=joke, command=lambda: random_text())
show_time = tk.Label(master, font = joke)
random_output = tk.scrolledtext.ScrolledText(master, wrap = "word", font = joke)


#Find Text Widgets
search_top_frame = tk.Frame(master)
search_entry_widget = tk.Entry(search_top_frame, font = joke, textvariable ="StringVar", width = 37)
search_button = tk.Button(search_top_frame, font = joke, text ="Search", command = lambda: find_text())
search_scroll_frame = tk.Frame(master)
search_text_scrollbar = tk.Scrollbar(search_scroll_frame, orient ="vertical")
search_scroll_canvas = tk.Canvas(search_scroll_frame, height = 1000)


#Surroundings Widgets
surroundings_scroll_frame = tk.Frame(master, pady = 3, padx = 2)
surroundings_scrollbar = tk.Scrollbar(surroundings_scroll_frame, orient = "vertical")
surroundings_scroll_canvas = tk.Canvas(surroundings_scroll_frame, height = 1000, width = 600)


#Information Widgets



#Close and clear messages
tk.mainloop()
try:
    f.close()
except:
    pass
messages = []