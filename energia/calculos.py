"""Fórmulas de energia, potência, eficiência, custo, geração solar e emissões.

Unidades: potência em W (ou kW), energia em kWh, tarifa em R$/kWh, emissões em kgCO2.
"""
import math


# ---------- energia, potência e custo ----------

def energia_kwh(potencia_w, horas_dia, dias_mes=30.0, quantidade=1):
    """Energia = potência x tempo. kWh = (W x h) / 1000."""
    return quantidade * potencia_w * horas_dia * dias_mes / 1000.0


def tarifa_final(p):
    """Tarifa por kWh com bandeira e tributos.

    Os tributos (ICMS, PIS/COFINS) são cobrados "por dentro", por isso a divisão por (1 - alíquota).
    """
    return (p["tarifa_sem_tributos"] + p["bandeira_sem_tributos"]) / (1.0 - p["tributos_totais"])


def custo_rs(kwh, tarifa):
    return kwh * tarifa


def emissao_kg(kwh, p):
    """kgCO2 associados a uma quantidade de eletricidade da rede (SIN)."""
    return kwh * p["fator_emissao_sin"]


# ---------- eficiência ----------

def eficacia_luminosa(lumens, potencia_w):
    """Eficiência energética de uma lâmpada: lúmens (luz) por watt (energia)."""
    return lumens / potencia_w


# ---------- consumo da residência ----------

def consumo_por_equipamento(equipamentos):
    """Adiciona 'kwh_mes' a cada equipamento e devolve a lista ordenada do maior para o menor."""
    itens = []
    for e in equipamentos:
        kwh = energia_kwh(e["potencia_w"], e["horas_dia"], e["dias_mes"], e["quantidade"])
        itens.append({**e, "kwh_mes": kwh})
    return sorted(itens, key=lambda x: x["kwh_mes"], reverse=True)


def consumo_total_kwh(equipamentos):
    return sum(i["kwh_mes"] for i in consumo_por_equipamento(equipamentos))


def kwh_por_minuto_de_banho(equipamentos, p):
    """kWh/mês economizados ao reduzir 1 minuto de cada banho (1 banho por pessoa por dia)."""
    chuveiro = next(e for e in equipamentos if e["categoria"] == "banho")
    return chuveiro["potencia_w"] / 1000.0 * (1 / 60.0) * p["pessoas_residencia"] * chuveiro["dias_mes"]


# ---------- energia solar fotovoltaica ----------

def producao_fv_kwh_mes(kwp, p):
    """Geração mensal = potência instalada x irradiação diária x taxa de desempenho x dias."""
    return kwp * p["irradiacao_kwh_m2_dia"] * p["performance_ratio"] * p["dias_mes"]


def dimensionar_fv(consumo_mes_kwh, p):
    """Dimensiona o sistema para cobrir o consumo acima do custo de disponibilidade.

    Retorna dict com kWp mínimo, nº de módulos, kWp instalado e energia a compensar.
    """
    alvo = max(consumo_mes_kwh - p["custo_disponibilidade_kwh"], 0.0)
    kwp_por_kwh = producao_fv_kwh_mes(1.0, p)  # kWh/mês gerados por 1 kWp
    kwp_min = alvo / kwp_por_kwh
    modulos = math.ceil(kwp_min * 1000.0 / p["modulo_wp"])
    kwp_instalado = modulos * p["modulo_wp"] / 1000.0
    return {
        "alvo_kwh_mes": alvo,
        "kwp_minimo": kwp_min,
        "modulos": modulos,
        "kwp_instalado": kwp_instalado,
    }
