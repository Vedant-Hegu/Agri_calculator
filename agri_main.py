import tkinter as tk
from tkinter import ttk
from agri_ui_components import *
from agri_backend import AgriBackend

APP_TITLE = "AgriCalc"
APP_SIZE = "950x650"

class AgriApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(APP_SIZE)
        self.root.configure(bg=C_BG_MAIN)
        
        # Initialize Backend
        self.backend = AgriBackend()

        # 1. Sidebar
        self.sidebar = GradientSidebar(root, self.switch_page, width=250)
        self.sidebar.pack(side="left", fill="y")

        # 2. Content Area
        self.content_area = tk.Frame(root, bg=C_BG_MAIN)
        self.content_area.pack(side="right", fill="both", expand=True)

        # 3. Setup Menu
        self.sidebar.add_menu_button("🌱 Seed Counter", "seed_page", 100)
        self.sidebar.add_menu_button("💧 Germination", "germ_page", 160)
        self.sidebar.add_menu_button("📊 Comparison", "comp_page", 220)
        self.sidebar.add_menu_button("📈 Monitoring", "mon_page", 280)

        # 4. Initialize Pages
        self.frames = {}
        self._init_seed_page()
        self._init_germ_page()
        self._init_comp_page()
        self._init_monitor_page()

        self.switch_page("seed_page")

    def switch_page(self, page_name):
        self.sidebar.set_active(page_name)
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[page_name].pack(fill="both", expand=True)

    def _create_centered_card(self, parent, title, subtitle):
        container = tk.Frame(parent, bg=C_BG_MAIN)
        container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.9)

        tk.Label(container, text=title, font=("Segoe UI", 28, "bold"), bg=C_BG_MAIN, fg=C_TEXT_MAIN).pack(anchor="center", pady=(0, 5))
        tk.Label(container, text=subtitle, font=("Segoe UI", 11), bg=C_BG_MAIN, fg=C_TEXT_SUB).pack(anchor="center", pady=(0, 20))

        card = tk.Frame(container, bg=C_CARD_BG, highlightbackground="#E2E8F0", highlightthickness=1)
        card.pack(fill="both", expand=True, padx=20, pady=20)
        
        inner = tk.Frame(card, bg=C_CARD_BG)
        inner.pack(fill="both", expand=True, padx=20, pady=20)
        return inner

    # --- Page 1: Seed Counter ---
    def _init_seed_page(self):
        frame = tk.Frame(self.content_area, bg=C_BG_MAIN)
        self.frames["seed_page"] = frame
        card = self._create_centered_card(frame, "Seed Estimator", "Calculate total seeds from batch weight")
        
        content = tk.Frame(card, bg=C_CARD_BG)
        content.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8)

        self.input_crop = ModernEntry(content, "Select Crop Type", widget_type="combo", values=list(self.backend.CROP_DATA.keys()), readonly=True)
        self.input_crop.pack(fill="x", pady=(0, 20))
        self.input_crop.current(0)

        self.input_weight = ModernEntry(content, "Total Batch Weight (g)")
        self.input_weight.pack(fill="x", pady=(0, 30))

        ModernButton(content, "Calculate Seeds", self.calc_seeds, width=250).pack(pady=(0, 30))

        self.lbl_seed_res = tk.Label(content, text="Ready to calculate", font=("Segoe UI", 16, "bold"), bg=C_CARD_BG, fg=C_TEXT_SUB)
        self.lbl_seed_res.pack()
        self.lbl_seed_details = tk.Label(content, text="", font=("Segoe UI", 10), bg=C_CARD_BG, fg=C_TEXT_SUB)
        self.lbl_seed_details.pack(pady=(5,0))

    def calc_seeds(self):
        try:
            crop = self.input_crop.get()
            weight = float(self.input_weight.get())
            
            total, sample_weight = self.backend.calculate_seeds_from_weight(crop, weight)
            
            self.lbl_seed_res.config(text=f"{total:,} Seeds", fg=C_SUCCESS)
            self.lbl_seed_details.config(text=f"Based on {crop} ({sample_weight}g / {self.backend.FIXED_SAMPLE_COUNT} seeds)")
        except ValueError:
            self.lbl_seed_res.config(text="Invalid Input", fg=C_ERROR)
            self.lbl_seed_details.config(text="Please check weight and selection")

    # --- Page 2: Germination ---
    def _init_germ_page(self):
        frame = tk.Frame(self.content_area, bg=C_BG_MAIN)
        self.frames["germ_page"] = frame
        card = self._create_centered_card(frame, "Germination Planner", "Predict viability based on historical data")

        content = tk.Frame(card, bg=C_CARD_BG)
        content.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8)

        self.input_germ_crop = ModernEntry(content, "Select Crop Type", widget_type="combo", values=list(self.backend.GERM_RATES.keys()), readonly=True)
        self.input_germ_crop.pack(fill="x", pady=(0, 20))
        self.input_germ_crop.current(0)

        self.input_germ_target = ModernEntry(content, "Seed Count (To Sow/Target)")
        self.input_germ_target.pack(fill="x", pady=(0, 30))

        ModernButton(content, "Analyze Viability", self.predict_germ, width=250).pack(pady=(0, 30))

        self.lbl_germ_rate_display = tk.Label(content, text="Select crop to see rate", font=("Segoe UI", 14), bg=C_CARD_BG, fg=C_ACCENT)
        self.lbl_germ_rate_display.pack()
        
        self.lbl_germ_extra = tk.Label(content, text="", font=("Segoe UI", 11, "bold"), bg=C_CARD_BG, fg=C_WARNING)
        self.lbl_germ_extra.pack(pady=(10, 0))

    def predict_germ(self):
        try:
            crop = self.input_germ_crop.get()
            target = int(self.input_germ_target.get())
            if target <= 0: raise ValueError

            res = self.backend.calculate_germination_needs(crop, target)
            
            self.lbl_germ_rate_display.config(text=f"Historical Viability: {res['rate_percent']:.1f}%\nExpected Viable: {res['expected_viable']} plants")
            
            if res['extra_seeds'] > 0:
                self.lbl_germ_extra.config(
                    text=f"To get {target} successful plants,\nsow {res['extra_seeds']} EXTRA seeds (Total: {res['needed_total']}).",
                    fg=C_WARNING
                )
            else:
                self.lbl_germ_extra.config(text="Rate is 100% (Theoretical). No extra seeds needed.", fg=C_SUCCESS)
        except ValueError:
            self.lbl_germ_rate_display.config(text="Invalid Input", fg=C_ERROR)
            self.lbl_germ_extra.config(text="")

    # --- Page 3: Comparison ---
    def _init_comp_page(self):
        frame = tk.Frame(self.content_area, bg=C_BG_MAIN)
        self.frames["comp_page"] = frame
        
        container = tk.Frame(frame, bg=C_BG_MAIN)
        container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.95)

        tk.Label(container, text="Growth Comparison", font=("Segoe UI", 28, "bold"), bg=C_BG_MAIN, fg=C_TEXT_MAIN).pack(pady=(0, 5))
        tk.Label(container, text="Analyze effect of environmental controls vs No Control", font=("Segoe UI", 11), bg=C_BG_MAIN, fg=C_TEXT_SUB).pack(pady=(0, 15))

        card = tk.Frame(container, bg=C_CARD_BG, highlightbackground=C_BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=20, pady=10)

        controls = tk.Frame(card, bg=C_CARD_BG)
        controls.pack(fill="x", padx=20, pady=20)
        
        self.comp_crop = ModernEntry(controls, "Select Seed", widget_type="combo", values=list(self.backend.CROP_DATA.keys()), readonly=True)
        self.comp_crop.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.comp_crop.current(0)

        self.comp_mode = ModernEntry(controls, "Control Mode", widget_type="combo", values=["Soil Controlled", "Humidity and Moisture Control"], readonly=True)
        self.comp_mode.pack(side="left", fill="x", expand=True, padx=(10, 10))
        self.comp_mode.current(0)
        
        btn_frame = tk.Frame(controls, bg=C_CARD_BG, pady=10)
        btn_frame.pack(side="left", padx=(10, 0))
        ModernButton(btn_frame, "Compare", self.update_graph, width=120, height=45).pack()

        graph_row = tk.Frame(card, bg=C_CARD_BG)
        graph_row.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.graph_canvas = SimpleGraph(graph_row, bg=C_CARD_BG, width=420, height=320)
        self.graph_canvas.pack(side="left", fill="both", expand=True)
        
        insight_frame = tk.Frame(graph_row, bg=C_INPUT_BG, relief="flat", padx=10, pady=10)
        insight_frame.pack(side="right", fill="y", padx=(10, 0), anchor="n")
        
        self.lbl_insight = tk.Label(insight_frame, text="Select options and\nclick Compare to\nsee insights.", font=("Segoe UI", 10), bg=C_INPUT_BG, fg=C_TEXT_MAIN, justify="left", wraplength=220, anchor="nw")
        self.lbl_insight.pack(fill="both", expand=True)

        legend = tk.Frame(card, bg=C_CARD_BG)
        legend.pack(fill="x", pady=(0, 15))
        
        l1 = tk.Frame(legend, bg=C_CARD_BG)
        l1.pack(side="top", anchor="center")
        
        tk.Label(l1, text="― ● ", fg=C_LINE_CONTROL, font=("Arial", 14, "bold"), bg=C_CARD_BG).pack(side="left")
        tk.Label(l1, text="Selected Mode", fg=C_TEXT_MAIN, font=("Segoe UI", 10), bg=C_CARD_BG).pack(side="left", padx=(0, 20))
        
        tk.Label(l1, text="- - ● ", fg=C_LINE_NO_CONTROL, font=("Arial", 14, "bold"), bg=C_CARD_BG).pack(side="left")
        tk.Label(l1, text="No Control (Baseline)", fg=C_TEXT_MAIN, font=("Segoe UI", 10), bg=C_CARD_BG).pack(side="left")

        info_frame = tk.Frame(card, bg=C_INPUT_BG, padx=15, pady=10)
        info_frame.pack(fill="x", padx=20, pady=(0, 20))

        tk.Label(info_frame, text="How to interpret this graph:", font=("Segoe UI", 9, "bold"), bg=C_INPUT_BG, fg=C_TEXT_MAIN).pack(anchor="w")
        
        info_text = ("The solid purple line represents seed germination under your selected controlled conditions (Soil or Humidity). "
            "The dashed grey line shows the baseline 'No Control' results for comparison. "
            "A higher purple peak indicates that the control method is improving germination rates.")
        tk.Label(info_frame, text=info_text, font=("Segoe UI", 9), bg=C_INPUT_BG, fg=C_TEXT_SUB, justify="left", wraplength=700).pack(anchor="w", pady=(2,0))

        self.root.after(100, self.update_graph)

    def update_graph(self):
        crop = self.comp_crop.get()
        mode = self.comp_mode.get()
        if not crop or not mode: return
        
        data_main, data_ref = self.backend.get_graph_data(mode, crop)
        
        self.graph_canvas.draw_chart(title=f"{crop} Performance", x_labels=list(data_main.keys()), data_main=data_main, label_main=mode, data_ref=data_ref, label_ref="No Control")

        insight = self.backend.INSIGHTS.get(crop, "No specific insights available for this crop selection.")
        self.lbl_insight.config(text=insight)

    # --- Page 4: Monitoring ---
    def _init_monitor_page(self):
        frame = tk.Frame(self.content_area, bg=C_BG_MAIN)
        self.frames["mon_page"] = frame
        
        container = tk.Frame(frame, bg=C_BG_MAIN)
        container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.95)

        tk.Label(container, text="Project Data Log", font=("Segoe UI", 28, "bold"), bg=C_BG_MAIN, fg=C_TEXT_MAIN).pack(pady=(0, 5))
        tk.Label(container, text="Historical sensor readings from past recording sessions", font=("Segoe UI", 11), bg=C_BG_MAIN, fg=C_TEXT_SUB).pack(pady=(0, 15))

        # Stats
        stats_frame = tk.Frame(container, bg=C_BG_MAIN)
        stats_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.lbl_avg_temp = self._create_stat_box(stats_frame, "Avg Temp", C_LINE_TEMP)
        self.lbl_avg_hum = self._create_stat_box(stats_frame, "Avg Humidity", C_LINE_HUM)
        self.lbl_avg_soil = self._create_stat_box(stats_frame, "Avg Soil Moisture", C_LINE_SOIL)

        # Graph Card
        card = tk.Frame(container, bg=C_CARD_BG, highlightbackground=C_BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=20, pady=10)

        # Controls
        ctrl = tk.Frame(card, bg=C_CARD_BG)
        ctrl.pack(fill="x", padx=20, pady=20)
        
        tk.Label(ctrl, text="Visualizing:", font=("Segoe UI", 12, "bold"), bg=C_CARD_BG, fg=C_TEXT_MAIN).pack(side="left")
        btn_frame = tk.Frame(ctrl, bg=C_CARD_BG)
        btn_frame.pack(side="left", padx=20)

        ModernButton(btn_frame, "Temperature", lambda: self.update_mon_graph("temp"), width=120, height=35, color=C_LINE_TEMP).pack(side="left", padx=5)
        ModernButton(btn_frame, "Humidity", lambda: self.update_mon_graph("humidity"), width=120, height=35, color=C_LINE_HUM).pack(side="left", padx=5)
        ModernButton(btn_frame, "Soil Moisture", lambda: self.update_mon_graph("soil"), width=120, height=35, color=C_LINE_SOIL).pack(side="left", padx=5)

        self.mon_graph = SimpleGraph(card, bg=C_CARD_BG, width=600, height=300)
        self.mon_graph.pack(fill="both", expand=True, padx=20, pady=10)

        self.alert_frame = tk.Frame(card, bg=C_INPUT_BG, padx=15, pady=10)
        self.alert_frame.pack(fill="x", padx=20, pady=20)
        self.lbl_alert = tk.Label(self.alert_frame, text="Log Analysis: specific dataset loaded", font=("Segoe UI", 10, "bold"), bg=C_INPUT_BG, fg=C_TEXT_SUB)
        self.lbl_alert.pack(anchor="w")

        self.current_mon_view = "temp"
        self.calculate_mon_stats()
        self.root.after(500, lambda: self.update_mon_graph("temp"))

    def _create_stat_box(self, parent, title, color):
        box = tk.Frame(parent, bg=C_CARD_BG, highlightbackground=color, highlightthickness=1, width=200, height=100)
        box.pack(side="left", fill="both", expand=True, padx=10)
        box.pack_propagate(False)
        
        tk.Label(box, text=title, font=("Segoe UI", 10), bg=C_CARD_BG, fg=C_TEXT_SUB).pack(anchor="w", padx=15, pady=(15, 5))
        val_lbl = tk.Label(box, text="--", font=("Segoe UI", 20, "bold"), bg=C_CARD_BG, fg=color)
        val_lbl.pack(anchor="w", padx=15)
        return val_lbl

    def calculate_mon_stats(self):
        t_avg, h_avg, s_avg = self.backend.get_monitoring_stats()
        self.lbl_avg_temp.config(text=f"{t_avg:.1f}°C")
        self.lbl_avg_hum.config(text=f"{int(h_avg)}%")
        self.lbl_avg_soil.config(text=f"{int(s_avg)}")

    def update_mon_graph(self, metric):
        self.current_mon_view = metric
        
        c_map = {"temp": C_LINE_TEMP, "humidity": C_LINE_HUM, "soil": C_LINE_SOIL}
        t_map = {"temp": "Temperature (°C)", "humidity": "Humidity (%)", "soil": "Soil Moisture"}
        color = c_map.get(metric, C_LINE_CONTROL)
        title = t_map.get(metric, metric.title())

        data_map = {}
        values = self.backend.MONITOR_DATA.get(metric, [])
        timestamps = self.backend.MONITOR_DATA.get("time", [])

        for i, val in enumerate(values):
            if i < len(timestamps):
                data_map[timestamps[i]] = val
        
        self.mon_graph.draw_chart(title=title, x_labels=timestamps, data_main=data_map, label_main="Sensor Data", line_color=color)

        latest_val = values[-1]
        msg = f"Last Recorded: {latest_val}"
        
        if metric == "soil" and latest_val < 65:
            msg += " (Low Moisture in record)"
            self.lbl_alert.config(fg=C_ERROR, text=msg)
        elif metric == "temp" and latest_val > 30:
            msg += " (High Temp in record)"
            self.lbl_alert.config(fg=C_ERROR, text=msg)
        else:
            msg += " (Within normal range)"
            self.lbl_alert.config(fg=C_SUCCESS, text=msg)

if __name__ == "__main__":
    root = tk.Tk()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - 950) // 2
    y = (sh - 650) // 2
    root.geometry(f"950x650+{x}+{y}")
    app = AgriApp(root)
    root.mainloop()