import unittest
# import codigo_HU3


# =- Testes para a história de usuário (3) e seus critérios de aceitação -=
class TestAlertasLesao(unittest.TestCase):

    def test_3_1_volume_semanal_e_acwr(self):
        self.assertEqual(calcular_acwr(40, 25), 1.6)
        self.assertEqual(calcular_acwr(20, 15), 1.33)

        treinos = [
            { "data": "06/10/2026", "distancia": 20.0, "tempo": 120.0},
            { "data": "13/10/2026", "distancia": 20.0, "tempo": 120.0},
            { "data": "20/10/2026", "distancia": 20.0, "tempo": 120.0},
            { "data": "27/10/2026", "distancia": 25.0, "tempo": 150.0},
            { "data": "29/10/2026", "distancia": 15.0, "tempo": 90.0}
        ]
        semana = analisar_semanas(treinos)[3]

        self.assertEqual(semana["semana"], "25/10/2026")
        self.assertEqual(semana["volume"], 40.0)
        self.assertEqual(semana["volume_cronico"], 25.0)
        self.assertEqual(semana["acwr"], 1.6)

        treinos = [
            { "data": "06/10/2026", "distancia": 20.0, "tempo": 120.0},
            { "data": "20/10/2026", "distancia": 20.0, "tempo": 120.0},
            { "data": "27/10/2026", "distancia": 20.0, "tempo": 120.0}
        ]
        semana = analisar_semanas(treinos)[2]
        self.assertEqual(semana["volume_cronico"], 15.0)
        self.assertEqual(semana["acwr"], 1.33)

    def test_3_2_classificacao_e_alertas_de_volume(self):
        self.assertEqual(classificar_acwr(0.79), "Abaixo da zona segura")
        self.assertEqual(classificar_acwr(0.8), "Zona segura")
        self.assertEqual(classificar_acwr(1.3), "Zona segura")
        self.assertEqual(classificar_acwr(1.31), "Atenção")
        self.assertEqual(classificar_acwr(1.5), "Atenção")
        self.assertEqual(classificar_acwr(1.51), "Zona de perigo")

        base = [
            { "data": "06/10/2026", "distancia": 10.0, "tempo": 60.0},
            { "data": "13/10/2026", "distancia": 10.0, "tempo": 60.0},
            { "data": "20/10/2026", "distancia": 10.0, "tempo": 60.0}
        ]

        atencao = analisar_semanas(base + [{ "data": "27/10/2026", "distancia": 16.0, "tempo": 96.0}])[3]
        self.assertEqual(atencao["alertas"],
                         ["ATENÇÃO (volume): 16.0 km nesta semana contra média de 11.5 km nas últimas 4 semanas (ACWR 1.39)."])

        perigo = analisar_semanas(base + [{ "data": "27/10/2026", "distancia": 30.0, "tempo": 180.0}])[3]
        self.assertEqual(perigo["alertas"],
                         ["ALERTA (volume): 30.0 km nesta semana contra média de 15.0 km nas últimas 4 semanas (ACWR 2.00). Zona de perigo para lesões."])

        abaixo = analisar_semanas(base + [{ "data": "27/10/2026", "distancia": 5.0, "tempo": 30.0}])[3]
        self.assertEqual(abaixo["nivel_volume"], "Abaixo da zona segura")
        self.assertEqual(abaixo["alertas"], [])

    def test_3_3_mudanca_brusca_de_pace(self):
        self.assertEqual(calcular_diferenca_pace(5.0, 6.0), 16.7)
        self.assertEqual(calcular_diferenca_pace(5.1, 6.0), 15.0)
        self.assertEqual(calcular_diferenca_pace(5.2, 6.0), 13.3)

        treinos = [
            { "data": "06/10/2026", "distancia": 10.0, "tempo": 60.0},
            { "data": "13/10/2026", "distancia": 10.0, "tempo": 60.0},
            { "data": "20/10/2026", "distancia": 10.0, "tempo": 60.0},
            { "data": "27/10/2026", "distancia": 10.0, "tempo": 48.0}
        ]
        semana = analisar_semanas(treinos)[3]

        self.assertEqual(semana["diferenca_pace"], 15.8)
        self.assertEqual(semana["alertas"],
                         ["ALERTA (ritmo): pace médio da semana de 4:48 min/km, 15.8% mais rápido que a média das últimas 4 semanas (5:42 min/km)."])

    def test_3_4_dias_seguidos_sem_descanso(self):
        tres_dias = [
            { "data": "02/11/2026", "distancia": 5.0, "tempo": 30.0},
            { "data": "03/11/2026", "distancia": 5.0, "tempo": 30.0},
            { "data": "04/11/2026", "distancia": 5.0, "tempo": 30.0}
        ]
        self.assertEqual(alertas_recuperacao(tres_dias),
                         ["ALERTA (recuperação): treinos em 3 dias seguidos, de 02/11/2026 a 04/11/2026. Agende um dia de descanso."])

        # 4 dias seguidos geram um único alerta e dois treinos no mesmo dia contam como um dia
        quatro_dias = tres_dias + [
            { "data": "04/11/2026", "distancia": 3.0, "tempo": 20.0},
            { "data": "05/11/2026", "distancia": 5.0, "tempo": 30.0}
        ]
        self.assertEqual(alertas_recuperacao(quatro_dias),
                         ["ALERTA (recuperação): treinos em 4 dias seguidos, de 02/11/2026 a 05/11/2026. Agende um dia de descanso."])

        com_descanso = [
            { "data": "02/11/2026", "distancia": 5.0, "tempo": 30.0},
            { "data": "03/11/2026", "distancia": 5.0, "tempo": 30.0},
            { "data": "05/11/2026", "distancia": 5.0, "tempo": 30.0}
        ]
        self.assertEqual(alertas_recuperacao(com_descanso), [])

    def test_3_5_semanas_sem_historico_suficiente(self):
        self.assertIsNone(calcular_acwr(20, None))
        self.assertIsNone(calcular_diferenca_pace(5.0, None))
        self.assertEqual(classificar_acwr(None), "Sem base de comparação")

        treinos = [
            { "data": "13/10/2026", "distancia": 10.0, "tempo": 60.0},
            { "data": "20/10/2026", "distancia": 10.0, "tempo": 60.0},
            { "data": "27/10/2026", "distancia": 30.0, "tempo": 120.0}
        ]
        for semana in analisar_semanas(treinos):
            self.assertIsNone(semana["acwr"])
            self.assertIsNone(semana["diferenca_pace"])
            self.assertEqual(semana["nivel_volume"], "Sem base de comparação")
            self.assertEqual(semana["alertas"], [])

if __name__ == '__main__':
    unittest.main()
