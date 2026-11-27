# Refatoração da história de usuário (3) - Sprint 4
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

from src.historia1 import processar_linha_csv
from src.historia2 import agruparSemana, indentificarDomingo

# =- padrão de projeto escolhido : Observer -=
# =- Motivo : desacoplar o cálculo dos alertas da forma como eles são exibidos
"""
        Na versão da Sprint 3 cada função da HU 3 calculava um valor, alterava o perfil do usuário e já
    imprimia o alerta no terminal com print(). Com isso o cálculo ficava preso à saída no terminal, e para
    levar os alertas para o relatório em txt (saída final do sistema) teríamos que mexer em todas as funções.
        Com o Observer, a classe AnalisadorLesoes (sujeito) só faz os cálculos e avisa os observadores
    cadastrados quando acontece um alerta. Quem decide o que fazer com o alerta é o observador:
    o AlertaTerminal imprime no terminal (mesmo comportamento da Sprint 3) e o ColetorAlertas guarda os
    alertas em uma lista, que é usada nos testes e vai ser usada na geração do relatório.
        Para uma nova saída basta criar outro observador, sem alterar a classe de análise.
"""

"""
Regras de negócio para HU 3 (mesmas da Sprint 3):
- O volume agudo é a soma das distâncias da semana.
- O volume crônico é a soma das distâncias das últimas 4 semanas (incluindo a atual) dividida por 4.
- O pace agudo é a média dos paces dos treinos da semana (pace = tempo / distancia, em min/km).
- O pace crônico é a média dos paces de todos os treinos das últimas 4 semanas.
- O ACWR é volume agudo / volume crônico, arredondado para 2 casas decimais.
- Classificação do ACWR:
    - Abaixo da zona segura: ACWR < 0.8 (sem alerta)
    - Zona segura: 0.8 <= ACWR <= 1.3 (sem alerta)
    - Atenção: 1.3 < ACWR <= 1.5 (alerta de atenção)
    - Zona de perigo: ACWR > 1.5 (alerta de perigo de lesões)
    - Sem base de comparação: menos de 4 semanas de histórico ou volume crônico 0 (sem alerta)
- Alerta de ritmo: ((pace_cronico - pace_agudo) / pace_cronico) * 100, arredondado para 1 casa, >= 15.
- Alerta de recuperação: um alerta para cada sequência de 3 ou mais dias seguidos com treino.
  Dois treinos no mesmo dia contam como um dia só. O alerta fica na semana do último dia da sequência.

Diferenças em relação à Sprint 3:
- Semana sem treino fica com pace agudo None (causava um bug de alerta de ritmo de 100%).
- "Sem base de comparação" virou a classificação da semana e não é mais impresso como alerta (critério 3.5).
- Como o histórico chega inteiro, o alerta de recuperação sai uma vez por sequência (critério 3.4),
  e não mais a cada novo treino (foi um erro de interpretação inicial, mas já foi concertado).
"""


# =- Observer -=

# Interface dos observadores, abstrata para não ser instanciada
class ObservadorAlerta(ABC):
    @abstractmethod
    def atualizar(self, semana, mensagem):
        pass


# Observador Concreto que imprime o alerta no terminal
class AlertaTerminal(ObservadorAlerta):
    def atualizar(self, semana, mensagem):
        print(mensagem)


# Observador Concreto que guarda os alertas para o relatório e para os testes
class ColetorAlertas(ObservadorAlerta):
    def __init__(self):
        self.alertas = []

    def atualizar(self, semana, mensagem):
        self.alertas.append({"semana": semana, "mensagem": mensagem})

    def mensagens(self):
        return [alerta["mensagem"] for alerta in self.alertas]


# =- classe de análise de risco de lesões (sujeito do Observer) -=

class AnalisadorLesoes:

    def __init__(self, treinos):
        self.__observadores = []
        self.__treinos = treinos
        self.__banco_semanas = self.montar_semanas(treinos)

    # Lê o CSV com o histórico completo usando a leitura da HU 1
    # Cabeçalho e linhas inválidas são ignorados (critério 1.3)
    @classmethod
    def de_csv(cls, caminho_csv):
        treinos = []
        with open(caminho_csv, encoding="utf-8-sig") as arquivo:
            for linha in arquivo:
                dados = processar_linha_csv(linha)
                if dados is None:
                    continue

                data, distancia, tempo, freq_cardiaca = dados
                if distancia <= 0 or tempo <= 0:
                    continue
                try:
                    datetime.strptime(data, "%d/%m/%Y")
                except ValueError:
                    continue

                treinos.append({"data": data, "distancia": distancia, "tempo": tempo, "freq_cardiaca": freq_cardiaca})
        return cls(treinos)

    def adicionar_observador(self, observador):
        self.__observadores.append(observador)

    def remover_observador(self, observador):
        self.__observadores.remove(observador)

    def notificar(self, semana, mensagem):
        for observador in self.__observadores:
            observador.atualizar(semana, mensagem)

    def get_banco_semanas(self):
        return self.__banco_semanas

    # Agrupa os treinos por semana com a HU 2 e completa as semanas sem treino entre a primeira e a última
    # Formato igual ao banco de semanas da Sprint 3: [ { "Semana DD/MM/AAAA:": [treinos] }, ... ]
    @staticmethod
    def montar_semanas(treinos):
        if not treinos:
            return []

        semanas = {indentificarDomingo(grupo[0]["data"]): grupo for grupo in agruparSemana(treinos)}

        banco_semanas = []
        domingo = min(semanas)
        while domingo <= max(semanas):
            banco_semanas.append({f"Semana {domingo.strftime('%d/%m/%Y')}:": semanas.get(domingo, [])})
            domingo += timedelta(days=7)
        return banco_semanas

    # Analisa todas as semanas do histórico e devolve a lista de perfis (um por semana)
    def analisar(self):
        alertas_recuperacao = self.verificar_recuperacao()
        resultados = []

        for indice, semana in enumerate(self.__banco_semanas):
            nome_semana = list(semana.keys())[0]
            perfil = {
                "semana": nome_semana,
                "volume_agudo": None,
                "pace_agudo": None,
                "volume_cronico": None,
                "pace_cronico": None,
                "acwr": None,
                "classificacao": None
            }

            self.calcular_volume_pace_agudo(indice, perfil)
            self.calcular_volume_pace_cronico(indice, perfil)
            self.calcular_acwr(perfil)
            self.classificar_acwr(perfil)
            self.classificar_pace(perfil)

            for mensagem in alertas_recuperacao.get(nome_semana, []):
                self.notificar(nome_semana, mensagem)

            resultados.append(perfil)

        return resultados

    def treinos_da_semana(self, indice):
        return list(self.__banco_semanas[indice].values())[0]

    def calcular_volume_pace_agudo(self, indice, perfil):
        treinos = self.treinos_da_semana(indice)

        perfil["volume_agudo"] = sum(treino["distancia"] for treino in treinos)
        if treinos:
            perfil["pace_agudo"] = sum(treino["tempo"] / treino["distancia"] for treino in treinos) / len(treinos)
        else:
            perfil["pace_agudo"] = None

    def calcular_volume_pace_cronico(self, indice, perfil):
        # Sem 4 semanas de histórico (contando a partir da primeira semana com treino)
        if indice < 3:
            return

        treinos = [treino for i in range(indice - 3, indice + 1) for treino in self.treinos_da_semana(i)]

        perfil["volume_cronico"] = sum(treino["distancia"] for treino in treinos) / 4
        if treinos:
            perfil["pace_cronico"] = sum(treino["tempo"] / treino["distancia"] for treino in treinos) / len(treinos)
        else:
            perfil["pace_cronico"] = None

    def calcular_acwr(self, perfil):
        if not perfil["volume_cronico"]:
            perfil["acwr"] = None
            return

        perfil["acwr"] = round(perfil["volume_agudo"] / perfil["volume_cronico"], 2)

    def classificar_acwr(self, perfil):
        acwr = perfil["acwr"]
        if acwr is None:
            perfil["classificacao"] = "Sem base de comparação"
        elif acwr < 0.8:
            perfil["classificacao"] = "Abaixo da zona segura"
        elif acwr <= 1.3:
            perfil["classificacao"] = "Zona segura"
        elif acwr <= 1.5:
            perfil["classificacao"] = "Atenção"
            self.notificar(perfil.get("semana"), f"ATENÇÃO (volume): {perfil['volume_agudo']:.1f} km nesta semana contra média de {perfil['volume_cronico']:.1f} km nas últimas 4 semanas (ACWR {acwr:.2f}).")
        else:
            perfil["classificacao"] = "Zona de perigo"
            self.notificar(perfil.get("semana"), f"ALERTA (volume): {perfil['volume_agudo']:.1f} km nesta semana contra média de {perfil['volume_cronico']:.1f} km nas últimas 4 semanas (ACWR {acwr:.2f}). Zona de perigo para lesões.")

    def classificar_pace(self, perfil):
        pace_agudo = perfil["pace_agudo"]
        pace_cronico = perfil["pace_cronico"]
        if pace_agudo is None or pace_cronico is None:
            return

        diferenca = round(((pace_cronico - pace_agudo) / pace_cronico) * 100, 1)
        if diferenca >= 15:
            segundos_agudo = round(pace_agudo * 60)
            segundos_cronico = round(pace_cronico * 60)
            self.notificar(perfil.get("semana"), f"ALERTA (ritmo): pace médio da semana de {segundos_agudo // 60}:{segundos_agudo % 60:02d} min/km, {diferenca}% mais rápido que a média das últimas 4 semanas ({segundos_cronico // 60}:{segundos_cronico % 60:02d} min/km).")

    # Procura as sequências de dias seguidos no histórico inteiro
    # Devolve { "Semana DD/MM/AAAA:": [mensagens] }, com a semana do último dia de cada sequência
    def verificar_recuperacao(self):
        datas = sorted({datetime.strptime(treino["data"], "%d/%m/%Y") for treino in self.__treinos})

        sequencias = []
        for data in datas:
            if sequencias and data - sequencias[-1][1] == timedelta(days=1):
                sequencias[-1][1] = data
            else:
                sequencias.append([data, data])

        alertas = {}
        for inicio, fim in sequencias:
            dias = (fim - inicio).days + 1
            if dias >= 3:
                semana = f"Semana {indentificarDomingo(fim.strftime('%d/%m/%Y')).strftime('%d/%m/%Y')}:"
                alertas.setdefault(semana, []).append(f"ALERTA (recuperação): treinos em {dias} dias seguidos, de {inicio.strftime('%d/%m/%Y')} a {fim.strftime('%d/%m/%Y')}. Agende um dia de descanso.")
        return alertas


# Execução pelo terminal (a partir da raiz do repositório):
# python -m src.analisador_lesoes caminho/do/historico.csv
if __name__ == "__main__":
    import sys

    analisador = AnalisadorLesoes.de_csv(sys.argv[1])
    analisador.adicionar_observador(AlertaTerminal())
    for perfil in analisador.analisar():
        print(f"{perfil['semana']} {perfil['volume_agudo']:.1f} km - {perfil['classificacao']}")
