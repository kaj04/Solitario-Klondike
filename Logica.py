# gioco.py
from Klondike import Mazzo  # type: ignore
from Klondike import Colonna  # type: ignore
from Klondike import Fondazione  # type: ignore
from Klondike import Carta  # type: ignore
import random

class Gioco:
    def __init__(self):
        self.mazzo = Mazzo()
        self.fondazioni = {seme: Fondazione(seme) for seme in ['cuori', 'fiori', 'quadri', 'picche']}
        self.colonne = [Colonna() for _ in range(7)]
        self.turno = 0
        self.distribuisci_carte()

    def distribuisci_carte(self):
        self.mazzo.mischia()
        for i in range(7):
            for j in range(i, 7):
                carta = self.mazzo.pesca(aggiungi_a_scarti=False)
                self.colonne[j].aggiungi(carta)
        for colonna in self.colonne:
            for carta in colonna.carte[:-1]:
                carta.copri()
            colonna.carte[-1].scopri()

        self.mazzo.pesca()

    def mostra_stato(self):
        print("\n--- Mazzo ---")
        print(f"Carte coperte: {len(self.mazzo.carte)}")
        if self.mazzo.scarti.vuoto():
            print("Nessuna carta pescata")
        else:
            print(f"Ultima carta girata: {self.mazzo.scarti.ultima()}")

        print("\n--- Fondazioni ---")
        for seme, fondazione in self.fondazioni.items():
            cima = fondazione.cima()
            cima_str = str(cima) if cima else 'Vuota'
            print(f"{seme.capitalize()}: {cima_str}")

        print("\n--- Colonne ---")
        for i, colonna in enumerate(self.colonne):
            carte_str = [str(c) for c in colonna.carte]
            print(f"C{i+1}: {carte_str}")

    def gestisci_comando(self, comando):
        if comando == "R":
            if len(self.mazzo.carte) == 0:
                if self.mazzo.scarti.vuoto():
                    raise ValueError("Non ci sono carte negli scarti da ricaricare.")
                self.mazzo.ricarica()
                print("Mazzo ricaricato.")
            else:
                print("Non puoi ricaricare: ci sono ancora carte nel mazzo.")
            return

        if comando == "P":
            if len(self.mazzo.carte) == 0:
                print("Non ci sono più carte da pescare nel mazzo. Premi 'R' per ricaricare dagli scarti.")
            carta = self.mazzo.pesca()
            print(f"Carta pescata: {carta}")
            return

        if '->' not in comando:
            raise ValueError("Formato non valido. Usa 'C4->C1' o 'C4[7 di fiori]->C5' o 'P->C3'.")

        origine, destinazione = comando.split('->')
        origine = origine.strip()
        destinazione = destinazione.strip()
        sequenza = []
        carta = None

        # --- ORIGINE ---
        if origine.startswith('C') and '[' in origine:
            nome_colonna, carta_descr = origine.split('[')
            idx = int(nome_colonna[1:]) - 1
            carta_descr = carta_descr.strip('] ')
            pila_origine = self.colonne[idx]
            for c in reversed(pila_origine.carte):
                if not c.coperta and str(c) == carta_descr:
                    indice = pila_origine.carte.index(c)
                    sequenza = pila_origine.carte[indice:]
                    carta = sequenza[0]
                    break
            else:
                raise ValueError(f"La carta '{carta_descr}' non è presente tra quelle scoperte.")
        elif origine.startswith('C'):
            idx = int(origine[1:]) - 1
            pila_origine = self.colonne[idx]
            carta = pila_origine.cima()
            if not carta or carta.coperta:
                raise ValueError("Nessuna carta scoperta da spostare.")
            sequenza = [carta]
            # ⚠️ NON rimuovere qui — rimozione gestita dopo conferma mossa
        elif origine == 'P':
            carta = self.mazzo.scarti.ultima()
            if not carta:
                raise ValueError("Nessuna carta girata.")
            sequenza = [carta]
        else:
            raise ValueError("Origine non valida.")

        # --- DESTINAZIONE ---
        if destinazione.startswith("C"):
            idx = int(destinazione[1:]) - 1
            pila_destinazione = self.colonne[idx]
        elif destinazione.lower().startswith("f"):
            seme = destinazione[1:].lower()
            if seme not in self.fondazioni:
                raise ValueError(f"Fondazione '{seme}' non valida.")
            pila_destinazione = self.fondazioni[seme]
        else:
            raise ValueError("Destinazione non valida.")

        if not pila_destinazione.può_aggiungere(carta):
            raise ValueError("Mossa non valida.")

        # --- ESECUZIONE MOVIMENTO ---
        for c in sequenza:
            pila_destinazione.aggiungi(c)

        if origine.startswith('C') and '[' in origine:
            for _ in range(len(sequenza)):
                pila_origine.rimuovi()

        # --- RIMOZIONE E SCOPERTURA ---
        if origine.startswith('C'):
            if '[' not in origine:
                for _ in sequenza:
                    pila_origine.rimuovi()
            if pila_origine.carte and pila_origine.cima().coperta:
                pila_origine.cima().scopri()
        elif origine == 'P':
            self.mazzo.scarti.prendi()

        print(f"{'Sequenza' if len(sequenza) > 1 else 'Carta'} spostata: {sequenza}")

    def inizia(self):
        while True:
            self.mostra_stato()
            comando = input("\nComando (es: C3->C1, C4[7 di fiori]->C5, C4->Fcuori, P->C5, P per Pescare, R per ricaricare, Q per uscire): ").strip()
            if comando.upper() == 'Q':
                print("Partita terminata.")
                break
            try:
                self.gestisci_comando(comando)
            except Exception as e:
                print(f"Errore: {e}")
                
    def controlla_vittoria(self):
        """Verifica se tutte le fondazioni sono complete."""
        return all(len(f.carte) == 13 for f in self.fondazioni.values())
