import csv
import math
from datetime import datetime
import sys

inputFile = sys.argv[1]
inputExtension = ".csv"
outputExtension = "_metrico.csv"
inputFilename = inputFile + inputExtension
outputFilename = inputFile + outputExtension

# Constantes para conversão
MIN_LAT = -23.06705
MAX_LAT = -22.69617
MIN_LON = -43.8092
LAT_MEDIA = (MAX_LAT + MIN_LAT) / 2.0

METROS_POR_GRAU_LAT = 111320
METROS_POR_GRAU_LON = 111320 * math.cos(math.radians(LAT_MEDIA))

def latlon_para_xy(lat, lon):
    x = int((lon - MIN_LON) * METROS_POR_GRAU_LON)
    y = int((lat - MIN_LAT) * METROS_POR_GRAU_LAT)
    return x, y

data = []

# 1. Leitura e Processamento
with open(inputFilename, mode='r', encoding='utf-8') as inputFile:
    csv_reader = csv.reader(inputFile)
    header = next(csv_reader)

    for line in csv_reader:
        if not line:
            continue
        
        try:
            timestamp = line[0]
            bus_id = line[1]
            latitude = float(line[2])
            longitude = float(line[3])

            x, y = latlon_para_xy(latitude, longitude)
            
            # Converte para objeto datetime e discretiza em minutos
            time_obj = datetime.fromisoformat(timestamp)
            discrete_time = int(time_obj.timestamp() // 60)
            
            # Adicionamos como lista para poder editar o tempo depois
            data.append([discrete_time, bus_id, x, y])
        except (ValueError, IndexError):
            continue

# 2. Ordenação e Normalização do Tempo
if data:
    data.sort()  # Ordena pelo primeiro elemento (discrete_time)
    
    min_time = data[0][0]

    for row in data:
        row[0] = row[0] - min_time # Normaliza: o mais antigo vira 0

    max_time = data[-1][0]
    print(f"O maior tempo e {max_time}")

# 3. Escrita do Resultado
with open(outputFilename, mode='w', encoding='utf-8', newline='') as outputFile:
    writer = csv.writer(outputFile)
    writer.writerow(["time", "id_veiculo", "x", "y"])
    
    for row in data:
        writer.writerow(row)




"""
#Esse e o meu codigo original, so que ele esta feio e com identacao errada, entao o gemini deu um help
import csv
import math
from datetime import datetime

inputFilename = "GPS_18-03-26_dia-inteiro.csv"
outputFilename = "GPS_18-03-26_dia-inteiro_metrico.csv"


MIN_LAT = -23.06705
MAX_LAT = -22.69617
MIN_LON = -43.8092
LAT_MEDIA = (MAX_LAT + MIN_LAT)/2.0

METROS_POR_GRAU_LAT = 111_320
METROS_POR_GRAU_LON = (
    111_320 * math.cos(math.radians(LAT_MEDIA))
)

def latlon_para_xy(lat, lon):
    x = int((lon - MIN_LON) * METROS_POR_GRAU_LON)
    y = int((lat - MIN_LAT) * METROS_POR_GRAU_LAT)
    return x, y

data = []

with open(outputFilename, mode='w', encoding='utf-8', newline='') as outputFile:
	with open(inputFilename, mode='r', encoding='utf-8') as inputFile:
		csv_reader = csv.reader(inputFile)
        next(csv_reader)

        for line in csv_reader:
            if not line:
                continue
            
            timestamp = line[0]
            bus_id = line[1]
            
            latitude = float(line[2])
            longitude = float(line[3])

            x, y = latlon_para_xy(latitude, longitude)
            
            time = datetime.fromisoformat(timestamp)
            discrete_time = int(time.timestamp() // 60)
            
            data.append([discrete_time, bus_id, x, y])
            
    writer = csv.writer(outputFile)
    writer.writerow(["time","id_veiculo", "x", "y"])
    
    data.sort()
    
    MIN_TIME = data[0][0]
    
    for line in data:
		line[0] = line[0] - MIN_TIME
    
	for discrete_time, bus_id, x, y in data:
		writer.writerow([discrete_time, bus_id, x, y])
		
	print(f"O Menor tempo e {MIN_TIME}")
		
		
            
 """