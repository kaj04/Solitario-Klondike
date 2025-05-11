import pygame
import os
from Logica import Gioco # type: ignore
from Klondike import Carta # type: ignore

# Costanti
LARGHEZZA, ALTEZZA = 1024, 768
DIM_CARTA = (71, 96)
MARGINE_SINISTRA = 50
MARGINE_SUPERIORE = 150
SPAZIO_COLONNA = 120
SPAZIO_VERTICALE = 30

pygame.init()
finestra = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Klondike Solitaire")
font = pygame.font.SysFont("arial", 20)

# Caricamento immagini
def carica_immagini():
    immagini = {}
    valori_map = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
    semi_map = {'cuori': 'H', 'quadri': 'D', 'fiori': 'C', 'picche': 'S'}

    for valore in range(1, 14):
        val_str = valori_map.get(valore, str(valore))
        for seme_nome, seme_abbr in semi_map.items():
            nome_file = f"{val_str}{seme_abbr}.png"
            percorso = os.path.join("cards", nome_file)
            if os.path.exists(percorso):
                img = pygame.image.load(percorso)
                immagini[f"{valore}_{seme_nome}"] = pygame.transform.scale(img, DIM_CARTA)

    immagini["coperta"] = pygame.transform.scale(pygame.image.load("img/1B.png"), DIM_CARTA)
    return immagini

immagini_carte = carica_immagini()
gioco = Gioco()
print(f"Carte nel mazzo: {len(gioco.mazzo.carte)} + scarti: {len(gioco.mazzo.scarti)} + colonne: {sum(len(c.carte) for c in gioco.colonne)} = totale: {len(gioco.mazzo.carte) + len(gioco.mazzo.scarti) + sum(len(c.carte) for c in gioco.colonne)}")


# Variabili drag & drop
trascina = {
    "carte": [],
    "offset": (0, 0),
    "origine": None  # (tipo, indice) es: ('colonna', 3)
}

def disegna_carta(carta, x, y):
    if carta.coperta:
        img = immagini_carte["coperta"]
    else:
        chiave = f"{carta.valore}_{carta.seme}"
        img = immagini_carte.get(chiave)
    if img:
        finestra.blit(img, (x, y))
    else:
        pygame.draw.rect(finestra, (255, 0, 0), (x, y, *DIM_CARTA), 2)

def disegna():
    finestra.fill((0, 128, 0))
    # Colonne
    for i, colonna in enumerate(gioco.colonne):
        x = MARGINE_SINISTRA + i * SPAZIO_COLONNA
        y = MARGINE_SUPERIORE
        for carta in colonna.carte:
            if carta in trascina["carte"]:
                continue
            disegna_carta(carta, x, y)
            y += SPAZIO_VERTICALE

    # Fondazioni
    for idx, seme in enumerate(['cuori', 'fiori', 'quadri', 'picche']):
        x = MARGINE_SINISTRA + idx * SPAZIO_COLONNA
        y = 20
        # Bordo elegante vuoto
        pygame.draw.rect(finestra, (240, 240, 240), (x, y, *DIM_CARTA), width=3, border_radius=10)
        # Disegna carta sulla fondazione se presente
        fondazione = gioco.fondazioni[seme]
        cima = fondazione.cima()
        if cima:
            disegna_carta(cima, x, y)
        # Testo sotto la fondazione
        font_fondazione = pygame.font.SysFont("georgia", 18, bold=True)
        testo = font_fondazione.render(seme.capitalize(), True, (255, 255, 255))
        testo_rect = testo.get_rect(center=(x + DIM_CARTA[0] // 2, y + DIM_CARTA[1] + 10))
        finestra.blit(testo, testo_rect)

    # Mazzo
    if gioco.mazzo.carte:
        finestra.blit(immagini_carte["coperta"], (700, 20))
    else:
        pygame.draw.rect(finestra, (200, 200, 200), (700, 20, *DIM_CARTA), 2)

    # Scarti
    if not gioco.mazzo.scarti.vuoto():
        disegna_carta(gioco.mazzo.scarti.ultima(), 800, 20)
    else:
        pygame.draw.rect(finestra, (200, 200, 200), (800, 20, *DIM_CARTA), 2)

    # Bottone "Ricarica"
    if not gioco.mazzo.carte and not gioco.mazzo.scarti.vuoto():
        pygame.draw.rect(finestra, (255, 223, 100), (700, 130, DIM_CARTA[0], 30), border_radius=6)
        pygame.draw.rect(finestra, (200, 180, 80), (700, 130, DIM_CARTA[0], 30), 2, border_radius=6)
        testo = font.render("Ricarica", True, (0, 0, 0))
        finestra.blit(testo, (705, 135))

    # Carte trascinate
    if trascina["carte"]:
        x, y = pygame.mouse.get_pos()
        dx, dy = trascina["offset"]
        for idx, carta in enumerate(trascina["carte"]):
            disegna_carta(carta, x - dx, y - dy + idx * SPAZIO_VERTICALE)

    # Controlla se il giocatore ha vinto
    carte_fondazioni = sum(len(gioco.fondazioni[s].carte) for s in gioco.fondazioni)
    if carte_fondazioni == 52:
        testo_vittoria = pygame.font.SysFont("arial", 48, bold=True).render("Hai vinto!", True, (255, 255, 255))
        rettangolo = testo_vittoria.get_rect(center=(LARGHEZZA // 2, ALTEZZA // 2))
        pygame.draw.rect(finestra, (0, 0, 0), rettangolo.inflate(20, 20))
        finestra.blit(testo_vittoria, rettangolo)

    pygame.display.flip()

def trova_carta(pos):
    x, y = pos
    # Scarti
    if 800 <= x <= 800 + DIM_CARTA[0] and 20 <= y <= 20 + DIM_CARTA[1]:
        carta = gioco.mazzo.scarti.ultima()
        if carta and not carta.coperta:
            return ("scarti", carta)

    # Colonne
    for i, colonna in enumerate(gioco.colonne):
        cx = MARGINE_SINISTRA + i * SPAZIO_COLONNA
        cy = MARGINE_SUPERIORE
        for j, carta in enumerate(colonna.carte):
            rett = pygame.Rect(cx, cy, DIM_CARTA[0], DIM_CARTA[1])
            if rett.collidepoint(x, y) and not carta.coperta:
                return ("colonna", i, j)
            cy += SPAZIO_VERTICALE
    return None

# Gestione click per pesca/ricarica
def gestisci_click(pos):
    x, y = pos
    # Click sul mazzo per pescare una carta
    if 700 <= x <= 700 + DIM_CARTA[0] and 20 <= y <= 20 + DIM_CARTA[1]:
        if gioco.mazzo.carte:
            print("Pesco una carta")
            gioco.gestisci_comando("P")  # Invia il comando una sola volta
            print(f"Carte negli scarti: {[str(c) for c in gioco.mazzo.scarti.tutte()]}")
        else:
            print("Mazzo vuoto, prova a ricaricare.")
    # Click sul bottone "Ricarica"
    elif 700 <= x <= 700 + DIM_CARTA[0] and 130 <= y <= 160:
        if not gioco.mazzo.carte and not gioco.mazzo.scarti.vuoto():
            print("Rigiro gli scarti nel mazzo")
            gioco.gestisci_comando("R")

def gestisci_rilascio(pos):
    global trascina
    if not trascina["carte"]:
        return

    x, y = pos
    rilasciato = False

    # Rilascio su colonna
    for i in range(7):
        cx = MARGINE_SINISTRA + i * SPAZIO_COLONNA
        cy = MARGINE_SUPERIORE
        rett = pygame.Rect(cx, cy, DIM_CARTA[0], ALTEZZA)
        if rett.collidepoint(x, y):
            comando = f"C{trascina['origine'][1]+1}[{trascina['carte'][0]}]->C{i+1}"
            try:
                gioco.gestisci_comando(comando)
                rilasciato = True
            except Exception as e:
                print("Errore:", e)
            break

    # Rilascio su fondazione
    if not rilasciato and len(trascina["carte"]) == 1:
        for idx, seme in enumerate(['cuori', 'fiori', 'quadri', 'picche']):
            fx = MARGINE_SINISTRA + idx * SPAZIO_COLONNA
            fy = 20
            rett = pygame.Rect(fx, fy, *DIM_CARTA)
            if rett.collidepoint(x, y):
                carta = trascina["carte"][0]
                if carta.seme == seme:  # Controlla che il seme corrisponda
                    comando = f"C{trascina['origine'][1]+1}[{carta}]->F{seme.lower()}"
                    try:
                        gioco.gestisci_comando(comando)
                    except Exception as e:
                        print("Errore:", e)
                else:
                    print(f"Errore: La carta {carta} non appartiene alla fondazione {seme}.")
                break

    trascina["carte"] = []
    trascina["origine"] = None

print(f"Carte iniziali nel mazzo: {len(gioco.mazzo.carte)}")
print(f"Carte iniziali negli scarti: {len(gioco.mazzo.scarti)}")
#inizio ciclio 
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            risultato = trova_carta(event.pos)
            if risultato:
                if risultato[0] == "scarti":
                    carta = risultato[1]
                    trascina["carte"] = [carta]
                    trascina["origine"] = ("scarti", None)
                    mx, my = pygame.mouse.get_pos()
                    trascina["offset"] = (mx - 800, my - 20)
                elif risultato[0] == "colonna":
                    col_idx, carta_idx = risultato[1], risultato[2]
                    colonna = gioco.colonne[col_idx]
                    carte = colonna.carte[carta_idx:]
                    trascina["carte"] = carte
                    trascina["origine"] = ("colonna", col_idx)
                    mx, my = pygame.mouse.get_pos()
                    x_inizio = MARGINE_SINISTRA + col_idx * SPAZIO_COLONNA
                    y_inizio = MARGINE_SUPERIORE + carta_idx * SPAZIO_VERTICALE
                    trascina["offset"] = (mx - x_inizio, my - y_inizio)
            else:
                gestisci_click(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if trascina["carte"]:
                mx, my = pygame.mouse.get_pos()
                # Controllo drop su colonne
                rilasciato = False

                for i in range(7):
                    x = MARGINE_SINISTRA + i * SPAZIO_COLONNA
                    y = MARGINE_SUPERIORE
                    rett = pygame.Rect(x, y, DIM_CARTA[0], ALTEZZA - y)
                    if rett.collidepoint(mx, my):
                        sorgente = trascina["origine"]
                        carta = trascina["carte"][0]
                        if sorgente[0] == "colonna":
                            comando = f"C{sorgente[1]+1}[{str(carta)}]->C{i+1}"
                        elif sorgente[0] == "scarti":
                            comando = f"P->C{i+1}"
                        else:
                            comando = ""
                        try:
                            gioco.gestisci_comando(comando)
                        except Exception as e:
                            print("Errore:", e)
                        rilasciato = True
                        break 

                if not rilasciato and len(trascina["carte"]) == 1:
                    # Controllo drop su fondazioni
                    for idx, seme in enumerate(['cuori', 'fiori', 'quadri', 'picche']):
                        x = MARGINE_SINISTRA + idx * SPAZIO_COLONNA
                        y = 20
                        rett = pygame.Rect(x, y, *DIM_CARTA)
                        if rett.collidepoint(mx, my):
                            sorgente = trascina["origine"]
                            carta = trascina["carte"][0]
                            if sorgente[0] == "colonna":
                                comando = f"C{sorgente[1]+1}[{str(carta)}]->F{seme.lower()}"
                            elif sorgente[0] == "scarti":
                                comando = f"P->F{seme.lower()}"
                            else:
                                comando = ""
                            try:
                                gioco.gestisci_comando(comando)
                            except Exception as e:
                                print("Errore:", e)
                            break
                        
                trascina["carte"] = []
                trascina["origine"] = None
    disegna()
    clock.tick(60)

pygame.quit()