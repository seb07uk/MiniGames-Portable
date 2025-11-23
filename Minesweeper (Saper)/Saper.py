import tkinter as tk
from tkinter import messagebox
import random

POZIOMY = {
    "Łatwy": {"rozmiar": 8, "miny": 10},
    "Średni": {"rozmiar": 10, "miny": 15},
    "Trudny": {"rozmiar": 12, "miny": 25}
}

class Pole:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ma_mine = False
        self.oznaczone = False
        self.odkryte = False
        self.sasiadowe_miny = 0

class SaperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Saper - Minesweeper")
        self.poziom = "Średni"
        self.czas = 0
        self.timer_id = None
        self.tworz_menu()
        self.restartuj_gre()

    def tworz_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        gra_menu = tk.Menu(menu, tearoff=0)
        for poziom in POZIOMY:
            gra_menu.add_command(label=poziom, command=lambda p=poziom: self.zmien_poziom(p))
        menu.add_cascade(label="Gra", menu=gra_menu)

        pomoc_menu = tk.Menu(menu, tearoff=0)
        pomoc_menu.add_command(label="O programie", command=self.pokaz_o_programie)
        menu.add_cascade(label="Pomoc", menu=pomoc_menu)

    def pokaz_o_programie(self):
        messagebox.showinfo("O programie", "polsoft.ITS London\n\nSaper - Minesweeper v1.0\n\nCopyright 2025© Sebastian Januchowski")

    def zmien_poziom(self, poziom):
        self.poziom = poziom
        self.restartuj_gre()

    def restartuj_gre(self):
        if hasattr(self, "ramka"):
            self.ramka.destroy()
        if hasattr(self, "czas_label"):
            self.czas_label.destroy()
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        self.rozmiar = POZIOMY[self.poziom]["rozmiar"]
        self.liczba_min = POZIOMY[self.poziom]["miny"]
        self.plansza = [[Pole(x, y) for y in range(self.rozmiar)] for x in range(self.rozmiar)]
        self.rozmiesc_miny()
        self.oblicz_sasiadowe_miny()
        self.czas = 0
        self.czas_label = tk.Label(self.root, text="Czas: 0 s", font=("Arial", 12))
        self.czas_label.pack()
        self.aktualizuj_czas()
        self.tworz_interfejs()

    def aktualizuj_czas(self):
        self.czas += 1
        self.czas_label.config(text=f"Czas: {self.czas} s")
        self.timer_id = self.root.after(1000, self.aktualizuj_czas)

    def rozmiesc_miny(self):
        miny = 0
        while miny < self.liczba_min:
            x = random.randint(0, self.rozmiar - 1)
            y = random.randint(0, self.rozmiar - 1)
            if not self.plansza[x][y].ma_mine:
                self.plansza[x][y].ma_mine = True
                miny += 1

    def oblicz_sasiadowe_miny(self):
        for x in range(self.rozmiar):
            for y in range(self.rozmiar):
                if self.plansza[x][y].ma_mine:
                    continue
                licznik = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.rozmiar and 0 <= ny < self.rozmiar:
                            if self.plansza[nx][ny].ma_mine:
                                licznik += 1
                self.plansza[x][y].sasiadowe_miny = licznik

    def tworz_interfejs(self):
        self.ramka = tk.Frame(self.root)
        self.ramka.pack()
        self.przyciski = [[None for _ in range(self.rozmiar)] for _ in range(self.rozmiar)]
        for x in range(self.rozmiar):
            for y in range(self.rozmiar):
                btn = tk.Button(self.ramka, width=2, height=1, font=("Arial", 12), command=lambda x=x, y=y: self.odkryj_pole(x, y))
                btn.bind("<Button-3>", lambda e, x=x, y=y: self.oznacz_mine(x, y))
                btn.grid(row=x, column=y)
                self.przyciski[x][y] = btn

    def odkryj_pole(self, x, y):
        pole = self.plansza[x][y]
        if pole.odkryte or pole.oznaczone:
            return
        pole.odkryte = True
        btn = self.przyciski[x][y]
        if pole.ma_mine:
            btn.config(text="💣", bg="red")
            self.koniec_gry(False)
        else:
            btn.config(text=str(pole.sasiadowe_miny) if pole.sasiadowe_miny > 0 else "", bg="lightgrey")
            if pole.sasiadowe_miny == 0:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.rozmiar and 0 <= ny < self.rozmiar:
                            self.odkryj_pole(nx, ny)
        self.sprawdz_wygrana()

    def oznacz_mine(self, x, y):
        pole = self.plansza[x][y]
        if pole.odkryte:
            return
        pole.oznaczone = not pole.oznaczone
        btn = self.przyciski[x][y]
        btn.config(text="🚩" if pole.oznaczone else "")

    def sprawdz_wygrana(self):
        for x in range(self.rozmiar):
            for y in range(self.rozmiar):
                pole = self.plansza[x][y]
                if not pole.ma_mine and not pole.odkryte:
                    return
        self.koniec_gry(True)

    def koniec_gry(self, wygrana):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        for x in range(self.rozmiar):
            for y in range(self.rozmiar):
                pole = self.plansza[x][y]
                btn = self.przyciski[x][y]
                if pole.ma_mine:
                    btn.config(text="💣", bg="red")
        komunikat = "Wygrałeś!" if wygrana else "Przegrałeś!"
        wynik = tk.Label(self.root, text=f"{komunikat} Czas: {self.czas} s", font=("Arial", 14), fg="blue")
        wynik.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = SaperGUI(root)
    root.mainloop()