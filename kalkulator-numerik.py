"""
INSTALL LIBRARY YANG DIBUTUHKAN SEBELUM MENJALANKAN PROGRAM

        >>>> Install: pip install -r requirements.txt <<<<

"""

import sys

missing_deps = []

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext, filedialog, colorchooser
except ImportError:
    missing_deps.append("tkinter -> Linux: sudo apt-get install python3-tk")

try:
    import sympy as sp
    from sympy import sympify, Symbol, diff, lambdify, sqrt, sin, cos, tan, log, exp, pi, E, N
except ImportError:
    missing_deps.append("sympy -> pip install sympy")

try:
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    from matplotlib.figure import Figure
except ImportError:
    missing_deps.append("matplotlib -> pip install matplotlib")

try:
    import numpy as np
except ImportError:
    missing_deps.append("numpy -> pip install numpy")

try:
    import pandas as pd
except ImportError:
    missing_deps.append("pandas -> pip install pandas")

try:
    from PIL import Image
except ImportError:
    missing_deps.append("Pillow -> pip install Pillow")

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas as pdfcanvas
    from reportlab.lib.units import cm
except ImportError:
    missing_deps.append("reportlab -> pip install reportlab")

try:
    import openpyxl
except ImportError:
    missing_deps.append("openpyxl -> pip install openpyxl")

if missing_deps:
    print("=" * 60)
    print("ERROR: DEPENDENCY BELUM TERINSTALL!")
    print("=" * 60)
    for i, dep in enumerate(missing_deps, 1):
        print(f"{i}. {dep}")
    print("\nInstall semua: pip install -r requirements.txt")
    print("=" * 60)
    sys.exit(1)

import math
import os
from datetime import datetime
import io
import tempfile

x = Symbol('x')

# ============================================================
# KELAS TOOLTIP (Fitur #12)
# ============================================================
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        try:
            x, y, _, _ = self.widget.bbox("insert")
        except Exception:
            x, y = 0, 0
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, justify=tk.LEFT,
                        background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                        font=("Segoe UI", 9), wraplength=300)
        label.pack()

    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

# ============================================================
# KELAS UTAMA
# ============================================================
class KalkulatorNumerikUltimate:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator Metode Numerik - ULTIMATE EDITION")
        self.root.geometry("1400x950")
        self.root.minsize(1200, 800)

        # Tema
        self.dark_mode = False
        self.themes = {
            "light": {"bg": "#f0f0f0", "fg": "#2c3e50", "card": "#ecf0f1", 
                     "input": "white", "text": "black", "accent": "#3498db"},
            "dark": {"bg": "#1a1a2e", "fg": "#eaeaea", "card": "#16213e", 
                    "input": "#0f3460", "text": "#eaeaea", "accent": "#e94560"}
        }
        self.current_theme = self.themes["light"]

        # Data & History
        self.history = []  # list of dict
        self.step_mode = False
        self.step_data = None
        self.step_index = 0
        self.step_method = None
        self.step_fig = None
        self.step_ax = None
        self.step_canvas = None

        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.active_entry = None
        self.build_ui()
        self.apply_theme()

    def apply_theme(self):
        t = self.current_theme
        self.root.configure(bg=t["bg"])
        # Update all frames recursively would be complex; 
        # we set at build time using t dict

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.current_theme = self.themes["dark" if self.dark_mode else "light"]
        t = self.current_theme

        # Update root
        self.root.configure(bg=t["bg"])

        # Update header
        self.header.configure(bg="#0f3460" if self.dark_mode else "#2c3e50")
        self.header_label.configure(bg=self.header.cget("bg"), fg="white")

        # Update main
        self.main.configure(bg=t["bg"])

        # Update notebook style
        if self.dark_mode:
            self.style.configure('TNotebook', background=t["bg"], tabmargins=[2,2,2,0])
            self.style.configure('TNotebook.Tab', background=t["card"], foreground=t["text"])
            self.style.map('TNotebook.Tab', background=[("selected", t["accent"])])
        else:
            self.style.configure('TNotebook', background=t["bg"])
            self.style.configure('TNotebook.Tab', background="#ddd", foreground="black")
            self.style.map('TNotebook.Tab', background=[("selected", "#3498db")])

        messagebox.showinfo("Tema", f"Tema {'Dark' if self.dark_mode else 'Light'} Mode aktif!")

    def build_ui(self):
        t = self.current_theme

        # Header
        self.header = tk.Frame(self.root, bg="#2c3e50", height=60)
        self.header.pack(fill=tk.X)
        self.header_label = tk.Label(self.header, 
            text="KALKULATOR METODE NUMERIK - ULTIMATE EDITION", 
            font=('Segoe UI', 16, 'bold'), bg="#2c3e50", fg="white")
        self.header_label.pack(pady=12)

        # Top toolbar
        toolbar = tk.Frame(self.root, bg=t["bg"])
        toolbar.pack(fill=tk.X, padx=10, pady=(5,0))

        tk.Button(toolbar, text="🌙 Dark/Light Mode", font=('Segoe UI', 9), 
                 command=self.toggle_dark_mode, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="📜 History", font=('Segoe UI', 9), 
                 command=self.show_history, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="❓ Bantuan", font=('Segoe UI', 9), 
                 command=self.show_help, cursor="hand2").pack(side=tk.RIGHT, padx=5)

        # Main
        self.main = tk.Frame(self.root, bg=t["bg"])
        self.main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left: Keypad + Kalkulator Biasa
        left_frame = tk.Frame(self.main, bg=t["bg"], width=320)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10))
        left_frame.pack_propagate(False)

        self.build_keypad(left_frame)
        self.build_kalkulator_biasa(left_frame)

        # Right: Notebook
        right_frame = tk.Frame(self.main, bg=t["bg"])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tabs
        self.tab_rf = tk.Frame(self.notebook, bg=t["card"])
        self.notebook.add(self.tab_rf, text="  Regula Falsi  ")
        self.build_regula_falsi(self.tab_rf)

        self.tab_nr = tk.Frame(self.notebook, bg=t["card"])
        self.notebook.add(self.tab_nr, text=" Newton-Raphson ")
        self.build_newton_raphson(self.tab_nr)

        self.tab_iter = tk.Frame(self.notebook, bg=t["card"])
        self.notebook.add(self.tab_iter, text=" Iterasi ")
        self.build_iterasi(self.tab_iter)

        self.tab_comp = tk.Frame(self.notebook, bg=t["card"])
        self.notebook.add(self.tab_comp, text=" 🔥 Perbandingan ")
        self.build_perbandingan(self.tab_comp)

        self.tab_step = tk.Frame(self.notebook, bg=t["card"])
        self.notebook.add(self.tab_step, text=" ⏯️ Step-by-Step ")
        self.build_step_by_step(self.tab_step)

    # ========== KEYPAD ILMIAH ==========
    def build_keypad(self, parent):
        t = self.current_theme
        calc_frame = tk.LabelFrame(parent, text="Keypad Ilmiah", font=('Segoe UI', 11, 'bold'),
                                  bg=t["card"], fg=t["fg"], padx=8, pady=8)
        calc_frame.pack(fill=tk.X, pady=(0,10))

        self.display = tk.Entry(calc_frame, font=('Consolas', 14), justify='right',
                               bd=2, relief=tk.SUNKEN, bg=t["input"], fg=t["text"])
        self.display.grid(row=0, column=0, columnspan=5, sticky="ew", pady=(0,8), ipady=6)
        self.display.bind("<FocusIn>", lambda e: self.set_active(self.display))
        ToolTip(self.display, "Layar kalkulator. Klik tombol keypad lalu 'Masukkan ke Field Aktif'")

        buttons = [
            ('C', '#e74c3c'), ('⌫', '#e67e22'), ('(', '#95a5a6'), (')', '#95a5a6'), ('^', '#95a5a6'),
            ('7', '#34495e'), ('8', '#34495e'), ('9', '#34495e'), ('/', '#f39c12'), ('sqrt', '#95a5a6'),
            ('4', '#34495e'), ('5', '#34495e'), ('6', '#34495e'), ('*', '#f39c12'), ('x', '#1abc9c'),
            ('1', '#34495e'), ('2', '#34495e'), ('3', '#34495e'), ('-', '#f39c12'), ('y', '#1abc9c'),
            ('0', '#34495e'), ('.', '#34495e'), ('pi', '#1abc9c'), ('+', '#f39c12'), ('e', '#1abc9c'),
            ('sin', '#9b59b6'), ('cos', '#9b59b6'), ('tan', '#9b59b6'), ('ln', '#9b59b6'), ('log', '#9b59b6'),
        ]

        row, col = 1, 0
        for (text, bg) in buttons:
            btn = tk.Button(calc_frame, text=text, font=('Segoe UI', 10, 'bold'),
                           bg=bg, fg='white', width=5, height=1,
                           command=lambda t=text: self.on_calc_button(t),
                           cursor="hand2", relief=tk.RAISED, bd=2)
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
            if col > 4:
                col = 0
                row += 1

        tk.Button(calc_frame, text="⬇ Masukkan ke Field Aktif", font=('Segoe UI', 10, 'bold'),
                 bg="#27ae60", fg="white", command=self.insert_to_active,
                 cursor="hand2").grid(row=row, column=0, columnspan=5, sticky="ew", pady=(8,0), ipady=4)

    def on_calc_button(self, text):
        if text == 'C':
            self.display.delete(0, tk.END)
        elif text == '⌫':
            current = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(0, current[:-1])
        elif text in ('sin', 'cos', 'tan', 'ln', 'log', 'sqrt'):
            self.display.insert(tk.END, text + "(")
        elif text == '^':
            self.display.insert(tk.END, "**")
        elif text == 'pi':
            self.display.insert(tk.END, "pi")
        elif text == 'e':
            self.display.insert(tk.END, "E")
        else:
            self.display.insert(tk.END, text)

    def insert_to_active(self):
        if self.active_entry is None:
            messagebox.showwarning("Perhatian", "Klik field input yang ingin diisi terlebih dahulu!")
            return
        val = self.display.get()
        if val:
            self.active_entry.insert(tk.END, val)

    # ========== KALKULATOR BIASA (Fitur #8) ==========
    def build_kalkulator_biasa(self, parent):
        t = self.current_theme
        frame = tk.LabelFrame(parent, text="🧮 Kalkulator Cepat", font=('Segoe UI', 11, 'bold'),
                             bg=t["card"], fg=t["fg"], padx=8, pady=8)
        frame.pack(fill=tk.X)

        tk.Label(frame, text="Ekspresi:", font=('Segoe UI', 9), bg=t["card"], fg=t["text"]).pack(anchor="w")
        self.calc_expr = tk.Entry(frame, font=('Consolas', 11), bg=t["input"], fg=t["text"])
        self.calc_expr.pack(fill=tk.X, pady=3)
        self.calc_expr.bind("<FocusIn>", lambda e: self.set_active(self.calc_expr))
        ToolTip(self.calc_expr, "Masukkan ekspresi matematika, lalu tekan =")

        btn_frame = tk.Frame(frame, bg=t["card"])
        btn_frame.pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="= HITUNG", font=('Segoe UI', 10, 'bold'),
                 bg="#3498db", fg="white", command=self.eval_kalkulator,
                 cursor="hand2").pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(btn_frame, text="C", font=('Segoe UI', 10),
                 bg="#e74c3c", fg="white", command=lambda: self.calc_expr.delete(0,tk.END),
                 cursor="hand2").pack(side=tk.RIGHT, padx=(5,0))

        tk.Label(frame, text="Hasil:", font=('Segoe UI', 9), bg=t["card"], fg=t["text"]).pack(anchor="w")
        self.calc_hasil = tk.Entry(frame, font=('Consolas', 12, 'bold'), 
                                  bg="#d5f5e3", fg="#145a32", justify='center', state='readonly')
        self.calc_hasil.pack(fill=tk.X, pady=3)

    def eval_kalkulator(self):
        try:
            expr = self.calc_expr.get().replace('^', '**')
            result = sympify(expr, locals={'pi': pi, 'E': E, 'sin': sin, 'cos': cos, 
                                            'tan': tan, 'log': log, 'sqrt': sqrt, 'exp': exp})
            val = float(N(result))
            self.calc_hasil.config(state='normal')
            self.calc_hasil.delete(0, tk.END)
            self.calc_hasil.insert(0, str(val))
            self.calc_hasil.config(state='readonly')
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghitung:\n{e}")

    # ========== HELPERS ==========
    def set_active(self, entry_widget):
        self.active_entry = entry_widget

    def validate_expr(self, entry, label_widget):
        """Validasi real-time (Fitur #5)"""
        try:
            txt = entry.get().replace('^', '**')
            if txt.strip():
                sympify(txt, locals={'x': x, 'pi': pi, 'E': E, 'sin': sin, 'cos': cos, 
                                    'tan': tan, 'log': log, 'sqrt': sqrt, 'exp': exp})
                label_widget.config(text="✓ Valid", fg="#27ae60")
            else:
                label_widget.config(text="", fg="black")
        except:
            label_widget.config(text="✗ Invalid", fg="#e74c3c")

    def parse_function(self, expr_str):
        try:
            expr_str = expr_str.replace('^', '**')
            expr = sympify(expr_str, locals={'x': x, 'pi': pi, 'E': E, 
                                              'sin': sin, 'cos': cos, 'tan': tan,
                                              'log': log, 'ln': log, 'sqrt': sqrt,
                                              'exp': exp})
            f = lambdify(x, expr, modules=['math', 'sympy'])
            return f, expr
        except Exception as e:
            raise ValueError(f"Gagal memparse fungsi: {e}\nTips: Gunakan 'x', '**' untuk pangkat, contoh: x**3-x-2")

    def create_labeled_entry(self, parent, label, row, default="", width=30, validate_label=None):
        t = self.current_theme
        tk.Label(parent, text=label, font=('Segoe UI', 10), bg=t["card"], fg=t["text"], anchor="w").grid(row=row, column=0, sticky="w", pady=4)
        entry = tk.Entry(parent, font=('Consolas', 11), width=width, bd=2, relief=tk.SUNKEN,
                        bg=t["input"], fg=t["text"])
        entry.grid(row=row, column=1, sticky="ew", pady=4, padx=5)
        entry.insert(0, default)
        entry.bind("<FocusIn>", lambda e: self.set_active(entry))
        if validate_label:
            entry.bind("<KeyRelease>", lambda e: self.validate_expr(entry, validate_label))
        return entry

    def create_graph_area(self, parent, figsize=(6.5, 4.2)):
        t = self.current_theme
        fig = Figure(figsize=figsize, dpi=100, facecolor=t["card"])
        ax = fig.add_subplot(111)
        ax.set_facecolor(t["card"])
        ax.tick_params(colors=t["text"])
        ax.xaxis.label.set_color(t["text"])
        ax.yaxis.label.set_color(t["text"])
        ax.title.set_color(t["text"])
        ax.grid(True, alpha=0.3)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, parent)
        toolbar.update()

        return fig, ax, canvas

    def save_figure(self, fig, default_name="grafik.png"):
        try:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialfile=default_name,
                title="Simpan Grafik"
            )
            if filepath:
                fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
                messagebox.showinfo("Sukses", f"Grafik disimpan ke:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan grafik:\n{e}")

    def export_csv(self, data_dict, default_name="hasil.csv"):
        """Export data iterasi ke CSV (Fitur #1)"""
        try:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=default_name
            )
            if not filepath:
                return
            df = pd.DataFrame(data_dict)
            if filepath.endswith('.xlsx'):
                df.to_excel(filepath, index=False)
            else:
                df.to_csv(filepath, index=False)
            messagebox.showinfo("Sukses", f"Data disimpan ke:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal export:\n{e}")

    def export_pdf_report(self, method_name, func_str, result_text, fig):
        """Export PDF Report (Fitur #9)"""
        try:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile=f"laporan_{method_name.lower().replace(' ', '_')}.pdf"
            )
            if not filepath:
                return

            # Save figure to temp PNG
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                tmp_path = tmp.name
            fig.savefig(tmp_path, dpi=200, bbox_inches='tight', facecolor='white')

            c = pdfcanvas.Canvas(filepath, pagesize=A4)
            width, height = A4

            c.setFont("Helvetica-Bold", 16)
            c.drawString(2*cm, height - 2*cm, "LAPORAN METODE NUMERIK")
            c.setFont("Helvetica", 10)
            c.drawString(2*cm, height - 2.8*cm, f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            c.drawString(2*cm, height - 3.4*cm, f"Metode: {method_name}")
            c.drawString(2*cm, height - 4*cm, f"Fungsi: {func_str}")

            # Insert image
            c.drawImage(tmp_path, 2*cm, height - 16*cm, width=17*cm, height=10*cm, preserveAspectRatio=True)

            # Result text
            c.setFont("Courier", 8)
            text_obj = c.beginText(2*cm, height - 17*cm)
            for line in result_text.split('\n')[:40]:
                text_obj.textLine(line)
            c.drawText(text_obj)

            c.showPage()
            c.save()
            os.unlink(tmp_path)
            messagebox.showinfo("Sukses", f"PDF laporan disimpan ke:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuat PDF:\n{e}")

    def save_gif(self, frames, default_name="animasi.gif"):
        """Simpan frames jadi GIF animasi (Fitur #3)"""
        try:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".gif",
                filetypes=[("GIF files", "*.gif"), ("All files", "*.*")],
                initialfile=default_name
            )
            if not filepath or not frames:
                return
            images = [Image.open(f) for f in frames]
            images[0].save(filepath, save_all=True, append_images=images[1:], 
                        duration=800, loop=0)
            # Cleanup temp files
            for f in frames:
                os.unlink(f)
            messagebox.showinfo("Sukses", f"Animasi GIF disimpan ke:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuat GIF:\n{e}")

    def add_history(self, method, func, result, iter_count):
        """Tambah ke history (Fitur #4)"""
        self.history.append({
            "waktu": datetime.now().strftime("%H:%M:%S"),
            "metode": method,
            "fungsi": func,
            "akar": result,
            "iterasi": iter_count
        })

    def show_history(self):
        win = tk.Toplevel(self.root)
        win.title("Riwayat Perhitungan")
        win.geometry("600x400")
        text = scrolledtext.ScrolledText(win, font=('Consolas', 10), bg="white")
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        if not self.history:
            text.insert(tk.END, "Belum ada riwayat perhitungan.")
        else:
            text.insert(tk.END, f"{'Waktu':<10}{'Metode':<20}{'Akar':<20}{'Iter':<8}\n")
            text.insert(tk.END, "-"*60 + "\n")
            for h in self.history[-50:]:
                text.insert(tk.END, f"{h['waktu']:<10}{h['metode']:<20}{str(h['akar'])[:18]:<20}{h['iterasi']:<8}\n")

    def show_help(self):
        help_text = """PANDUAN PENGGUNAAN:

1. Keypad Ilmiah: Klik field input, tekan tombol keypad, lalu 'Masukkan ke Field Aktif'
2. Validasi Real-time: Field berubah hijau (valid) atau merah (invalid) saat mengetik
3. Preset Soal: Pilih dari dropdown untuk auto-fill contoh soal
4. Auto-Detect Bracket: Klik tombol 'Auto Cari a,b' untuk Regula Falsi
5. Step-by-Step: Mode iterasi per klik untuk belajar visual
6. Export: Simpan hasil ke PNG, CSV, Excel, PDF, atau GIF animasi
7. Dark Mode: Toggle tema gelap/terang di toolbar atas
8. Kalkulator Cepat: Hitung ekspresi matematika langsung tanpa metode numerik
"""
        messagebox.showinfo("Bantuan", help_text)

    def auto_detect_bracket(self, f, entry_a, entry_b):
        """Auto cari interval [a,b] yang f(a)*f(b)<0 (Fitur #10)"""
        try:
            # Scan dari -10 sampai 10 dengan step 0.5
            scan_points = np.arange(-10, 10.5, 0.5)
            vals = [f(p) for p in scan_points]
            for i in range(len(scan_points)-1):
                if vals[i] * vals[i+1] < 0:
                    entry_a.delete(0, tk.END)
                    entry_a.insert(0, str(scan_points[i]))
                    entry_b.delete(0, tk.END)
                    entry_b.insert(0, str(scan_points[i+1]))
                    messagebox.showinfo("Auto-Detect", 
                        f"Interval ditemukan:\na = {scan_points[i]}\nb = {scan_points[i+1]}\n"
                        f"f(a) = {vals[i]:.4f}\nf(b) = {vals[i+1]:.4f}")
                    return True
            messagebox.showwarning("Auto-Detect", "Tidak ditemukan interval dengan tanda berbeda di [-10, 10].\nCoba ubah fungsi.")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Auto-detect gagal: {e}")
            return False

    # ========== PRESET DROPDOWN HELPER ==========
    def build_preset(self, parent, row, callback):
        t = self.current_theme
        tk.Label(parent, text="Preset Soal:", font=('Segoe UI', 9), bg=t["card"], fg=t["text"]).grid(row=row, column=0, sticky="w", pady=4)
        presets = [
            "-- Pilih contoh soal --",
            "x^2 - 5 | RF:a=1,b=3 | NR:x0=2 | IT:g=(x+5/x)/2",
            "x^3 - x - 2 | RF:a=1,b=2 | NR:x0=2 | IT:g=(x+2)^(1/3)",
            "sin(x) - x/2 | RF:a=1,b=3 | NR:x0=2 | IT:g=2*sin(x)",
            "exp(x) - 3 | RF:a=0,b=2 | NR:x0=1 | IT:g=x-exp(x)+3+x",
            "x^2 - 7 | RF:a=2,b=3 | NR:x0=3 | IT:g=(x+7/x)/2",
        ]
        combo = ttk.Combobox(parent, values=presets, font=('Segoe UI', 9), width=45, state="readonly")
        combo.current(0)
        combo.grid(row=row, column=1, sticky="ew", pady=4, padx=5)
        combo.bind("<<ComboboxSelected>>", lambda e: callback(combo.get()))
        return combo

    # ========== REGULA FALSI ==========
    def build_regula_falsi(self, parent):
        t = self.current_theme
        container = tk.Frame(parent, bg=t["card"], padx=10, pady=10)
        container.pack(fill=tk.BOTH, expand=True)

        input_frame = tk.Frame(container, bg=t["card"])
        input_frame.pack(fill=tk.X, pady=(0,8))

        tk.Label(input_frame, text="Regula Falsi (False Position)", 
                font=('Segoe UI', 13, 'bold'), bg=t["card"], fg=t["fg"]).grid(row=0, column=0, columnspan=4, pady=(0,8), sticky="w")

        # Validasi labels
        self.rf_val = tk.Label(input_frame, text="", font=('Segoe UI', 8), bg=t["card"])
        self.rf_val.grid(row=1, column=2, sticky="w")
        self.rf_f = self.create_labeled_entry(input_frame, "f(x) =", 1, "x**2 - 5", validate_label=self.rf_val)
        ToolTip(self.rf_f, "Masukkan fungsi f(x). Contoh: x**3 - x - 2, sin(x), exp(x)-3")

        self.rf_a = self.create_labeled_entry(input_frame, "a =", 2, "1")
        ToolTip(self.rf_a, "Batas kiri interval. f(a) harus berbeda tanda dengan f(b)")
        self.rf_b = self.create_labeled_entry(input_frame, "b =", 3, "3")
        ToolTip(self.rf_b, "Batas kanan interval. f(b) harus berbeda tanda dengan f(a)")
        self.rf_tol = self.create_labeled_entry(input_frame, "Toleransi =", 4, "0.0001")
        self.rf_max = self.create_labeled_entry(input_frame, "Iterasi Maks =", 5, "50")

        # Preset
        def apply_preset(val):
            if "x^2 - 5" in val:
                self.rf_f.delete(0,tk.END); self.rf_f.insert(0,"x**2 - 5")
                self.rf_a.delete(0,tk.END); self.rf_a.insert(0,"1")
                self.rf_b.delete(0,tk.END); self.rf_b.insert(0,"3")
            elif "x^3 - x - 2" in val:
                self.rf_f.delete(0,tk.END); self.rf_f.insert(0,"x**3 - x - 2")
                self.rf_a.delete(0,tk.END); self.rf_a.insert(0,"1")
                self.rf_b.delete(0,tk.END); self.rf_b.insert(0,"2")
            elif "sin(x)" in val:
                self.rf_f.delete(0,tk.END); self.rf_f.insert(0,"sin(x) - x/2")
                self.rf_a.delete(0,tk.END); self.rf_a.insert(0,"1")
                self.rf_b.delete(0,tk.END); self.rf_b.insert(0,"3")
            elif "exp(x)" in val:
                self.rf_f.delete(0,tk.END); self.rf_f.insert(0,"exp(x) - 3")
                self.rf_a.delete(0,tk.END); self.rf_a.insert(0,"0")
                self.rf_b.delete(0,tk.END); self.rf_b.insert(0,"2")
            elif "x^2 - 7" in val:
                self.rf_f.delete(0,tk.END); self.rf_f.insert(0,"x**2 - 7")
                self.rf_a.delete(0,tk.END); self.rf_a.insert(0,"2")
                self.rf_b.delete(0,tk.END); self.rf_b.insert(0,"3")
        self.build_preset(input_frame, 6, apply_preset)

        # Buttons
        btn_frame = tk.Frame(input_frame, bg=t["card"])
        btn_frame.grid(row=7, column=0, columnspan=4, pady=8, sticky="ew")
        tk.Button(btn_frame, text="🔍 HITUNG", font=('Segoe UI', 10, 'bold'),
                 bg="#3498db", fg="white", command=self.hitung_regula_falsi,
                 cursor="hand2", relief=tk.RAISED, bd=3).pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        tk.Button(btn_frame, text="🎯 Auto Cari a,b", font=('Segoe UI', 10, 'bold'),
                 bg="#9b59b6", fg="white", command=self.auto_rf_bracket,
                 cursor="hand2", relief=tk.RAISED, bd=3).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8,0), ipady=4)
        tk.Button(btn_frame, text="💾 PNG", font=('Segoe UI', 10),
                 bg="#e67e22", fg="white", command=lambda: self.save_figure(self.rf_fig, "regula_falsi.png"),
                 cursor="hand2").pack(side=tk.LEFT, padx=(8,0), ipady=4)
        tk.Button(btn_frame, text="📊 CSV", font=('Segoe UI', 10),
                 bg="#27ae60", fg="white", command=self.export_rf_csv,
                 cursor="hand2").pack(side=tk.LEFT, padx=(8,0), ipady=4)
        tk.Button(btn_frame, text="📄 PDF", font=('Segoe UI', 10),
                 bg="#c0392b", fg="white", command=self.export_rf_pdf,
                 cursor="hand2").pack(side=tk.LEFT, padx=(8,0), ipady=4)

        bottom = tk.Frame(container, bg=t["card"])
        bottom.pack(fill=tk.BOTH, expand=True)

        graph_frame = tk.LabelFrame(bottom, text="Grafik", font=('Segoe UI', 10, 'bold'),
                                    bg=t["card"], fg=t["fg"])
        graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,4))
        self.rf_fig, self.rf_ax, self.rf_canvas = self.create_graph_area(graph_frame)

        text_frame = tk.LabelFrame(bottom, text="Hasil Iterasi", font=('Segoe UI', 10, 'bold'),
                                   bg=t["card"], fg=t["fg"])
        text_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(4,0))
        self.rf_hasil = scrolledtext.ScrolledText(text_frame, font=('Consolas', 9), 
                                                  height=12, width=38, bg=t["input"], fg=t["text"], wrap=tk.WORD)
        self.rf_hasil.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        input_frame.columnconfigure(1, weight=1)

        # Simpan data iterasi untuk export
        self.rf_iter_data = []
        self.rf_expr_str = ""

    def auto_rf_bracket(self):
        try:
            f, _ = self.parse_function(self.rf_f.get())
            self.auto_detect_bracket(f, self.rf_a, self.rf_b)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_rf_csv(self):
        if not self.rf_iter_data:
            messagebox.showwarning("Export", "Belum ada data. Hitung dulu!")
            return
        data = {
            "Iterasi": [d[0] for d in self.rf_iter_data],
            "a": [d[1] for d in self.rf_iter_data],
            "b": [d[2] for d in self.rf_iter_data],
            "c": [d[3] for d in self.rf_iter_data],
            "f(c)": [d[6] for d in self.rf_iter_data]
        }
        self.export_csv(data, "regula_falsi.csv")

    def export_rf_pdf(self):
        if not self.rf_iter_data:
            messagebox.showwarning("Export", "Belum ada data. Hitung dulu!")
            return
        self.export_pdf_report("Regula Falsi", self.rf_expr_str, self.rf_hasil.get(1.0, tk.END), self.rf_fig)

    def hitung_regula_falsi(self):
        try:
            f, expr = self.parse_function(self.rf_f.get())
            a = float(self.rf_a.get())
            b = float(self.rf_b.get())
            tol = float(self.rf_tol.get())
            max_iter = int(self.rf_max.get())

            fa, fb = f(a), f(b)
            if fa * fb > 0:
                messagebox.showerror("Error", 
                    f"f(a) dan f(b) harus berbeda tanda!\nf({a})={fa:.4f}, f({b})={fb:.4f}")
                return

            self.rf_hasil.delete(1.0, tk.END)
            self.rf_hasil.insert(tk.END, f"f(x) = {expr}\n\n")
            self.rf_hasil.insert(tk.END, f"{'Iter':<6}{'a':<13}{'b':<13}{'c':<13}{'f(c)':<15}{'Error':<12}\n")
            self.rf_hasil.insert(tk.END, "-"*70 + "\n")

            self.rf_iter_data = []
            self.rf_expr_str = str(expr)
            c_old = None
            for i in range(1, max_iter + 1):
                c = (a * fb - b * fa) / (fb - fa)
                fc = f(c)
                err = abs(c - c_old) if c_old is not None else float('inf')
                self.rf_iter_data.append((i, a, b, c, fa, fb, fc))

                self.rf_hasil.insert(tk.END, f"{i:<6}{a:<13.6f}{b:<13.6f}{c:<13.6f}{fc:<15.6e}{err:<12.6e}\n")

                if abs(fc) < tol or err < tol:
                    self.rf_hasil.insert(tk.END, f"\n✓ AKAR: x = {c:.12f}\n")
                    self.add_history("Regula Falsi", str(expr), c, i)
                    break

                if fa * fc < 0:
                    b, fb = c, fc
                else:
                    a, fa = c, fc
                c_old = c
            else:
                self.rf_hasil.insert(tk.END, "\n⚠ Tidak konvergen.\n")
                return

            self.plot_regula_falsi(f, expr, self.rf_iter_data)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def plot_regula_falsi(self, f, expr, iter_data):
        self.rf_ax.clear()
        t = self.current_theme
        self.rf_ax.set_facecolor(t["card"])
        self.rf_ax.tick_params(colors=t["text"])

        all_x = [d[3] for d in iter_data] + [d[1] for d in iter_data] + [d[2] for d in iter_data]
        x_min, x_max = min(all_x), max(all_x)
        margin = (x_max - x_min) * 0.5 if x_max != x_min else 1
        x_min -= margin; x_max += margin

        xs = np.linspace(x_min, x_max, 400)
        ys = [f(xi) for xi in xs]

        self.rf_ax.plot(xs, ys, 'b-', linewidth=2, label=f'f(x)={expr}')
        self.rf_ax.axhline(y=0, color='k', linewidth=0.8)

        if iter_data:
            i, a, b, c, fa, fb, fc = iter_data[-1]
            self.rf_ax.plot(a, fa, 'ro', markersize=8, label=f'a={a:.3f}')
            self.rf_ax.plot(b, fb, 'go', markersize=8, label=f'b={b:.3f}')
            self.rf_ax.plot(c, fc, 'mo', markersize=10, label=f'akar≈{c:.4f}')
            self.rf_ax.plot([a, b], [fa, fb], 'r--', alpha=0.6, linewidth=1.5, label='secant')
            self.rf_ax.plot([c, c], [0, fc], 'm:', alpha=0.7)

        self.rf_ax.set_xlabel('x', color=t["text"]); self.rf_ax.set_ylabel('f(x)', color=t["text"])
        self.rf_ax.set_title('Regula Falsi', color=t["text"], fontweight='bold')
        self.rf_ax.legend(loc='best', fontsize=8)
        self.rf_fig.tight_layout()
        self.rf_canvas.draw()

    # ========== NEWTON-RAPHSON ==========
    def build_newton_raphson(self, parent):
        t = self.current_theme
        container = tk.Frame(parent, bg=t["card"], padx=10, pady=10)
        container.pack(fill=tk.BOTH, expand=True)

        input_frame = tk.Frame(container, bg=t["card"])
        input_frame.pack(fill=tk.X, pady=(0,8))

        tk.Label(input_frame, text="Newton-Raphson Method", 
                font=('Segoe UI', 13, 'bold'), bg=t["card"], fg=t["fg"]).grid(row=0, column=0, columnspan=4, pady=(0,8), sticky="w")

        self.nr_val = tk.Label(input_frame, text="", font=('Segoe UI', 8), bg=t["card"])
        self.nr_val.grid(row=1, column=2, sticky="w")
        self.nr_f = self.create_labeled_entry(input_frame, "f(x) =", 1, "x**2 - 5", validate_label=self.nr_val)
        ToolTip(self.nr_f, "Masukkan f(x). Turunan f'(x) akan dihitung otomatis oleh SymPy")

        self.nr_x0 = self.create_labeled_entry(input_frame, "x₀ =", 2, "2")
        ToolTip(self.nr_x0, "Tebakan awal. Semakin dekat akar, semakin cepat konvergen")
        self.nr_tol = self.create_labeled_entry(input_frame, "Toleransi =", 3, "0.0001")
        self.nr_max = self.create_labeled_entry(input_frame, "Iterasi Maks =", 4, "50")

        tk.Label(input_frame, text="✓ f'(x) otomatis", font=('Segoe UI', 8, 'italic'), 
                bg=t["card"], fg="#27ae60").grid(row=5, column=0, columnspan=2, sticky="w")

        def apply_preset(val):
            if "x^2 - 5" in val:
                self.nr_f.delete(0,tk.END); self.nr_f.insert(0,"x**2 - 5")
                self.nr_x0.delete(0,tk.END); self.nr_x0.insert(0,"2")
            elif "x^3 - x - 2" in val:
                self.nr_f.delete(0,tk.END); self.nr_f.insert(0,"x**3 - x - 2")
                self.nr_x0.delete(0,tk.END); self.nr_x0.insert(0,"2")
            elif "sin(x)" in val:
                self.nr_f.delete(0,tk.END); self.nr_f.insert(0,"sin(x) - x/2")
                self.nr_x0.delete(0,tk.END); self.nr_x0.insert(0,"2")
            elif "exp(x)" in val:
                self.nr_f.delete(0,tk.END); self.nr_f.insert(0,"exp(x) - 3")
                self.nr_x0.delete(0,tk.END); self.nr_x0.insert(0,"1")
            elif "x^2 - 7" in val:
                self.nr_f.delete(0,tk.END); self.nr_f.insert(0,"x**2 - 7")
                self.nr_x0.delete(0,tk.END); self.nr_x0.insert(0,"3")
        self.build_preset(input_frame, 6, apply_preset)

        btn_frame = tk.Frame(input_frame, bg=t["card"])
        btn_frame.grid(row=7, column=0, columnspan=4, pady=8, sticky="ew")
        tk.Button(btn_frame, text="🔍 HITUNG", font=('Segoe UI', 10, 'bold'),
                 bg="#9b59b6", fg="white", command=self.hitung_newton_raphson,
                 cursor="hand2", relief=tk.RAISED, bd=3).pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        tk.Button(btn_frame, text="💾 PNG", font=('Segoe UI', 10),
                 bg="#e67e22", fg="white", command=lambda: self.save_figure(self.nr_fig, "newton_raphson.png"),
                 cursor="hand2").pack(side=tk.LEFT, padx=(8,0), ipady=4)
        tk.Button(btn_frame, text="📊 CSV", font=('Segoe UI', 10),
                 bg="#27ae60", fg="white", command=self.export_nr_csv,
                 cursor="hand2").pack(side=tk.LEFT, padx=(8,0), ipady=4)
        tk.Button(btn_frame, text="📄 PDF", font=('Segoe UI', 10),
                 bg="#c0392b", fg="white", command=self.export_nr_pdf,
                 cursor="hand2").pack(side=tk.LEFT, padx=(8,0), ipady=4)
        tk.Button(btn_frame, text="🎬 GIF", font=('Segoe UI', 10),
                 bg="#16a085", fg="white", command=self.export_nr_gif,
                 cursor="hand2").pack(side=tk.LEFT, padx=(8,0), ipady=4)

        bottom = tk.Frame(container, bg=t["card"])
        bottom.pack(fill=tk.BOTH, expand=True)

        graph_frame = tk.LabelFrame(bottom, text="Grafik", font=('Segoe UI', 10, 'bold'),
                                    bg=t["card"], fg=t["fg"])
        graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,4))
        self.nr_fig, self.nr_ax, self.nr_canvas = self.create_graph_area(graph_frame)

        text_frame = tk.LabelFrame(bottom, text="Hasil Iterasi", font=('Segoe UI', 10, 'bold'),
                                   bg=t["card"], fg=t["fg"])
        text_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(4,0))
        self.nr_hasil = scrolledtext.ScrolledText(text_frame, font=('Consolas', 9), 
                                                  height=12, width=38, bg=t["input"], fg=t["text"], wrap=tk.WORD)
        self.nr_hasil.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        input_frame.columnconfigure(1, weight=1)
        self.nr_iter_data = []
        self.nr_expr_str = ""
        self.nr_gif_frames = []

    def export_nr_csv(self):
        if not self.nr_iter_data:
            messagebox.showwarning("Export", "Belum ada data. Hitung dulu!"); return
        data = {"Iterasi": [d[0] for d in self.nr_iter_data], "x_i": [d[1] for d in self.nr_iter_data],
                "f(x_i)": [d[2] for d in self.nr_iter_data], "f'(x_i)": [d[3] for d in self.nr_iter_data],
                "x_next": [d[4] for d in self.nr_iter_data]}
        self.export_csv(data, "newton_raphson.csv")

    def export_nr_pdf(self):
        if not self.nr_iter_data:
            messagebox.showwarning("Export", "Belum ada data. Hitung dulu!"); return
        self.export_pdf_report("Newton-Raphson", self.nr_expr_str, self.nr_hasil.get(1.0, tk.END), self.nr_fig)

    def export_nr_gif(self):
        if not self.nr_gif_frames:
            messagebox.showwarning("Export", "Belum ada data. Hitung dulu!"); return
        self.save_gif(self.nr_gif_frames, "newton_raphson.gif")

    def hitung_newton_raphson(self):
        try:
            expr_str = self.nr_f.get().replace('^', '**')
            expr = sympify(expr_str, locals={'x': x, 'pi': pi, 'E': E, 
                                            'sin': sin, 'cos': cos, 'tan': tan,
                                            'log': log, 'ln': log, 'sqrt': sqrt, 'exp': exp})
            f = lambdify(x, expr, modules=['math', 'sympy'])
            df_expr = diff(expr, x)
            df = lambdify(x, df_expr, modules=['math', 'sympy'])

            x0 = float(self.nr_x0.get())
            tol = float(self.nr_tol.get())
            max_iter = int(self.nr_max.get())

            self.nr_hasil.delete(1.0, tk.END)
            self.nr_hasil.insert(tk.END, f"f(x) = {expr}\n")
            self.nr_hasil.insert(tk.END, f"f'(x) = {df_expr}\n\n")
            hdr = "{:<6}{:<15}{:<15}{:<15}{:<12}\n".format("Iter", "x_i", "f(x_i)", "f'(x_i)", "Error")
            self.nr_hasil.insert(tk.END, hdr)
            self.nr_hasil.insert(tk.END, "-"*70 + "\n")

            self.nr_iter_data = []
            self.nr_expr_str = str(expr)
            self.nr_gif_frames = []
            xi = x0

            for i in range(1, max_iter + 1):
                fxi = f(xi)
                dfxi = df(xi)
                if abs(dfxi) < 1e-15:
                    self.nr_hasil.insert(tk.END, f"\n⚠ Turunan nol di x={xi}. Gagal.\n"); return
                x_next = xi - fxi / dfxi
                err = abs(x_next - xi)
                self.nr_iter_data.append((i, xi, fxi, dfxi, x_next))

                self.nr_hasil.insert(tk.END, f"{i:<6}{xi:<15.8f}{fxi:<15.6e}{dfxi:<15.6e}{err:<12.6e}\n")

                # Simpan frame untuk GIF
                frame_file = self._save_nr_frame(f, df, expr, self.nr_iter_data, x_next, i)
                if frame_file:
                    self.nr_gif_frames.append(frame_file)

                if abs(fxi) < tol or err < tol:
                    self.nr_hasil.insert(tk.END, f"\n✓ AKAR: x = {x_next:.12f}\n")
                    self.add_history("Newton-Raphson", str(expr), x_next, i)
                    break
                xi = x_next
            else:
                self.nr_hasil.insert(tk.END, "\n⚠ Tidak konvergen.\n"); return

            self.plot_newton_raphson(f, df, expr, self.nr_iter_data, x_next)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _save_nr_frame(self, f, df, expr, iter_data, root_val, current_iter):
        """Simpan 1 frame untuk GIF animasi"""
        try:
            fig = Figure(figsize=(6, 4), dpi=80, facecolor='white')
            ax = fig.add_subplot(111)
            ax.set_facecolor('white')

            all_x = [d[1] for d in iter_data] + [d[4] for d in iter_data]
            x_min, x_max = min(all_x), max(all_x)
            margin = max(abs(x_min), abs(x_max)) * 0.5
            x_min -= margin; x_max += margin

            xs = np.linspace(x_min, x_max, 200)
            ys = [f(xi) for xi in xs]
            ax.plot(xs, ys, 'b-', linewidth=2)
            ax.axhline(y=0, color='k', linewidth=0.8)

            colors = plt.cm.viridis(np.linspace(0, 1, len(iter_data)))
            for idx, (ii, xi, fxi, dfxi, x_next) in enumerate(iter_data):
                ax.plot(xi, fxi, 'o', color=colors[idx], markersize=6)
                if ii <= current_iter:
                    x_tan = np.linspace(xi - 0.3*margin, xi + 0.3*margin, 30)
                    y_tan = [fxi + dfxi * (xt - xi) for xt in x_tan]
                    ax.plot(x_tan, y_tan, '--', color=colors[idx], alpha=0.5, linewidth=1)

            ax.plot(root_val, f(root_val), 'r*', markersize=12)
            ax.set_title(f'Newton-Raphson - Iterasi {current_iter}')
            fig.tight_layout()

            tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            fig.savefig(tmp.name, dpi=80, facecolor='white')
            plt.close(fig)
            return tmp.name
        except:
            return None

    def plot_newton_raphson(self, f, df, expr, iter_data, root_val):
        self.nr_ax.clear()
        t = self.current_theme
        self.nr_ax.set_facecolor(t["card"])
        self.nr_ax.tick_params(colors=t["text"])

        all_x = [d[1] for d in iter_data] + [d[4] for d in iter_data]
        x_min, x_max = min(all_x), max(all_x)
        margin = max(abs(x_min), abs(x_max)) * 0.5
        x_min -= margin; x_max += margin

        xs = np.linspace(x_min, x_max, 400)
        ys = [f(xi) for xi in xs]

        self.nr_ax.plot(xs, ys, 'b-', linewidth=2, label=f'f(x)={expr}')
        self.nr_ax.axhline(y=0, color='k', linewidth=0.8)

        colors = plt.cm.viridis(np.linspace(0, 1, len(iter_data)))
        for idx, (i, xi, fxi, dfxi, x_next) in enumerate(iter_data):
            self.nr_ax.plot(xi, fxi, 'o', color=colors[idx], markersize=8, 
                           label=f'x{i}={xi:.3f}' if i <= 3 else None)
            x_tan = np.linspace(xi - 0.3*margin, xi + 0.3*margin, 50)
            y_tan = [fxi + dfxi * (xt - xi) for xt in x_tan]
            self.nr_ax.plot(x_tan, y_tan, '--', color=colors[idx], alpha=0.5, linewidth=1.2)
            self.nr_ax.plot([x_next, x_next], [0, f(x_next)], ':', color=colors[idx], alpha=0.5)

        self.nr_ax.plot(root_val, f(root_val), 'r*', markersize=15, label=f'akar≈{root_val:.4f}')
        self.nr_ax.set_xlabel('x', color=t["text"]); self.nr_ax.set_ylabel('f(x)', color=t["text"])
        self.nr_ax.set_title('Newton-Raphson', color=t["text"], fontweight='bold')
        self.nr_ax.legend(loc='best', fontsize=8)
        self.nr_fig.tight_layout()
        self.nr_canvas.draw()

    # ========== ITERASI (FIXED-POINT) ==========
    def build_iterasi(self, parent):
        t = self.current_theme
        container = tk.Frame(parent, bg=t["card"], padx=10, pady=10)
        container.pack(fill=tk.BOTH, expand=True)

        input_frame = tk.Frame(container, bg=t["card"])
        input_frame.pack(fill=tk.X, pady=(0,8))

        tk.Label(input_frame, text="Iterasi Titik Tetap (Fixed-Point)", 
                font=('Segoe UI', 13, 'bold'), bg=t["card"], fg=t["fg"]).grid(row=0, column=0, columnspan=4, pady=(0,8), sticky="w")

        tk.Label(input_frame, text="Susun f(x)=0 menjadi x = g(x)", 
                font=('Segoe UI', 9, 'italic'), bg=t["card"], fg="#e74c3c").grid(row=1, column=0, columnspan=2, sticky="w")

        self.it_val = tk.Label(input_frame, text="", font=('Segoe UI', 8), bg=t["card"])
        self.it_val.grid(row=2, column=2, sticky="w")
        self.it_g = self.create_labeled_entry(input_frame, "g(x) =", 2, "(x + 5/x) / 2", validate_label=self.it_val)
        ToolTip(self.it_g, "Masukkan g(x) dari bentuk x = g(x). Contoh: (x+5/x)/2 untuk akar sqrt(5)")

        self.it_x0 = self.create_labeled_entry(input_frame, "x₀ =", 3, "2")
        self.it_tol = self.create_labeled_entry(input_frame, "Toleransi =", 4, "0.0001")
        self.it_max = self.create_labeled_entry(input_frame, "Iterasi Maks =", 5, "50")

        def apply_preset(val):
            if "x^2 - 5" in val:
                self.it_g.delete(0,tk.END); self.it_g.insert(0,"(x + 5/x) / 2")
                self.it_x0.delete(0,tk.END); self.it_x0.insert(0,"2")
            elif "x^3 - x - 2" in val:
                self.it_g.delete(0,tk.END); self.it_g.insert(0,"(x + 2)**(1/3)")
                self.it_x0.delete(0,tk.END); self.it_x0.insert(0,"2")
            elif "sin(x)" in val:
                self.it_g.delete(0,tk.END); self.it_g.insert(0,"2*sin(x)")
                self.it_x0.delete(0,tk.END); self.it_x0.insert(0,"2")
            elif "exp(x)" in val:
                self.it_g.delete(0,tk.END); self.it_g.insert(0,"x - (exp(x) - 3) * exp(-x)")
                self.it_x0.delete(0,tk.END); self.it_x0.insert(0,"1")
            elif "x^2 - 7" in val:
                self.it_g.delete(0,tk.END); self.it_g.insert(0,"(x + 7/x) / 2")
                self.it_x0.delete(0,tk.END); self.it_x0.insert(0,"3")
        self.build_preset(input_frame, 6, apply_preset)

        btn_frame = tk.Frame(input_frame, bg=t["card"])
        btn_frame.grid(row=7, column=0, columnspan=4, pady=8, sticky="ew")
        tk.Button(btn_frame, text="🔍 HITUNG", font=('Segoe UI', 10, 'bold'),
                 bg="#27ae60", fg="white", command=self.hitung_iterasi,
                 cursor="hand2", relief=tk.RAISED, bd=3).pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        tk.Button(btn_frame, text="💾 PNG", font=('Segoe UI', 10),
                 bg="#e67e22", fg="white", command=lambda: self.save_figure(self.it_fig, "iterasi.png"),
                 cursor="hand2").pack(side=tk.LEFT, padx=(8,0), ipady=4)
        tk.Button(btn_frame, text="📊 CSV", font=('Segoe UI', 10),
                 bg="#27ae60", fg="white", command=self.export_it_csv,
                 cursor="hand2").pack(side=tk.LEFT, padx=(8,0), ipady=4)
        tk.Button(btn_frame, text="📄 PDF", font=('Segoe UI', 10),
                 bg="#c0392b", fg="white", command=self.export_it_pdf,
                 cursor="hand2").pack(side=tk.LEFT, padx=(8,0), ipady=4)
        tk.Button(btn_frame, text="🎬 GIF", font=('Segoe UI', 10),
                 bg="#16a085", fg="white", command=self.export_it_gif,
                 cursor="hand2").pack(side=tk.LEFT, padx=(8,0), ipady=4)

        bottom = tk.Frame(container, bg=t["card"])
        bottom.pack(fill=tk.BOTH, expand=True)

        graph_frame = tk.LabelFrame(bottom, text="Grafik", font=('Segoe UI', 10, 'bold'),
                                    bg=t["card"], fg=t["fg"])
        graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,4))
        self.it_fig, self.it_ax, self.it_canvas = self.create_graph_area(graph_frame)

        text_frame = tk.LabelFrame(bottom, text="Hasil Iterasi", font=('Segoe UI', 10, 'bold'),
                                   bg=t["card"], fg=t["fg"])
        text_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(4,0))
        self.it_hasil = scrolledtext.ScrolledText(text_frame, font=('Consolas', 9), 
                                                  height=12, width=38, bg=t["input"], fg=t["text"], wrap=tk.WORD)
        self.it_hasil.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        input_frame.columnconfigure(1, weight=1)
        self.it_iter_data = []
        self.it_expr_str = ""
        self.it_gif_frames = []

    def export_it_csv(self):
        if not self.it_iter_data:
            messagebox.showwarning("Export", "Belum ada data. Hitung dulu!"); return
        data = {"Iterasi": [d[0] for d in self.it_iter_data], "x_i": [d[1] for d in self.it_iter_data],
                "g(x_i)": [d[2] for d in self.it_iter_data]}
        self.export_csv(data, "iterasi.csv")

    def export_it_pdf(self):
        if not self.it_iter_data:
            messagebox.showwarning("Export", "Belum ada data. Hitung dulu!"); return
        self.export_pdf_report("Iterasi Titik Tetap", self.it_expr_str, self.it_hasil.get(1.0, tk.END), self.it_fig)

    def export_it_gif(self):
        if not self.it_gif_frames:
            messagebox.showwarning("Export", "Belum ada data. Hitung dulu!"); return
        self.save_gif(self.it_gif_frames, "iterasi.gif")

    def hitung_iterasi(self):
        try:
            g, expr = self.parse_function(self.it_g.get())
            x0 = float(self.it_x0.get())
            tol = float(self.it_tol.get())
            max_iter = int(self.it_max.get())

            self.it_hasil.delete(1.0, tk.END)
            self.it_hasil.insert(tk.END, f"g(x) = {expr}\n\n")
            self.it_hasil.insert(tk.END, f"{'Iter':<6}{'x_i':<15}{'g(x_i)':<15}{'Error':<15}\n")
            self.it_hasil.insert(tk.END, "-"*55 + "\n")

            self.it_iter_data = []
            self.it_expr_str = str(expr)
            self.it_gif_frames = []
            xi = x0
            self.it_hasil.insert(tk.END, f"{0:<6}{xi:<15.8f}{'-':<15}{'-':<15}\n")

            for i in range(1, max_iter + 1):
                x_next = g(xi)
                err = abs(x_next - xi)
                self.it_iter_data.append((i, xi, x_next))

                self.it_hasil.insert(tk.END, f"{i:<6}{xi:<15.8f}{x_next:<15.8f}{err:<15.8e}\n")

                # Frame untuk GIF
                frame_file = self._save_it_frame(g, expr, self.it_iter_data, x_next, i)
                if frame_file:
                    self.it_gif_frames.append(frame_file)

                if err < tol:
                    self.it_hasil.insert(tk.END, f"\n✓ AKAR: x = {x_next:.12f}\n")
                    self.add_history("Iterasi", str(expr), x_next, i)
                    break
                xi = x_next
            else:
                self.it_hasil.insert(tk.END, "\n⚠ Tidak konvergen.\n"); return

            self.plot_iterasi(g, expr, self.it_iter_data, x_next)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _save_it_frame(self, g, expr, iter_data, root_val, current_iter):
        try:
            fig = Figure(figsize=(6, 4), dpi=80, facecolor='white')
            ax = fig.add_subplot(111)
            ax.set_facecolor('white')

            all_x = [d[1] for d in iter_data] + [d[2] for d in iter_data]
            x_min, x_max = min(all_x), max(all_x)
            margin = (x_max - x_min) * 0.3 if x_max != x_min else 1
            x_min -= margin; x_max += margin

            xs = np.linspace(x_min, x_max, 200)
            ys_g = [g(xi) for xi in xs]
            ax.plot(xs, ys_g, 'b-', linewidth=2)
            ax.plot(xs, xs, 'k--', linewidth=1.5, alpha=0.7)

            colors = plt.cm.plasma(np.linspace(0, 1, len(iter_data)))
            for idx, (ii, xi, x_next) in enumerate(iter_data):
                if ii <= current_iter:
                    ax.plot([xi, xi], [xi, x_next], '-', color=colors[idx], alpha=0.6, linewidth=1.5)
                    ax.plot([xi, x_next], [x_next, x_next], '-', color=colors[idx], alpha=0.6, linewidth=1.5)

            ax.plot(root_val, root_val, 'r*', markersize=12)
            ax.set_title(f'Iterasi - Iterasi {current_iter}')
            fig.tight_layout()

            tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            fig.savefig(tmp.name, dpi=80, facecolor='white')
            plt.close(fig)
            return tmp.name
        except:
            return None

    def plot_iterasi(self, g, expr, iter_data, root_val):
        self.it_ax.clear()
        t = self.current_theme
        self.it_ax.set_facecolor(t["card"])
        self.it_ax.tick_params(colors=t["text"])

        all_x = [d[1] for d in iter_data] + [d[2] for d in iter_data]
        x_min, x_max = min(all_x), max(all_x)
        margin = (x_max - x_min) * 0.3 if x_max != x_min else 1
        x_min -= margin; x_max += margin

        xs = np.linspace(x_min, x_max, 400)
        ys_g = [g(xi) for xi in xs]

        self.it_ax.plot(xs, ys_g, 'b-', linewidth=2, label=f'g(x)={expr}')
        self.it_ax.plot(xs, xs, 'k--', linewidth=1.5, alpha=0.7, label='y=x')
        self.it_ax.axhline(y=0, color='k', linewidth=0.5)
        self.it_ax.axvline(x=0, color='k', linewidth=0.5)

        colors = plt.cm.plasma(np.linspace(0, 1, len(iter_data)))
        for idx, (i, xi, x_next) in enumerate(iter_data):
            self.it_ax.plot([xi, xi], [xi, x_next], '-', color=colors[idx], alpha=0.6, linewidth=1.5)
            self.it_ax.plot([xi, x_next], [x_next, x_next], '-', color=colors[idx], alpha=0.6, linewidth=1.5)
            self.it_ax.plot(xi, xi, 'o', color=colors[idx], markersize=6)
            self.it_ax.plot(xi, x_next, 's', color=colors[idx], markersize=6)

        self.it_ax.plot(root_val, root_val, 'r*', markersize=15, label=f'akar≈{root_val:.4f}')
        self.it_ax.set_xlabel('x', color=t["text"]); self.it_ax.set_ylabel('y', color=t["text"])
        self.it_ax.set_title('Iterasi Titik Tetap', color=t["text"], fontweight='bold')
        self.it_ax.legend(loc='best', fontsize=8)
        self.it_fig.tight_layout()
        self.it_canvas.draw()

    # ========== PERBANDINGAN 3 METODE + GRAFIK ERROR (Fitur #7) ==========
    def build_perbandingan(self, parent):
        t = self.current_theme
        container = tk.Frame(parent, bg=t["card"], padx=10, pady=10)
        container.pack(fill=tk.BOTH, expand=True)

        input_frame = tk.Frame(container, bg=t["card"])
        input_frame.pack(fill=tk.X, pady=(0,8))

        tk.Label(input_frame, text="🔥 Perbandingan 3 Metode Sekaligus", 
                font=('Segoe UI', 14, 'bold'), bg=t["card"], fg="#c0392b").grid(row=0, column=0, columnspan=4, pady=(0,8), sticky="w")

        tk.Label(input_frame, text="Masukkan f(x) dan parameter, ketiga metode akan dijalankan & dibandingkan.", 
                font=('Segoe UI', 9, 'italic'), bg=t["card"], fg=t["text"]).grid(row=1, column=0, columnspan=4, sticky="w", pady=(0,8))

        self.comp_f = self.create_labeled_entry(input_frame, "f(x) =", 2, "x**2 - 5")
        self.comp_a = self.create_labeled_entry(input_frame, "RF: a =", 3, "1")
        self.comp_b = self.create_labeled_entry(input_frame, "RF: b =", 4, "3")
        self.comp_x0 = self.create_labeled_entry(input_frame, "NR & IT: x₀ =", 5, "2")
        self.comp_tol = self.create_labeled_entry(input_frame, "Toleransi =", 6, "0.0001")
        self.comp_max = self.create_labeled_entry(input_frame, "Iterasi Maks =", 7, "50")
        self.comp_g = self.create_labeled_entry(input_frame, "IT: g(x) =", 8, "(x + 5/x) / 2")

        btn_frame = tk.Frame(input_frame, bg=t["card"])
        btn_frame.grid(row=9, column=0, columnspan=4, pady=8, sticky="ew")
        tk.Button(btn_frame, text="🔥 BANDINGKAN 3 METODE", font=('Segoe UI', 12, 'bold'),
                 bg="#c0392b", fg="white", command=self.hitung_perbandingan,
                 cursor="hand2", relief=tk.RAISED, bd=3).pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        tk.Button(btn_frame, text="💾 PNG", font=('Segoe UI', 10),
                 bg="#e67e22", fg="white", command=lambda: self.save_figure(self.comp_fig, "perbandingan.png"),
                 cursor="hand2").pack(side=tk.LEFT, padx=(10,0), ipady=4)
        tk.Button(btn_frame, text="📄 PDF", font=('Segoe UI', 10),
                 bg="#c0392b", fg="white", command=self.export_comp_pdf,
                 cursor="hand2").pack(side=tk.LEFT, padx=(10,0), ipady=4)

        bottom = tk.Frame(container, bg=t["card"])
        bottom.pack(fill=tk.BOTH, expand=True)

        # Grafik perbandingan akar
        graph_frame = tk.LabelFrame(bottom, text="Grafik Perbandingan Akar", font=('Segoe UI', 10, 'bold'),
                                    bg=t["card"], fg=t["fg"])
        graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,4))
        self.comp_fig, self.comp_ax, self.comp_canvas = self.create_graph_area(graph_frame, figsize=(6.5, 4))

        # Panel kanan: hasil teks + grafik error
        right_panel = tk.Frame(bottom, bg=t["card"])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(4,0))

        text_frame = tk.LabelFrame(right_panel, text="Ringkasan", font=('Segoe UI', 10, 'bold'),
                                   bg=t["card"], fg=t["fg"])
        text_frame.pack(fill=tk.BOTH, expand=True)
        self.comp_hasil = scrolledtext.ScrolledText(text_frame, font=('Consolas', 9), 
                                                  height=8, width=40, bg=t["input"], fg=t["text"], wrap=tk.WORD)
        self.comp_hasil.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Grafik error vs iterasi
        err_frame = tk.LabelFrame(right_panel, text="Grafik Error vs Iterasi", font=('Segoe UI', 10, 'bold'),
                                  bg=t["card"], fg=t["fg"])
        err_frame.pack(fill=tk.BOTH, expand=True, pady=(4,0))
        self.err_fig, self.err_ax, self.err_canvas = self.create_graph_area(err_frame, figsize=(6, 3.5))

        input_frame.columnconfigure(1, weight=1)
        self.comp_data = {}

    def export_comp_pdf(self):
        if not self.comp_data:
            messagebox.showwarning("Export", "Belum ada data. Hitung dulu!"); return
        text = self.comp_hasil.get(1.0, tk.END)
        self.export_pdf_report("Perbandingan 3 Metode", self.comp_data.get("func",""), text, self.comp_fig)

    def hitung_perbandingan(self):
        try:
            expr_str = self.comp_f.get().replace('^', '**')
            expr = sympify(expr_str, locals={'x': x, 'pi': pi, 'E': E, 
                                            'sin': sin, 'cos': cos, 'tan': tan,
                                            'log': log, 'ln': log, 'sqrt': sqrt, 'exp': exp})
            f = lambdify(x, expr, modules=['math', 'sympy'])
            df_expr = diff(expr, x)
            df = lambdify(x, df_expr, modules=['math', 'sympy'])

            a = float(self.comp_a.get())
            b = float(self.comp_b.get())
            x0 = float(self.comp_x0.get())
            tol = float(self.comp_tol.get())
            max_iter = int(self.comp_max.get())

            g_expr_str = self.comp_g.get().replace('^', '**')
            g_expr = sympify(g_expr_str, locals={'x': x, 'pi': pi, 'E': E, 
                                                  'sin': sin, 'cos': cos, 'tan': tan,
                                                  'log': log, 'ln': log, 'sqrt': sqrt, 'exp': exp})
            g = lambdify(x, g_expr, modules=['math', 'sympy'])

            self.comp_hasil.delete(1.0, tk.END)
            self.comp_hasil.insert(tk.END, f"f(x) = {expr}\n")
            self.comp_hasil.insert(tk.END, f"g(x) = {g_expr}\n\n")

            # --- REGULA FALSI ---
            fa, fb = f(a), f(b)
            rf_root, rf_iter, rf_errors = None, 0, []
            if fa * fb <= 0:
                aa, bb, faa, fbb = a, b, fa, fb
                c_old = None
                for i in range(1, max_iter + 1):
                    c = (aa * fbb - bb * faa) / (fbb - faa)
                    fc = f(c)
                    err = abs(c - c_old) if c_old is not None else float('inf')
                    rf_errors.append(err if err != float('inf') else abs(fc))
                    rf_iter = i
                    if abs(fc) < tol or err < tol:
                        rf_root = c; break
                    if faa * fc < 0:
                        bb, fbb = c, fc
                    else:
                        aa, faa = c, fc
                    c_old = c
                else:
                    rf_root = c

            # --- NEWTON-RAPHSON ---
            nr_root, nr_iter, nr_errors = None, 0, []
            xi = x0
            for i in range(1, max_iter + 1):
                fxi = f(xi)
                dfxi = df(xi)
                if abs(dfxi) < 1e-15: break
                x_next = xi - fxi / dfxi
                err = abs(x_next - xi)
                nr_errors.append(err)
                nr_iter = i
                if abs(fxi) < tol or err < tol:
                    nr_root = x_next; break
                xi = x_next
            else:
                nr_root = xi

            # --- ITERASI ---
            it_root, it_iter, it_errors = None, 0, []
            xi = x0
            for i in range(1, max_iter + 1):
                x_next = g(xi)
                err = abs(x_next - xi)
                it_errors.append(err)
                it_iter = i
                if err < tol:
                    it_root = x_next; break
                xi = x_next
            else:
                it_root = xi

            # Tampilkan ringkasan
            self.comp_hasil.insert(tk.END, "="*58 + "\n")
            self.comp_hasil.insert(tk.END, "RINGKASAN PERBANDINGAN\n")
            self.comp_hasil.insert(tk.END, "="*58 + "\n\n")
            self.comp_hasil.insert(tk.END, f"{'Metode':<25}{'Akar':<20}{'Iterasi':<10}{'Status':<10}\n")
            self.comp_hasil.insert(tk.END, "-"*58 + "\n")

            status = lambda r: "✓" if r is not None else "✗"
            self.comp_hasil.insert(tk.END, f"{'Regula Falsi':<25}{str(rf_root)[:18]:<20}{rf_iter:<10}{status(rf_root):<10}\n")
            self.comp_hasil.insert(tk.END, f"{'Newton-Raphson':<25}{str(nr_root)[:18]:<20}{nr_iter:<10}{status(nr_root):<10}\n")
            self.comp_hasil.insert(tk.END, f"{'Iterasi Titik Tetap':<25}{str(it_root)[:18]:<20}{it_iter:<10}{status(it_root):<10}\n")
            self.comp_hasil.insert(tk.END, "\n" + "="*58 + "\n")
            self.comp_hasil.insert(tk.END, "Iterasi terkecil = metode tercepat\n")
            self.comp_hasil.insert(tk.END, "="*58 + "\n")

            self.comp_data = {"func": str(expr), "rf": rf_root, "nr": nr_root, "it": it_root}

            # Plot
            self.plot_perbandingan(f, expr, rf_root, nr_root, it_root, a, b, x0)
            self.plot_error_graph(rf_errors, nr_errors, it_errors)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def plot_perbandingan(self, f, expr, rf_root, nr_root, it_root, a, b, x0):
        self.comp_ax.clear()
        t = self.current_theme
        self.comp_ax.set_facecolor(t["card"])
        self.comp_ax.tick_params(colors=t["text"])

        roots = [r for r in [rf_root, nr_root, it_root] if r is not None]
        if roots:
            center = sum(roots) / len(roots)
            margin = max(abs(r - center) for r in roots) * 2 + 1
            x_min, x_max = center - margin, center + margin
        else:
            x_min, x_max = min(a, b, x0) - 2, max(a, b, x0) + 2

        xs = np.linspace(x_min, x_max, 400)
        ys = [f(xi) for xi in xs]

        self.comp_ax.plot(xs, ys, 'b-', linewidth=2, label=f'f(x)={expr}')
        self.comp_ax.axhline(y=0, color='k', linewidth=0.8)

        if rf_root is not None:
            self.comp_ax.plot(rf_root, f(rf_root), 'ro', markersize=12, label=f'RF: {rf_root:.6f}')
        if nr_root is not None:
            self.comp_ax.plot(nr_root, f(nr_root), 'gs', markersize=12, label=f'NR: {nr_root:.6f}')
        if it_root is not None:
            self.comp_ax.plot(it_root, f(it_root), 'm^', markersize=12, label=f'IT: {it_root:.6f}')

        self.comp_ax.set_xlabel('x', color=t["text"]); self.comp_ax.set_ylabel('f(x)', color=t["text"])
        self.comp_ax.set_title('Perbandingan 3 Metode', color=t["text"], fontweight='bold')
        self.comp_ax.legend(loc='best', fontsize=9)
        self.comp_fig.tight_layout()
        self.comp_canvas.draw()

    def plot_error_graph(self, rf_err, nr_err, it_err):
        """Grafik error vs iterasi (Fitur #7)"""
        self.err_ax.clear()
        t = self.current_theme
        self.err_ax.set_facecolor(t["card"])
        self.err_ax.tick_params(colors=t["text"])

        if rf_err:
            self.err_ax.semilogy(range(1, len(rf_err)+1), rf_err, 'ro-', label='Regula Falsi', linewidth=1.5, markersize=5)
        if nr_err:
            self.err_ax.semilogy(range(1, len(nr_err)+1), nr_err, 'gs-', label='Newton-Raphson', linewidth=1.5, markersize=5)
        if it_err:
            self.err_ax.semilogy(range(1, len(it_err)+1), it_err, 'm^-', label='Iterasi', linewidth=1.5, markersize=5)

        self.err_ax.set_xlabel('Iterasi', color=t["text"])
        self.err_ax.set_ylabel('Error (log scale)', color=t["text"])
        self.err_ax.set_title('Konvergensi: Error vs Iterasi', color=t["text"], fontweight='bold')
        self.err_ax.legend(loc='best', fontsize=9)
        self.err_ax.grid(True, alpha=0.3)
        self.err_fig.tight_layout()
        self.err_canvas.draw()

    # ========== STEP-BY-STEP MODE (Fitur #11) ==========
    def build_step_by_step(self, parent):
        t = self.current_theme
        container = tk.Frame(parent, bg=t["card"], padx=10, pady=10)
        container.pack(fill=tk.BOTH, expand=True)

        tk.Label(container, text="⏯️ Mode Step-by-Step (Belajar Iterasi per Klik)", 
                font=('Segoe UI', 14, 'bold'), bg=t["card"], fg="#16a085").pack(anchor="w", pady=(0,8))

        info = tk.Label(container, text="Jalankan 1 iterasi per klik untuk melihat perubahan secara bertahap.", 
                       font=('Segoe UI', 9, 'italic'), bg=t["card"], fg=t["text"])
        info.pack(anchor="w", pady=(0,10))

        input_frame = tk.Frame(container, bg=t["card"])
        input_frame.pack(fill=tk.X, pady=(0,8))

        tk.Label(input_frame, text="Metode:", font=('Segoe UI', 10), bg=t["card"], fg=t["text"]).grid(row=0, column=0, sticky="w")
        self.step_method_var = tk.StringVar(value="Newton-Raphson")
        ttk.Combobox(input_frame, textvariable=self.step_method_var, 
                    values=["Regula Falsi", "Newton-Raphson", "Iterasi"], 
                    font=('Segoe UI', 10), width=20, state="readonly").grid(row=0, column=1, sticky="w", padx=5)

        self.step_f = self.create_labeled_entry(input_frame, "f(x) / g(x) =", 1, "x**2 - 5")
        self.step_x0 = self.create_labeled_entry(input_frame, "x₀ / a =", 2, "2")
        self.step_b = self.create_labeled_entry(input_frame, "b (khusus RF) =", 3, "3")
        self.step_tol = self.create_labeled_entry(input_frame, "Toleransi =", 4, "0.0001")

        btn_frame = tk.Frame(input_frame, bg=t["card"])
        btn_frame.grid(row=5, column=0, columnspan=4, pady=8, sticky="ew")
        tk.Button(btn_frame, text="▶️ START", font=('Segoe UI', 11, 'bold'),
                 bg="#27ae60", fg="white", command=self.step_start,
                 cursor="hand2", relief=tk.RAISED, bd=3).pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        tk.Button(btn_frame, text="⏭️ NEXT ITERASI", font=('Segoe UI', 11, 'bold'),
                 bg="#3498db", fg="white", command=self.step_next,
                 cursor="hand2", relief=tk.RAISED, bd=3).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8,0), ipady=4)
        tk.Button(btn_frame, text="🔄 RESET", font=('Segoe UI', 11, 'bold'),
                 bg="#e74c3c", fg="white", command=self.step_reset,
                 cursor="hand2", relief=tk.RAISED, bd=3).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8,0), ipady=4)

        bottom = tk.Frame(container, bg=t["card"])
        bottom.pack(fill=tk.BOTH, expand=True)

        graph_frame = tk.LabelFrame(bottom, text="Grafik Step-by-Step", font=('Segoe UI', 10, 'bold'),
                                    bg=t["card"], fg=t["fg"])
        graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,4))
        self.step_fig, self.step_ax, self.step_canvas = self.create_graph_area(graph_frame, figsize=(7, 4.5))

        text_frame = tk.LabelFrame(bottom, text="Log Iterasi", font=('Segoe UI', 10, 'bold'),
                                   bg=t["card"], fg=t["fg"])
        text_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(4,0))
        self.step_log = scrolledtext.ScrolledText(text_frame, font=('Consolas', 9), 
                                                  height=12, width=38, bg=t["input"], fg=t["text"], wrap=tk.WORD)
        self.step_log.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        input_frame.columnconfigure(1, weight=1)

    def step_start(self):
        try:
            method = self.step_method_var.get()
            expr_str = self.step_f.get().replace('^', '**')
            expr = sympify(expr_str, locals={'x': x, 'pi': pi, 'E': E, 
                                            'sin': sin, 'cos': cos, 'tan': tan,
                                            'log': log, 'ln': log, 'sqrt': sqrt, 'exp': exp})
            f = lambdify(x, expr, modules=['math', 'sympy'])

            self.step_data = {
                "method": method,
                "f": f,
                "expr": expr,
                "tol": float(self.step_tol.get()),
                "max_iter": 100,
                "index": 0,
                "iter_data": []
            }

            if method == "Regula Falsi":
                a = float(self.step_x0.get())
                b = float(self.step_b.get())
                fa, fb = f(a), f(b)
                if fa * fb > 0:
                    messagebox.showerror("Error", "f(a) dan f(b) harus beda tanda!"); return
                self.step_data.update({"a": a, "b": b, "fa": fa, "fb": fb, "c_old": None})
            elif method == "Newton-Raphson":
                df = lambdify(x, diff(expr, x), modules=['math', 'sympy'])
                self.step_data.update({"x": float(self.step_x0.get()), "df": df})
            else:  # Iterasi
                g_expr = sympify(self.step_f.get().replace('^','**'), locals={'x':x, 'pi':pi, 'E':E, 'sin':sin, 'cos':cos, 'tan':tan, 'log':log, 'sqrt':sqrt, 'exp':exp})
                g = lambdify(x, g_expr, modules=['math', 'sympy'])
                self.step_data.update({"x": float(self.step_x0.get()), "g": g, "g_expr": g_expr})

            self.step_log.delete(1.0, tk.END)
            self.step_log.insert(tk.END, f"METODE: {method}\n")
            self.step_log.insert(tk.END, f"f(x) = {expr}\n\n")
            self.step_log.insert(tk.END, "Tekan 'NEXT ITERASI' untuk mulai.\n")
            self.step_index = 0
            self.step_plot_init()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def step_plot_init(self):
        self.step_ax.clear()
        t = self.current_theme
        self.step_ax.set_facecolor(t["card"])
        self.step_ax.tick_params(colors=t["text"])
        self.step_ax.text(0.5, 0.5, "Tekan 'NEXT ITERASI'", ha='center', va='center', 
                         transform=self.step_ax.transAxes, fontsize=14, color=t["text"])
        self.step_fig.tight_layout()
        self.step_canvas.draw()

    def step_next(self):
        if not self.step_data:
            messagebox.showwarning("Step", "Tekan 'START' dulu!"); return

        d = self.step_data
        if self.step_index >= d["max_iter"]:
            self.step_log.insert(tk.END, f"\n⚠ Batas iterasi maksimum ({d['max_iter']}) tercapai.\n")
            self.step_data = None; return

        d = self.step_data
        method = d["method"]
        f = d["f"]
        expr = d["expr"]
        tol = d["tol"]

        self.step_index += 1
        i = self.step_index

        if method == "Regula Falsi":
            a, b, fa, fb = d["a"], d["b"], d["fa"], d["fb"]
            c = (a * fb - b * fa) / (fb - fa)
            fc = f(c)
            err = abs(c - d.get("c_old", c))
            d["iter_data"].append((i, a, b, c, fa, fb, fc))

            self.step_log.insert(tk.END, f"\nIterasi {i}:\n")
            self.step_log.insert(tk.END, f"  a={a:.6f}, b={b:.6f}\n")
            self.step_log.insert(tk.END, f"  c={c:.6f}, f(c)={fc:.6e}\n")

            if abs(fc) < tol or err < tol:
                self.step_log.insert(tk.END, f"\n✓ KONVERGEN! Akar = {c:.10f}\n")
                self.step_data = None; return

            if fa * fc < 0:
                d["b"], d["fb"] = c, fc
            else:
                d["a"], d["fa"] = c, fc
            d["c_old"] = c

            self.step_plot_rf(f, expr, d["iter_data"])

        elif method == "Newton-Raphson":
            xi = d["x"]
            fxi = f(xi)
            dfxi = d["df"](xi)
            if abs(dfxi) < 1e-15:
                self.step_log.insert(tk.END, "\n⚠ Turunan nol! Gagal.\n"); return
            x_next = xi - fxi / dfxi
            err = abs(x_next - xi)
            d["iter_data"].append((i, xi, fxi, dfxi, x_next))

            self.step_log.insert(tk.END, f"\nIterasi {i}:\n")
            self.step_log.insert(tk.END, f"  x{i-1}={xi:.6f}\n")
            self.step_log.insert(tk.END, f"  f(x)={fxi:.6e}, f'(x)={dfxi:.6e}\n")
            self.step_log.insert(tk.END, f"  x{i}={x_next:.6f}\n")

            if abs(fxi) < tol or err < tol:
                self.step_log.insert(tk.END, f"\n✓ KONVERGEN! Akar = {x_next:.10f}\n")
                self.step_data = None; return

            d["x"] = x_next
            self.step_plot_nr(f, d["df"], expr, d["iter_data"])

        else:  # Iterasi
            xi = d["x"]
            x_next = d["g"](xi)
            err = abs(x_next - xi)
            d["iter_data"].append((i, xi, x_next))

            self.step_log.insert(tk.END, f"\nIterasi {i}:\n")
            self.step_log.insert(tk.END, f"  x{i-1}={xi:.6f}\n")
            self.step_log.insert(tk.END, f"  g(x)={x_next:.6f}, error={err:.6e}\n")

            if err < tol:
                self.step_log.insert(tk.END, f"\n✓ KONVERGEN! Akar = {x_next:.10f}\n")
                self.step_data = None; return

            d["x"] = x_next
            self.step_plot_it(d["g"], d["g_expr"], d["iter_data"])

    def step_plot_rf(self, f, expr, iter_data):
        self.step_ax.clear()
        t = self.current_theme
        self.step_ax.set_facecolor(t["card"]); self.step_ax.tick_params(colors=t["text"])

        all_x = [d[3] for d in iter_data] + [d[1] for d in iter_data] + [d[2] for d in iter_data]
        x_min, x_max = min(all_x), max(all_x)
        margin = (x_max - x_min) * 0.5 if x_max != x_min else 1
        xs = np.linspace(x_min - margin, x_max + margin, 300)
        self.step_ax.plot(xs, [f(xi) for xi in xs], 'b-', linewidth=2, label=f'f(x)={expr}')
        self.step_ax.axhline(y=0, color='k', linewidth=0.8)

        i, a, b, c, fa, fb, fc = iter_data[-1]
        self.step_ax.plot(a, fa, 'ro', markersize=8, label=f'a={a:.3f}')
        self.step_ax.plot(b, fb, 'go', markersize=8, label=f'b={b:.3f}')
        self.step_ax.plot(c, fc, 'mo', markersize=10, label=f'c={c:.4f}')
        self.step_ax.plot([a, b], [fa, fb], 'r--', alpha=0.6)
        self.step_ax.plot([c, c], [0, fc], 'm:', alpha=0.7)

        self.step_ax.set_title(f'Regula Falsi - Iterasi {i}', color=t["text"], fontweight='bold')
        self.step_ax.legend(loc='best', fontsize=8)
        self.step_fig.tight_layout(); self.step_canvas.draw()

    def step_plot_nr(self, f, df, expr, iter_data):
        self.step_ax.clear()
        t = self.current_theme
        self.step_ax.set_facecolor(t["card"]); self.step_ax.tick_params(colors=t["text"])

        all_x = [d[1] for d in iter_data] + [d[4] for d in iter_data]
        x_min, x_max = min(all_x), max(all_x)
        margin = max(abs(x_min), abs(x_max)) * 0.5
        xs = np.linspace(x_min - margin, x_max + margin, 300)
        self.step_ax.plot(xs, [f(xi) for xi in xs], 'b-', linewidth=2, label=f'f(x)={expr}')
        self.step_ax.axhline(y=0, color='k', linewidth=0.8)

        for idx, (ii, xi, fxi, dfxi, x_next) in enumerate(iter_data):
            self.step_ax.plot(xi, fxi, 'o', color=plt.cm.viridis(idx/len(iter_data)), markersize=8)
            x_tan = np.linspace(xi - 0.3*margin, xi + 0.3*margin, 30)
            y_tan = [fxi + dfxi * (xt - xi) for xt in x_tan]
            self.step_ax.plot(x_tan, y_tan, '--', color=plt.cm.viridis(idx/len(iter_data)), alpha=0.5)

        self.step_ax.set_title(f'Newton-Raphson - Iterasi {iter_data[-1][0]}', color=t["text"], fontweight='bold')
        self.step_ax.legend(loc='best', fontsize=8)
        self.step_fig.tight_layout(); self.step_canvas.draw()

    def step_plot_it(self, g, expr, iter_data):
        self.step_ax.clear()
        t = self.current_theme
        self.step_ax.set_facecolor(t["card"]); self.step_ax.tick_params(colors=t["text"])

        all_x = [d[1] for d in iter_data] + [d[2] for d in iter_data]
        x_min, x_max = min(all_x), max(all_x)
        margin = (x_max - x_min) * 0.3 if x_max != x_min else 1
        xs = np.linspace(x_min - margin, x_max + margin, 300)
        self.step_ax.plot(xs, [g(xi) for xi in xs], 'b-', linewidth=2, label=f'g(x)={expr}')
        self.step_ax.plot(xs, xs, 'k--', linewidth=1.5, alpha=0.7, label='y=x')

        for idx, (ii, xi, x_next) in enumerate(iter_data):
            c = plt.cm.plasma(idx/len(iter_data))
            self.step_ax.plot([xi, xi], [xi, x_next], '-', color=c, alpha=0.6, linewidth=1.5)
            self.step_ax.plot([xi, x_next], [x_next, x_next], '-', color=c, alpha=0.6, linewidth=1.5)

        self.step_ax.set_title(f'Iterasi - Iterasi {iter_data[-1][0]}', color=t["text"], fontweight='bold')
        self.step_ax.legend(loc='best', fontsize=8)
        self.step_fig.tight_layout(); self.step_canvas.draw()

    def step_reset(self):
        self.step_data = None
        self.step_index = 0
        self.step_log.delete(1.0, tk.END)
        self.step_log.insert(tk.END, "Tekan 'START' untuk memulai.\n")
        self.step_plot_init()
        # Cleanup GIF temp files
        for frames in (self.nr_gif_frames, self.it_gif_frames):
            for f in frames:
                try:
                    os.unlink(f)
                except OSError:
                    pass
        self.nr_gif_frames = []
        self.it_gif_frames = []


# ========== JALANKAN APLIKASI ==========
if __name__ == "__main__":
    root = tk.Tk()
    app = KalkulatorNumerikUltimate(root)
    root.mainloop()
