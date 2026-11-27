# Arquivo destinado aos testes automatizados da história de usuário 1.
import unittest

# Importa as funções desenvolvidas
from src.historia1 import processar_linha_csv, calcular_pace_formatado

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

if __name__ == '__main__':
    unittest.main()