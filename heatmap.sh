#!/bin/bash

set -e

BASE=$1


python contagem.py "$BASE"

python dimensoes.py "$BASE"

python preprocessamento.py "$BASE"

python limpador.py "$BASE"

python simulador.py "$BASE"

python grid.py "$BASE"

python heatmap.py "$BASE"
