# Arquivo destinado aos testes automatizados da história de usuário 1.
import unittest

# =- Funções e classes para a história de usuário (1) e seus critérios de aceitação -= 
def calcular_pace_formatado(distancia_km, tempo_minutos):

    if distancia_km <= 0 or tempo_minutos <= 0:
        return None
    
    pace_decimal = tempo_minutos / distancia_km
    
    minutos = int(pace_decimal)
    fracao_decimal = pace_decimal - minutos
    
    segundos = int(round(fracao_decimal * 60))
    
    if segundos == 60:
        minutos += 1
        segundos = 0
        
    return f"{minutos}:{segundos:02d} min/km"

class TestHistorialPace(unittest.TestCase):

    def test_1_1_leitura_dados_validos(self):
        distancia = 5.0
        tempo = 30.0
        
        self.assertGreater(distancia, 0)
        self.assertGreater(tempo, 0)

    def test_1_2_e_1_4_calculo_e_formatacao_pace(self):
        pace_obtido_1 = calcular_pace_formatado(10.0, 55.0)
        self.assertEqual(pace_obtido_1, "5:30 min/km")

        pace_obtido_2 = calcular_pace_formatado(5.0, 25.0)
        self.assertEqual(pace_obtido_2, "5:00 min/km")

    def test_1_3_ignorar_linhas_invalidas(self):
        self.assertIsNone(calcular_pace_formatado(0, 30))
        self.assertIsNone(calcular_pace_formatado(-5, 25))
        self.assertIsNone(calcular_pace_formatado(5, 0))
        self.assertIsNone(calcular_pace_formatado(5, -10))

if __name__ == '__main__':
    unittest.main()