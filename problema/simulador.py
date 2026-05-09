import random
import math
import csv

import sys

inputFile = sys.argv[1]
inputExtension = "_preprocessado.csv"
outputExtension = "_datapoints.csv"
inputFilename = inputFile + inputExtension
outputfile = inputFile + outputExtension

results = []

samples = 5000

NOISE = 500

MAX_WAIT = 300

DIST_MAX = 20_000
DIST_MAX2 = DIST_MAX * DIST_MAX

DUMP_FREQUENCE = 100

RADIUS = 300
RADIUS2 = RADIUS * RADIUS

MAX_X = 82902
MAX_Y = 41286

MAX_TIME = 1440

def generate_point(data_per_time):

    time = random.randint(0, MAX_TIME - 1)

    record = data_per_time[time]

    id_veiculo, base_x, base_y = random.choice(record)

    x = base_x + random.randint(-NOISE, NOISE)
    y = base_y + random.randint(-NOISE, NOISE)

    return x, y
    
def generate_A_B(data_per_time):

    ax, ay = generate_point(data_per_time)
    while True:

        bx, by = generate_point(data_per_time)

        dist2 = distance2(ax, ay, bx, by)

        if dist2 <= DIST_MAX2:

            return ax, ay, bx, by

def load_data_per_time(csv_path):
    
    data_per_time = {}
    
    with open(csv_path, newline="", encoding="utf-8") as file:
        
        reader = csv.reader(file)
        
        next(reader)
        
        for line in reader:
            
            time = int(float(line[0]))
            id_veiculo = line[1]
            x = int(float(line[2]))
            y = int(float(line[3]))
            
            if time not in data_per_time:
                data_per_time[time] = []
        
            data_per_time[time].append([id_veiculo, x, y])
    
    return data_per_time
            

def distance2(x1, y1, x2, y2):

    dx = x1 - x2
    dy = y1 - y2

    return dx*dx + dy*dy


def simulation(data_per_time):
    
    init_time = random.randint(0, MAX_TIME - 1)

    ax, ay, bx, by = generate_A_B(data_per_time)
    
    onibus_em_A = {}
    
    for time in range(init_time, MAX_TIME):
        
        if time - init_time > MAX_WAIT:
            return None
            
        if time not in data_per_time:
            continue
            
        candidatos_B = []
        
        record = data_per_time[time]
        
        for id_veiculo, x, y in record:
            
            if distance2(x, y, ax, ay) <= RADIUS2:
                
                if id_veiculo not in onibus_em_A:
                    
                    onibus_em_A[id_veiculo] = time
                    
            if distance2(x,y, bx, by) <= RADIUS2:
                
                if id_veiculo in onibus_em_A:
                    
                    candidatos_B.append(id_veiculo)
        
        
        if candidatos_B:
            
            best = min(candidatos_B, key=lambda bus: onibus_em_A[bus])
            
            wait_time = onibus_em_A[best] - init_time
            
            return (ax, ay, init_time, wait_time)
            
    return None
    
data = load_data_per_time(inputFilename)

if data:
    
    with open(outputfile, mode='w', newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["x", "y", "tempo", "tempo_espera"])

        for i in range(1, samples + 1):
            r = simulation(data)
            if r is not None:
                results.append(r)
				
            if r is None:
                print("Nenhuma rota encontrada")

            if i % DUMP_FREQUENCE == 0:
                if results:
                    writer.writerows(results)
                    results = []
            
            print(f"Progresso: {i}/{samples} amostras processadas.")
