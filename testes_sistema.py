import os
import tempfile
import unittest
from sistema_corrida import *


class TestHistorialPace(unittest.TestCase):

    #Testa a leitura dos dados válidos do CSV
    def test_1_1_leitura_dados_validos(self):
        linha_csv_exemplo = "10/01/2020,5.0,30.0,150"
        dados = processar_linha_csv(linha_csv_exemplo)
        
        self.assertIsNotNone(dados)
        data, distancia, tempo, freq_cardiaca = dados
        
        self.assertEqual(data, "10/01/2020")
        self.assertEqual(distancia, 5.0)
        self.assertEqual(tempo, 30.0)
        self.assertEqual(freq_cardiaca, 150)

    # Testa a realização do cálculo de pace
    def test_1_2_calculo_pace(self):
        pace_obtido = calcular_pace_formatado(10.0, 55.0)
        self.assertIsNotNone(pace_obtido)

    # Testa os casos inválidos, nesse caso, valores nulos ou negativos
    def test_1_3_ignorar_linhas_invalidas(self):
        self.assertIsNone(calcular_pace_formatado(0, 30))
        self.assertIsNone(calcular_pace_formatado(-5, 25))
        self.assertIsNone(calcular_pace_formatado(5, 0))
        self.assertIsNone(calcular_pace_formatado(5, -10))

    # Testa a formatação do pace, deve ser dessa forma: "MM:SS min/km"
    def test_1_4_formatacao_pace(self):
        pace_obtido_1 = calcular_pace_formatado(10.0, 55.0)
        self.assertEqual(pace_obtido_1, "5:30 min/km")

        pace_obtido_2 = calcular_pace_formatado(5.0, 25.0)
        self.assertEqual(pace_obtido_2, "5:00 min/km")


class TestHistorialVolume(unittest.TestCase):
    # testa o funcionamento do agrupamento das semanas, quantas semanas foram registradas e se os dias dentro das semanas estão de acordo
    def test_2_1_agrupamento_semanal(self):
        treinos = [
            { "data": "05/11/2026", "distancia": 7.8},
            { "data": "01/11/2026", "distancia": 5.0},
            { "data": "10/11/2026", "distancia": 4.6}
        ]

        resultado = agruparSemana(treinos)

        self.assertEqual(len(resultado), 2)

        self.assertEqual(len(resultado[0]), 2)
        self.assertEqual(resultado[0][0]['data'], '01/11/2026')
        self.assertEqual(resultado[0][1]['data'], '05/11/2026')

        self.assertEqual(len(resultado[1]), 1)
        self.assertEqual(resultado[1][0]['data'], '10/11/2026')

    # Testa o calculo do volume semanal do corredor, retornando junto de sua unidade de medida
    def test_2_2_calculo_volumeSemanal(self):
        distancias = [5.0, 3.34, 2.25, 4.76, 1.44]

        volume_semanal = calcular_volume_semanal(distancias)
        self.assertEqual(volume_semanal, "16.79 km")

    # Testa a atribuição e atualização dos recordes pessoais
    def test_2_3_recordePessoal(self):
        recordPessoal = RecordPessoal()
        recordPessoal.set_maiorDistancia(5.0)
        recordPessoal.set_maiorVolumeSemanal(16.79)
        recordPessoal.set_maiorNumTreinos(7)
        recordPessoal.set_menorPaceMedio(5.30)

        recordes = [6.0, 18.23, 8, 4.0]

        recordPessoal.set_maiorDistancia(recordes[0])
        recordPessoal.set_maiorVolumeSemanal(recordes[1])
        recordPessoal.set_maiorNumTreinos(recordes[2])
        recordPessoal.set_menorPaceMedio(recordes[3])

        self.assertEqual(recordPessoal.get_maiorDistancia(), recordes[0])
        self.assertEqual(recordPessoal.get_maiorVolumeSemanal(), recordes[1])
        self.assertEqual(recordPessoal.get_maiorNumTreinos(), recordes[2])
        self.assertEqual(recordPessoal.get_menorPaceMedio(), recordes[3])

    # Testa a identificação de cada agrupamento de semana, seguindo do padrão : "Semana DD/MM/AAAA (domingo da semana)"
    def test_2_4_identificacao_agrupamentos_semanais(self):
        treinos = [
            {"data": "05/11/2026", "distancia": 7.8},
            {"data": "01/11/2026", "distancia": 5.0},
            {"data": "10/11/2026", "distancia": 4.6}
        ]

        resultado = identificarSemana(treinos)

        chaves = list(resultado.keys())

        self.assertIn("Semana 01/11/2026:", chaves)
        self.assertIn("Semana 08/11/2026:", chaves)

        self.assertEqual(len(resultado["Semana 01/11/2026:"]), 2)
        self.assertEqual(len(resultado["Semana 08/11/2026:"]), 1)


# =- Testes para a história de usuário (3) e seus critérios de aceitação -=
class TestAnalisadorLesoes(unittest.TestCase):

    def setUp(self):
        # 5 semanas: a primeira fica fora da janela das últimas 4 semanas
        # A linha com distância 0 é inválida e deve ser ignorada (critério 1.3)
        self.csv_mais_4 = [
            "data,distancia_km,tempo_min,fc_media",
            "05/10/2026,20.0,120.0,150",
            "07/10/2026,20.0,120.0,150",
            "08/10/2026,0.0,30.0,140",
            "13/10/2026,10.0,60.0,150",
            "20/10/2026,10.0,60.0,150",
            "27/10/2026,10.0,60.0,150",
            "03/11/2026,10.0,60.0,150",
            "05/11/2026,6.0,36.0,150"
        ]

        # 3 semanas: ainda não tem 4 semanas de histórico
        self.csv_menos_4 = [
            "data,distancia_km,tempo_min,fc_media",
            "20/10/2026,10.0,60.0,150",
            "27/10/2026,10.0,60.0,150",
            "03/11/2026,30.0,120.0,160"
        ]

    # Cria um CSV temporário com as linhas e devolve o analisador com um coletor de alertas (observador)
    def criar_analisador(self, linhas):
        arquivo = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
        arquivo.write("\n".join(linhas))
        arquivo.close()
        self.addCleanup(os.remove, arquivo.name)

        analisador = AnalisadorLesoes.de_csv(arquivo.name)
        self.coletor = ColetorAlertas()
        analisador.adicionar_observador(self.coletor)
        return analisador

    # Troca os treinos da semana atual (Semana 01/11/2026) do histórico com mais de 4 semanas
    def semana_atual(self, linhas):
        return self.csv_mais_4[:7] + linhas

    def alertas_de(self, tipo):
        return [mensagem for mensagem in self.coletor.mensagens() if mensagem.startswith(tipo)]

    # Testa o cálculo do volume agudo, volume crônico (últimas 4 semanas, semana sem treino conta como 0) e ACWR
    def test_3_1_volume_semanal_e_acwr(self):
        resultados = self.criar_analisador(self.csv_mais_4).analisar()

        self.assertEqual(len(resultados), 5)
        self.assertEqual(resultados[-1]["semana"], "Semana 01/11/2026:")
        self.assertEqual(resultados[-1]["volume_agudo"], 16.0)
        self.assertEqual(resultados[-1]["volume_cronico"], 11.5)
        self.assertEqual(resultados[-1]["acwr"], 1.39)

        # Sem o treino do dia 20/10 a semana 18/10 fica vazia, mas continua no histórico com 0 km
        resultados = self.criar_analisador([linha for linha in self.csv_mais_4 if not linha.startswith("20/10/2026")]).analisar()

        self.assertEqual(len(resultados), 5)
        self.assertEqual(resultados[2]["semana"], "Semana 18/10/2026:")
        self.assertEqual(resultados[2]["volume_agudo"], 0.0)
        self.assertEqual(resultados[-1]["volume_cronico"], 9.0)
        self.assertEqual(resultados[-1]["acwr"], 1.78)

    # Testa a classificação do ACWR e as mensagens de alerta de volume
    def test_3_2_classificacao_e_alertas_de_volume(self):
        resultados = self.criar_analisador(self.csv_mais_4).analisar()
        self.assertEqual(resultados[-1]["classificacao"], "Atenção")
        self.assertEqual(self.coletor.mensagens(),
                         ["ATENÇÃO (volume): 16.0 km nesta semana contra média de 11.5 km nas últimas 4 semanas (ACWR 1.39)."])
        self.assertEqual(self.coletor.alertas[0]["semana"], "Semana 01/11/2026:")

        resultados = self.criar_analisador(self.semana_atual(["03/11/2026,30.0,180.0,160"])).analisar()
        self.assertEqual(resultados[-1]["classificacao"], "Zona de perigo")
        self.assertEqual(self.coletor.mensagens(),
                         ["ALERTA (volume): 30.0 km nesta semana contra média de 15.0 km nas últimas 4 semanas (ACWR 2.00). Zona de perigo para lesões."])

        # Zona segura e abaixo da zona segura não geram alerta
        resultados = self.criar_analisador(self.semana_atual(["03/11/2026,10.0,60.0,150"])).analisar()
        self.assertEqual(resultados[-1]["classificacao"], "Zona segura")
        self.assertEqual(self.coletor.mensagens(), [])

        resultados = self.criar_analisador(self.semana_atual(["03/11/2026,5.0,30.0,150"])).analisar()
        self.assertEqual(resultados[-1]["classificacao"], "Abaixo da zona segura")
        self.assertEqual(self.coletor.mensagens(), [])

        # Limites das faixas
        analisador = self.criar_analisador(self.csv_mais_4)
        limites = [(0.79, "Abaixo da zona segura", 0), (0.8, "Zona segura", 0), (1.3, "Zona segura", 0),
                   (1.31, "Atenção", 1), (1.5, "Atenção", 2), (1.51, "Zona de perigo", 3)]
        for acwr, classificacao, total_alertas in limites:
            perfil = {"semana": "Semana 01/11/2026:", "volume_agudo": 16.0, "volume_cronico": 11.5, "acwr": acwr}
            analisador.classificar_acwr(perfil)
            self.assertEqual(perfil["classificacao"], classificacao)
            self.assertEqual(len(self.coletor.alertas), total_alertas)

        self.assertTrue(self.coletor.mensagens()[1].startswith("ATENÇÃO (volume)"))
        self.assertTrue(self.coletor.mensagens()[2].startswith("ALERTA (volume)"))

    # Testa o pace agudo, o pace crônico (média dos treinos das últimas 4 semanas) e o alerta de mudança brusca de pace
    def test_3_3_mudanca_brusca_de_pace(self):
        resultados = self.criar_analisador(self.semana_atual(["03/11/2026,10.0,48.0,165"])).analisar()

        self.assertAlmostEqual(resultados[-1]["pace_agudo"], 4.8)
        self.assertAlmostEqual(resultados[-1]["pace_cronico"], 5.7)
        self.assertEqual(self.alertas_de("ALERTA (ritmo)"),
                         ["ALERTA (ritmo): pace médio da semana de 4:48 min/km, 15.8% mais rápido que a média das últimas 4 semanas (5:42 min/km)."])

        # O pace crônico é a média de todos os treinos, e não a média dos paces semanais
        resultados = self.criar_analisador(self.semana_atual(["03/11/2026,10.0,48.0,165", "05/11/2026,10.0,48.0,165"])).analisar()

        self.assertAlmostEqual(resultados[-1]["pace_cronico"], 5.52)
        self.assertEqual(self.alertas_de("ALERTA (ritmo)"), [])

        # Semana sem treino não tem pace da semana e não gera alerta de ritmo
        resultados = self.criar_analisador(self.semana_atual(["10/11/2026,10.0,60.0,150"])).analisar()

        self.assertEqual(resultados[4]["semana"], "Semana 01/11/2026:")
        self.assertIsNone(resultados[4]["pace_agudo"])
        self.assertAlmostEqual(resultados[4]["pace_cronico"], 6.0)
        self.assertEqual(self.alertas_de("ALERTA (ritmo)"), [])

        # Limite de 15% (diferença arredondada para 1 casa decimal) e pace mais lento não gera alerta
        analisador = self.criar_analisador(self.csv_mais_4)
        for pace_agudo, total_alertas in [(5.1, 1), (5.2, 1), (7.0, 1)]:
            analisador.classificar_pace({"semana": "Semana 01/11/2026:", "pace_agudo": pace_agudo, "pace_cronico": 6.0})
            self.assertEqual(len(self.coletor.alertas), total_alertas)

        self.assertIn("15.0% mais rápido", self.coletor.mensagens()[0])

    # Testa o alerta de recuperação: um alerta para cada sequência de 3 ou mais dias seguidos
    def test_3_4_dias_seguidos_sem_descanso(self):
        linhas = [
            "data,distancia_km,tempo_min,fc_media",
            "02/11/2026,5.0,30.0,150",
            "03/11/2026,5.0,30.0,150",
            # Dois treinos no mesmo dia contam como um dia só
            "03/11/2026,3.0,20.0,150",
            "04/11/2026,5.0,30.0,150",
            "05/11/2026,5.0,30.0,150",
            # Descanso no dia 06, o treino do dia 07 começa outra sequência
            "07/11/2026,5.0,30.0,150",
            "09/11/2026,5.0,30.0,150",
            "10/11/2026,5.0,30.0,150",
            "11/11/2026,5.0,30.0,150",
            # Só 2 dias seguidos, sem alerta
            "13/11/2026,5.0,30.0,150",
            "14/11/2026,5.0,30.0,150"
        ]

        self.criar_analisador(linhas).analisar()

        self.assertEqual(self.coletor.mensagens(), [
            "ALERTA (recuperação): treinos em 4 dias seguidos, de 02/11/2026 a 05/11/2026. Agende um dia de descanso.",
            "ALERTA (recuperação): treinos em 3 dias seguidos, de 09/11/2026 a 11/11/2026. Agende um dia de descanso."
        ])
        self.assertEqual(self.coletor.alertas[0]["semana"], "Semana 01/11/2026:")
        self.assertEqual(self.coletor.alertas[1]["semana"], "Semana 08/11/2026:")

    # Testa semanas sem 4 semanas de histórico ou com volume crônico 0
    def test_3_5_semanas_sem_historico_suficiente(self):
        resultados = self.criar_analisador(self.csv_menos_4).analisar()

        self.assertEqual(len(resultados), 3)
        for perfil in resultados:
            self.assertEqual(perfil["classificacao"], "Sem base de comparação")
            self.assertIsNone(perfil["volume_cronico"])
            self.assertIsNone(perfil["pace_cronico"])
            self.assertIsNone(perfil["acwr"])
        self.assertEqual(resultados[-1]["volume_agudo"], 30.0)
        self.assertEqual(self.coletor.mensagens(), [])

        # 4 semanas seguidas sem treino deixam o volume crônico em 0 (Semana 15/11/2026)
        linhas = [
            "data,distancia_km,tempo_min,fc_media",
            "05/10/2026,10.0,60.0,150",
            "12/10/2026,10.0,60.0,150",
            "19/10/2026,10.0,60.0,150",
            "24/11/2026,10.0,60.0,150"
        ]
        resultados = self.criar_analisador(linhas).analisar()

        self.assertEqual(len(resultados), 8)
        self.assertEqual(resultados[6]["semana"], "Semana 15/11/2026:")
        self.assertEqual(resultados[6]["volume_agudo"], 0.0)
        self.assertIsNone(resultados[6]["pace_agudo"])
        self.assertEqual(resultados[6]["volume_cronico"], 0.0)
        self.assertIsNone(resultados[6]["acwr"])
        self.assertEqual(resultados[6]["classificacao"], "Sem base de comparação")
        # A volta depois das semanas paradas é zona de perigo
        self.assertEqual(self.coletor.mensagens(),
                         ["ALERTA (volume): 10.0 km nesta semana contra média de 2.5 km nas últimas 4 semanas (ACWR 4.00). Zona de perigo para lesões."])

        # CSV sem nenhum treino válido não tem semanas para analisar
        self.assertEqual(self.criar_analisador(["data,distancia_km,tempo_min,fc_media"]).analisar(), [])


if __name__ == '__main__':
    unittest.main()
