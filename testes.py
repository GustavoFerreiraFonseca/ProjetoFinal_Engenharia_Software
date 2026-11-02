# Arquivo destinado aos testes automatizados.
import unittest
from datetime import datetime, timedelta

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

# =- Funções e classes para a história de usuário (2) e seus critérios de aceitação -= 

class RecordPessoal:
    def __init__(self):
        self.__maiorDistancia = 0
        self.__maiorVolumeSemanal = 0
        self.__maiorNumTreinos = 0
        self.__menorPaceMedio = 0

    def isgreater(self, novo_recorde, atual_recorde):
        if novo_recorde > atual_recorde or atual_recorde == 0:
            return True
        return False

    def islower(self, novo_recorde, atual_recorde):
        if novo_recorde < atual_recorde or atual_recorde == 0:
            return True
        return False

    def get_maiorDistancia(self): return self.__maiorDistancia 
    def get_maiorVolumeSemanal(self): return self.__maiorVolumeSemanal 
    def get_maiorNumTreinos(self): return self.__maiorNumTreinos 
    def get_menorPaceMedio(self): return self.__menorPaceMedio 

    def set_maiorDistancia(self, maiorDistancia): 
        if self.isgreater(maiorDistancia, self.get_maiorDistancia()):
            self.__maiorDistancia = maiorDistancia

    def set_maiorVolumeSemanal(self, maiorVolumeSemanal): 
        if self.isgreater(maiorVolumeSemanal, self.get_maiorVolumeSemanal()):
            self.__maiorVolumeSemanal = maiorVolumeSemanal

    def set_maiorNumTreinos(self, maiorNumTreinos): 
        if self.isgreater(maiorNumTreinos, self.get_maiorNumTreinos()):
            self.__maiorNumTreinos = maiorNumTreinos

    def set_menorPaceMedio(self, menorPaceMedio): 
        if self.islower(menorPaceMedio, self.get_menorPaceMedio()):    
            self.__menorPaceMedio = menorPaceMedio

def calcular_volume_semanal(distancias):
    volume_semanal = sum(distancias)
    return f"{volume_semanal:.2f} km"

def ordenarSemana(treinos):
    return sorted(treinos, key= lambda x: datetime.strptime(x["data"], "%d/%m/%Y"))

def identificarSemana(treinos):
    treinos_ordenados = ordenarSemana(treinos)

    semanas = {}
    for treino in treinos_ordenados:
        dia = datetime.strptime(treino['data'], '%d/%m/%Y')

        dias_para_domingo = (dia.weekday() + 1) % 7
        domingo = dia - timedelta(days=dias_para_domingo)
        
        chave_semana = f"Semana {domingo.strftime('%d/%m/%Y')}:"
        
        if chave_semana not in semanas:
            semanas[chave_semana] = []
        semanas[chave_semana].append(treino)
        
    return semanas

class TestHistorialVolume(unittest.TestCase):
    def test_2_1_e_2_4_agrupamento_e_identificacao(self):
        treinos = [
            { "data": "05/11/2026", "distancia": 7.8},
            { "data": "01/11/2026", "distancia": 5.0},
            { "data": "10/11/2026", "distancia": 4.6}
        ]

        resultado = identificarSemana(treinos)
        chaves = list(resultado.keys())

        self.assertIn("Semana 01/11/2026:", chaves)
        self.assertIn("Semana 08/11/2026:", chaves)

        semana1_treinos = resultado["Semana 01/11/2026:"]
        self.assertEqual(len(semana1_treinos), 2)
        self.assertEqual(semana1_treinos[0]['data'], '01/11/2026')
        self.assertEqual(semana1_treinos[1]['data'], '05/11/2026')

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

    def test_2_2_calculo_volumeSemanal(self):
        distancias = [5.0, 3.34, 2.25, 4.76, 1.44]

        volume_semanal = calcular_volume_semanal(distancias)
        self.assertEqual(volume_semanal, "16.79 km")

if __name__ == '__main__':
    unittest.main()