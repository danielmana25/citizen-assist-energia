"""Interface de terminal do módulo de Energia do Citizen Assist AI.

Para integrar ao assistente do grupo, basta chamar menu_energia() a partir do menu principal
ou responder(pergunta) para obter a resposta de energia como texto.
"""
import re
import unicodedata

from . import calculos as c
from .comparacao import comparar, cenario_led, cenario_fv
from .dados import carregar_equipamentos, carregar_parametros

AVISO = (
    "Atenção: valores são estimativas com dados do perfil exemplo (3 pessoas) e preços de 2025/2026; "
    "não são garantia de economia. Use a tarifa e o consumo da sua fatura para um resultado mais fiel."
)


# ---------- formatação em português ----------

def brl(valor):
    return "R$ " + f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def num(valor, casas=1):
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def meses_texto(meses):
    if meses < 24:
        return f"{num(meses, 1)} meses"
    return f"{num(meses / 12, 1)} anos ({num(meses, 0)} meses)"


def _normalizar(texto):
    sem_acento = unicodedata.normalize("NFD", texto.lower())
    return "".join(ch for ch in sem_acento if unicodedata.category(ch) != "Mn")


# ---------- respostas do assistente ----------

def texto_consumo(p, eq, tarifa):
    itens = c.consumo_por_equipamento(eq)
    total = sum(i["kwh_mes"] for i in itens)
    linhas = ["CONSUMO DA RESIDÊNCIA EXEMPLO (energia = potência x tempo)", ""]
    linhas.append(f"{'Equipamento':<36}{'W':>7}{'h/dia':>7}{'kWh/mês':>9}{'%':>6}")
    for i in itens:
        nome = i["equipamento"] + (f" x{i['quantidade']}" if i["quantidade"] > 1 else "")
        linhas.append(
            f"{nome:<36}{num(i['potencia_w'], 0):>7}{num(i['horas_dia'], 2):>7}"
            f"{num(i['kwh_mes']):>9}{num(i['kwh_mes'] / total * 100, 0):>6}"
        )
    linhas.append(f"{'TOTAL':<36}{'':>7}{'':>7}{num(total):>9}{'100':>6}")
    linhas += [
        "",
        f"Conta estimada: {num(total)} kWh x {brl(tarifa)}/kWh = {brl(total * tarifa)} por mês.",
        f"Para comparar: o consumo residencial médio do Brasil foi {num(p['consumo_medio_brasil'])} kWh/mês (EPE, ago/2026).",
        f"Maior consumidor: {itens[0]['equipamento']}. Cada minuto a menos em cada banho economiza "
        f"{num(c.kwh_por_minuto_de_banho(eq, p))} kWh/mês ({brl(c.kwh_por_minuto_de_banho(eq, p) * tarifa)}).",
        "Fontes: R1, R3, R4. Os equipamentos e horas de uso são estimados (tipo 'estimado' em dados/).",
        AVISO,
    ]
    return "\n".join(linhas)


def texto_led(p, eq, tarifa):
    r = cenario_led(p, eq, tarifa)
    return "\n".join(
        [
            "ALTERNATIVA A - TROCAR FLUORESCENTES POR LED (eficiência energética)",
            "",
            f"Hoje: {r['quantidade']} lâmpadas de {num(p['lampada_antiga_w'], 0)} W = {num(r['kwh_antes'])} kWh/mês.",
            f"Com LED de {num(p['lampada_led_w'], 0)} W e a mesma luz ({num(p['lampada_lumens'], 0)} lm): {num(r['kwh_depois'])} kWh/mês.",
            f"Eficiência luminosa: {num(r['eficacia_antes'])} lm/W -> {num(r['eficacia_depois'])} lm/W.",
            f"Economia: {num(r['economia_kwh_mes'])} kWh/mês = {brl(r['economia_rs_mes'])}/mês ({brl(r['economia_rs_ano'])}/ano).",
            f"Custo: {r['quantidade']} x {brl(p['lampada_led_preco'])} = {brl(r['custo_inicial'])}. Retorno em {meses_texto(r['payback_meses'])}.",
            f"Ganho líquido em {num(p['horizonte_anos'], 0)} anos: {brl(r['ganho_liquido_horizonte'])}. "
            f"Vida útil estimada: {num(r['vida_util_anos'])} anos de uso.",
            f"Ambiente: evita {num(r['co2_evitado_kg_ano'])} kgCO2/ano (a rede brasileira já é muito renovável, então o ganho é pequeno). "
            "As fluorescentes antigas contêm mercúrio: descarte em ponto de coleta (logística reversa).",
            "Fontes: R5, R11, R12.",
            AVISO,
        ]
    )


def texto_solar(p, eq, tarifa):
    consumo = c.consumo_total_kwh(eq)
    a = cenario_fv(p, consumo, p["fio_b_pct_2026"], tarifa)
    b = cenario_fv(p, consumo, p["fio_b_pct_2028"], tarifa)
    return "\n".join(
        [
            "ALTERNATIVA B - ENERGIA SOLAR FOTOVOLTAICA (fonte renovável)",
            "",
            f"Meta: cobrir {num(a['alvo_kwh_mes'])} kWh/mês (consumo de {num(consumo)} menos {num(p['custo_disponibilidade_kwh'], 0)} kWh de custo de disponibilidade).",
            f"Geração de 1 kWp = {num(p['irradiacao_kwh_m2_dia'])} kWh/m²/dia x {num(p['performance_ratio'], 2)} x {num(p['dias_mes'])} dias = {num(c.producao_fv_kwh_mes(1, p))} kWh/mês.",
            f"Tamanho: {num(a['kwp_minimo'], 2)} kWp necessários -> {a['modulos']} módulos de {num(p['modulo_wp'], 0)} Wp = {num(a['kwp_instalado'], 2)} kWp.",
            f"Geração: {num(a['geracao_kwh_mes'])} kWh/mês (cobre {num(a['cobertura_pct'], 0)}% do consumo).",
            f"Custo: {num(a['kwp_instalado'] * 1000, 0)} Wp x {brl(p['preco_fv_rs_wp'])}/Wp = {brl(a['custo_inicial'])}.",
            f"Economia com Fio B de 2026 ({num(a['fio_b_pct'] * 100, 0)}%): {brl(a['economia_rs_mes'])}/mês. Retorno em {meses_texto(a['payback_meses'])}.",
            f"Economia com Fio B de 2028 ({num(b['fio_b_pct'] * 100, 0)}%): {brl(b['economia_rs_mes'])}/mês. Retorno em {meses_texto(b['payback_meses'])}.",
            f"Ganho líquido em {num(p['horizonte_anos'], 0)} anos (cenário 2028): {brl(b['ganho_liquido_horizonte'])}.",
            f"Ambiente: evita {num(a['co2_evitado_kg_ano'])} kgCO2/ano. A fabricação e o descarte dos módulos também têm impacto.",
            "Fontes: R6, R7, R8, R9, R10, R11.",
            "Limites: depende de telhado sem sombra e com boa orientação, aprovação da distribuidora, troca do inversor (cerca de 10 a 15 anos) "
            "e da regra de compensação após 2029, ainda a definir pela ANEEL.",
            AVISO,
        ]
    )


def texto_comparacao(p, eq, tarifa):
    r = comparar(p, eq, tarifa)
    led, a, b = r["led"], r["fv_2026"], r["fv_2028"]
    linhas = [
        "COMPARAÇÃO: COMO REDUZIR A CONTA DE LUZ (mesma casa, 12 meses e horizonte de 10 anos)",
        "",
        f"Conta atual estimada: {num(r['consumo_kwh_mes'])} kWh/mês = {brl(r['conta_rs_mes'])}/mês (tarifa {brl(r['tarifa'])}/kWh).",
        "",
        f"{'':<22}{'LED':>14}{'Solar (2026)':>15}{'Solar (2028)':>15}",
        f"{'Custo inicial':<22}{brl(led['custo_inicial']):>14}{brl(a['custo_inicial']):>15}{brl(b['custo_inicial']):>15}",
        f"{'Economia por mês':<22}{brl(led['economia_rs_mes']):>14}{brl(a['economia_rs_mes']):>15}{brl(b['economia_rs_mes']):>15}",
        f"{'Economia por ano':<22}{brl(led['economia_rs_ano']):>14}{brl(a['economia_rs_ano']):>15}{brl(b['economia_rs_ano']):>15}",
        f"{'Retorno (meses)':<22}{num(led['payback_meses']):>14}{num(a['payback_meses']):>15}{num(b['payback_meses']):>15}",
        f"{'Ganho líquido 10 anos':<22}{brl(led['ganho_liquido_horizonte']):>14}{brl(a['ganho_liquido_horizonte']):>15}{brl(b['ganho_liquido_horizonte']):>15}",
        f"{'kWh evitados por ano':<22}{num(led['economia_kwh_mes'] * 12, 0):>14}{num(a['economia_kwh_mes'] * 12, 0):>15}{num(b['economia_kwh_mes'] * 12, 0):>15}",
        f"{'CO2 evitado (kg/ano)':<22}{num(led['co2_evitado_kg_ano']):>14}{num(a['co2_evitado_kg_ano']):>15}{num(b['co2_evitado_kg_ano']):>15}",
        "",
        "Recomendação:",
        f"1) Comece pelo LED: custa {brl(led['custo_inicial'])} e se paga em cerca de {num(led['payback_meses'], 0)} meses, com risco baixo.",
        f"2) O solar economiza muito mais ({brl(a['economia_rs_ano'])}/ano), mas exige {brl(a['custo_inicial'])} de investimento, "
        f"retorna em torno de {num(a['payback_meses'] / 12, 1)} a {num(b['payback_meses'] / 12, 1)} anos e a economia diminui com o avanço do Fio B (Lei 14.300). "
        "Vale mais para quem é dono do imóvel, tem telhado adequado e consumo alto e constante.",
        "3) Em CO2 os dois ganhos são pequenos, porque a eletricidade brasileira já emite pouco; o principal benefício é financeiro.",
        "Fontes: R1 a R12 (lista completa em docs/referencias.md).",
        AVISO,
    ]
    return "\n".join(linhas)


def texto_co2(p, eq, tarifa):
    consumo = c.consumo_total_kwh(eq)
    return "\n".join(
        [
            "IMPACTO AMBIENTAL (emissões de CO2 da eletricidade)",
            "",
            f"Fator da rede: {num(p['fator_emissao_sin'] * 1000, 1)} kgCO2 por MWh ({num(p['fator_emissao_sin'], 4)} kg/kWh), média do SIN em 2023.",
            f"Sua casa exemplo: {num(consumo)} kWh/mês x {num(p['fator_emissao_sin'], 4)} = {num(c.emissao_kg(consumo, p))} kgCO2/mês.",
            "Como a matriz brasileira é cerca de 93% renovável, economizar kWh evita pouco CO2; o ganho maior é na conta de luz.",
            "Ficam de fora desta conta: emissões de fabricação de painéis e lâmpadas e o descarte no fim da vida útil.",
            "Fontes: R11.",
            AVISO,
        ]
    )


def texto_chuveiro(p, eq, tarifa):
    itens = c.consumo_por_equipamento(eq)
    total = sum(i["kwh_mes"] for i in itens)
    ch = next(i for i in itens if i["categoria"] == "banho")
    por_min = c.kwh_por_minuto_de_banho(eq, p)
    return "\n".join(
        [
            "CHUVEIRO ELÉTRICO",
            "",
            f"Potência {num(ch['potencia_w'], 0)} W x {num(ch['horas_dia'], 1)} h/dia x {num(ch['dias_mes'], 0)} dias = {num(ch['kwh_mes'])} kWh/mês "
            f"({num(ch['kwh_mes'] / total * 100, 0)}% do consumo, {brl(ch['kwh_mes'] * tarifa)}/mês).",
            f"Cada minuto a menos em cada banho ({num(p['pessoas_residencia'], 0)} pessoas) economiza {num(por_min)} kWh/mês = {brl(por_min * tarifa)}/mês, sem custo.",
            "Fontes: R4 (participação típica do chuveiro no consumo residencial).",
            AVISO,
        ]
    )


def texto_fio_b(p, eq, tarifa):
    return "\n".join(
        [
            "FIO B E A LEI 14.300 (por que o solar compensa menos a cada ano)",
            "",
            "Quem gera energia solar e injeta na rede deixa de compensar uma parcela da tarifa (o Fio B, que paga o uso da rede).",
            "Parcela não compensada: 60% em 2026, 75% em 2027 e 90% em 2028. A partir de 2029 a ANEEL define a regra.",
            f"Nesta casa, o Fio B custaria {brl(cenario_fv(p, c.consumo_total_kwh(eq), p['fio_b_pct_2026'], tarifa)['custo_fio_b_rs_mes'])}/mês em 2026 "
            f"e {brl(cenario_fv(p, c.consumo_total_kwh(eq), p['fio_b_pct_2028'], tarifa)['custo_fio_b_rs_mes'])}/mês em 2028.",
            "O valor real do Fio B varia por distribuidora; aqui usamos uma aproximação de mercado (28% da tarifa).",
            "Fontes: R8, R9, R10.",
            AVISO,
        ]
    )


AJUDA = (
    "Posso orientar sobre: consumo da casa, chuveiro, lâmpadas LED, energia solar, Fio B/Lei 14.300, "
    "impacto ambiental (CO2) e a comparação LED x solar. Exemplo: 'vale a pena colocar painel solar?'"
)

# (palavras-chave, função de resposta); a ordem importa: os temas mais específicos vêm primeiro
ROTEAMENTO = [
    (("fio b", "14.300", "14300", "lei 14"), texto_fio_b),
    (("chuveiro", "banho"), texto_chuveiro),
    (("co2", "emissao", "emissoes", "ambient", "sustent", "carbono"), texto_co2),
    (("comparar", "compara", "melhor", "o que fazer", "reduzir", "economizar", "economia", "conta"), texto_comparacao),
    (("led", "lampada", "iluminacao"), texto_led),
    (("solar", "painel", "paineis", "fotovolta", "placa", "renovavel"), texto_solar),
    (("consumo", "consome", "gasta", "gasto", "equipamento", "aparelho", "kwh"), texto_consumo),
]


def responder(pergunta, p=None, eq=None, tarifa=None):
    """Devolve a resposta de energia (texto) para uma pergunta em linguagem natural."""
    if p is None:
        p, _ = carregar_parametros()
    if eq is None:
        eq = carregar_equipamentos()
    tarifa = tarifa or c.tarifa_final(p)
    alvo = _normalizar(pergunta)
    palavras_da_pergunta = re.findall(r"[a-z0-9.]+", alvo)
    for chaves, funcao in ROTEAMENTO:
        for chave in chaves:
            # chave com espaço (ex.: "fio b") busca no texto; as demais casam o início de uma palavra
            achou = chave in alvo if " " in chave else any(w.startswith(chave) for w in palavras_da_pergunta)
            if achou:
                return funcao(p, eq, tarifa)
    return AJUDA


# ---------- menu interativo ----------

def _ler_numero(mensagem, padrao=None):
    while True:
        bruto = input(mensagem).strip().replace(",", ".")
        if bruto == "" and padrao is not None:
            return padrao
        try:
            valor = float(bruto)
            if valor >= 0:
                return valor
        except ValueError:
            pass
        print("Digite um número válido (ex.: 5,5).")


def calcular_aparelho(p, tarifa):
    print("\nCALCULAR O CONSUMO DE UM APARELHO")
    print("Dica: a potência (W) está na etiqueta do aparelho.")
    potencia = _ler_numero("Potência em watts (W): ")
    horas = _ler_numero("Horas de uso por dia: ")
    dias = _ler_numero("Dias de uso por mês [30]: ", 30.0)
    kwh = c.energia_kwh(potencia, horas, dias)
    print(
        f"\nEnergia = {num(potencia, 0)} W x {num(horas, 2)} h x {num(dias, 0)} dias / 1000 = {num(kwh)} kWh/mês\n"
        f"Custo = {num(kwh)} kWh x {brl(tarifa)} = {brl(kwh * tarifa)} por mês\n"
        f"CO2 = {num(c.emissao_kg(kwh, p))} kgCO2/mês\n"
        "Fontes: R1, R11. " + AVISO
    )


def menu_energia():
    p, _ = carregar_parametros()
    eq = carregar_equipamentos()
    tarifa = c.tarifa_final(p)
    print("\n=== Citizen Assist AI | Energia e Sustentabilidade ===")
    print(f"Tarifa usada: {brl(tarifa)}/kWh (média nacional ANEEL + tributos, bandeira verde).")
    usar_propria = input("Digite a tarifa da sua fatura em R$/kWh (ou Enter para usar a padrão): ").strip().replace(",", ".")
    if usar_propria:
        try:
            tarifa = float(usar_propria)
            print(f"Usando sua tarifa: {brl(tarifa)}/kWh.")
        except ValueError:
            print("Valor inválido; mantendo a tarifa padrão.")
    while True:
        print(
            "\n1) Consumo da residência exemplo\n2) Comparar alternativas (LED x solar)\n"
            "3) Calcular o consumo de um aparelho\n4) Perguntar ao assistente\n"
            "5) Impacto ambiental (CO2)\n0) Voltar"
        )
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            print("\n" + texto_consumo(p, eq, tarifa))
        elif opcao == "2":
            print("\n" + texto_comparacao(p, eq, tarifa))
        elif opcao == "3":
            calcular_aparelho(p, tarifa)
        elif opcao == "4":
            pergunta = input("Sua pergunta: ")
            print("\n" + responder(pergunta, p, eq, tarifa))
        elif opcao == "5":
            print("\n" + texto_co2(p, eq, tarifa))
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")
