# Funções e classes da História de usuário 2.

from datetime import datetime, timedelta

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

def indentificarDomingo(data):
    dia = datetime.strptime(data, '%d/%m/%Y')
    
    dias_para_domingo = (dia.weekday() + 1) % 7
    domingo = dia - timedelta(days=dias_para_domingo)
            
    return domingo

def agruparSemana(treinos):
    treinos_ordenados = ordenarSemana(treinos)

    semanas = {}

    for treino in treinos_ordenados:
        domingo = indentificarDomingo(treino['data'])

        chave = domingo.strftime('%d/%m/%Y')

        if chave not in semanas:
            semanas[chave] = []

        semanas[chave].append(treino)

    return list(semanas.values())

def identificarSemana(treinos):
    agrupamentos = agruparSemana(treinos)

    semanas = {}

    for grupo in agrupamentos:
        domingo = indentificarDomingo(grupo[0]['data'])

        chave_semana = f"Semana {domingo.strftime('%d/%m/%Y')}:"

        semanas[chave_semana] = grupo

    return semanas