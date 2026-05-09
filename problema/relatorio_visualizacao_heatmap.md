# Relatório de Desenvolvimento — Visualização e Heatmap

## Objetivo

O objetivo da etapa de visualização foi transformar os resultados das simulações de Monte Carlo em uma representação espacial interpretável da acessibilidade do sistema de ônibus da cidade do Rio de Janeiro.

O produto final desejado foi um heatmap sobreposto a um mapa real da cidade, representando espacialmente o tempo médio de espera para obtenção de uma rota válida segundo os critérios definidos na simulação.

# Estrutura dos Dados de Entrada

A simulação produziu um conjunto de pontos contendo:

```text
x, y, tempo_inicial, tempo_espera
```

Onde:
- `x` e `y` representam coordenadas cartesianas em metros;
- `tempo_espera` representa o tempo necessário até encontrar um ônibus que posteriormente alcança o ponto de destino.

Os dados já estavam:
- convertidos para sistema métrico cartesiano;
- discretizados temporalmente;
- normalizados em relação ao espaço da cidade.

# Decisão 1 — Representação Espacial Discretizada

## Escolha

A cidade foi discretizada em uma grade regular de células quadradas de:

```text
2km × 2km
```

Resultando em aproximadamente:

```text
40 × 20 células
```

## Motivação

A escolha foi motivada por:
- baixa densidade relativa de amostras;
- necessidade de estabilidade visual;
- simplicidade computacional;
- rapidez de implementação.

Uma resolução espacial muito fina produziria:
- muitas células vazias;
- ruído visual;
- baixa confiabilidade estatística.

## Trade-off

### Ganhos
- estabilidade visual;
- redução de ruído;
- implementação simples;
- custo computacional baixo.

### Perdas
- perda de resolução espacial fina;
- incapacidade de observar microestruturas urbanas.

# Decisão 2 — Agregação por Média

## Escolha

Cada célula armazenou:
- soma dos tempos observados;
- quantidade de observações.

O valor final da célula foi definido como:

```text
média dos tempos de espera
```

## Motivação

A média foi escolhida por:
- simplicidade;
- interpretabilidade;
- facilidade de implementação.

# Decisão 3 — Interpolação Local

## Problema

Grande parte das células permaneceu vazia devido:
- à natureza aleatória da amostragem;
- à baixa densidade de pontos;
- à existência de áreas urbanas pouco cobertas.

## Escolha

Foi implementada uma interpolação local baseada apenas nas células adjacentes imediatas.

Kernel utilizado:

```text
1 2 1
2 X 2
1 2 1
```

Onde:
- vizinhos ortogonais possuem peso 2;
- vizinhos diagonais possuem peso 1.

## Regras da Interpolação

- apenas células vazias eram interpoladas;
- células reais nunca eram modificadas;
- apenas uma rodada de interpolação era executada;
- vizinhos vazios eram ignorados;
- células sem vizinhos válidos permaneciam nulas.

## Motivação

A abordagem buscou:
- suavizar descontinuidades visuais;
- evitar propagação excessiva de informação;
- manter o algoritmo simples e rápido.

# Decisão 4 — Representação de Células Nulas

## Escolha

Células sem informação permaneceram marcadas como:

```text
-1
```

durante exportação CSV.

Na renderização:
- valores nulos foram convertidos para transparência.

# Decisão 5 — Overlay em Mapa Real

## Escolha

O heatmap foi renderizado sobre uma imagem real da cidade do Rio de Janeiro.

A imagem foi utilizada apenas como referência visual de fundo.

## Motivação

A sobreposição sobre mapa real melhora:
- interpretabilidade;
- reconhecimento urbano;
- leitura espacial humana.

## Abordagem Escolhida

Foi utilizada uma estratégia pragmática:
- alinhamento manual da imagem;
- uso do mesmo sistema cartesiano local;
- ausência de georreferenciamento formal.

# Decisão 6 — Saturação da Escala de Cor

## Problema

Outliers elevados:
- comprimiam visualmente os demais valores;
- tornavam o mapa pouco legível.

## Escolha

Foi aplicada saturação da escala de cores utilizando:
- limites máximos fixos;
ou:
- percentis do conjunto de dados.

## Motivação

O objetivo foi:
- aumentar contraste visual;
- reduzir impacto de valores extremos;
- melhorar leitura dos gradientes urbanos.

# Decisão 7 — Pipeline Automatizada

## Escolha

Todo o processo foi estruturado como uma pipeline sequencial automatizada via scripts Python e Bash.

Cada etapa:
- recebe um arquivo de entrada;
- produz um arquivo de saída padronizado.

## Motivação

A automação buscou:
- reprodutibilidade;
- redução de intervenção manual;
- rapidez operacional.

# Considerações Finais

A etapa de visualização priorizou:
- simplicidade;
- rapidez de desenvolvimento;
- interpretabilidade visual;
- viabilidade prática.

Diversas decisões abriram mão de:
- rigor geoespacial formal;
- modelagem estatística sofisticada;
- arquitetura de software complexa.

Em troca, foi obtido:
- um sistema funcional;
- reproduzível;
- computacionalmente viável;
- capaz de produzir representações espaciais úteis em curto prazo de desenvolvimento.
