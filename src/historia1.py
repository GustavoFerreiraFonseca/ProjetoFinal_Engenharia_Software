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

    def ler_linhas(self, caminho_arquivo):
        pass

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
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
        # ignora a primeira linha (cabeçalho)
        return linhas[1:] if len(linhas) > 1 else []

    def extrair_e_validar(self, linha):
        return processar_linha_csv(linha)
