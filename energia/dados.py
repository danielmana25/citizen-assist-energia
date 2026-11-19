"""Leitura dos dados em CSV (parâmetros e equipamentos da residência)."""
import csv
from pathlib import Path

PASTA_DADOS = Path(__file__).resolve().parent.parent / "dados"


def carregar_parametros(caminho=None):
    """Retorna (valores, meta).

    valores: {nome: float}
    meta:    {nome: {unidade, tipo, ref, observacao}}
    """
    caminho = Path(caminho) if caminho else PASTA_DADOS / "parametros.csv"
    valores, meta = {}, {}
    with open(caminho, newline="", encoding="utf-8") as f:
        for linha in csv.DictReader(f):
            nome = linha["parametro"]
            valores[nome] = float(linha["valor"])
            meta[nome] = {
                "unidade": linha["unidade"],
                "tipo": linha["tipo"],
                "ref": linha["ref"],
                "observacao": linha["observacao"],
            }
    return valores, meta


def carregar_equipamentos(caminho=None):
    """Retorna a lista de equipamentos da residência exemplo."""
    caminho = Path(caminho) if caminho else PASTA_DADOS / "equipamentos_residencia.csv"
    equipamentos = []
    with open(caminho, newline="", encoding="utf-8") as f:
        for linha in csv.DictReader(f):
            equipamentos.append(
                {
                    "equipamento": linha["equipamento"],
                    "categoria": linha["categoria"],
                    "quantidade": int(linha["quantidade"]),
                    "potencia_w": float(linha["potencia_w"]),
                    "horas_dia": float(linha["horas_dia"]),
                    "dias_mes": float(linha["dias_mes"]),
                    "tipo": linha["tipo"],
                    "observacao": linha["observacao"],
                }
            )
    return equipamentos
