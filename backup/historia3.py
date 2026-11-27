# Implementação inicial da história de usuário (3) e seus critérios de aceitação

from datetime import datetime, timedelta

"""
Funções para HU 3:
- alertas_recuperacao: A cada nova entrada de treinos ele verifica se os treinos no cache de treinos foram em dias seguidos, se sim, ele retorna um alerta de recuperação com as datas.
- calcular_volume_pace_cronico: A cada nova entrada no banco de semanas ele verifica se já existem 4 semanas, se sim, ele calcula o volume e pace crônicos, atualizando o valor anterior no perfil ou adicionando um valor após as primeiras 4 semanas de uso.
- calcular_volume_pace_agudo: A cada nova entrada no banco de semanas ele calcula o novo valor de volume e pace agudos, após isso atualiza o perfil do usuário com os novos valores.
- calcular_acwr: A cada nova entrada de volume agudo e crônico no perfil do usuário, ele calcula o ACWR, atualizando o valor anterior no perfil do usuário.
- classificar_acwr: A cada nova entrada de ACWR no perfil do usuário, ele classifica o valor em uma das 4 zonas de risco (abaixo da zona segura, zona segura, atenção e zona de perigo).
- classificar_pace: A cada nova entrada de pace agudo e crônico no perfil do usuário, ele classifica se o pace agudo está 15% ou mais abaixo (mais rápido) do pace crônico pela fórmula ((pace_cronico - pace_agudo) / pace_cronico)*100 >= 15, se sim, ele retorna um alerta de mudança brusca de pace.
"""

"""
Regras de negócio para HU 3:
- O volume agudo é calculado somando-se os volumes de treino da semnana.
- O volume crônico é calculado somando-se os volumes de treino das últimas 4 semanas e dividindo o resultado por 4.
- o pace agudo é calculado pela média dos paces da semana.
- o pace crônico é calculado pela média dos paces das últimas 4 semanas.
- o ACWR é calculado dividindo-se o volume agudo pelo volume crônico, se o volume crônico for diferente de zero e arrendondando para 2 casas decimais.
- a classificação do ACWR é feita da seguinte forma:
    - Abaixo da zona segura: ACWR < 0.8 (sem alertas)
    - Zona segura: 0.8 <= ACWR <= 1.3 (sem alertas)
    - Atenção: 1.3 < ACWR <= 1.5 (alerta de atenção)
    - Zona de perigo: ACWR > 1.5 (alerta de perigo de lesões)

- a classificação do pace é feita da seguinte forma:
    - Se o pace agudo estiver 15% acima do pace crônico, ele retorna um alerta de mudança brusca de pace. (deve arredondar para 1 casa decimal o resultado da diferença percentual entre os paces)

- a classificação de dias seguidos de treino é feita da seguinte forma:
    - Se houver 3 ou mais dias seguidos de treino, ele retorna um alerta de recuperação com as datas dos treinos.
    - Ele manda o alerta todos os dias se continuar aumentando os dias seguidos de treino, ou seja, se houver 4 dias seguidos de treino, ele retorna um alerta de recuperação com as datas dos treinos.

"""

"""
Padrões definidos para os bancos (Sprint 3):
- Cache de treinos: lista de treinos no formato da HU 2 -> { "data": "DD/MM/AAAA", "distancia": float, "tempo": float }
- Banco de semanas: lista de semanas no formato do identificarSemana da HU 2 -> [ { "Semana DD/MM/AAAA:": [treinos] }, ... ]
    - Uma semana sem treino chega no banco com a lista vazia e conta como 0 km.
    - As últimas 4 semanas são as 4 últimas entradas do banco, incluindo a atual.
- Perfil do usuário: { "volume_agudo", "pace_agudo", "volume_cronico", "pace_cronico", "acwr" } em float, None enquanto não puder ser calculado.
- Pace em minutos por km (float), pace de cada treino = tempo / distancia.
- Pace crônico = média dos paces de todos os treinos das últimas 4 semanas.
- Semana atual sem treino: volume agudo 0.0 e pace agudo 0.0.
- As funções alteram o perfil direto e não retornam nada, os alertas são impressos no terminal.
- Quando o ACWR não puder ser calculado ele fica None no perfil e é impresso "Sem base de comparação".
- Dois treinos no mesmo dia contam como um dia só na sequência de dias seguidos.
"""


def alertas_recuperacao(cache_treinos):
    datas = sorted({datetime.strptime(treino["data"], "%d/%m/%Y") for treino in cache_treinos})
    if not datas:
        return

    fim = inicio = datas[-1]
    for data in reversed(datas[:-1]):
        if inicio - data != timedelta(days=1):
            break
        inicio = data

    dias = (fim - inicio).days + 1
    if dias >= 3:
        print(f"ALERTA (recuperação): treinos em {dias} dias seguidos, de {inicio.strftime('%d/%m/%Y')} a {fim.strftime('%d/%m/%Y')}. Agende um dia de descanso.")


def calcular_volume_pace_agudo(banco_semanas, perfil):
    treinos = list(banco_semanas[-1].values())[0]

    perfil["volume_agudo"] = sum(treino["distancia"] for treino in treinos)
    if treinos:
        perfil["pace_agudo"] = sum(treino["tempo"] / treino["distancia"] for treino in treinos) / len(treinos)
    else:
        perfil["pace_agudo"] = 0.0


def calcular_volume_pace_cronico(banco_semanas, perfil):
    if len(banco_semanas) < 4:
        return

    treinos = [treino for semana in banco_semanas[-4:] for treino in list(semana.values())[0]]

    perfil["volume_cronico"] = sum(treino["distancia"] for treino in treinos) / 4
    if treinos:
        perfil["pace_cronico"] = sum(treino["tempo"] / treino["distancia"] for treino in treinos) / len(treinos)
    else:
        perfil["pace_cronico"] = None


def calcular_acwr(perfil):
    if not perfil["volume_cronico"]:
        perfil["acwr"] = None
        print("Sem base de comparação")
        return

    perfil["acwr"] = round(perfil["volume_agudo"] / perfil["volume_cronico"], 2)


def classificar_acwr(perfil):
    acwr = perfil["acwr"]
    if acwr is None:
        return

    if 1.3 < acwr <= 1.5:
        print(f"ATENÇÃO (volume): {perfil['volume_agudo']:.1f} km nesta semana contra média de {perfil['volume_cronico']:.1f} km nas últimas 4 semanas (ACWR {acwr:.2f}).")
    elif acwr > 1.5:
        print(f"ALERTA (volume): {perfil['volume_agudo']:.1f} km nesta semana contra média de {perfil['volume_cronico']:.1f} km nas últimas 4 semanas (ACWR {acwr:.2f}). Zona de perigo para lesões.")


def classificar_pace(perfil):
    pace_agudo = perfil["pace_agudo"]
    pace_cronico = perfil["pace_cronico"]
    if pace_agudo is None or pace_cronico is None:
        return

    diferenca = round(((pace_cronico - pace_agudo) / pace_cronico) * 100, 1)
    if diferenca >= 15:
        segundos_agudo = round(pace_agudo * 60)
        segundos_cronico = round(pace_cronico * 60)
        print(f"ALERTA (ritmo): pace médio da semana de {segundos_agudo // 60}:{segundos_agudo % 60:02d} min/km, {diferenca}% mais rápido que a média das últimas 4 semanas ({segundos_cronico // 60}:{segundos_cronico % 60:02d} min/km).")
