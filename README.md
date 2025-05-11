# 🃏 Solitario Klondike in Python (con GUI)

Benvenuto! Questo è un progetto universitario che riproduce il classico **Solitario Klondike** con un’interfaccia grafica, interamente realizzato in **Python**. È pensato per essere **intuitivo da usare** anche da chi non ha competenze tecniche avanzate.

---

## 📌 Cos'è questo progetto?

Un'applicazione desktop che permette di giocare al Solitario Klondike con **immagini delle carte** e interazioni tramite **mouse e finestre** (niente terminale o comandi testuali).

---

## ⚙️ Tecnologie utilizzate

- **Python 3**
- **pygames** – libreria GUI integrata in Python
- **OOP (Object-Oriented Programming)** – ogni elemento del gioco è modellato come oggetto
- **Immagini PNG** – rappresentazione grafica delle carte da gioco

---

## 📥 Come scaricare e usare il gioco (per principianti)

### 🔽 1. Scarica il gioco
1. Vai in alto su questa pagina GitHub
2. Clicca sul pulsante verde **`Code`**
3. Seleziona **`Download ZIP`**
4. Estrai lo ZIP in una cartella a tua scelta (es. sul Desktop)

### 🐍 2. Installa Python (se non lo hai già)
1. Vai su [python.org/downloads](https://www.python.org/downloads/)
2. Scarica e installa **Python 3**
3. Durante l'installazione, spunta l'opzione **“Add Python to PATH”**

### ▶️ 3. Avvia il gioco
1. Apri la cartella dove hai estratto il progetto
2. Fai **doppio clic su `GUI.py`** (si aprirà la finestra del gioco)

> Se il doppio clic non funziona:
- Apri la cartella
- Fai clic destro su `GUI.py`
- Seleziona **“Apri con > Python”**

---

## 🧠 Obiettivo del gioco

Ordinare tutte le carte in **quattro fondazioni** (una per seme) in ordine crescente, **dall’Asso al Re**, secondo le regole classiche del Solitario Klondike.

---

## 📜 Regole principali

- Il mazzo contiene 52 carte standard
- Le carte sono distribuite in **7 colonne** (solo l’ultima di ogni colonna è scoperta)
- Le restanti carte formano il **Pozzo** (da cui pescare)
- Puoi:
  - Spostare una carta (o una sequenza) tra colonne
  - Inviare carte alle **fondazioni**
  - Pescare una nuova carta dal **Pozzo**
  - Rimescolare il Pozzo quando esaurito

- Le sequenze devono **alternare colori** e avere valori **decrescenti**

---

## 🛠️ Architettura del progetto

Klondike-Solitario/
├── GUI.py # Avvia l'interfaccia grafica del gioco
├── Klondike.py # Entry point e logica generale
├── Logica.py # Gestione regole e struttura del gioco
├── cards/ # Cartella con immagini PNG delle carte
│ ├── 2C.png
│ ├── ...
└── README.md # Questo file


---

## 📚 Classi principali (per sviluppatori)

- `Carta`: rappresenta una singola carta (valore, seme, colore)
- `Mazzo`: gestisce mescolamento, pesca e carte scartate
- `Colonna`: gestisce le carte in gioco (coperte/scoperte)
- `Fondazione`: pila ordinata di carte per seme
- `Gioco`: stato complessivo del gioco
- `GUI`: gestione della finestra, interazioni e visualizzazione

---

## 🎯 Obiettivi didattici del progetto

- Applicare i principi della **programmazione a oggetti**
- Gestire una **GUI interattiva** con Python
- Strutturare un'applicazione in moduli e classi riutilizzabili
- Implementare una logica di gioco complessa ma intuitiva
- Gettare le basi per future espansioni (es. versione web)

---

## 👤 Autore

**Francesco Colasurdo**  
📧 francesco.colasurdo04@gmail.com  
🔗 [LinkedIn](www.linkedin.com/in/francesco-colasurdo)  

---

## 📜 Licenza

Questo progetto è open-source con licenza **MIT**: puoi usarlo, modificarlo e condividerlo liberamente.
