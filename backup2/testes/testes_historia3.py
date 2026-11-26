# Arquivo destinado aos testes automatizados da história de usuário 3.
import io
import unittest
from contextlib import redirect_stdout
from src.historia3 import *


# =- Testes para a história de usuário (3) e seus critérios de aceitação -=
class TestAlertasLesao(unittest.TestCase):

    # Simula os bancos: perfil do usuário, cache de treinos e banco de semanas (+4 semanas e -4 semanas)
    def setUp(self):
        self.perfil = {
            "volume_agudo": None,
            "pace_agudo": None,
            "volume_cronico": None,
            "pace_cronico": None,
            "acwr": None
        }

        self.cache_treinos = []

        # 5 semanas: a primeira fica fora da janela das últimas 4 semanas
        self.banco_mais_4 = [
            {"Semana 04/10/2026:": [
                { "data": "05/10/2026", "distancia": 20.0, "tempo": 120.0},
                { "data": "07/10/2026", "distancia": 20.0, "tempo": 120.0}
            ]},
            {"Semana 11/10/2026:": [{ "data": "13/10/2026", "distancia": 10.0, "tempo": 60.0}]},
            {"Semana 18/10/2026:": [{ "data": "20/10/2026", "distancia": 10.0, "tempo": 60.0}]},
            {"Semana 25/10/2026:": [{ "data": "27/10/2026", "distancia": 10.0, "tempo": 60.0}]},
            {"Semana 01/11/2026:": [
                { "data": "03/11/2026", "distancia": 10.0, "tempo": 60.0},
                { "data": "05/11/2026", "distancia": 6.0, "tempo": 36.0}
            ]}
        ]

        # 3 semanas: ainda não tem 4 semanas de histórico
        self.banco_menos_4 = [
            {"Semana 18/10/2026:": [{ "data": "20/10/2026", "distancia": 10.0, "tempo": 60.0}]},
            {"Semana 25/10/2026:": [{ "data": "27/10/2026", "distancia": 10.0, "tempo": 60.0}]},
            {"Semana 01/11/2026:": [{ "data": "03/11/2026", "distancia": 30.0, "tempo": 120.0}]}
        ]

    # Ativa a função e devolve o que ela imprimiu no terminal
    def saida(self, funcao, *args):
        terminal = io.StringIO()
        with redirect_stdout(terminal):
            funcao(*args)
        return terminal.getvalue().strip()

    # Simula a entrada de uma nova semana no banco e atualiza o perfil
    def processar_semanas(self, banco_semanas):
        calcular_volume_pace_agudo(banco_semanas, self.perfil)
        calcular_volume_pace_cronico(banco_semanas, self.perfil)
        return self.saida(calcular_acwr, self.perfil)

    # Testa o cálculo do volume agudo, volume crônico (últimas 4 semanas, semana sem treino conta como 0) e ACWR
    def test_3_1_volume_semanal_e_acwr(self):
        self.processar_semanas(self.banco_mais_4)

        self.assertEqual(self.perfil["volume_agudo"], 16.0)
        self.assertEqual(self.perfil["volume_cronico"], 11.5)
        self.assertEqual(self.perfil["acwr"], 1.39)

        self.banco_mais_4[2] = {"Semana 18/10/2026:": []}
        self.processar_semanas(self.banco_mais_4)

        self.assertEqual(self.perfil["volume_cronico"], 9.0)
        self.assertEqual(self.perfil["acwr"], 1.78)

    # Testa a classificação do ACWR e as mensagens de alerta de volume
    def test_3_2_classificacao_e_alertas_de_volume(self):
        self.processar_semanas(self.banco_mais_4)
        self.assertEqual(self.saida(classificar_acwr, self.perfil),
                         "ATENÇÃO (volume): 16.0 km nesta semana contra média de 11.5 km nas últimas 4 semanas (ACWR 1.39).")

        self.banco_mais_4[-1] = {"Semana 01/11/2026:": [{ "data": "03/11/2026", "distancia": 30.0, "tempo": 180.0}]}
        self.processar_semanas(self.banco_mais_4)
        self.assertEqual(self.saida(classificar_acwr, self.perfil),
                         "ALERTA (volume): 30.0 km nesta semana contra média de 15.0 km nas últimas 4 semanas (ACWR 2.00). Zona de perigo para lesões.")

        # Zona segura e abaixo da zona segura não geram alerta
        self.banco_mais_4[-1] = {"Semana 01/11/2026:": [{ "data": "03/11/2026", "distancia": 10.0, "tempo": 60.0}]}
        self.processar_semanas(self.banco_mais_4)
        self.assertEqual(self.saida(classificar_acwr, self.perfil), "")

        self.banco_mais_4[-1] = {"Semana 01/11/2026:": [{ "data": "03/11/2026", "distancia": 5.0, "tempo": 30.0}]}
        self.processar_semanas(self.banco_mais_4)
        self.assertEqual(self.saida(classificar_acwr, self.perfil), "")

        # Limites das faixas
        self.perfil["acwr"] = 1.3
        self.assertEqual(self.saida(classificar_acwr, self.perfil), "")
        self.perfil["acwr"] = 1.31
        self.assertTrue(self.saida(classificar_acwr, self.perfil).startswith("ATENÇÃO (volume)"))
        self.perfil["acwr"] = 1.5
        self.assertTrue(self.saida(classificar_acwr, self.perfil).startswith("ATENÇÃO (volume)"))
        self.perfil["acwr"] = 1.51
        self.assertTrue(self.saida(classificar_acwr, self.perfil).startswith("ALERTA (volume)"))

    # Testa o pace agudo, o pace crônico (média dos treinos das últimas 4 semanas) e o alerta de mudança brusca de pace
    def test_3_3_mudanca_brusca_de_pace(self):
        self.banco_mais_4[-1] = {"Semana 01/11/2026:": [{ "data": "03/11/2026", "distancia": 10.0, "tempo": 48.0}]}
        self.processar_semanas(self.banco_mais_4)

        self.assertAlmostEqual(self.perfil["pace_agudo"], 4.8)
        self.assertAlmostEqual(self.perfil["pace_cronico"], 5.7)
        self.assertEqual(self.saida(classificar_pace, self.perfil),
                         "ALERTA (ritmo): pace médio da semana de 4:48 min/km, 15.8% mais rápido que a média das últimas 4 semanas (5:42 min/km).")

        # O pace crônico é a média de todos os treinos, e não a média dos paces semanais
        self.banco_mais_4[-1] = {"Semana 01/11/2026:": [
            { "data": "03/11/2026", "distancia": 10.0, "tempo": 48.0},
            { "data": "05/11/2026", "distancia": 10.0, "tempo": 48.0}
        ]}
        self.processar_semanas(self.banco_mais_4)

        self.assertAlmostEqual(self.perfil["pace_cronico"], 5.52)
        self.assertEqual(self.saida(classificar_pace, self.perfil), "")

        # Limite de 15% (diferença arredondada para 1 casa decimal) e pace mais lento não gera alerta
        self.perfil["pace_cronico"] = 6.0
        self.perfil["pace_agudo"] = 5.1
        self.assertIn("15.0% mais rápido", self.saida(classificar_pace, self.perfil))
        self.perfil["pace_agudo"] = 5.2
        self.assertEqual(self.saida(classificar_pace, self.perfil), "")
        self.perfil["pace_agudo"] = 7.0
        self.assertEqual(self.saida(classificar_pace, self.perfil), "")

    # Testa o alerta de recuperação a cada nova entrada no cache de treinos
    def test_3_4_dias_seguidos_sem_descanso(self):
        entradas = [
            ({ "data": "02/11/2026", "distancia": 5.0, "tempo": 30.0}, ""),
            ({ "data": "03/11/2026", "distancia": 5.0, "tempo": 30.0}, ""),
            # Dois treinos no mesmo dia contam como um dia só
            ({ "data": "03/11/2026", "distancia": 3.0, "tempo": 20.0}, ""),
            ({ "data": "04/11/2026", "distancia": 5.0, "tempo": 30.0},
             "ALERTA (recuperação): treinos em 3 dias seguidos, de 02/11/2026 a 04/11/2026. Agende um dia de descanso."),
            ({ "data": "05/11/2026", "distancia": 5.0, "tempo": 30.0},
             "ALERTA (recuperação): treinos em 4 dias seguidos, de 02/11/2026 a 05/11/2026. Agende um dia de descanso."),
            # Sem treino no dia 06 (descanso), o treino do dia 07 não gera alerta
            ({ "data": "07/11/2026", "distancia": 5.0, "tempo": 30.0}, "")
        ]

        for treino, alerta in entradas:
            self.cache_treinos.append(treino)
            self.assertEqual(self.saida(alertas_recuperacao, self.cache_treinos), alerta)

    # Testa semanas sem 4 semanas de histórico ou com volume crônico 0
    def test_3_5_semanas_sem_historico_suficiente(self):
        self.assertEqual(self.processar_semanas(self.banco_menos_4), "Sem base de comparação")

        self.assertEqual(self.perfil["volume_agudo"], 30.0)
        self.assertIsNone(self.perfil["volume_cronico"])
        self.assertIsNone(self.perfil["pace_cronico"])
        self.assertIsNone(self.perfil["acwr"])
        self.assertEqual(self.saida(classificar_acwr, self.perfil), "")
        self.assertEqual(self.saida(classificar_pace, self.perfil), "")

        semanas_vazias = [{"Semana 11/10/2026:": []}, {"Semana 18/10/2026:": []},
                          {"Semana 25/10/2026:": []}, {"Semana 01/11/2026:": []}]
        self.assertEqual(self.processar_semanas(semanas_vazias), "Sem base de comparação")

        self.assertEqual(self.perfil["volume_agudo"], 0.0)
        self.assertEqual(self.perfil["pace_agudo"], 0.0)
        self.assertEqual(self.perfil["volume_cronico"], 0.0)
        self.assertIsNone(self.perfil["acwr"])

if __name__ == '__main__':
    unittest.main()
