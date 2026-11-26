# Arquivo destinado aos testes automatizados da história de usuário 2.
import unittest
from src.historia2 import *
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

if __name__ == '__main__':
    unittest.main()