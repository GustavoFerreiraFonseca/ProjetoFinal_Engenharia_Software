from datetime import datetime, timedelta
from abc import ABC, abstractmethod

def processar_linha_csv(linha_texto):
    partes = linha_texto.split(',')
    if len(partes) < 4:
        return None
    try:
        data = partes[0].strip()
        distancia = float(partes[1])
        tempo = float(partes[2])
        freq_cardiaca = int(partes[3])
        if distancia <= 0 or tempo <= 0 or freq_cardiaca <= 0:
            return None
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

# ----------Template Method-----------
# Define o esqueleto do algoritmo de importação e validação de treinos,
# permitindo que as outras classes derivadas implementem a leitura específica de cada formato

class ProcessadorArquivoTreino(ABC):
    def processar(self, caminho_arquivo):
        linhas_brutas = self.ler_linhas(caminho_arquivo)
        treinos_validos = []

        for linha in linhas_brutas:
            dados_extraidos = self.extrair_e_validar(linha)
            if dados_extraidos is not None:
                registro = self.montar_registro(dados_extraidos)
                treinos_validos.append(registro)

        return treinos_validos

    @abstractmethod
    def ler_linhas(self, caminho_arquivo):
        pass

    @abstractmethod
    def extrair_e_validar(self, linha):
        pass

    def montar_registro(self, dados_extraidos):
        data, distancia, tempo, freq_cardiaca = dados_extraidos
        pace = calcular_pace_formatado(distancia, tempo)
        return {
            "data": data,
            "distancia": distancia,
            "tempo": tempo,
            "frequencia_cardiaca": freq_cardiaca,
            "pace": pace
        }

class ProcessadorCSV(ProcessadorArquivoTreino):
    def ler_linhas(self, caminho_arquivo):
        with open(caminho_arquivo, "r", encoding="utf-8-sig") as arquivo:
            linhas = arquivo.readlines()
        # ignora a primeira linha (cabeçalho)
        return linhas[1:] if len(linhas) > 1 else []

    def extrair_e_validar(self, linha):
        dados = processar_linha_csv(linha)
        if dados is None:
            return None
        try:
            datetime.strptime(dados[0], "%d/%m/%Y")
            return dados
        except ValueError:
            return None

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

# Interface dos observadores, abstrata para não ser instanciada
class ObservadorAlerta(ABC):
    @abstractmethod
    def atualizar(self, semana, mensagem):
        pass

# Observador que imprime o alerta no terminal
class AlertaTerminal(ObservadorAlerta):
    def atualizar(self, semana, mensagem):
        print(mensagem)

# Observador que guarda os alertas para o relatório e para os testes
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

    @classmethod
    def de_csv(cls, caminho_csv):
        treinos = ProcessadorCSV().processar(caminho_csv)
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

def gerar_relatorio(caminho_csv, caminho_saida="relatorio_final.txt"):
    treinos = ProcessadorCSV().processar(caminho_csv)
    if not treinos:
        return "Nenhum treino válido encontrado no arquivo."

    semanas = identificarSemana(treinos)
    recordes = RecordPessoal()

    for treino in treinos:
        recordes.set_maiorDistancia(treino["distancia"])
        pace_decimal = treino["tempo"] / treino["distancia"]
        recordes.set_menorPaceMedio(pace_decimal)

    for lista_treinos in semanas.values():
        volume_semana = sum(t["distancia"] for t in lista_treinos)
        recordes.set_maiorVolumeSemanal(volume_semana)
        recordes.set_maiorNumTreinos(len(lista_treinos))

    analisador = AnalisadorLesoes(treinos)
    coletor = ColetorAlertas()
    analisador.adicionar_observador(coletor)
    perfis = analisador.analisar()

    linhas = []
    linhas.append("=" * 60)
    linhas.append("RELATÓRIO DE ANÁLISE DE TREINOS DE CORRIDA")
    linhas.append("=" * 60)
    linhas.append(f"Total de treinos válidos: {len(treinos)}\n")

    linhas.append("--- RESUMO SEMANAL ---")
    for chave_semana, lista_treinos in semanas.items():
        vol_formatado = calcular_volume_semanal([t["distancia"] for t in lista_treinos])
        linhas.append(f"{chave_semana} {len(lista_treinos)} treinos | Volume: {vol_formatado}")
        for t in lista_treinos:
            linhas.append(f"  - {t['data']}: {t['distancia']} km em {t['tempo']} min | Pace: {t['pace']} | FC: {t['frequencia_cardiaca']} bpm")

    linhas.append("\n--- RECORDES PESSOAIS ---")
    linhas.append(f"Maior distância: {recordes.get_maiorDistancia():.2f} km")
    linhas.append(f"Maior volume semanal: {recordes.get_maiorVolumeSemanal():.2f} km")
    linhas.append(f"Maior número de treinos na semana: {recordes.get_maiorNumTreinos()}")
    linhas.append(f"Menor pace (mais rápido): {calcular_pace_formatado(1.0, recordes.get_menorPaceMedio())}")

    linhas.append("\n--- ANÁLISE DE CARGA E RISCO DE LESÕES (ACWR) ---")
    for perfil in perfis:
        acwr_texto = f"{perfil['acwr']:.2f}" if perfil["acwr"] is not None else "N/A"
        linhas.append(f"{perfil['semana']} Volume: {perfil['volume_agudo']:.2f} km | ACWR: {acwr_texto} | Status: {perfil['classificacao']}")

    linhas.append("\n--- ALERTAS PREVENTIVOS ---")
    if coletor.alertas:
        for item in coletor.alertas:
            linhas.append(f"[{item['semana']}] {item['mensagem']}")
    else:
        linhas.append("Nenhum alerta de sobrecarga ou recuperação detectado.")
    linhas.append("=" * 60)

    relatorio_texto = "\n".join(linhas)
    with open(caminho_saida, "w", encoding="utf-8") as arquivo_saida:
        arquivo_saida.write(relatorio_texto + "\n")

    return relatorio_texto

if __name__ == "__main__":
    import sys

    caminho = sys.argv[1] if len(sys.argv) > 1 else input("Informe o caminho do arquivo CSV: ").strip()
    print(gerar_relatorio(caminho))
