"""Testes dos cálculos. Executar com: python -m unittest discover tests"""
import unittest

from energia import calculos as c
from energia.assistente import AJUDA, responder
from energia.comparacao import cenario_fv, cenario_led, comparar
from energia.dados import carregar_equipamentos, carregar_parametros


class TestCalculos(unittest.TestCase):
    def setUp(self):
        self.p, _ = carregar_parametros()
        self.eq = carregar_equipamentos()

    def test_energia_kwh(self):
        # chuveiro 5500 W por 0,4 h em 30 dias = 66 kWh
        self.assertAlmostEqual(c.energia_kwh(5500, 0.4, 30), 66.0)

    def test_consumo_total_da_residencia(self):
        self.assertAlmostEqual(c.consumo_total_kwh(self.eq), 194.3, places=6)

    def test_tarifa_final(self):
        # 0,839 / (1 - 0,22) = 1,07564...
        self.assertAlmostEqual(c.tarifa_final(self.p), 0.839 / 0.78)

    def test_led(self):
        r = cenario_led(self.p, self.eq)
        self.assertAlmostEqual(r["economia_kwh_mes"], 9.0)  # 10 x (15-9) W x 5 h x 30 d
        self.assertAlmostEqual(r["custo_inicial"], 60.0)
        self.assertAlmostEqual(r["payback_meses"], 60.0 / (9.0 * c.tarifa_final(self.p)))

    def test_dimensionamento_fv(self):
        d = c.dimensionar_fv(194.3, self.p)
        self.assertEqual(d["modulos"], 3)
        self.assertAlmostEqual(d["kwp_instalado"], 1.65)

    def test_fv_geracao_e_custo(self):
        r = cenario_fv(self.p, 194.3, self.p["fio_b_pct_2026"])
        self.assertAlmostEqual(r["geracao_kwh_mes"], 1.65 * 4.6 * 0.75 * 30.4)
        self.assertAlmostEqual(r["custo_inicial"], 4686.0)

    def test_fio_b_maior_reduz_economia(self):
        c26 = cenario_fv(self.p, 194.3, self.p["fio_b_pct_2026"])
        c28 = cenario_fv(self.p, 194.3, self.p["fio_b_pct_2028"])
        self.assertLess(c28["economia_rs_mes"], c26["economia_rs_mes"])
        self.assertGreater(c28["payback_meses"], c26["payback_meses"])

    def test_fv_nao_compensa_mais_que_o_consumo(self):
        r = cenario_fv(self.p, 194.3, self.p["fio_b_pct_2026"])
        self.assertLessEqual(r["compensada_kwh_mes"], 194.3 - self.p["custo_disponibilidade_kwh"] + 1e-9)

    def test_consumo_abaixo_do_custo_de_disponibilidade(self):
        self.assertEqual(c.dimensionar_fv(40.0, self.p)["modulos"], 0)

    def test_comparacao_led_paga_antes_do_solar(self):
        r = comparar(self.p, self.eq)
        self.assertLess(r["led"]["payback_meses"], r["fv_2026"]["payback_meses"])

    def test_assistente_roteia_perguntas(self):
        self.assertIn("ALTERNATIVA B", responder("vale a pena colocar painel solar?"))
        self.assertIn("LED", responder("devo trocar as lâmpadas?"))
        self.assertIn("CHUVEIRO", responder("o chuveiro gasta muito?"))
        self.assertIn("FIO B", responder("o que é o fio b?"))
        self.assertIn("CONSUMO DA RESIDÊNCIA", responder("como encontrar o consumo da casa?"))
        self.assertEqual(responder("qual a capital da França?"), AJUDA)

    def test_resposta_traz_fontes_e_limitacoes(self):
        for pergunta in ("solar", "led", "consumo", "comparar", "co2", "chuveiro", "fio b"):
            texto = responder(pergunta)
            self.assertIn("Fontes:", texto, pergunta)
            self.assertIn("Atenção:", texto, pergunta)


if __name__ == "__main__":
    unittest.main()
