import unittest

import pandas as pd

from limpeza import limpar_leituras_climaticas


class LimpezaLeiturasClimaticasTest(unittest.TestCase):
    def test_descarta_valores_fisicamente_impossiveis_e_interpola_lacuna(self):
        dados = pd.DataFrame(
            {
                "medido_em": pd.to_datetime(
                    ["2026-01-01 00:00", "2026-01-01 01:00", "2026-01-01 02:00"]
                ),
                "temperatura": [20, 200, 22],
                "umidade": [60, 55, 62],
            }
        )

        limpas = limpar_leituras_climaticas(dados)

        self.assertEqual(len(limpas), 3)
        self.assertAlmostEqual(limpas.loc["2026-01-01 01:00", "temperatura"], 21)
        self.assertFalse((limpas["temperatura"] > 85).any())

    def test_remove_umidade_fora_da_faixa(self):
        dados = pd.DataFrame(
            {
                "medido_em": pd.to_datetime(["2026-01-01 00:00", "2026-01-01 01:00"]),
                "temperatura": [20, 21],
                "umidade": [60, -1],
            }
        )

        limpas = limpar_leituras_climaticas(dados)

        self.assertEqual(len(limpas), 1)
        self.assertEqual(float(limpas.iloc[0]["umidade"]), 60)

    def test_rejeita_colunas_ausentes(self):
        with self.assertRaises(ValueError):
            limpar_leituras_climaticas(pd.DataFrame({"temperatura": [20]}))


if __name__ == "__main__":
    unittest.main()
