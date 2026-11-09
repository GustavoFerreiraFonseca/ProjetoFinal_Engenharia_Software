# Funções da História de usuário 1.

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