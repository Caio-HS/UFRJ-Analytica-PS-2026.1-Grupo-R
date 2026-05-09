# Relatório de Desenvolvimento — Simulação Monte Carlo de Conectividade por Ônibus no Rio de Janeiro

## Objetivo

O projeto teve como objetivo construir uma estimativa espacial de acessibilidade por ônibus na cidade do Rio de Janeiro a partir de dados reais de GPS da frota urbana.

A ideia central foi estimar, para diferentes pontos da cidade:

> quanto tempo é necessário esperar até aparecer um ônibus que eventualmente alcance outra região da cidade.

O projeto foi desenvolvido sob forte prioridade de agilidade de desenvolvimento, favorecendo:

- simplicidade operacional;
- facilidade de depuração;
- geração rápida de resultados exploratórios.

A precisão metodológica máxima não foi a prioridade principal nesta etapa.

---

# Base de Dados

A base utilizada contém registros de GPS de ônibus urbanos da cidade do Rio de Janeiro e foi obtida a partir do serviço BigQuery, da Google, onde a prefeitura mantem um datalake com os dados da frota de ônibus.

Existiam diversos dados, mas os relevantes que foram obtidos a partir de uma consulta SQL e posteriormente mantidos no meu drive pessoal fora:

- timestamp;
- identificador único do ônibus (`id_veiculo`);
- latitude;
- longitude.

O volume total da base é da ordem de aproximadamente 1GB e representa um dia intero de registros do dia 18/03/2026

---

# Pré-processamento dos Dados

## 1. Conversão espacial

As coordenadas geográficas (latitude/longitude) foram convertidas para um sistema cartesiano aproximado.

### Motivação

O objetivo foi:

- simplificar cálculos espaciais;
- permitir uso de distância euclidiana;
- reduzir complexidade computacional.

### Aproximação utilizada

Foi assumida uma projeção plana local da cidade do Rio de Janeiro.

### Trade-off

**Ganhos**
- simplicidade;
- velocidade;
- cálculo direto de distâncias.

**Perdas**
- precisão geodésica;
- curvatura da Terra;
- pequenas distorções espaciais.

A aproximação foi considerada aceitável devido:
- à escala relativamente pequena da cidade;
- ao ruído natural dos dados de GPS;
- ao caráter exploratório do projeto.

---

## 2. Conversão para inteiros

As coordenadas espaciais foram armazenadas como inteiros.

### Motivação

- reduzir uso de memória;
- acelerar operações;
- simplificar estruturas de dados.

### Trade-off

**Ganhos**
- operações mais rápidas;
- menor uso de RAM.

**Perdas**
- precisão submétrica.

A perda foi considerada irrelevante frente ao raio espacial adotado.

---

## 3. Discretização temporal

Os timestamps foram agrupados em intervalos discretos de 1 minuto.

Estrutura temporal final:

```text
time ∈ [0, 1439]
```

### Motivação

- simplificar a simulação;
- reduzir cardinalidade temporal;
- permitir indexação simples por tempo.

### Trade-off

**Ganhos**
- estrutura simples;
- processamento eficiente;
- loops lineares.

**Perdas**
- perda de precisão temporal fina;
- eventos intra-minuto deixam de ser distinguidos.

---

## 4. Estrutura final dos dados

Os dados passaram a assumir a estrutura:

```text
(time, bus_id, x, y)
```

Foi garantida unicidade do par:

```text
(time, bus_id)
```
Ou seja:
- cada ônibus possui no máximo uma posição por minuto.

**Ganhos**
- Simplicidade no processamento 

**Perdas**
- perda de precisão, pois registros "duplicados" (no mesmo minuto) foram descartadls

---

# Estratégia Computacional

## Carregamento integral em RAM

Toda a base foi carregada em memória principal.

### Motivação

- eliminar custo de IO;
- simplificar arquitetura;
- acelerar buscas.

### Trade-off

**Ganhos**
- acesso rápido;
- implementação simples;
- menor complexidade arquitetural.

**Perdas**
- menor escalabilidade;
- maior consumo de RAM.

A decisão foi considerada aceitável devido:
- ao tamanho manejável da base;
- ao ambiente limitado.

---

## Estrutura temporal

Os dados foram organizados como:

```python
dados_por_tempo[tempo] -> lista de ônibus
```

### Motivação

- acesso temporal O(1);
- simplicidade;
- boa localidade de memória.

### Trade-off

**Ganhos**
- implementação simples;
- baixo overhead estrutural.

**Perdas**
- ausência de indexação espacial;
- necessidade de varreduras lineares.

---

## Ausência de indexação espacial sofisticada

O projeto deliberadamente não utilizou:
- KD-trees;
- R-trees;
- GIS especializado;
- grids espaciais sofisticados.

### Motivação

Priorizar:
- simplicidade;
- rapidez de implementação;
- facilidade de depuração.

### Trade-off

**Ganhos**
- baixo tempo de desenvolvimento;
- código compacto;
- menos dependências.

**Perdas**
- perda significativa de eficiência espacial.

---

# Modelagem da Simulação

## Objetivo operacional

A simulação NÃO mede:
- tempo de viagem entre A e B.

Ela mede:

> quanto tempo é necessário esperar até surgir, em A, um ônibus que eventualmente alcance B.

---

# Algoritmo Inicial

A primeira versão:

1. encontrava o primeiro ônibus que aparecia em A;
2. acompanhava esse ônibus até verificar se chegava em B.

## Problema identificado

Esse modelo falhava porque:
- o primeiro ônibus encontrado podia não possuir conectividade com B;
- ônibus posteriores poderiam fornecer conexão válida rapidamente.

Isso gerava falsos negativos relevantes.

---

# Modelo Final da Simulação

A versão final passou a operar da seguinte forma:

1. escolhe-se:
   - ponto A;
   - ponto B;
   - instante inicial `t0`;

2. a simulação avança temporalmente;

3. todos os ônibus que entram em A são registrados;

4. continuamente verifica-se se algum ônibus previamente registrado em A alcança B;

5. quando isso ocorre:
   - escolhe-se o ônibus que entrou mais cedo em A;
   - calcula-se:

```text
tempo_espera =
tempo_entrada_em_A - t0
```

---

# Estrutura Auxiliar

Foi utilizada a estrutura:

```python
onibus_em_A = {
    bus_id: tempo_entrada
}
```

### Motivação

- evitar duplicações;
- busca O(1);
- simplicidade.

---

# Escolha dos Pontos Espaciais

## Problema inicial

Amostragem espacial uniforme produzia:
- muitos pontos em regiões sem infraestrutura;
- oceano;
- montanhas;
- áreas sem cobertura de ônibus.

Resultado:
- maioria das simulações retornava falha (`None`).

---

# Estratégia adotada

Os pontos passaram a ser gerados:
- a partir da posição real de ônibus;
- adicionando pequeno ruído espacial aleatório.

### Motivação

Utilizar implicitamente a própria densidade da frota como:
- máscara urbana;
- estimador de relevância espacial.

### Trade-off

**Ganhos**
- remoção de áreas irrelevantes;
- aumento da taxa de sucesso;
- distribuição urbana mais plausível.

**Perdas**
- perda de amostragem espacial uniforme.

---

# Restrição de distância

Foi imposta uma distância máxima aproximada de 20km entre A e B.

### Motivação

- evitar trajetos extremamente improváveis;
- aumentar taxa de sucesso;
- melhorar plausibilidade operacional.

### Trade-off

**Ganhos**
- redução de casos absurdos;
- maior conectividade observável.

**Perdas**
- exclusão de viagens muito longas.

---

# Definição do Raio Espacial

Foi utilizado raio de captura espacial da ordem de centenas de metros.

### Motivação

Representar:
- distância caminhável;
- tolerância ao ruído de GPS;
- aproximação espacial razoável.

### Trade-off

**Ganhos**
- robustez espacial;
- maior tolerância ao ruído.

**Perdas**
- perda de precisão espacial local.

---

# Paralelização

As simulações foram executadas independentemente em múltiplas máquinas.

### Motivação

O problema possui natureza:
- embaraçosamente paralelizável.

Cada experimento:
- é independente;
- não requer sincronização.

### Trade-off

**Ganhos**
- escalabilidade quase linear;
- simplicidade operacional.

**Perdas**
- duplicação de memória;
- ausência de compartilhamento inteligente.

---

# Geração do Heatmap

## Objetivo

Construir uma visualização espacial dos tempos médios de espera.

---

# Discretização espacial do mapa

O Rio de Janeiro foi discretizado em células de aproximadamente:

```text
2km × 2km
```

Grid aproximado:
- 40 × 20 células.

### Motivação

- estabilizar estatísticas;
- evitar excesso de vazios;
- produzir visualização legível.

### Trade-off

**Ganhos**
- maior densidade estatística;
- visualização mais robusta.

**Perdas**
- perda de resolução fina.

---

# Agregação

Para cada célula:
- calcula-se a média dos tempos dos pontos contidos nela.

---

# Interpolação local

Células sem dados utilizam interpolação local baseada nas vizinhas.

Kernel adotado:

```text
1 2 1
2 X 2
1 2 1
```

### Motivação

- suavizar buracos;
- evitar visualização excessivamente esparsa.

### Trade-off

**Ganhos**
- continuidade visual;
- redução de ruído.

**Perdas**
- introdução de informação inferida;
- perda parcial de fidelidade local.

### Mitigações adotadas

- apenas uma rodada de interpolação;
- células com dados reais permanecem intactas;
- células totalmente isoladas permanecem nulas.

---

# Considerações Finais

O projeto priorizou:
- simplicidade;
- agilidade de desenvolvimento;
- geração rápida de resultados exploratórios.

Diversas escolhas sacrificaram:
- precisão geodésica;
- sofisticação estatística;
- escalabilidade ideal.

Em contrapartida, foi possível construir rapidamente uma pipeline funcional de análise espacial urbana baseada em dados reais de GPS de ônibus.




