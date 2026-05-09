import csv
import numpy as np
import matplotlib.pyplot as plt
import time

import sys

inputFile = sys.argv[1]
inputExtension = "_grid_interpolado.csv"
outputExtension = ".png"
ARQUIVO_HEATMAP = inputFile + inputExtension
outputFilename = inputFile + "_" + time.time_ns() + outputExtension


CELL = 2000

MAX_X = 82902
MAX_Y = 41286

GRID_W = MAX_X // CELL
GRID_H = MAX_Y // CELL

ARQUIVO_MAPA = "rio.png"


# ============================================================
# CARREGA GRID
# ============================================================

heatmap = np.full(
    (GRID_H, GRID_W),
    np.nan
)

with open(ARQUIVO_HEATMAP, newline="") as f:

    reader = csv.reader(f)

    next(reader)

    for row in reader:

        cell_x = int(row[0])
        cell_y = int(row[1])

        value = float(row[2])

        # -1 = célula nula
        if value == -1:
            continue

        heatmap[GRID_H - 1 - cell_y][cell_x] = value

# ============================================================
# CARREGA MAPA
# ============================================================

mapa = plt.imread(ARQUIVO_MAPA)

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(14, 7))

# mapa de fundo
plt.imshow(
    mapa,
    extent=[0, MAX_X, 0, MAX_Y],
    origin="upper"
)

# heatmap
img = plt.imshow(
    heatmap,

    extent=[0, MAX_X, 0, MAX_Y],

    origin="lower",

    alpha=0.5,

#    cmap="hot",

    vmin = 5,
    vmax = 90
)

# barra lateral
plt.colorbar(
    img,
    label="Tempo médio de espera"
)

# título
plt.title(
    "Heatmap de Tempo Médio de Espera"
)

# remove eixos
plt.xticks([])
plt.yticks([])

# ============================================================
# SALVA E MOSTRA
# ============================================================

plt.savefig(
    outputFile,
    dpi=300,
    bbox_inches="tight"
)

plt.show()