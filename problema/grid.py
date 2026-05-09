# MAO FORTE DO CHATGPT NESSE KERNEL, EU PENSEI OS PESOS E ENTENDI, MAS ELE MONTOU O CODIGO
import csv
import sys

inputFile = sys.argv[1]
inputExtension = "_datapoints.csv"
outputExtension1 = "_grid.csv"
outputExtension1 = "_grid_interpolado.csv"
INPUT_FILENAME = inputFile + inputExtension
OUTPUT_FILENAME_1 = inputFile + outputExtension1
OUTPUT_FILENAME_1 = inputFile + outputExtension2

# --- CONSTANTES GERAIS ---
CELL = 2000
MAX_X = 82902
MAX_Y = 41286

GRID_W = MAX_X // CELL
GRID_H = MAX_Y // CELL

# Pesos para o kernel 3x3 ao redor da célula
PESOS = [
    (-1, -1, 1), ( 0, -1, 2), ( 1, -1, 1),
    (-1,  0, 2),              ( 1,  0, 2),
    (-1,  1, 1), ( 0,  1, 2), ( 1,  1, 1),
]

def processar_csv(filename):
    """Lê o CSV original, processa as coordenadas e retorna o grid inicial com as médias."""
    soma = [[0 for _ in range(GRID_W)] for _ in range(GRID_H)]
    contagem = [[0 for _ in range(GRID_W)] for _ in range(GRID_H)]
    grid = [[None for _ in range(GRID_W)] for _ in range(GRID_H)]

    with open(filename, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Pula o cabeçalho

        for row in reader:
            x = float(row[0])
            y = float(row[1])
            tempo = float(row[3])

            cx = int(x // CELL)
            cy = int(y // CELL)

            # Verifica se está dentro dos limites do grid
            if 0 <= cx < GRID_W and 0 <= cy < GRID_H:
                soma[cy][cx] += tempo
                contagem[cy][cx] += 1

    # Calcula a média em cada célula que recebeu dados
    for y in range(GRID_H):
        for x in range(GRID_W):
            if contagem[y][x] > 0:
                grid[y][x] = soma[y][x] / contagem[y][x]

    return grid


def interpolar_grid(grid_original):
    """Retorna um novo grid aplicando a interpolação nas células vazias."""
    # Cria uma cópia rasa das linhas do grid original
    grid_novo = [row[:] for row in grid_original]

    for y in range(GRID_H):
        for x in range(GRID_W):
            
            # Só interpola onde está vazio; o resto já foi copiado acima
            if grid_original[y][x] is not None:
                continue

            soma_valores = 0
            soma_pesos = 0

            for dx, dy, peso in PESOS:
                nx = x + dx
                ny = y + dy

                # Garante que o vizinho existe no limite do grid
                if 0 <= nx < GRID_W and 0 <= ny < GRID_H:
                    valor = grid_original[ny][nx]
                    if valor is not None:
                        soma_valores += valor * peso
                        soma_pesos += peso

            # Se achou pelo menos um vizinho com valor, calcula a média ponderada
            if soma_pesos > 0:
                grid_novo[y][x] = soma_valores / soma_pesos

    return grid_novo


def salvar_grid_csv(filename, grid):
    """Salva o grid em um arquivo CSV, convertendo valores nulos para -1."""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["cell_x", "cell_y", "value"])

        for y in range(GRID_H):
            for x in range(GRID_W):
                valor = grid[y][x]
                
                # Células sem valor viram -1
                if valor is None:
                    valor = -1
                    
                writer.writerow([x, y, valor])


def main():
    print("Processando pontos do GPS...")
    grid_bruto = processar_csv(INPUT_FILENAME)

    print("Calculando interpolação...")
    grid_interpolado = interpolar_grid(grid_bruto)

    print("Exportando os resultados para CSV...")
    salvar_grid_csv(OUTPUT_FILENAME_1, grid_bruto)
    salvar_grid_csv(OUTPUT_FILENAME_2, grid_interpolado)
    
    print("Concluído!")


if __name__ == "__main__":
    main()