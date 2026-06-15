import tkinter as tk
from tkinter import font as tkfont


# ── Fruit Data ──────────────────────────────────────────────────────
FRUITS = [
    {"name": "Apple", "calories": 52},
    {"name": "Banana", "calories": 89},
    {"name": "Orange", "calories": 47},
    {"name": "Mango", "calories": 60},
    {"name": "Grapes", "calories": 69},
    {"name": "Pineapple", "calories": 50},
    {"name": "Watermelon", "calories": 30},
    {"name": "Papaya", "calories": 43},
    {"name": "Guava", "calories": 68},
    {"name": "Pomegranate", "calories": 83},
    {"name": "Strawberry", "calories": 32},
    {"name": "Blueberries", "calories": 57},
    {"name": "Kiwi", "calories": 61},
    {"name": "Pear", "calories": 57},
    {"name": "Peach", "calories": 39},
    {"name": "Plum", "calories": 46},
    {"name": "Lychee", "calories": 66},
    {"name": "Avocado", "calories": 160},
    {"name": "Coconut (fresh)", "calories": 354},
    {"name": "Dragon Fruit", "calories": 60},
]

# Emoji mapping for fruits
FRUIT_EMOJI = {
    "apple": "🍎", "banana": "🍌", "orange": "🍊", "mango": "🥭",
    "grapes": "🍇", "pineapple": "🍍", "watermelon": "🍉", "papaya": "🍈",
    "guava": "🍐", "pomegranate": "🫐", "strawberry": "🍓", "blueberries": "🫐",
    "kiwi": "🥝", "pear": "🍐", "peach": "🍑", "plum": "🍑",
    "lychee": "🍒", "avocado": "🥑", "coconut (fresh)": "🥥", "dragon fruit": "🐉",
}

# ── Color Palette ───────────────────────────────────────────────────
BG_DARK       = "#1a1b2e"
BG_CARD       = "#252745"
BG_INPUT      = "#2e3054"
ACCENT        = "#7c5cfc"
ACCENT_HOVER  = "#9b82fc"
ACCENT_GLOW   = "#6a4aeb"
TEXT_PRIMARY   = "#e8e6f0"
TEXT_SECONDARY = "#9896a8"
TEXT_DIM       = "#6b6980"
SUCCESS       = "#4ade80"
WARNING       = "#fbbf24"
ERROR         = "#f87171"
BORDER        = "#3a3c5e"
SUGGESTION_BG = "#2e3054"
SUGGESTION_HL = "#3d4070"


# ── Helper: calorie bar color ───────────────────────────────────────
def calorie_color(cal):
    if cal <= 50:
        return SUCCESS
    elif cal <= 80:
        return WARNING
    return ERROR


# ── Main Application ───────────────────────────────────────────────
class NutritionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🍎 Fruit Nutrition Lookup")
        self.configure(bg=BG_DARK)
        self.resizable(False, False)

        # Center on screen
        w, h = 480, 560
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        # Fonts
        self.title_font   = tkfont.Font(family="Segoe UI", size=22, weight="bold")
        self.sub_font     = tkfont.Font(family="Segoe UI", size=11)
        self.input_font   = tkfont.Font(family="Segoe UI", size=14)
        self.result_font  = tkfont.Font(family="Segoe UI", size=36, weight="bold")
        self.label_font   = tkfont.Font(family="Segoe UI", size=12)
        self.btn_font     = tkfont.Font(family="Segoe UI", size=12, weight="bold")
        self.suggest_font = tkfont.Font(family="Segoe UI", size=11)
        self.small_font   = tkfont.Font(family="Segoe UI", size=9)

        self._build_ui()
        self.entry.focus_set()

    # ── Build UI ────────────────────────────────────────────────────
    def _build_ui(self):
        # Title area
        title_frame = tk.Frame(self, bg=BG_DARK)
        title_frame.pack(pady=(30, 0))

        tk.Label(
            title_frame, text="Fruit Nutrition", font=self.title_font,
            fg=TEXT_PRIMARY, bg=BG_DARK,
        ).pack()
        tk.Label(
            title_frame, text="Type a fruit name to see its calories (per 100 g)",
            font=self.sub_font, fg=TEXT_SECONDARY, bg=BG_DARK,
        ).pack(pady=(4, 0))

        # ── Card ────────────────────────────────────────────────────
        card = tk.Frame(self, bg=BG_CARD, highlightbackground=BORDER,
                        highlightthickness=1, bd=0)
        card.pack(padx=30, pady=24, fill="x")

        # Search row
        search_frame = tk.Frame(card, bg=BG_CARD)
        search_frame.pack(padx=20, pady=(20, 0), fill="x")

        input_wrap = tk.Frame(search_frame, bg=BORDER, bd=0,
                              highlightthickness=0)
        input_wrap.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.entry = tk.Entry(
            input_wrap, font=self.input_font, bg=BG_INPUT, fg=TEXT_PRIMARY,
            insertbackground=ACCENT, relief="flat", bd=8,
            highlightthickness=0,
        )
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", lambda e: self._search())
        self.entry.bind("<KeyRelease>", self._on_key)

        self.search_btn = tk.Button(
            search_frame, text="Search", font=self.btn_font,
            bg=ACCENT, fg="white", activebackground=ACCENT_HOVER,
            activeforeground="white", relief="flat", bd=0,
            padx=18, pady=6, cursor="hand2",
            command=self._search,
        )
        self.search_btn.pack(side="right")
        self.search_btn.bind("<Enter>", lambda e: self.search_btn.config(bg=ACCENT_HOVER))
        self.search_btn.bind("<Leave>", lambda e: self.search_btn.config(bg=ACCENT))

        # Suggestion dropdown (hidden by default)
        self.suggest_frame = tk.Frame(card, bg=SUGGESTION_BG, bd=0)
        self.suggest_labels = []

        # Divider
        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=20, pady=18)

        # Result area
        self.result_frame = tk.Frame(card, bg=BG_CARD)
        self.result_frame.pack(padx=20, pady=(0, 24), fill="x")

        # Emoji label
        self.emoji_label = tk.Label(
            self.result_frame, text="🔍", font=tkfont.Font(family="Segoe UI Emoji", size=42),
            bg=BG_CARD, fg=TEXT_PRIMARY,
        )
        self.emoji_label.pack()

        # Calorie number
        self.cal_label = tk.Label(
            self.result_frame, text="—", font=self.result_font,
            fg=TEXT_DIM, bg=BG_CARD,
        )
        self.cal_label.pack(pady=(4, 0))

        # "kcal" subtitle
        self.unit_label = tk.Label(
            self.result_frame, text="type a fruit name above",
            font=self.label_font, fg=TEXT_SECONDARY, bg=BG_CARD,
        )
        self.unit_label.pack()

        # Calorie bar
        self.bar_frame = tk.Frame(self.result_frame, bg=BG_INPUT, height=8)
        self.bar_frame.pack(fill="x", pady=(14, 0))
        self.bar_frame.pack_propagate(False)

        self.bar_fill = tk.Frame(self.bar_frame, bg=BG_INPUT, height=8)
        self.bar_fill.place(x=0, y=0, relheight=1.0, width=0)

        # Bar legend
        self.legend_label = tk.Label(
            self.result_frame, text="", font=self.small_font,
            fg=TEXT_DIM, bg=BG_CARD,
        )
        self.legend_label.pack(pady=(6, 0))

        # ── Footer ─────────────────────────────────────────────────
        tk.Label(
            self, text=f"{len(FRUITS)} fruits in database",
            font=self.small_font, fg=TEXT_DIM, bg=BG_DARK,
        ).pack(side="bottom", pady=(0, 14))

    # ── Suggestions ─────────────────────────────────────────────────
    def _on_key(self, event):
        query = self.entry.get().strip().lower()
        # Clear previous suggestions
        self.suggest_frame.pack_forget()
        for lbl in self.suggest_labels:
            lbl.destroy()
        self.suggest_labels.clear()

        if not query:
            return

        matches = [f for f in FRUITS if f["name"].lower().startswith(query)]
        if not matches or (len(matches) == 1 and matches[0]["name"].lower() == query):
            return

        self.suggest_frame.pack(padx=20, fill="x", after=self.entry.master.master)
        for fruit in matches[:5]:
            lbl = tk.Label(
                self.suggest_frame, text=f"  {FRUIT_EMOJI.get(fruit['name'].lower(), '🍏')}  {fruit['name']}",
                font=self.suggest_font, fg=TEXT_PRIMARY, bg=SUGGESTION_BG,
                anchor="w", padx=10, pady=5, cursor="hand2",
            )
            lbl.pack(fill="x")
            lbl.bind("<Enter>", lambda e, l=lbl: l.config(bg=SUGGESTION_HL))
            lbl.bind("<Leave>", lambda e, l=lbl: l.config(bg=SUGGESTION_BG))
            lbl.bind("<Button-1>", lambda e, name=fruit["name"]: self._pick(name))
            self.suggest_labels.append(lbl)

    def _pick(self, name):
        self.entry.delete(0, "end")
        self.entry.insert(0, name)
        self.suggest_frame.pack_forget()
        for lbl in self.suggest_labels:
            lbl.destroy()
        self.suggest_labels.clear()
        self._search()

    # ── Search Logic ────────────────────────────────────────────────
    def _search(self):
        query = self.entry.get().strip().lower()
        if not query:
            return

        # Hide suggestions
        self.suggest_frame.pack_forget()
        for lbl in self.suggest_labels:
            lbl.destroy()
        self.suggest_labels.clear()

        result = None
        for f in FRUITS:
            if f["name"].lower() == query:
                result = f
                break

        if result:
            cal = result["calories"]
            emoji = FRUIT_EMOJI.get(result["name"].lower(), "🍏")
            color = calorie_color(cal)

            self.emoji_label.config(text=emoji)
            self.cal_label.config(text=str(cal), fg=color)
            self.unit_label.config(text=f"kcal per 100 g  ·  {result['name']}")

            # Animate bar (fraction of max 400 kcal)
            max_cal = 400
            bar_width = self.bar_frame.winfo_width()
            fill_w = int(bar_width * min(cal / max_cal, 1.0))
            self.bar_fill.config(bg=color)
            self._animate_bar(0, fill_w)

            if cal <= 50:
                self.legend_label.config(text="● Low calorie", fg=SUCCESS)
            elif cal <= 80:
                self.legend_label.config(text="● Moderate calorie", fg=WARNING)
            else:
                self.legend_label.config(text="● High calorie", fg=ERROR)
        else:
            self.emoji_label.config(text="❌")
            self.cal_label.config(text="?", fg=ERROR)
            self.unit_label.config(text=f'"{self.entry.get().strip()}" not found')
            self.bar_fill.place(x=0, y=0, relheight=1.0, width=0)
            self.legend_label.config(text="Try another fruit name", fg=TEXT_DIM)

    # ── Bar animation ──────────────────────────────────────────────
    def _animate_bar(self, current, target, step=4):
        if current < target:
            current = min(current + step, target)
            self.bar_fill.place(x=0, y=0, relheight=1.0, width=current)
            self.after(10, self._animate_bar, current, target, step)
        else:
            self.bar_fill.place(x=0, y=0, relheight=1.0, width=target)


# ── Run ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = NutritionApp()
    app.mainloop()
