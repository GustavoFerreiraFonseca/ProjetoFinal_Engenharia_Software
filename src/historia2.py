
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

# =- padrão de projeto escolhido : Strategy -=
# =- Motivo : Otimização da estratégia de comparação no sistema de recordes Pessoais
"""
        Na implementação original, os recordes pessoais erão atualizados baseados nos seguintes metodos: 
    isgreater(self) e islower(self), que simplismente tinha como oobjetivo compararem o valor atual com o novo recebido
    e atualizar o recorde dependendo da resposta do metodo.
        Para fins de desaclopamento de responsabilidades, foi utilizado o padrão de projeto Strategy com o objetivo de criar 
    uma forma de manter a responsabilidade de armazenamento e atualização dos dados, no caso de recordes pessoais apenas 
    para a classe RecordPessoal, enquanto a função de comparação para a interface EstretegiaRecorde.
        Dessa maneira, o sistema preservou o comportamento original, e com o uso do Strategy, conseguimos reduzir a 
    concentração de regras e responsabilidades em um só lugar, melhorando a organização do código. 
"""

# Define Interface EstretegiaRecorde para definir um padrão para os tipos de estratégia
# definimos como abstrata para que não exista a possibilidade de que exista uma instância com essa classe
class EstrategiaRecorde(ABC):
    @abstractmethod
    def deve_atualizar(self, novo_recorde, atual_recorde):
        pass

# estratégia de maior recorde -> define como verdadeiro se o novo valor for maior que o atual 
class MaiorRecorde(EstrategiaRecorde):
    def deve_atualizar(self, novo_recorde, atual_recorde):
        return novo_recorde > atual_recorde or atual_recorde == 0


# estratégia de menor recorde -> define como verdadeiro se o novo valor for menor que o atual 
class MenorRecorde(EstrategiaRecorde):
    def deve_atualizar(self, novo_recorde, atual_recorde):
        return novo_recorde < atual_recorde or atual_recorde == 0


# =- classe de Recorde Pessoal -=

class RecordPessoal:

    def __init__(self):
        self.__maiorDistancia = 0
        self.__maiorVolumeSemanal = 0
        self.__maiorNumTreinos = 0
        self.__menorPaceMedio = 0

        # Estratégias utilizadas para atualizar os recordes
        self.__estrategiaMaior = MaiorRecorde()
        self.__estrategiaMenor = MenorRecorde()

    def isgreater(self, novo_recorde, atual_recorde):
        return self.__estrategiaMaior.deve_atualizar(
            novo_recorde, atual_recorde
        )

    def islower(self, novo_recorde, atual_recorde):
        return self.__estrategiaMenor.deve_atualizar(
            novo_recorde, atual_recorde
        )

    def get_maiorDistancia(self):
        return self.__maiorDistancia

    def get_maiorVolumeSemanal(self):
        return self.__maiorVolumeSemanal

    def get_maiorNumTreinos(self):
        return self.__maiorNumTreinos

    def get_menorPaceMedio(self):
        return self.__menorPaceMedio

    def set_maiorDistancia(self, maiorDistancia):
        if self.__estrategiaMaior.deve_atualizar(maiorDistancia, self.__maiorDistancia):
            self.__maiorDistancia = maiorDistancia

    def set_maiorVolumeSemanal(self, maiorVolumeSemanal):
        if self.__estrategiaMaior.deve_atualizar(maiorVolumeSemanal, self.__maiorVolumeSemanal):
            self.__maiorVolumeSemanal = maiorVolumeSemanal

    def set_maiorNumTreinos(self, maiorNumTreinos):
        if self.__estrategiaMaior.deve_atualizar(maiorNumTreinos, self.__maiorNumTreinos):
            self.__maiorNumTreinos = maiorNumTreinos

    def set_menorPaceMedio(self, menorPaceMedio):
        if self.__estrategiaMenor.deve_atualizar(menorPaceMedio, self.__menorPaceMedio):
            self.__menorPaceMedio = menorPaceMedio


# =- Funções para calculo de volume semanal e organização semanal -=

def calcular_volume_semanal(distancias):
    volume_semanal = sum(distancias)
    return f"{volume_semanal:.2f} km"


def ordenarSemana(treinos):
    return sorted(
        treinos,
        key=lambda x: datetime.strptime(x["data"], "%d/%m/%Y")
    )


def indentificarDomingo(data):
    dia = datetime.strptime(data, "%d/%m/%Y")

    dias_para_domingo = (dia.weekday() + 1) % 7
    domingo = dia - timedelta(days=dias_para_domingo)

    return domingo


def agruparSemana(treinos):
    treinos_ordenados = ordenarSemana(treinos)

    semanas = {}

    for treino in treinos_ordenados:
        domingo = indentificarDomingo(treino["data"])
        chave = domingo.strftime("%d/%m/%Y")

        if chave not in semanas:
            semanas[chave] = []

        semanas[chave].append(treino)

    return list(semanas.values())


def identificarSemana(treinos):
    agrupamentos = agruparSemana(treinos)

    semanas = {}

    for grupo in agrupamentos:
        domingo = indentificarDomingo(grupo[0]["data"])

        chave_semana = f"Semana {domingo.strftime('%d/%m/%Y')}:"

        semanas[chave_semana] = grupo

    return semanas
