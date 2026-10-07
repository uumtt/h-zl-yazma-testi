import tkinter as tk
import random
import sys

# Windows Yüksek Çözünürlük (High DPI) Düzeltmesi
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass

KELIMELER = [
    "güçlü", "araba", "sistem", "sürücü", "pratik", "tekerlek", "otoban", "oyun",
    "seviye", "yazılım", "basit", "direksiyon", "klavye", "hızlı", "yazma", "testi",
    "kodlama", "ekran", "veri", "donanım", "internet", "program", "tasarım", "başarı"
]

class HizliYazmaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hızlı Yazma Testi")
        self.root.geometry("900x580")
        self.root.configure(bg="#0F172A")

        self.sure_limit = self.kalan_sure = 30
        self.basladi_mi = False
        self.current_idx = self.dogru_harf = self.toplam_harf = 0
        self.score_frame = None

        self.setup_ui()
        self.yeni_test_hazirla()
        self.root.bind("<Key>", self.tus_basildi)

    def setup_ui(self):
        # Üst Bar
        top_bar = tk.Frame(self.root, bg="#0F172A", pady=15)
        top_bar.pack(fill="x", padx=30)

        tk.Label(top_bar, text="⌨ Hızlı Yazma", font=("Segoe UI", 16, "bold"), bg="#0F172A", fg="#F8FAFC").pack(side="left")
        tk.Label(top_bar, text="v1.0", font=("Segoe UI", 9, "bold"), bg="#E07A5F", fg="#FFFFFF", padx=8, pady=2).pack(side="left", padx=10)

        # Kontrol Barı
        control_card = tk.Frame(self.root, bg="#1E293B", pady=10, padx=15)
        control_card.pack(fill="x", padx=30, pady=(0, 15))

        f_frame = tk.Frame(control_card, bg="#1E293B")
        f_frame.pack(side="left")

        tk.Label(f_frame, text="Türkçe", font=("Segoe UI", 9, "bold"), bg="#E07A5F", fg="#FFFFFF", padx=10, pady=3).pack(side="left", padx=(0, 10))

        self.btn_sureler = {}
        for t in [15, 30, 60]:
            btn = tk.Button(f_frame, text=f"{t}s", font=("Segoe UI", 9, "bold"), bg="#0F172A", fg="#94A3B8", bd=0, padx=10, pady=3, command=lambda x=t: self.sure_degistir(x))
            btn.pack(side="left", padx=2)
            self.btn_sureler[t] = btn

        tk.Button(f_frame, text="🔄 Yenile", font=("Segoe UI", 9, "bold"), bg="#334155", fg="#F8FAFC", bd=0, padx=10, pady=3, command=self.yeni_test_hazirla).pack(side="left", padx=(10, 0))

        # İstatistikler
        s_frame = tk.Frame(control_card, bg="#1E293B")
        s_frame.pack(side="right")

        self.lbl_sure = self._stat_box(s_frame, "SÜRE", "30", "#E07A5F")
        self.lbl_wpm = self._stat_box(s_frame, "WPM", "0", "#F8FAFC")
        self.lbl_dogruluk = self._stat_box(s_frame, "DOĞRULUK", "%100", "#22C55E")

        # Metin Ekranı Kartı
        self.text_card = tk.Frame(self.root, bg="#1E293B")
        self.text_card.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        self.text_display = tk.Text(self.text_card, font=("Consolas", 20, "bold"), bg="#1E293B", fg="#475569", bd=0, wrap="word", padx=25, pady=25, highlightthickness=0)
        self.text_display.pack(fill="both", expand=True)

        self.text_display.tag_config("dogru", foreground="#22C55E")
        self.text_display.tag_config("yanlis", foreground="#EF4444", background="#450A0A")
        self.text_display.tag_config("aktif", foreground="#FFFFFF", background="#E07A5F")
        self.text_display.tag_config("bekleyen", foreground="#475569")

    def _stat_box(self, parent, title, val, color):
        box = tk.Frame(parent, bg="#1E293B", padx=10)
        box.pack(side="left")
        tk.Label(box, text=title, font=("Segoe UI", 7, "bold"), bg="#1E293B", fg="#64748B").pack()
        lbl = tk.Label(box, text=val, font=("Segoe UI", 14, "bold"), bg="#1E293B", fg=color)
        lbl.pack()
        return lbl

    def sure_degistir(self, sure):
        self.sure_limit = sure
        self.yeni_test_hazirla()

    def yeni_test_hazirla(self):
        if self.score_frame:
            self.score_frame.destroy()
            self.score_frame = None

        for t, btn in self.btn_sureler.items():
            btn.config(bg="#E07A5F" if t == self.sure_limit else "#0F172A", fg="#FFFFFF" if t == self.sure_limit else "#94A3B8")

        self.text_display.pack(fill="both", expand=True)
        words = KELIMELER * 4
        random.shuffle(words)
        self.tam_metin = " ".join(words)

        self.current_idx = self.dogru_harf = self.toplam_harf = 0
        self.basladi_mi = False
        self.kalan_sure = self.sure_limit

        self.lbl_sure.config(text=str(self.kalan_sure))
        self.lbl_wpm.config(text="0")
        self.lbl_dogruluk.config(text="%100")

        self.text_display.config(state="normal")
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert("1.0", self.tam_metin)
        self.text_display.tag_add("bekleyen", "1.0", tk.END)
        self.text_display.config(state="disabled")

        self.imlec_guncelle()

    def imlec_guncelle(self):
        self.text_display.config(state="normal")
        self.text_display.tag_remove("aktif", "1.0", tk.END)
        if self.current_idx < len(self.tam_metin):
            pos = f"1.0 + {self.current_idx} chars"
            self.text_display.tag_add("aktif", pos, f"{pos} + 1 chars")
        self.text_display.config(state="disabled")

    def zamanlayiciyi_baslat(self):
        if not self.basladi_mi:
            return

        if self.kalan_sure > 0:
            self.kalan_sure -= 1
            self.lbl_sure.config(text=str(self.kalan_sure))

            gecen = self.sure_limit - self.kalan_sure
            if gecen > 0:
                self.lbl_wpm.config(text=str(int((self.dogru_harf / 5) / (gecen / 60))))

            if self.kalan_sure == 0:
                self.basladi_mi = False
                self.skor_ekranini_goster()
            else:
                self.root.after(1000, self.zamanlayiciyi_baslat)

    def skor_ekranini_goster(self):
        self.text_display.pack_forget()
        self.score_frame = tk.Frame(self.text_card, bg="#1E293B")
        self.score_frame.pack(expand=True, fill="both")

        wpm = int((self.dogru_harf / 5) / (self.sure_limit / 60))
        dogruluk = int((self.dogru_harf / self.toplam_harf) * 100) if self.toplam_harf else 100
        yanlis_harf = self.toplam_harf - self.dogru_harf

        tk.Label(self.score_frame, text="🎉 Test Tamamlandı!", font=("Segoe UI", 18, "bold"), bg="#1E293B", fg="#F8FAFC").pack(pady=20)

        s_box = tk.Frame(self.score_frame, bg="#1E293B")
        s_box.pack(pady=10)

        for title, val, color in [("WPM (HIZ)", str(wpm), "#E07A5F"), ("DOĞRULUK", f"%{dogruluk}", "#22C55E"), ("DOĞRU / YANLIŞ", f"{self.dogru_harf} / {yanlis_harf}", "#F8FAFC")]:
            card = tk.Frame(s_box, bg="#0F172A", padx=25, pady=15)
            card.pack(side="left", padx=10)
            tk.Label(card, text=title, font=("Segoe UI", 8, "bold"), bg="#0F172A", fg="#64748B").pack()
            tk.Label(card, text=val, font=("Segoe UI", 24, "bold"), bg="#0F172A", fg=color).pack(pady=(5, 0))

        tk.Button(self.score_frame, text="🔄 Yeniden Başlat", font=("Segoe UI", 11, "bold"), bg="#E07A5F", fg="#FFFFFF", bd=0, padx=20, pady=8, command=self.yeni_test_hazirla).pack(pady=25)

    def tus_basildi(self, event):
        # Süre bittiğinde veya skor ekranındayken basılan tuşları engelle
        if self.kalan_sure <= 0 or self.score_frame is not None:
            return

        if event.keysym in ['Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R', 'Caps_Lock', 'Tab', 'Return', 'Escape']:
            return

        if not self.basladi_mi:
            self.basladi_mi = True
            self.zamanlayiciyi_baslat()

        self.text_display.config(state="normal")
        pos, next_pos = f"1.0 + {self.current_idx} chars", f"1.0 + {self.current_idx + 1} chars"

        if event.keysym == 'BackSpace' and self.current_idx > 0:
            self.current_idx -= 1
            p1, p2 = f"1.0 + {self.current_idx} chars", f"1.0 + {self.current_idx + 1} chars"
            for tag in ["dogru", "yanlis"]:
                self.text_display.tag_remove(tag, p1, p2)
            self.text_display.tag_add("bekleyen", p1, p2)

        elif event.keysym == 'space':
            next_sp = self.tam_metin.find(' ', self.current_idx)
            if next_sp != -1:
                for i in range(self.current_idx, next_sp):
                    self.text_display.tag_add("yanlis", f"1.0 + {i} chars", f"1.0 + {i + 1} chars")
                self.current_idx = next_sp + 1

        elif len(event.char) == 1 and event.char.isprintable() and self.current_idx < len(self.tam_metin):
            self.toplam_harf += 1
            is_correct = (event.char == self.tam_metin[self.current_idx])
            if is_correct:
                self.dogru_harf += 1

            self.text_display.tag_remove("bekleyen", pos, next_pos)
            self.text_display.tag_add("dogru" if is_correct else "yanlis", pos, next_pos)
            self.current_idx += 1

            if self.toplam_harf:
                self.lbl_dogruluk.config(text=f"%{int((self.dogru_harf / self.toplam_harf) * 100)}")

        self.imlec_guncelle()
        self.text_display.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = HizliYazmaApp(root)
    root.mainloop()