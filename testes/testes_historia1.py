# Arquivo destinado aos testes automatizados da história de usuário 1.
import unittest

# =- Funções para a história de usuário 1 e seus critérios de aceitação -= 

def processar_linha_csv(linha_texto):
    partes = linha_texto.split(',')
    if len(partes) < 4:
        return None
    try:
        data = partes[0].strip()
        distancia = float(partes[1])
        tempo = float(partes[2])
        freq_cardiaca = int(partes[3])
        return data, distancia, tempo, freq_cardiaca
    except ValueError:
        return None

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
        linha_csv_exemplo = "2026-11-01,5.0,30.0,150"
        dados = processar_linha_csv(linha_csv_exemplo)
        
        self.assertIsNotNone(dados)
        data, distancia, tempo, freq_cardiaca = dados
        
        self.assertEqual(data, "2026-11-01")
        self.assertEqual(distancia, 5.0)
        self.assertEqual(tempo, 30.0)
        self.assertEqual(freq_cardiaca, 150)

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
