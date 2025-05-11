# carta.py
import random

class Carta:
    SEMI = ['cuori', 'quadri', 'fiori', 'picche']
    VALORI = list(range(1, 14))  # 1 = Asso, 11 = Jack, 12 = Regina, 13 = Re

    def __init__(self, seme, valore, coperta=True):
        self.seme = seme
        self.valore = valore
        self.coperta = coperta

    def scopri(self):
        self.coperta = False
    
    def copri(self):
        self.coperta = True

    def __str__(self):
        nomi_valori = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
        val = nomi_valori.get(self.valore, str(self.valore))
        return f"{val} di {self.seme}" if not self.coperta else "🂠"

    def __repr__(self):
        return str(self)

# mazzo.py
class Mazzo:
    def __init__(self):
        # tutte le carte coperte
        self.carte = [Carta(seme, valore) for seme in Carta.SEMI for valore in Carta.VALORI]
        random.shuffle(self.carte)
        self.scarti = Scarti()

    def mischia(self):
        """Re-mixa le carte rimaste coperte."""
        random.shuffle(self.carte)

    def pesca(self, aggiungi_a_scarti=True):
        """Pesca l’ultima carta coperta, la scopre e la mette negli scarti."""
        if not self.carte:
            return None
        carta = self.carte.pop()
        carta.scopri()
        if aggiungi_a_scarti:
            self.scarti.aggiungi(carta)
        return carta

    def ricarica(self):
        """
        Quando il mazzo è vuoto e ci sono scarti, ribalta gli scarti nel mazzo
        in ordine inverso, coprendole di nuovo.
        """
        if self.scarti.vuoto():
            return False
        pile=self.scarti.svuota()
        for carta in pile:
            carta.copri()
        self.carte = (pile)
        return True

    def __len__(self):
        return len(self.carte)
    
# scarti.py
class Scarti:
    def __init__(self):
        self._pile = []

    def aggiungi(self, carta: Carta):
        """Aggiunge una carta girata agli scarti."""
        self._pile.append(carta)

    def prendi(self):
        """Ritorna e rimuove l'ultima carta girata, o None se vuoto."""
        return self._pile.pop() if self._pile else None

    def ultima(self):
        """Ritorna l'ultima carta girata senza rimuoverla."""
        return self._pile[-1] if self._pile else None

    def vuoto(self) -> bool:
        return not self._pile
    
    def tutte(self):
        """Ritorna una lista di tutte le carte presenti (per ricarica)."""
        return self._pile.copy()
    
    def svuota(self):
        """Svuota lo scarto, restituendo le carte (in ordine inverso per la ricarica)."""
        carte = list(reversed(self._pile))
        self._pile.clear()
        return carte
    
    def rimuovi(self, carta: Carta):
        if carta in self._pile:
            self._pile.remove(carta)

    def __len__(self):
        return len(self._pile)

# pila.py
from abc import ABC, abstractmethod
class Pila(ABC):
    def __init__(self):
        self.carte = []

    def aggiungi(self, carta: Carta):
        self.carte.append(carta)

    def rimuovi(self):
        return self.carte.pop() if self.carte else None

    def cima(self):
        return self.carte[-1] if self.carte else None

    def __len__(self):
        return len(self.carte)

    def __iter__(self):
        """Permette: for carta in pila"""
        return (c for c in self.carte)

    @abstractmethod
    def può_aggiungere(self, carta: Carta) -> bool:
        """Da implementare nelle sottoclassi"""
        pass

# colonna.py
class Colonna(Pila):
    def __init__(self):
        super().__init__()

    def carte_scoperte(self):
        """Generatore di sole carte scoperte nella colonna"""
        for carta in self.carte:
            if not carta.coperta:
                yield carta

    def può_aggiungere(self, carta: Carta) -> bool:
        """Regola: colore alternato, valore decrescente"""
        cima = self.cima()
        if cima is None:
            return carta.valore == 13  # Solo Re su colonna vuota
        colori_opposti = self.colore(carta) != self.colore(cima)
        valore_corretto = carta.valore == cima.valore - 1
        return colori_opposti and valore_corretto
    
    def prendi_sequenza(self, carta):
        # Controlla se la carta è tra quelle scoperte
        carte_scoperte = list(self.carte_scoperte())
        if carta not in carte_scoperte:
            raise ValueError(f"La carta {carta} non è tra quelle scoperte.")
        idx = self.carte.index(carta)
        sequenza = self.carte[idx:]
        self.carte = self.carte[:idx]
        return sequenza

    @staticmethod
    def colore(carta: Carta):
        """Ritorna 'rosso' o 'nero'"""
        if carta.seme in ['cuori', 'quadri']:
            return 'rosso'
        return 'nero'

# fondazione.py
class Fondazione(Pila):
    def __init__(self, seme):
        super().__init__()
        self.seme = seme

    def può_aggiungere(self, carta: Carta) -> bool:
        """Aggiungi una carta solo se è la successiva per seme"""
        cima = self.cima()
        if cima is None:
            return carta.valore == 1  # Solo Asso altrimenti la pila è vuota
        return carta.valore == cima.valore + 1 and carta.seme == self.seme

    def __str__(self):
        return f"Fondazione {self.seme} - Cima: {self.cima() if self.carte else 'Vuota'}"

