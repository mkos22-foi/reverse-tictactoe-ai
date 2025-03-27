import tkinter as tk
import random as rd

igrac = "X"
ai = "O"
igrac_naRedu = False
igrac_bira = ""
ploca = [["" for _ in range(3)] for _ in range(3)]
kocka_bacena = False

TAMNO_ZELENA = "#31473A"
SVIJETLO_SIVA = "#EDF4F2"
BIJELA = "#FFFFFF"

BOJA_POBJEDE = "#6FA287"
BOJA_PORAZA = "#D16A6A"
BOJA_NERIJESENO = "#7D8C84"

def igra_pokrenuta():
    global igrac_naRedu, igrac_bira

    izbor_prozor = tk.Toplevel(root)
    izbor_prozor.title("Pismo ili Glava")
    izbor_prozor.geometry("300x200")
    izbor_prozor.configure(bg=SVIJETLO_SIVA)
    izbor_prozor.transient(root)
    izbor_prozor.grab_set()
    izbor_prozor.resizable(False, False)

    def zatvori_prozor():
        root.destroy()

    izbor_prozor.protocol("WM_DELETE_WINDOW", zatvori_prozor)

    label_odabir = tk.Label(izbor_prozor, text="Odaberite stranu novčića", font=("Arial", 16), bg=SVIJETLO_SIVA, fg=TAMNO_ZELENA)
    label_odabir.pack(pady=10)

    def odaberi(izbor):
        global igrac_naRedu, igrac_bira, kocka_bacena
        igrac_bira = izbor.lower()

        info_lb.config(text=f"Odabrali ste {igrac_bira.capitalize()}.\nBaca se novčić...", fg=TAMNO_ZELENA)

        kocka_bacena = True
        root.after(2000, prikazi_rezultat)

        izbor_prozor.destroy()

    pismo_button = tk.Button(izbor_prozor, text="Pismo", font=("Arial", 15), width=10, bg=SVIJETLO_SIVA, fg=TAMNO_ZELENA, command=lambda: odaberi("pismo"))
    pismo_button.pack(pady=10)

    glava_button = tk.Button(izbor_prozor, text="Glava", font=("Arial", 15), width=10, bg=SVIJETLO_SIVA, fg=TAMNO_ZELENA, command=lambda: odaberi("glava"))
    glava_button.pack(pady=10)

def prikazi_rezultat():
    global igrac_naRedu, kocka_bacena
    rezultat_bacanja = rd.choice(["pismo", "glava"])

    if rezultat_bacanja == igrac_bira:
        igrac_naRedu = True
        if rezultat_bacanja == "pismo":
            tekst_rezultata = "Palo je"
        else:
            tekst_rezultata = "Pala je"
        info_lb.config(
            text=f"Odabrali ste {igrac_bira.capitalize()}.\n{tekst_rezultata} {rezultat_bacanja}. Vi ste na redu!", fg=TAMNO_ZELENA
        )
    else:
        igrac_naRedu = False
        if rezultat_bacanja == "pismo":
            tekst_rezultata = "Palo je"
        else:
            tekst_rezultata = "Pala je"
        info_lb.config(
            text=f"Odabrali ste {igrac_bira.capitalize()}.\n{tekst_rezultata} {rezultat_bacanja}. Ja sam na redu :)", fg=TAMNO_ZELENA
        )
        root.after(1000, igraAI)

    kocka_bacena = False

def odaberi_polje(event, canvas, red, stu):
    global igrac_naRedu, kocka_bacena

    if not canvas.find_withtag("mark") and ploca[red][stu] == "" and igrac_naRedu and not kocka_bacena:
        canvas.create_text(100, 100, text=igrac, font=("Arial", 100), tags="mark", fill=BIJELA)
        ploca[red][stu] = igrac
        if provjeri(igrac, ploca):
            info_lb.config(text="Izgubili ste! Spojili ste tri u nizu :(", fg=BOJA_PORAZA)
            onemoguci_plocu()
            return
        elif puna_ploca(ploca):
            info_lb.config(text="Neriješeno!", fg=BOJA_NERIJESENO)
            return
        baci_kocku()
    else:
        if not igrac_naRedu:
            info_lb.config(text="Nije vaš red.", fg=BOJA_PORAZA)

def igraAI():
    global igrac_naRedu, kocka_bacena

    if not kocka_bacena:
        najbolji_potez = None
        najbolja_vrijednost = float('-inf')

        for i in range(3):
            for j in range(3):
                if ploca[i][j] == "":
                    ploca[i][j] = ai
                    vrijednost = minimax(ploca, 0, False)
                    ploca[i][j] = ""
                    if vrijednost > najbolja_vrijednost:
                        najbolja_vrijednost = vrijednost
                        najbolji_potez = (i, j)

        if najbolji_potez:
            i, j = najbolji_potez
            polje = okvir_ploce.grid_slaves(row=i, column=j)[0]
            polje.create_text(100, 100, text=ai, font=("Arial", 100), tags="mark", fill=BIJELA)
            ploca[i][j] = ai
            if provjeri(ai, ploca):
                info_lb.config(text="Pobijedili ste! Računalo je spojilo tri u nizu :O", fg=BOJA_POBJEDE)
                onemoguci_plocu()
                return
            elif puna_ploca(ploca):
                info_lb.config(text="Neriješeno!", fg=BOJA_NERIJESENO)
                return
            baci_kocku()

def baci_kocku():
    global kocka_bacena
    kocka_bacena = True
    info_lb.config(text=f"Odabrali ste {igrac_bira.capitalize()}.\nBaca se novčić...", fg=TAMNO_ZELENA)
    root.after(2000, prikazi_rezultat)

def minimax(stanje, dubina, je_max):
    if provjeri(ai, stanje):
        return -10 + dubina
    elif provjeri(igrac, stanje):
        return 10 - dubina
    elif puna_ploca(stanje):
        return 0

    if je_max:
        max_vrijednost = float('-inf')
        for i in range(3):
            for j in range(3):
                if stanje[i][j] == "":
                    stanje[i][j] = ai
                    vrijednost = minimax(stanje, dubina + 1, False)
                    stanje[i][j] = ""
                    max_vrijednost = max(max_vrijednost, vrijednost)
        return max_vrijednost
    else:
        min_vrijednost = float('inf')
        for i in range(3):
            for j in range(3):
                if stanje[i][j] == "":
                    stanje[i][j] = igrac
                    vrijednost = minimax(stanje, dubina + 1, True)
                    stanje[i][j] = ""
                    min_vrijednost = min(min_vrijednost, vrijednost)
        return min_vrijednost

def provjeri(simbol, stanje):
    for i in range(3):
        if stanje[i][0] == simbol and stanje[i][1] == simbol and stanje[i][2] == simbol:
            return True

    for i in range(3):
        if stanje[0][i] == simbol and stanje[1][i] == simbol and stanje[2][i] == simbol:
            return True

    if stanje[0][0] == simbol and stanje[1][1] == simbol and stanje[2][2] == simbol:
        return True

    if stanje[0][2] == simbol and stanje[1][1] == simbol and stanje[2][0] == simbol:
        return True

    return False


def puna_ploca(stanje):
    return all(stanje[i][j] != "" for i in range(3) for j in range(3))

def onemoguci_plocu():
    for red in range(3):
        for stu in range(3):
            polje = okvir_ploce.grid_slaves(row=red, column=stu)[0]
            polje.unbind("<Button-1>")

def ponovno_pokreni():
    global igrac_naRedu, ploca, kocka_bacena, igrac_bira
    igrac_naRedu = False
    ploca = [["" for _ in range(3)] for _ in range(3)]
    kocka_bacena = False
    igrac_bira = ""
    igra_pokrenuta()

    for red in range(3):
        for stu in range(3):
            polje = okvir_ploce.grid_slaves(row=red, column=stu)[0]
            polje.delete("mark")
            polje.bind("<Button-1>", lambda event, p=polje, r=red, s=stu: odaberi_polje(event, p, r, s))

    info_lb.config(text="Odaberite pismo ili glava za početak igre.\n", fg=TAMNO_ZELENA)

root = tk.Tk()
root.title("Random-Reverse-Križić-kružić")
root.geometry("700x850")
root.configure(bg=SVIJETLO_SIVA)
root.resizable(False, False)

igra_pokrenuta()

naslov = tk.Label(root, text="Probajte me pobijediti :)", font=("Arial bold", 24), bg=SVIJETLO_SIVA, fg=TAMNO_ZELENA)
naslov.pack(pady=10)

okvir_ploce = tk.Frame(root, bg=SVIJETLO_SIVA)
okvir_ploce.pack()

for red in range(3):
    for stu in range(3):
        polje = tk.Canvas(okvir_ploce, width=200, height=200, bg=TAMNO_ZELENA, highlightthickness=1, highlightbackground=SVIJETLO_SIVA)
        polje.grid(row=red, column=stu, padx=5, pady=5)
        polje.bind("<Button-1>", lambda event, p=polje, r=red, s=stu: odaberi_polje(event, p, r, s))

okvir_btn = tk.Frame(root, bg=SVIJETLO_SIVA)
okvir_btn.pack(pady=20)

info_lb = tk.Label(okvir_btn, text="Odaberite pismo ili glava za početak igre.\n", font=("Arial bold", 14), fg=TAMNO_ZELENA, bg=SVIJETLO_SIVA, justify="center")
info_lb.grid(row=0, column=0, columnspan=2, pady=(0, 10))

restart_btn = tk.Button(okvir_btn, text="RESTART", font=("Arial bold", 15), width=15, height=1, bg=SVIJETLO_SIVA, fg=TAMNO_ZELENA, command=ponovno_pokreni)
restart_btn.grid(row=1, column=0, padx=10)

exit_btn = tk.Button(okvir_btn, text="EXIT", font=("Arial bold", 15), width=15, height=1, bg=SVIJETLO_SIVA, fg=TAMNO_ZELENA, command=root.quit)
exit_btn.grid(row=1, column=1, padx=10)

root.mainloop()