import pygame
import os
from Logica import Gioco  # type: ignore
from Klondike import Carta  # type: ignore

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
            percorso = os.path.join("img", nome_file)
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

# Funzione principale di disegno
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
        fondazione = gioco.fondazioni[seme]
        cima = fondazione.cima()
        if cima:
            disegna_carta(cima, x, y)
        else:
            pygame.draw.rect(finestra, (200, 200, 200), (x, y, *DIM_CARTA), 2)

    # Mazzo
    if gioco.mazzo.carte:
        finestra.blit(immagini_carte["coperta"], (700, 20))
    else:
        pygame.draw.rect(finestra, (200, 200, 200), (700, 20, *DIM_CARTA), 2)

    # Scarti
    if not gioco.mazzo.scarti.vuoto():
        disegna_carta(gioco.mazzo.scarti.ultima(), 800, 20)

    # Bottone "Ricarica"
    if not gioco.mazzo.carte and not gioco.mazzo.scarti.vuoto():
        pygame.draw.rect(finestra, (255, 255, 0), (700, 130, DIM_CARTA[0], 30))
        testo = font.render("Ricarica", True, (0, 0, 0))
        finestra.blit(testo, (705, 135))

    # Carte trascinate
    if trascina["carte"]:
        x, y = pygame.mouse.get_pos()
        dx, dy = trascina["offset"]
        for idx, carta in enumerate(trascina["carte"]):
            disegna_carta(carta, x - dx, y - dy + idx * SPAZIO_VERTICALE)

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
    if 700 <= x <= 700 + DIM_CARTA[0] and 20 <= y <= 20 + DIM_CARTA[1]:
        if gioco.mazzo.carte:
            print("Pesco una carta")
            gioco.gestisci_comando("P")
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
            successo = gioco.sposta("colonna", trascina["origine"], ("colonna", i), trascina["carte"])
            rilasciato = True
            break

    # Rilascio su fondazione
    if not rilasciato:
        for idx, seme in enumerate(['cuori', 'fiori', 'quadri', 'picche']):
            fx = MARGINE_SINISTRA + idx * SPAZIO_COLONNA
            fy = 20
            rett = pygame.Rect(fx, fy, *DIM_CARTA)
            if rett.collidepoint(x, y) and len(trascina["carte"]) == 1:
                gioco.sposta("fondazione", trascina["origine"], seme, trascina["carte"])
                break

    trascina["carte"] = []
    trascina["origine"] = None

# Inizio ciclo
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            gestisci_click(event.pos)  # <-- Esegui SEMPRE
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
                    colonna = gioco.col

