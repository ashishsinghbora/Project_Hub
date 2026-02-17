import sqlite3
import numpy as np
from pathlib import Path
from src.brain import Brain


DB_PATH = Path("training.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS generations (
            generation INTEGER,
            best_fitness REAL
        )
    """)
    conn.commit()
    conn.close()


def save_generation(gen, fitness):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO generations VALUES (?, ?)", (gen, fitness))
    conn.commit()
    conn.close()


def save_best_brain(gen, brain):
    fname = f"best_gen_{gen}.npz"
    np.savez(fname, W1=brain.W1, W2=brain.W2)


def load_best_brain(gen):
    fname = f"best_gen_{gen}.npz"
    if Path(fname).exists():
        data = np.load(fname)
        b = Brain()
        b.W1 = data["W1"]
        b.W2 = data["W2"]
        return b
    return None
