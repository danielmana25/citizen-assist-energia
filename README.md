# Citizen Assist AI — Módulo de Energia e Sustentabilidade

Global Solution — Ciência da Computação / Turmas 1CC — Soluções em Energias Renováveis e Sustentáveis

## Integrantes

| Nome completo | RM |
|---|---|
| Gustavo Zagato Bottechia | 569420 |
| Davi Q. Zuolo | 571669 |
| Daniel Vilela Mana | 571632 |

Turma: 1CCPK

> **Contribuição de Soluções em Energias Renováveis e Sustentáveis:** todo o código de energia está na pasta `energia/`, os dados em `dados/` e a documentação em `docs/`. O restante do repositório do Citizen Assist AI pertence às demais disciplinas.

## Público e problema

**Público:** moradores de residências urbanas (famílias) que usam o Citizen Assist AI e querem entender e reduzir a conta de luz.

**Necessidade energética:** muita gente não sabe quais aparelhos pesam na conta nem se vale a pena investir em lâmpadas LED ou em energia solar. A ANEEL estimou alta média de 9,4% nas tarifas em 2026 (R13), então decidir bem importa.

**Como o assistente ajuda:** o Citizen Assist AI passa a responder, no terminal, perguntas sobre consumo, mostra de onde vem o gasto, compara alternativas para reduzir a conta (com cálculo, custo e impacto ambiental) e informa as fontes e os limites de cada estimativa.

## Funcionalidades de energia

| Função | O que faz |
|---|---|
| Consumo da residência | Tabela de consumo por aparelho (energia = potência x tempo), custo mensal e maior consumidor |
| Comparar alternativas | LED x solar fotovoltaico: custo, economia, retorno, ganho em 10 anos e CO2 evitado |
| Calcular um aparelho | O usuário informa potência, horas e dias de uso e recebe kWh, R$ e CO2 |
| Perguntar ao assistente | Perguntas em texto livre (ex.: "vale a pena colocar painel solar?") |
| Impacto ambiental | Emissões de CO2 da eletricidade usada |

Toda resposta termina com as **fontes** (códigos R1 a R13, listados em `docs/referencias.md`) e a **atenção** sobre as condições e os limites da estimativa.

## Como executar

Requer apenas Python 3.9 ou superior (só biblioteca padrão, sem instalar nada).

```bash
python main.py                       # menu interativo
python main.py --demo                # demonstração usada no vídeo
python main.py --pergunta "vale a pena colocar painel solar?"
python -m unittest discover tests    # testes dos cálculos
```

No menu, o usuário pode digitar a tarifa da própria fatura (R$/kWh) para trocar a tarifa padrão.

## Como integrar ao Citizen Assist AI do grupo

Copie a pasta `energia/` e a pasta `dados/` para o repositório do assistente e adicione ao menu principal:

```python
from energia.assistente import menu_energia, responder

# opção de menu
elif opcao == "E":
    menu_energia()

# ou, para usar dentro do fluxo de perguntas do assistente
resposta = responder("como reduzir minha conta de luz?")
```

A função `responder(pergunta)` devolve um texto pronto, então também pode ser chamada pelo código do assistente sem usar o menu.

## Estrutura

```
main.py                         executa só o módulo de energia
energia/
  dados.py                      leitura dos CSV
  calculos.py                   energia, potência, eficiência, custo, geração solar, CO2
  comparacao.py                 comparação das alternativas (LED x solar)
  assistente.py                 respostas e menu do Citizen Assist AI
dados/
  parametros.csv                tarifa, preços, irradiação etc. com origem e tipo
  equipamentos_residencia.csv   aparelhos da residência exemplo com potência e uso
tests/test_calculos.py          testes dos cálculos
docs/
  calculos_e_comparacao.md      fórmulas, contas passo a passo e sensibilidade
  justificativas_recomendacoes.md   custos, viabilidade e impactos ambientais
  referencias.md                fontes verificáveis
  testes_com_usuarios.md        roteiro e registro dos testes com usuários
  roteiro_video.md              roteiro do vídeo técnico (até 3 min)
```

## Dados e premissas

Cada valor em `dados/` tem **unidade**, **tipo** (`oficial`, `publicado` ou `estimado`) e **referência**. Os dados `estimado` são premissas do perfil exemplo (família de 3 pessoas, aparelhos e horas de uso típicos) e estão identificados como tal.

**Período considerado:** os consumos são mensais (30 dias de uso, 30,4 dias na geração solar); tarifas e bandeira são de novembro/2026, preços de 2025/2026; a comparação usa 12 meses e horizonte de 10 anos.

## Limitações

- As economias são **estimativas, não garantias**.
- O perfil exemplo não é a casa de ninguém; para um resultado fiel, use a tarifa e o consumo da fatura.
- A tarifa padrão é a média nacional da ANEEL, não a de uma distribuidora específica.
- No solar, o retorno depende do telhado, da aprovação da distribuidora, da troca do inversor e da regra de compensação a partir de 2029 (ainda a definir pela ANEEL).
- As emissões consideram só a eletricidade da rede; fabricação e descarte de painéis e lâmpadas ficam de fora.
