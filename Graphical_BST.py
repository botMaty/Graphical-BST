from tkinter import *

class Node:
    def __init__(self, value:int):
        self.value = value
        self.left = None
        self.right = None
        self.oval_id = None
        self.line_id = None
        self.text_id = None


class G_BST:

#--------------------------------------------------------------------------------------------------------------
# تابع سازنده

    def __init__(self, canvas:Canvas, rootCenterX, rootCenterY,
                radiuc, oval_fill:str, texts_and_lines_color:str,
                lines_width, on_scroll_color,text_size,
                message:Label, delay:int):
        
        self.root = None
        self.canvas = canvas
        self.rootCenterX = rootCenterX
        self.rootCenterY = rootCenterY
        self.radius = radiuc
        self.oval_fill = oval_fill
        self.texts_and_lines_color = texts_and_lines_color
        self.lines_width = lines_width
        self.on_scroll_color = on_scroll_color
        self.text_size = text_size
        self.message = message
        self.delay = delay

#--------------------------------------------------------------------------------------------------------------
# توابع عمومی

    def insert(self, value):
        """اضافه کردن یک گره جدید به درخت"""
        if self.root:
            self._change_message()
            self._search_recursive(self.root, value, "insert")
        else:
            self.root = Node(value)
            self.root.oval_id = self._make_oval(self.rootCenterX, self.rootCenterY)
            self.root.text_id = self._make_text(self.rootCenterX, self.rootCenterY, value)
            self._change_message(text= "value inseted", color=self.texts_and_lines_color)
            self._make_scroll_better()

            
    def remove(self, value):
        """حذف یک گره از درخت"""
        if self.root:
            self._change_message()
            self._search_recursive(self.root, value, "remove")
        else:
            self._change_message(text= "the BST is empty!", color= self.on_scroll_color)


    def search(self, value):
        """جستجو برای یک مقدار در درخت"""
        if self.root:
            self._change_message()
            self._search_recursive(self.root, value, None)
        else:
            self._change_message(text= "the BST is empty!", color= self.on_scroll_color)

#--------------------------------------------------------------------------------------------------------------
# توابع بازگشتی حذف و درج

    def _insert_recursive(self, node:Node, value, fromR=2): # fromR: تشخیص میدهد که آیا گره فعلی، فرزند راست بوده یا خیر
        """درج به صورت بازگشتی"""
        if value < node.value:
            if fromR == 1:
                self._move_tree(node, dx= 2*self.radius)

            if node.left is None:
                node.left = Node(value)
                x, y = self._get_center(node.oval_id)
                node.left.oval_id = self._make_oval(x - 2*self.radius, y + 4*self.radius)
                node.left.text_id = self._make_text(x - 2*self.radius, y + 4*self.radius, value)
                node.left.line_id = self._make_line(x, y + self.radius, x - 2*self.radius, y + 3*self.radius)
            else:
                self._insert_recursive(node.left, value, fromR=0)

                
        elif value > node.value:
            if fromR == 0:
                self._move_tree(node, dx= -2*self.radius)

            if node.right is None:
                node.right = Node(value)
                x, y = self._get_center(node.oval_id)
                node.right.oval_id = self._make_oval(x + 2*self.radius, y + 4*self.radius)
                node.right.text_id = self._make_text(x + 2*self.radius, y + 4*self.radius, value)
                node.right.line_id = self._make_line(x, y + self.radius, x + 2*self.radius, y + 3*self.radius)
            else:
                self._insert_recursive(node.right, value, fromR=1)


    def _remove_recursive(self, node:Node, value, fromR=2):
        """حذف گره به صورت بازگشتی"""
        if node is None:
            return node
        
        if value < node.value:
            if fromR == 1:
                self._move_tree(node, dx= -2*self.radius)
            node.left = self._remove_recursive(node.left, value, fromR=0)
        elif value > node.value:
            if fromR == 0:
                self._move_tree(node, dx= 2*self.radius)
            node.right = self._remove_recursive(node.right, value, fromR=1)
        else:
            # گره مورد نظر پیدا شد
            coords=[self.rootCenterX,self.rootCenterY - self.radius]
            if node.line_id:
                coords = self.canvas.coords(node.line_id)
            if node.left is None and node.right is None:
                self._remove_node_shapes(node)
                return None
            elif node.left is None:
                x, y = self._get_center(node.right.oval_id)
                self._remove_node_shapes(node)
                self.canvas.delete(node.right.line_id)
                node.right.line_id = self._make_line(coords[0], coords[1], x, y - self.radius)
                if fromR == 0:
                    self._move_tree(node.right, dy=-4*self.radius)
                else:
                    self._move_tree(node.right, dx= -2*self.radius, dy= -4*self.radius)
                return node.right
            elif node.right is None:
                x, y = self._get_center(node.left.oval_id)
                self._remove_node_shapes(node)
                self.canvas.delete(node.left.line_id)
                node.left.line_id = self._make_line(coords[0], coords[1], x, y - self.radius)
                if fromR == 1:
                    self._move_tree(node.left, dy= -4*self.radius)
                else:
                    self._move_tree(node.left, dx= 2*self.radius, dy= -3*self.radius)
                return node.left
            else:
                # گره دو فرزند دارد
                min_node = self._find_min(node.right)
                node.value = min_node.value
                self.canvas.itemconfig(node.text_id, text= min_node.value)
                node.right = self._remove_recursive(node.right, min_node.value, fromR=1)
                if fromR == 0:
                    self._move_tree(node, dx= 2*self.radius)
        return node

#--------------------------------------------------------------------------------------------------------------
# ساختن شکل ها

    def _make_oval(self, centerX, centerY):
        return self.canvas.create_oval(centerX - self.radius,
                                    centerY - self.radius,
                                    centerX + self.radius,
                                    centerY + self.radius,
                                    fill=self.oval_fill,
                                    outline=self.texts_and_lines_color,
                                    width=self.lines_width)
    

    def _make_text(self, centerX, centerY, value):
        return self.canvas.create_text(centerX, centerY,
                                    text=value,
                                    font=("Arial", self.text_size, "bold"),
                                    fill=self.texts_and_lines_color)
    

    def _make_line(self, centerX1, centerY1, centerX2, centerY2):
        return self.canvas.create_line(centerX1,
                                    centerY1,
                                    centerX2,
                                    centerY2,
                                    fill=self.texts_and_lines_color,
                                    arrow="last",
                                    width=self.lines_width)

#--------------------------------------------------------------------------------------------------------------
# پیمایش های نمایشی

    def _search_recursive(self, node:Node, value, command):

        if node is None:
            if command == "insert":
                self._change_message(text= "value inserted", color=self.texts_and_lines_color)
                self._insert_recursive(self.root, value)
                self.canvas.after(self.delay + 200, self._make_scroll_better)
            elif command == "remove":
                self._change_message(text= "value does not exist!", color=self.on_scroll_color)
            else:
                self._change_message(text= "value does not found!", color=self.on_scroll_color)
            return
         
        self._change_node_color(node, self.on_scroll_color)
        self.canvas.after(self.delay, self._change_node_color, node, self.texts_and_lines_color)

        if value == node.value:
            if command == "remove":
                if node.left and node.right:
                    self.canvas.after(self.delay, self._find_min_show, node.right, value)
                else:
                    self._change_message(text= "value has removed successfully", color=self.texts_and_lines_color)
                    self.root = self._remove_recursive(self.root, value)
                    if self.root:
                        self.canvas.after(self.delay + 200, self._root_on_center)
                    self.canvas.after(2*self.delay, self._make_scroll_better)
            elif command == "insert":
                self._change_message(text= "this value is exist!", color=self.on_scroll_color)
            else:
                self._change_message(text= "value has found", color=self.texts_and_lines_color)
            return
        elif value < node.value:
            self.canvas.after(self.delay, self._search_recursive, node.left, value, command)
        else:
            self.canvas.after(self.delay, self._search_recursive, node.right, value, command)
            

    def _find_min_show(self, node, value):

        if node.left:
            self._change_node_color(node, self.on_scroll_color)
            self.canvas.after(self.delay//2, self._change_node_color, node, self.texts_and_lines_color)
            self.canvas.after(self.delay//2, self._find_min_show, node.left, value)
        else:
            self._change_message(text= "value has removed successfully", color=self.texts_and_lines_color)
            self.root = self._remove_recursive(self.root, value)
            if self.root:
                self.canvas.after(self.delay + 200, self._root_on_center)
            self.canvas.after(2*self.delay, self._make_scroll_better)

#--------------------------------------------------------------------------------------------------------------
# بهینه سازی حالت درخت نمایشی

    def _move_node(self, node:Node, dx, dy, root):
        """جابجایی یک گره و خط متصل به آن"""
        self.canvas.move(node.oval_id, dx, dy)

        self.canvas.move(node.text_id, dx, dy)

        if node.line_id:
            coords = self.canvas.coords(node.line_id)
            if node == root:
                x, y = self._get_center(root.oval_id)
                self.canvas.coords(node.line_id, coords[0], coords[1], x , y - self.radius)
            else:
                self.canvas.coords(node.line_id, coords[0] + dx, coords[1] + dy, coords[2] + dx, coords[3] + dy)
            

    def _move_tree(self, root, dx=0, dy=0,steps=20):
        """جابجا کردن کل درخت به موقعیت جدید"""
        delay = self.delay//steps
        def animate_move(step=0):
            if step < steps:
                def move_subtree(node):
                    if node:
                        self._move_node(node, dx, dy, root)
                        move_subtree(node.left)
                        move_subtree(node.right)
                move_subtree(root)
                self.canvas.update()
                self.canvas.after(delay, animate_move, step + 1)
        dx = dx/steps
        dy = dy/steps
        animate_move()


    def _root_on_center(self):
        dx, _ = self._get_center(self.root.oval_id)
        dx = self.rootCenterX - dx

        if self.root.line_id:
            self.canvas.delete(self.root.line_id)
            self.root.line_id = None

        self._move_tree(self.root, dx)

    
    def _make_scroll_better(self):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

#--------------------------------------------------------------------------------------------------------------
# بقیه توابع

    # گرفتن مختصات مرکز دایره گره
    def _get_center(self, oval_id):
        x1, y1, x2, y2 = self.canvas.coords(oval_id)
        return (x1 + x2) / 2, (y1 + y2) / 2
    
    # حذف کننده شکل های یک گره
    def _remove_node_shapes(self, node:Node):
        self.canvas.delete(node.oval_id)
        if node.text_id:
            self.canvas.delete(node.text_id)
        if node.line_id:
            self.canvas.delete(node.line_id)

    # پیدا کننده کمترین مقدار در درخت با ریشه داده شده
    def _find_min(self, node):
        """یافتن کوچک‌ترین مقدار در درخت"""
        while node.left:
            node = node.left
        return node
    
    # تغییر دهنده رنگ text، oval outline، line
    def _change_node_color(self, node:Node ,color):
        self.canvas.itemconfig(node.oval_id, outline= color)
        self.canvas.itemconfig(node.text_id, fill=color)
        if node.line_id:
            self.canvas.itemconfig(node.line_id, fill=color)

    # تابع برای پیام کردن نتیجه
    def _change_message(self, text= "", color= "black"):
        self.message.config(text= text, fg= color)