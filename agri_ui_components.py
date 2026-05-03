import tkinter as tk
from tkinter import ttk
import math

# --- Color Palette ---
C_GRADIENT_TOP = "#2b5876"    # Deep Navy Blue
C_GRADIENT_BTM = "#4e4376"    # Royal Purple
C_BG_MAIN = "#F0F2F5"         # Very light grey/blue for main background
C_CARD_BG = "#FFFFFF"         # Pure White for cards
C_TEXT_MAIN = "#2D3748"       # Dark Slate for main text
C_TEXT_SUB = "#718096"        # Cool Grey for subtitles
C_TEXT_LIGHT = "#FFFFFF"      # White text
C_ACCENT = "#4e4376"          # Matches bottom gradient
C_ACCENT_HOVER = "#2b5876"    # Hover state
C_ERROR = "#E53E3E"           # Red
C_SUCCESS = "#38A169"         # Green
C_WARNING = "#E67E22"         # Orange
C_INPUT_BG = "#F7FAFC"        # Very light grey for inputs
C_BORDER = "#E2E8F0"          # Light border color

# Graph Specific Colors
C_LINE_CONTROL = "#4e4376"
C_LINE_NO_CONTROL = "#A0AEC0"
C_LINE_TEMP = "#E53E3E"
C_LINE_HUM = "#3182CE"
C_LINE_SOIL = "#38A169"

class ModernButton(tk.Canvas):
    """A rounded, modern button using Canvas."""
    def __init__(self, parent, text, command, width=200, height=45, color=C_ACCENT, **kwargs):
        super().__init__(parent, width=width, height=height, bg=C_CARD_BG, highlightthickness=0, **kwargs)
        self.command = command
        self.text = text
        self.width = width
        self.height = height
        
        self.normal_color = color
        self.hover_color = C_ACCENT_HOVER if color == C_ACCENT else color 
        
        self.rect = self.create_rounded_rect(2, 2, width-2, height-2, radius=10, fill=self.normal_color)
        self.text_id = self.create_text(width/2, height/2, text=text, fill="white", font=("Segoe UI", 11, "bold"))
        
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

    def _on_enter(self, e):
        self.itemconfig(self.rect, fill=self.hover_color)

    def _on_leave(self, e):
        self.itemconfig(self.rect, fill=self.normal_color)

    def _on_click(self, e):
        if self.command:
            self.command()

class ModernEntry(tk.Frame):
    """A wrapper for Entry/Combobox to give it a custom modern look."""
    def __init__(self, parent, label_text, widget_type="entry", values=None, readonly=False, default=None):
        super().__init__(parent, bg=C_CARD_BG)
        self.lbl = tk.Label(self, text=label_text, bg=C_CARD_BG, fg=C_TEXT_SUB, font=("Segoe UI", 9, "bold"))
        self.lbl.pack(anchor="w", pady=(0, 2))
        
        self.input_frame = tk.Frame(self, bg=C_INPUT_BG, highlightbackground=C_BORDER, highlightthickness=1)
        self.input_frame.pack(fill="x", ipady=2)
        
        if widget_type == "combo":
            self.widget = ttk.Combobox(self.input_frame, values=values, state="readonly" if readonly else "normal", font=("Segoe UI", 11))
        else:
            self.widget = tk.Entry(self.input_frame, bg=C_INPUT_BG, fg=C_TEXT_MAIN, font=("Segoe UI", 11), relief="flat")
        
        if default:
            self.set(default)
            
        self.widget.pack(fill="x", padx=10, pady=8)
        self.widget.bind("<FocusIn>", self._on_focus)
        self.widget.bind("<FocusOut>", self._on_unfocus)

    def _on_focus(self, e):
        self.input_frame.config(highlightbackground=C_ACCENT, highlightthickness=2)
        self.lbl.config(fg=C_ACCENT)

    def _on_unfocus(self, e):
        self.input_frame.config(highlightbackground=C_BORDER, highlightthickness=1)
        self.lbl.config(fg=C_TEXT_SUB)

    def get(self):
        return self.widget.get()

    def set(self, val):
        if isinstance(self.widget, ttk.Combobox):
            self.widget.set(val)
        else:
            self.widget.delete(0, tk.END)
            self.widget.insert(0, val)

    def current(self, index):
        if isinstance(self.widget, ttk.Combobox):
            self.widget.current(index)

class GradientSidebar(tk.Canvas):
    def __init__(self, parent, navigate_callback, **kwargs):
        super().__init__(parent, highlightthickness=0, **kwargs)
        self.navigate = navigate_callback
        self.buttons = {}
        self.selected_btn = None
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        r1, g1, b1 = self.winfo_rgb(C_GRADIENT_TOP)
        r2, g2, b2 = self.winfo_rgb(C_GRADIENT_BTM)
        for i in range(height):
            r = int(r1 + (r2 - r1) * i / height)
            g = int(g1 + (g2 - g1) * i / height)
            b = int(b1 + (b2 - b1) * i / height)
            color = "#%04x%04x%04x" % (r, g, b)
            self.create_line(0, i, width, i, tags=("gradient",), fill=color)
        self.tag_lower("gradient")

    def add_menu_button(self, text, page_name, y_pos):
        rect_id = self.create_rectangle(15, y_pos, 235, y_pos+50, fill="", outline="", tags=(page_name, "btn"))
        text_id = self.create_text(40, y_pos+25, text=text, anchor="w", font=("Segoe UI", 12), fill=C_TEXT_LIGHT, tags=(page_name, "btn"))
        self.buttons[page_name] = {'rect': rect_id, 'text': text_id}
        self.tag_bind(page_name, "<Button-1>", lambda e, p=page_name: self.navigate(p))
        self.tag_bind(page_name, "<Enter>", lambda e, p=page_name: self.itemconfigure(self.buttons[p]['rect'], fill="#ffffff", stipple="gray25"))
        self.tag_bind(page_name, "<Leave>", lambda e, p=page_name: self._check_active(p))

    def _check_active(self, page_name):
        if self.selected_btn != page_name:
            self.itemconfigure(self.buttons[page_name]['rect'], fill="")

    def set_active(self, page_name):
        for btn in self.buttons:
            self.itemconfigure(self.buttons[btn]['rect'], fill="")
            self.itemconfigure(self.buttons[btn]['text'], font=("Segoe UI", 12))
        self.selected_btn = page_name
        self.itemconfigure(self.buttons[page_name]['rect'], fill="#ffffff", stipple="gray50")
        self.itemconfigure(self.buttons[page_name]['text'], font=("Segoe UI", 12, "bold"))

class SimpleGraph(tk.Canvas):
    def __init__(self, parent, width=500, height=300, bg=C_CARD_BG, **kwargs):
        super().__init__(parent, width=width, height=height, bg=bg, highlightthickness=0, **kwargs)
        self.w = width
        self.h = height
        self.padding = 40

    def draw_chart(self, title, x_labels, data_main, label_main, data_ref=None, label_ref=None, line_color=C_LINE_CONTROL):
        self.delete("all")
        
        origin_x = self.padding
        origin_y = self.h - self.padding
        max_x = self.w - self.padding
        min_y = self.padding

        self.create_line(origin_x, origin_y, max_x, origin_y, fill=C_BORDER, width=2) # X
        self.create_line(origin_x, origin_y, origin_x, min_y, fill=C_BORDER, width=2) # Y

        vals_main = list(data_main.values())
        vals_ref = list(data_ref.values()) if data_ref else []
        all_values = vals_main + vals_ref
        
        max_val = max(all_values) if all_values else 5
        min_val = min(all_values) if all_values else 0
        
        y_range = max_val - min_val
        if y_range == 0: y_range = 10
        display_max = max_val + (y_range * 0.1)
        display_min = max(0, min_val - (y_range * 0.1))

        for i in range(5):
            val = display_min + (i * (display_max - display_min) / 4)
            y = origin_y - ((val - display_min) / (display_max - display_min)) * (origin_y - min_y)
            self.create_line(origin_x-5, y, origin_x, y, fill=C_TEXT_SUB)
            self.create_text(origin_x-20, y, text=f"{int(val)}", fill=C_TEXT_SUB, font=("Segoe UI", 8))

        keys = list(data_main.keys())
        num_points = len(keys)
        x_step = (max_x - origin_x) / (num_points - 1) if num_points > 1 else 0
        
        label_skip = 1
        if num_points > 10:
            label_skip = math.ceil(num_points / 8)

        point_coords_main = []
        point_coords_ref = []

        for idx, key in enumerate(keys):
            x = origin_x + (idx * x_step)
            if idx % label_skip == 0:
                self.create_text(x, origin_y + 15, text=str(key), fill=C_TEXT_SUB, font=("Segoe UI", 8), angle=0)
            
            val_m = data_main.get(key, 0)
            y_m = origin_y - ((val_m - display_min) / (display_max - display_min)) * (origin_y - min_y)
            point_coords_main.append((x, y_m))
            
            if data_ref:
                val_r = data_ref.get(key, 0)
                y_r = origin_y - ((val_r - display_min) / (display_max - display_min)) * (origin_y - min_y)
                point_coords_ref.append((x, y_r))

        if point_coords_ref and len(point_coords_ref) > 1:
            self.create_line(point_coords_ref, fill=C_LINE_NO_CONTROL, width=2, dash=(4, 2), smooth=True)

        if len(point_coords_main) > 1:
            self.create_line(point_coords_main, fill=line_color, width=3, smooth=True)
            if num_points < 20:
                for x, y in point_coords_main:
                    self.create_oval(x-3, y-3, x+3, y+3, fill=line_color, outline=C_CARD_BG)
        
        legend_text = f"{title}"
        if label_ref:
            legend_text += f" vs {label_ref}"
        self.create_text(self.w/2, 15, text=legend_text, font=("Segoe UI", 10, "bold"), fill=C_TEXT_MAIN)