"""Comparação das alternativas para o mesmo problema: reduzir a conta de luz da residência.

Período de referência comum: 12 meses (economia anual) e horizonte de 10 anos.
Alternativa A: trocar lâmpadas fluorescentes compactas por LED (eficiência energética).
Alternativa B: sistema solar fotovoltaico on-grid (fonte renovável).
Todas as economias são estimativas e não garantias.
"""
from . import calculos as c


def _fechar(nome, custo_inicial, economia_kwh_mes, economia_rs_mes, p):
    """Calcula os indicadores comuns às duas alternativas."""
    meses = p["horizonte_anos"] * 12
    return {
        "nome": nome,
        "custo_inicial": custo_inicial,
        "economia_kwh_mes": economia_kwh_mes,
        "economia_rs_mes": economia_rs_mes,
        "economia_rs_ano": economia_rs_mes * 12,
        "payback_meses": custo_inicial / economia_rs_mes if economia_rs_mes > 0 else float("inf"),
        "ganho_liquido_horizonte": economia_rs_mes * meses - custo_inicial,
        "co2_evitado_kg_ano": c.emissao_kg(economia_kwh_mes * 12, p),
    }


def cenario_led(p, equipamentos, tarifa=None):
    """Troca das lâmpadas fluorescentes compactas por LED de mesmo fluxo luminoso."""
    tarifa = tarifa or c.tarifa_final(p)
    lamp = next(e for e in equipamentos if e["categoria"] == "iluminacao")
    antes = c.energia_kwh(p["lampada_antiga_w"], lamp["horas_dia"], lamp["dias_mes"], lamp["quantidade"])
    depois = c.energia_kwh(p["lampada_led_w"], lamp["horas_dia"], lamp["dias_mes"], lamp["quantidade"])
    economia_kwh = antes - depois
    custo = lamp["quantidade"] * p["lampada_led_preco"]
    r = _fechar("LED no lugar das fluorescentes", custo, economia_kwh, economia_kwh * tarifa, p)
    horas_ano = lamp["horas_dia"] * 365
    r.update(
        {
            "quantidade": lamp["quantidade"],
            "kwh_antes": antes,
            "kwh_depois": depois,
            "eficacia_antes": c.eficacia_luminosa(p["lampada_lumens"], p["lampada_antiga_w"]),
            "eficacia_depois": c.eficacia_luminosa(p["lampada_lumens"], p["lampada_led_w"]),
            "vida_util_anos": p["lampada_led_vida_h"] / horas_ano,
        }
    )
    return r


def cenario_fv(p, consumo_mes_kwh, fio_b_pct, tarifa=None):
    """Sistema fotovoltaico dimensionado para o consumo acima do custo de disponibilidade.

    Fio B: parcela da tarifa que deixa de ser compensada sobre a energia injetada na rede
    (Lei 14.300). A energia consumida na hora (simultaneidade) não paga Fio B.
    """
    tarifa = tarifa or c.tarifa_final(p)
    dim = c.dimensionar_fv(consumo_mes_kwh, p)
    geracao = c.producao_fv_kwh_mes(dim["kwp_instalado"], p)
    compensada = min(geracao, dim["alvo_kwh_mes"])
    injetada = compensada * (1.0 - p["simultaneidade"])
    custo_fio_b = injetada * fio_b_pct * p["fio_b_parcela_tarifa"] * tarifa
    economia_rs = compensada * tarifa - custo_fio_b
    custo = dim["kwp_instalado"] * 1000.0 * p["preco_fv_rs_wp"]
    r = _fechar("Solar fotovoltaico", custo, compensada, economia_rs, p)
    r.update(
        {
            **dim,
            "geracao_kwh_mes": geracao,
            "compensada_kwh_mes": compensada,
            "custo_fio_b_rs_mes": custo_fio_b,
            "fio_b_pct": fio_b_pct,
            "cobertura_pct": compensada / consumo_mes_kwh * 100.0,
        }
    )
    return r


def comparar(p, equipamentos, tarifa=None):
    """Monta a comparação completa (baseline, LED, FV com Fio B de 2026 e de 2028)."""
    tarifa = tarifa or c.tarifa_final(p)
    consumo = c.consumo_total_kwh(equipamentos)
    return {
        "tarifa": tarifa,
        "consumo_kwh_mes": consumo,
        "conta_rs_mes": consumo * tarifa,
        "led": cenario_led(p, equipamentos, tarifa),
        "fv_2026": cenario_fv(p, consumo, p["fio_b_pct_2026"], tarifa),
        "fv_2028": cenario_fv(p, consumo, p["fio_b_pct_2028"], tarifa),
    }
