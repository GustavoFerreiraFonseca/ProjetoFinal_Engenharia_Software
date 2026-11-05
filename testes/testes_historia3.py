# Arquivo destinado aos testes automatizados da história de usuário 3.
import unittest
from datetime import datetime, timedelta
from testes_historia1 import calcular_pace_formatado
from testes_historia2 import identificarSemana

# =- Funções e classes para a história de usuário (3) e seus critérios de aceitação -=

# Faixas do ACWR tiradas de Gabbett (2016): zona segura entre 0.8 e 1.3 e zona de perigo acima de 1.5
ACWR_MIN_SEGURO = 0.8
ACWR_MAX_SEGURO = 1.3
ACWR_PERIGO = 1.5

# Volume e pace crônicos usam as últimas 4 semanas (28 dias), incluindo a semana atual
SEMANAS_CRONICAS = 4

# Mudança brusca de pace, ligada a lesões no tendão de Aquiles e na panturrilha por Nielsen et al. (2013)
LIMITE_PACE = 15.0

DIAS_SEGUIDOS_ALERTA = 3

def chave_para_data(chave):
    return datetime.strptime(chave.replace("Semana ", "").replace(":", ""), "%d/%m/%Y")

def calcular_pace_treino(treino):
    return treino["tempo"] / treino["distancia"]

def calcular_acwr(volume_agudo, volume_cronico):
    if volume_cronico is None or volume_cronico <= 0:
        return None
    return round(volume_agudo / volume_cronico, 2)

def classificar_acwr(acwr):
    if acwr is None:
        return "Sem base de comparação"
    if acwr > ACWR_PERIGO:
        return "Zona de perigo"
    if acwr > ACWR_MAX_SEGURO:
        return "Atenção"
    if acwr >= ACWR_MIN_SEGURO:
        return "Zona segura"
    return "Abaixo da zona segura"

def calcular_diferenca_pace(pace_semana, pace_cronico):
    if pace_cronico is None or pace_cronico <= 0:
        return None
    return round((pace_cronico - pace_semana) / pace_cronico * 100, 1)

def analisar_semanas(treinos):
    treinos = [t for t in treinos if t["distancia"] > 0 and t["tempo"] > 0]

    semanas = {}
    for chave, treinos_semana in identificarSemana(treinos).items():
        semanas[chave_para_data(chave)] = treinos_semana

    primeira_semana = min(semanas)
    resultado = []

    for domingo, treinos_semana in semanas.items():
        volume_agudo = sum(t["distancia"] for t in treinos_semana)
        pace_semana = sum(calcular_pace_treino(t) for t in treinos_semana) / len(treinos_semana)

        janela = [domingo - timedelta(days=7 * i) for i in range(SEMANAS_CRONICAS)]
        tem_historico = janela[-1] >= primeira_semana

        volume_cronico = None
        pace_cronico = None
        if tem_historico:
            volume_cronico = sum(sum(t["distancia"] for t in semanas.get(d, [])) for d in janela) / SEMANAS_CRONICAS
            paces_janela = [calcular_pace_treino(t) for d in janela for t in semanas.get(d, [])]
            pace_cronico = sum(paces_janela) / len(paces_janela)

        acwr = calcular_acwr(volume_agudo, volume_cronico)
        nivel = classificar_acwr(acwr)
        diferenca_pace = calcular_diferenca_pace(pace_semana, pace_cronico)

        alertas = []
        if nivel == "Atenção":
            alertas.append(f"ATENÇÃO (volume): {volume_agudo:.1f} km nesta semana contra média de "
                           f"{volume_cronico:.1f} km nas últimas 4 semanas (ACWR {acwr:.2f}).")
        if nivel == "Zona de perigo":
            alertas.append(f"ALERTA (volume): {volume_agudo:.1f} km nesta semana contra média de "
                           f"{volume_cronico:.1f} km nas últimas 4 semanas (ACWR {acwr:.2f}). Zona de perigo para lesões.")
        if diferenca_pace is not None and diferenca_pace >= LIMITE_PACE:
            alertas.append(f"ALERTA (ritmo): pace médio da semana de {calcular_pace_formatado(1, pace_semana)}, "
                           f"{diferenca_pace:.1f}% mais rápido que a média das últimas 4 semanas "
                           f"({calcular_pace_formatado(1, pace_cronico)}).")

        resultado.append({
            "semana": domingo.strftime("%d/%m/%Y"),
            "volume": volume_agudo,
            "volume_cronico": volume_cronico,
            "acwr": acwr,
            "nivel_volume": nivel,
            "diferenca_pace": diferenca_pace,
            "alertas": alertas
        })

    return resultado

def alertas_recuperacao(treinos):
    dias = sorted({datetime.strptime(t["data"], "%d/%m/%Y") for t in treinos})

    sequencias = []
    inicio = None
    for i, dia in enumerate(dias):
        if inicio is None or dia - dias[i - 1] != timedelta(days=1):
            inicio = dia
            sequencias.append([inicio, dia])
        else:
            sequencias[-1][1] = dia

    alertas = []
    for inicio, fim in sequencias:
        quantidade = (fim - inicio).days + 1
        if quantidade >= DIAS_SEGUIDOS_ALERTA:
            alertas.append(f"ALERTA (recuperação): treinos em {quantidade} dias seguidos, de "
                           f"{inicio.strftime('%d/%m/%Y')} a {fim.strftime('%d/%m/%Y')}. Agende um dia de descanso.")
    return alertas

class TestAlertasLesao(unittest.TestCase):

    def test_3_1_volume_semanal_e_acwr(self):
        self.assertEqual(calcular_acwr(40, 25), 1.6)
        self.assertEqual(calcular_acwr(20, 15), 1.33)

        treinos = [
            { "data": "06/10/2026", "distancia": 20.0, "tempo": 120.0},
            { "data": "13/10/2026", "distancia": 20.0, "tempo": 120.0},
            { "data": "20/10/2026", "distancia": 20.0, "tempo": 120.0},
            { "data": "27/10/2026", "distancia": 25.0, "tempo": 150.0},
            { "data": "29/10/2026", "distancia": 15.0, "tempo": 90.0}
        ]
        semana = analisar_semanas(treinos)[3]

        self.assertEqual(semana["semana"], "25/10/2026")
        self.assertEqual(semana["volume"], 40.0)
        self.assertEqual(semana["volume_cronico"], 25.0)
        self.assertEqual(semana["acwr"], 1.6)

        # semana sem treino dentro da janela conta como volume 0
        treinos = [
            { "data": "06/10/2026", "distancia": 20.0, "tempo": 120.0},
            { "data": "20/10/2026", "distancia": 20.0, "tempo": 120.0},
            { "data": "27/10/2026", "distancia": 20.0, "tempo": 120.0}
        ]
        semana = analisar_semanas(treinos)[2]
        self.assertEqual(semana["volume_cronico"], 15.0)
        self.assertEqual(semana["acwr"], 1.33)

    def test_3_2_classificacao_e_alertas_de_volume(self):
        self.assertEqual(classificar_acwr(0.79), "Abaixo da zona segura")
        self.assertEqual(classificar_acwr(0.8), "Zona segura")
        self.assertEqual(classificar_acwr(1.3), "Zona segura")
        self.assertEqual(classificar_acwr(1.31), "Atenção")
        self.assertEqual(classificar_acwr(1.5), "Atenção")
        self.assertEqual(classificar_acwr(1.51), "Zona de perigo")

        base = [
            { "data": "06/10/2026", "distancia": 10.0, "tempo": 60.0},
            { "data": "13/10/2026", "distancia": 10.0, "tempo": 60.0},
            { "data": "20/10/2026", "distancia": 10.0, "tempo": 60.0}
        ]

        atencao = analisar_semanas(base + [{ "data": "27/10/2026", "distancia": 16.0, "tempo": 96.0}])[3]
        self.assertEqual(atencao["alertas"],
                         ["ATENÇÃO (volume): 16.0 km nesta semana contra média de 11.5 km nas últimas 4 semanas (ACWR 1.39)."])

        perigo = analisar_semanas(base + [{ "data": "27/10/2026", "distancia": 30.0, "tempo": 180.0}])[3]
        self.assertEqual(perigo["alertas"],
                         ["ALERTA (volume): 30.0 km nesta semana contra média de 15.0 km nas últimas 4 semanas (ACWR 2.00). Zona de perigo para lesões."])

        abaixo = analisar_semanas(base + [{ "data": "27/10/2026", "distancia": 5.0, "tempo": 30.0}])[3]
        self.assertEqual(abaixo["nivel_volume"], "Abaixo da zona segura")
        self.assertEqual(abaixo["alertas"], [])

    def test_3_3_mudanca_brusca_de_pace(self):
        self.assertEqual(calcular_diferenca_pace(5.0, 6.0), 16.7)
        self.assertEqual(calcular_diferenca_pace(5.1, 6.0), 15.0)
        self.assertEqual(calcular_diferenca_pace(5.2, 6.0), 13.3)

        treinos = [
            { "data": "06/10/2026", "distancia": 10.0, "tempo": 60.0},
            { "data": "13/10/2026", "distancia": 10.0, "tempo": 60.0},
            { "data": "20/10/2026", "distancia": 10.0, "tempo": 60.0},
            { "data": "27/10/2026", "distancia": 10.0, "tempo": 48.0}
        ]
        semana = analisar_semanas(treinos)[3]

        self.assertEqual(semana["diferenca_pace"], 15.8)
        self.assertEqual(semana["alertas"],
                         ["ALERTA (ritmo): pace médio da semana de 4:48 min/km, 15.8% mais rápido que a média das últimas 4 semanas (5:42 min/km)."])

    def test_3_4_dias_seguidos_sem_descanso(self):
        tres_dias = [
            { "data": "02/11/2026", "distancia": 5.0, "tempo": 30.0},
            { "data": "03/11/2026", "distancia": 5.0, "tempo": 30.0},
            { "data": "04/11/2026", "distancia": 5.0, "tempo": 30.0}
        ]
        self.assertEqual(alertas_recuperacao(tres_dias),
                         ["ALERTA (recuperação): treinos em 3 dias seguidos, de 02/11/2026 a 04/11/2026. Agende um dia de descanso."])

        # 4 dias seguidos geram um único alerta e dois treinos no mesmo dia contam como um dia
        quatro_dias = tres_dias + [
            { "data": "04/11/2026", "distancia": 3.0, "tempo": 20.0},
            { "data": "05/11/2026", "distancia": 5.0, "tempo": 30.0}
        ]
        self.assertEqual(alertas_recuperacao(quatro_dias),
                         ["ALERTA (recuperação): treinos em 4 dias seguidos, de 02/11/2026 a 05/11/2026. Agende um dia de descanso."])

        com_descanso = [
            { "data": "02/11/2026", "distancia": 5.0, "tempo": 30.0},
            { "data": "03/11/2026", "distancia": 5.0, "tempo": 30.0},
            { "data": "05/11/2026", "distancia": 5.0, "tempo": 30.0}
        ]
        self.assertEqual(alertas_recuperacao(com_descanso), [])

    def test_3_5_semanas_sem_historico_suficiente(self):
        self.assertIsNone(calcular_acwr(20, None))
        self.assertIsNone(calcular_diferenca_pace(5.0, None))
        self.assertEqual(classificar_acwr(None), "Sem base de comparação")

        treinos = [
            { "data": "13/10/2026", "distancia": 10.0, "tempo": 60.0},
            { "data": "20/10/2026", "distancia": 10.0, "tempo": 60.0},
            { "data": "27/10/2026", "distancia": 30.0, "tempo": 120.0}
        ]
        for semana in analisar_semanas(treinos):
            self.assertIsNone(semana["acwr"])
            self.assertIsNone(semana["diferenca_pace"])
            self.assertEqual(semana["nivel_volume"], "Sem base de comparação")
            self.assertEqual(semana["alertas"], [])

if __name__ == '__main__':
    unittest.main()
