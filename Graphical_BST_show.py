from tkinter import *
from Graphical_BST import G_BST

#---------------------------------------------------------------------
# متغیر های قابل تغییر

# fullscreen on my screen: "1366x768"
Xview = "1366"
Yview = "768"

window_color = "white"                              # "white"
oval_and_button_and_entry_fill = "skyblue"            # "skyblue"
texts_and_lines_color = "black"                   # "black"
texts_and_lines_scrolling_tree_color = "red"    # "red"

entry_and_button_and_message_font_size = 13
nodes_text_font_size = 13

lines_width = 2
oval_radius = 20
delay = 600

#---------------------------------------------------------------------
# توابع برای کلید ها

def insertToBST():
    value = int(insert_entry.get())
    gbst.insert(value= value)

def removeFromBST():
    value = int(remove_entry.get())
    gbst.remove(value= value)

def searchOnBST():
    value = int(search_entry.get())
    gbst.search(value= value)

#---------------------------------------------------------------------
# توابع ساخت کلید و تسکبار

def make_entry(ribbon):  
    return Entry(ribbon,
                font=("Arial", entry_and_button_and_message_font_size),
                fg= texts_and_lines_color,
                bg = oval_and_button_and_entry_fill,
                bd= lines_width,
                relief= "solid",
                highlightthickness= lines_width,
                highlightbackground= texts_and_lines_color,
                highlightcolor= texts_and_lines_color)


def make_button(ribbon, text, command):
    return Button(ribbon, text= text,
                command= command,
                font=("Comic Sans", entry_and_button_and_message_font_size, 'bold'),
                fg= texts_and_lines_color,
                bg= oval_and_button_and_entry_fill,
                activeforeground= oval_and_button_and_entry_fill,
                activebackground= texts_and_lines_color)

#---------------------------------------------------------------------
# ایجاد پنجره اصلی

window = Tk()
window.title("Graphical BST")
window.config(background=window_color)
icon = PhotoImage(file="assets/BST_Icon.png")
window.iconphoto(True,icon)
window.geometry("{}x{}".format(Xview, Yview))

# Frame برای تسک‌بار
ribbon = Frame(window, bg = window_color)
ribbon.pack(side=TOP, fill=X)

# Frame برای Canvas و Scrollbar
canvos = Frame(window, bg = window_color)
canvos.pack(fill=BOTH, expand=True)

# Canvas با قابلیت اسکرول
canvas = Canvas(canvos, bg= window_color)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

# Scrollbar عمودی
v_scrollbar = Scrollbar(canvos, orient=VERTICAL, command=canvas.yview)
v_scrollbar.pack(side=RIGHT, fill=Y)


# Scrollbar افقی
h_scrollbar = Scrollbar(window, orient=HORIZONTAL, command=canvas.xview)
h_scrollbar.pack(side=BOTTOM, fill=X)

# افزودن اسکرول ها به canvas
canvas.config(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

#---------------------------------------------------------------------
# افزودن کلیدها ، تسکبارهاو پیام نتیجه

insert_entry = make_entry(ribbon= ribbon)
insert_entry.pack(side= LEFT)

insert_button = make_button(ribbon= ribbon, text= 'Insert', command= insertToBST)
insert_button.pack(side=LEFT)



remove_entry = make_entry(ribbon= ribbon)
remove_entry.pack(side=LEFT)

remove_button = make_button(ribbon= ribbon, text= 'Remove', command= removeFromBST)
remove_button.pack(side=LEFT)



search_entry = make_entry(ribbon= ribbon)
search_entry.pack(side=LEFT)

search_button = make_button(ribbon= ribbon, text= 'Search', command= searchOnBST)
search_button.pack(side=LEFT)



message = Label(ribbon, text= "",
                    font=("Arial", entry_and_button_and_message_font_size),
                    bg= window_color)
message.pack(side=RIGHT)

#---------------------------------------------------------------------
# ساختن درخت گرافیکی
gbst = G_BST(canvas=canvas,
            rootCenterX=int(Xview)//2,
            rootCenterY=60,
            radiuc= oval_radius,
            oval_fill= oval_and_button_and_entry_fill,
            texts_and_lines_color= texts_and_lines_color,
            lines_width= lines_width,
            on_scroll_color= texts_and_lines_scrolling_tree_color,
            text_size= nodes_text_font_size,
            message= message,
            delay=delay)

window.mainloop()
