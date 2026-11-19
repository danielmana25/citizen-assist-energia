# Cálculos e comparação das alternativas

**Problema comum:** reduzir a conta de luz da mesma residência.
**Período de referência comum:** 12 meses (economia anual) e horizonte de 10 anos (ganho líquido).
**Alternativas:** A) LED no lugar de fluorescentes (eficiência energética) e B) sistema solar fotovoltaico (fonte renovável).

Todos os valores abaixo são reproduzidos por `python main.py --demo` e conferidos em `tests/test_calculos.py`.

## 1. Conceitos usados

| Conceito | Fórmula | Unidade |
|---|---|---|
| Energia | E = P x t / 1000 | kWh (P em W, t em horas) |
| Custo | R$ = E x tarifa | R$ |
| Tarifa final | (tarifa sem tributos + bandeira) / (1 - tributos) | R$/kWh |
| Eficiência luminosa | lúmens / watts | lm/W |
| Geração solar | kWp x irradiação x PR x dias | kWh/mês |
| Emissões | E x fator de emissão da rede | kgCO2 |

## 2. Tarifa

- Tarifa média das distribuidoras sem tributos: **R$ 0,839/kWh** (ANEEL, R1).
- Bandeira verde em novembro/2026: **R$ 0,00** (R2).
- Tributos (ICMS 18% + PIS/COFINS ~4%): **22%**, estimado (R3).
- Tarifa final = 0,839 / (1 - 0,22) = **R$ 1,0756/kWh**.

Os tributos são cobrados "por dentro" do preço, por isso se divide por (1 - 0,22) em vez de multiplicar por 1,22.

## 3. Consumo da residência exemplo (dados estimados)

Perfil: família de 3 pessoas. Potências e horas de uso são típicas (tipo `estimado` em `dados/equipamentos_residencia.csv`).

| Equipamento | P (W) | h/dia | dias/mês | kWh/mês | % |
|---|---:|---:|---:|---:|---:|
| Chuveiro elétrico (3 pessoas x 8 min) | 5.500 | 0,40 | 30 | 66,0 | 34 |
| Geladeira Procel A (~300 L) | 55 | 24 | 30 | 39,6 | 20 |
| Fluorescente compacta x10 | 15 | 5 | 30 | 22,5 | 12 |
| TV LED 40" | 80 | 5 | 30 | 12,0 | 6 |
| Notebook | 60 | 6 | 30 | 10,8 | 6 |
| Roteador e carregadores | 15 | 24 | 30 | 10,8 | 6 |
| Ventilador | 80 | 4 | 30 | 9,6 | 5 |
| Micro-ondas | 1.200 | 0,25 | 30 | 9,0 | 5 |
| Ferro de passar | 1.000 | 1 | 8 | 8,0 | 4 |
| Máquina de lavar | 500 | 1 | 12 | 6,0 | 3 |
| **Total** | | | | **194,3** | 100 |

- Exemplo de conta: chuveiro = 5.500 W x 0,4 h x 30 dias / 1000 = 66 kWh/mês.
- **Conta estimada:** 194,3 kWh x R$ 1,0756 = **R$ 209,00/mês**.
- Verificação de coerência: o consumo residencial médio do Brasil foi 181,8 kWh/mês em agosto/2026 (EPE, R1), e a geladeira (20%) e a iluminação (12%) ficam nas faixas publicadas (R4, R5).
- Maior consumidor: o chuveiro. Cada minuto a menos em cada banho = 5,5 kW x (1/60) h x 3 pessoas x 30 dias = **8,25 kWh/mês (R$ 8,87)**.

## 4. Alternativa A — LED (eficiência energética)

Mesma luz (cerca de 800 lm), menos potência (R5): fluorescente compacta de 15 W por LED de 9 W.

| Item | Conta | Resultado |
|---|---|---|
| Consumo antes | 10 x 15 W x 5 h x 30 / 1000 | 22,5 kWh/mês |
| Consumo depois | 10 x 9 W x 5 h x 30 / 1000 | 13,5 kWh/mês |
| Economia | 22,5 - 13,5 | **9,0 kWh/mês** |
| Economia em R$ | 9,0 x 1,0756 | **R$ 9,68/mês** (R$ 116,17/ano) |
| Eficiência luminosa | 800/15 e 800/9 | 53,3 -> 88,9 lm/W |
| Custo | 10 x R$ 6,00 | **R$ 60,00** |
| Retorno | 60 / 9,68 | **6,2 meses** |
| Ganho líquido em 10 anos | 9,68 x 120 - 60 | **R$ 1.101,69** |
| Vida útil | 25.000 h / (5 h x 365) | 13,7 anos (uma compra cobre os 10 anos) |
| CO2 evitado | 108 kWh/ano x 0,0385 | 4,2 kgCO2/ano |

## 5. Alternativa B — Solar fotovoltaico (fonte renovável)

**Dimensionamento**

| Item | Conta | Resultado |
|---|---|---|
| Geração de 1 kWp | 4,6 x 0,75 x 30,4 | 104,9 kWh/mês |
| Consumo a cobrir | 194,3 - 50 (custo de disponibilidade) | 144,3 kWh/mês |
| kWp mínimo | 144,3 / 104,9 | 1,38 kWp |
| Módulos de 550 Wp | 1.376 Wp / 550 = 2,5, arredonda para cima | 3 módulos = **1,65 kWp** |
| Geração | 1,65 x 104,9 | 173,1 kWh/mês (cobre 74% do consumo) |
| Custo | 1.650 Wp x R$ 2,84 | **R$ 4.686,00** |

**Economia** (energia compensada = 144,3 kWh; 70% é injetada na rede e 30% consumida na hora, estimado)

| Item | Fio B 2026 (60%) | Fio B 2028 (90%) |
|---|---:|---:|
| Crédito bruto: 144,3 x 1,0756 | R$ 155,21 | R$ 155,21 |
| Fio B: 144,3 x 0,70 x % x (0,28 x 1,0756) | R$ 18,25 | R$ 27,38 |
| **Economia por mês** | **R$ 136,96** | **R$ 127,84** |
| Economia por ano | R$ 1.643,54 | R$ 1.534,02 |
| Retorno: 4.686 / economia | 34,2 meses | 36,7 meses |
| Ganho líquido em 10 anos | R$ 11.749,41 | R$ 10.654,21 |
| CO2 evitado: 1.732 kWh/ano x 0,0385 | 66,7 kgCO2/ano | 66,7 kgCO2/ano |

O Fio B sobe de 60% (2026) para 75% (2027) e 90% (2028) pela Lei 14.300 (R8); por isso mostramos os dois extremos.

## 6. Comparação final

| | LED | Solar (2026) | Solar (2028) |
|---|---:|---:|---:|
| Custo inicial | R$ 60,00 | R$ 4.686,00 | R$ 4.686,00 |
| Economia por mês | R$ 9,68 | R$ 136,96 | R$ 127,84 |
| Retorno | 6,2 meses | 34,2 meses | 36,7 meses |
| Ganho líquido em 10 anos | R$ 1.101,69 | R$ 11.749,41 | R$ 10.654,21 |
| kWh evitados por ano | 108 | 1.732 | 1.732 |
| CO2 evitado | 4,2 kg/ano | 66,7 kg/ano | 66,7 kg/ano |

## 7. Sensibilidade (solar, Fio B 2028)

Mostra o quanto as premissas estimadas mudam o resultado. O retorno fica entre 2,6 e 3,4 anos, então a conclusão não depende de um valor exato.

| Variação | Economia/mês | Retorno |
|---|---:|---:|
| Base | R$ 127,84 | 3,1 anos |
| Preço R$ 2,45/Wp (média nacional 2026) | R$ 127,84 | 2,6 anos |
| Tarifa sem tributos -10% | R$ 115,05 | 3,4 anos |
| Tarifa sem tributos +10% | R$ 140,62 | 2,8 anos |
| Bandeira vermelha 1 | R$ 134,64 | 2,9 anos |
| Simultaneidade 50% | R$ 135,66 | 2,9 anos |
| Fio B = 40% da tarifa | R$ 116,10 | 3,4 anos |
| Ligação monofásica (30 kWh) | R$ 145,55 | 2,7 anos |

A irradiação de 4,5 kWh/m²/dia (limite inferior da faixa publicada) não muda a economia, porque os 3 módulos já geram mais (cerca de 169 kWh) do que os 144 kWh a compensar. Como o dimensionamento arredonda para cima, há folga.

## 8. O que não foi considerado

Reajuste futuro da tarifa, perda de rendimento dos módulos ao longo dos anos, troca do inversor, financiamento, créditos de energia excedentes (cerca de 29 kWh/mês de sobra) e emissões de fabricação. Uns aumentam a economia (reajustes da tarifa) e outros diminuem (perda de rendimento, troca do inversor, juros de financiamento); por isso o retorno deve ser lido como ordem de grandeza, não como valor exato.
