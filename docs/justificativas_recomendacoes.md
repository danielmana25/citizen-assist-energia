# Justificativas das recomendações

O Citizen Assist AI recomenda, nesta ordem: **(1) LED, (2) solar fotovoltaico**, informando sempre custo, viabilidade, impacto ambiental e limites. Os números vêm de `docs/calculos_e_comparacao.md`.

## Recomendação 1 — Trocar fluorescentes por LED

| Critério | Justificativa |
|---|---|
| **Custo** | R$ 60,00 para 10 lâmpadas (R$ 6,00 cada). Economia de R$ 9,68/mês; retorno em cerca de 6 meses. |
| **Viabilidade** | Qualquer morador, inclusive quem aluga, pode fazer sozinho, sem obra nem aprovação da distribuidora. O LED de 9 W entrega a mesma luz (cerca de 800 lm) da fluorescente de 15 W. |
| **Impacto ambiental** | Evita 108 kWh/ano (4,2 kgCO2/ano), ganho pequeno porque a rede brasileira já emite pouco. Ponto positivo: as fluorescentes contêm mercúrio e a troca é uma chance de fazer o descarte correto em ponto de coleta (logística reversa, Lei 12.305/2010). |
| **Limites** | Economia pequena em valor absoluto (iluminação é cerca de 12% do consumo do perfil). LED sem selo de qualidade pode durar menos que as 25.000 h estimadas. |

**Por que é a primeira recomendação:** é a única com retorno em meses, risco baixo e acessível a todos. Eficiência vem antes de geração: gastar menos é mais barato do que produzir mais.

## Recomendação 2 — Solar fotovoltaico (fonte renovável)

| Critério | Justificativa |
|---|---|
| **Custo** | R$ 4.686,00 para 1,65 kWp (3 módulos), usando R$ 2,84/Wp (Greener, 2025). A média nacional de 2026 é R$ 2,45/Wp, que reduziria o custo para cerca de R$ 4.040. |
| **Viabilidade** | Economia de R$ 128 a R$ 137/mês, retorno em 2,9 a 3,1 anos, ganho líquido de R$ 10,7 mil a R$ 11,7 mil em 10 anos. Exige imóvel próprio, telhado sem sombra, aprovação da distribuidora e investimento inicial. |
| **Impacto ambiental** | Gera 1.732 kWh/ano de fonte renovável e evita 66,7 kgCO2/ano. A fabricação e o descarte dos módulos também têm impacto, não incluído na conta. |
| **Limites** | O Fio B (Lei 14.300) reduz a economia a cada ano: 60% em 2026, 75% em 2027, 90% em 2028, com regra a definir pela ANEEL após 2029. O inversor costuma precisar de troca em 10 a 15 anos. O resultado depende de premissas estimadas (simultaneidade, parcela do Fio B), mas a sensibilidade mostra retorno entre 2,6 e 3,4 anos. |

**Por que vem em segundo:** a economia é bem maior que a do LED, mas o investimento é 78 vezes maior (R$ 4.686 contra R$ 60) e a vantagem diminui com a regra do Fio B. Faz mais sentido para quem tem consumo alto e constante e é dono do imóvel.

## Observação sobre o chuveiro

O chuveiro elétrico é o maior consumidor do perfil (34%, 66 kWh/mês). O assistente informa que cada minuto a menos em cada banho economiza 8,25 kWh/mês (R$ 8,87), sem custo. Não entrou como alternativa comparada porque depende de hábito, não de um investimento com preço de mercado a comparar.

## Coerência entre os resultados e as respostas do assistente

As respostas do assistente usam as mesmas funções (`energia/calculos.py` e `energia/comparacao.py`) e os mesmos dados (`dados/`) que esta documentação, então os números não divergem. Isso é verificado em `tests/test_calculos.py`, que confere o consumo (194,3 kWh), a economia do LED (9,0 kWh), o dimensionamento (3 módulos, 1,65 kWp) e a presença de fontes e limitações em todas as respostas.
