# ProjetoFinal_Engenharia_Software
Repositório Público destinado para o projeto final da disciplina de engenharia de software.

## Estrutura do repositório

```
ProjetoFinal_Engenharia_Software/
├── README.md
├── testes/
│   ├── testes_historia1.py    # testes da história de usuário 1
│   ├── testes_historia2.py    # testes da história de usuário 2
│   └── testes_historia3.py    # testes da história de usuário 3
└── docs/
    ├── TrabalhoFinal.pdf      # documentação do trabalho (gerada a partir do LaTeX)
    ├── latex/
    │   └── TrabalhoFinal.tex  # fonte do documento
    └── enunciado/
        └── Enunciado_Trabalho_Final_ES_26-2.pdf
```

### Como rodar os testes

Todos os testes de uma vez (a partir da raiz do repositório):

```
python -m unittest discover -s testes -v
```

Os testes de uma história só:

```
cd testes
python testes_historia1.py
```

### Como gerar o PDF da documentação

Dentro de `docs/latex/`, rodar duas vezes (a segunda é para o sumário):

```
pdflatex TrabalhoFinal.tex
pdflatex TrabalhoFinal.tex
```

Depois copiar o `TrabalhoFinal.pdf` gerado para a pasta `docs/`.

---

## Sprint 1

**Trio:**
- Gustavo Ferreira da Fonseca, RA: 2669510
- Gustavo Henrique Gonçalves, RA: 2669528
- João Francisco Barcala Paulo, RA: 2669544

**Tema:** Analisador de Desempenho e Rotinas de Treino para Corrida. Esse será um sistema em que corredores poderão registrar seus treinos, além de acompanhar sua evolução ao longo das semanas de uso. Primeiramente, receberemos um arquivo CSV com todo o histórico de treino (data, tempo, distância, frequência cardíaca). Pegamos esses dados, processaremos para obter pace médio, volume semanal acumulado e recordes pessoais. Além disso, iremos realizar análises para verificar se não houve um aumento abrupto de volume que pode gerar lesões. Por fim, gerará um relatório em txt consolidando sua evolução semanal, destaques de desempenho e alertas de risco de lesões.

**Fontes de referência:**
- CAI, Jie; LI, Gang. Exercise or lie down? The impact of fitness app use on users' wellbeing. Frontiers in Public Health, v. 11, p. 1281323, 2024. DOI: 10.3389/fpubh.2023.1281323.
- VARELLA, Drauzio. Correr: O exercício, a cidade e a busca da superação. 1. ed. São Paulo: Companhia das Letras, 2015.
- LABORO. Os benefícios da prática de atividade física orientada via aplicativo. Blog Grupo Laboro, 2021. Disponível em: https://laboro.edu.br/blog/os-beneficios-da-pratica-de-atividade-fisica-orientada-via-aplicativo /. Acesso em: 30 out. 2026.
- VARELLA, Drauzio. Atividade física e metabolismo. Portal Drauzio Varella, UOL. Disponível em: https://drauziovarella.uol.com.br/drauzio/atividade-fisica-e-metabolismo-artigo/. Acesso em: 30 out. 2026.

As referências acima sustentam a importância da atividade física e, mais especificamente, os artigos “Exercise or lie down? The impact of fitness app use on users' wellbeing. Frontiers in Public Health” e “Os benefícios da prática de atividade física orientada via aplicativo. Blog Grupo Laboro, 2021” sustentam que o monitoramento da evolução por meio de aplicativos podem auxiliar os praticantes a começarem e a manterem a disciplina nos exercícios físicos.

---

## Sprint 2

### Histórias de Usuário

**1** - Como usuário eu quero carregar um arquivo csv com meu histórico de corrida e obter o cálculo do meu pace médio por treino para acompanhar minha evolução nos meus treinos.

**2** - Como usuário eu quero agrupar os meus treinos semanalmente, e a partir disso calcular o volume de treino e meus recordes.

**3** - Como corredor, eu quero receber alertas quando meu volume semanal, meu ritmo ou a sequência dos meus treinos mudarem de forma brusca, para reduzir o risco de ter uma lesão.

### Critérios de Aceitação

**História 1**

- **1.1:** O sistema deve ler o arquivo csv e ler a data do treino, a distância, o tempo total de cada corrida e a frequência cardíaca. Sendo a distância em Km, o tempo em minutos e a frequência cardíaca em bpm.
           A data deve ser formatada da seguinte forma: DD/MM/AAAA.
- **1.2:** Para cada corrida registrada, o sistema deve calcular corretamente o pace em minutos por quilômetro, dividindo o tempo decorrido pela distância, se atentando a conversão da parte decimal para segundos.
- **1.3:** Se o arquivo csv contiver distância igual ou inferior a 0 ou tempo igual ou inferior a 0, o sistema deve ignorar essa linha.
- **1.4:** O pace resultante deve ser formatado seguindo o seguinte exemplo: 5:30 min/km.

**História 2**

- **2.1:** O sistema, ao receber os dados dos treinos, deve organizá-los por semana e ordená-los por data caso não esteja ordenado.
- **2.2:** Ao analisar os treinos, o sistema irá calcular a somatória das distâncias percorridas na semana para determinar o volume semanal.
- **2.3:** O sistema deverá identificar e atualizar os recordes pessoais do usuário, que possui 4 campos de recorde pessoal:
  - Maior distância (km).
  - Maior volume semanal acumulado (km).
  - Maior número de treinos realizados em uma semana.
  - Menor pace médio registrado em um treino (min/km).
- **2.4:** Cada agrupamento semanal deve ser identificado pelo primeiro dia da semana (Domingo), seguindo com o padrão DD/MM/AAAA. Como exemplo: “semana 01/11/2026:”.

**História 3**

- **3.1:** Para cada semana (agrupamento da história 2), o sistema deve calcular o volume agudo (soma das distâncias da semana), o volume crônico (média do volume das últimas 4 semanas, incluindo a atual; semanas sem treino contam como 0 km) e o ACWR = volume agudo / volume crônico, arredondado para 2 casas decimais. O ACWR (*Acute:Chronic Workload Ratio*) foi tirado de Gabbett (2016).
- **3.2:** O sistema deve classificar o ACWR seguindo as faixas de Gabbett (2016): abaixo de 0,8 é “Abaixo da zona segura” e de 0,8 a 1,3 é “Zona segura” (nenhuma das duas gera alerta); acima de 1,3 até 1,5 é “Atenção”; acima de 1,5 é “Zona de perigo”. As mensagens devem seguir os exemplos:
  - “ATENÇÃO (volume): 16.0 km nesta semana contra média de 11.5 km nas últimas 4 semanas (ACWR 1.39).”
  - “ALERTA (volume): 30.0 km nesta semana contra média de 15.0 km nas últimas 4 semanas (ACWR 2.00). Zona de perigo para lesões.”
- **3.3:** O sistema deve calcular o pace de cada treino (tempo / distância), o pace médio da semana (média dos paces dos treinos da semana) e o pace crônico (média dos paces dos treinos das últimas 4 semanas, incluindo a atual). Se o pace da semana for 15% ou mais rápido que o crônico, pela fórmula ((pace crônico − pace da semana) / pace crônico) × 100 arredondada para 1 casa decimal, o sistema deve gerar o alerta, pois mudanças bruscas de ritmo estão ligadas a lesões no tendão de Aquiles, na panturrilha e na fáscia plantar (Nielsen et al., 2013). Exemplo:
  - “ALERTA (ritmo): pace médio da semana de 4:48 min/km, 15.8% mais rápido que a média das últimas 4 semanas (5:42 min/km).”
- **3.4:** Para cada sequência de 3 ou mais dias seguidos com treino, o sistema deve gerar um único alerta de recuperação com o primeiro e o último dia da sequência. Dois treinos no mesmo dia contam como um dia só. Exemplo:
  - “ALERTA (recuperação): treinos em 3 dias seguidos, de 02/11/2026 a 04/11/2026. Agende um dia de descanso.”
- **3.5:** Se a semana não tiver 4 semanas de histórico (contando a partir da primeira semana com treino), o sistema não calcula o ACWR nem a diferença de pace, classifica a semana como “Sem base de comparação” e não gera alertas de volume nem de ritmo.

### Relação entre testes e critérios

| Arquivo                         | Teste                                        | Critério(s) |
|---------------------------------|----------------------------------------------|-------------|
| `testes/testes_historia1.py`    | `test_1_1_leitura_dados_validos`             | 1.1         |
| `testes/testes_historia1.py`    | `test_1_2_e_1_4_calculo_e_formatacao_pace`   | 1.2 e 1.4   |
| `testes/testes_historia1.py`    | `test_1_3_ignorar_linhas_invalidas`          | 1.3         |
| `testes/testes_historia2.py`    | `test_2_1_e_2_4_agrupamento_e_identificacao` | 2.1 e 2.4   |
| `testes/testes_historia2.py`    | `test_2_2_calculo_volumeSemanal`             | 2.2         |
| `testes/testes_historia2.py`    | `test_2_3_recordePessoal`                    | 2.3         |
| `testes/testes_historia3.py`    | `test_3_1_volume_semanal_e_acwr`             | 3.1         |
| `testes/testes_historia3.py`    | `test_3_2_classificacao_e_alertas_de_volume` | 3.2         |
| `testes/testes_historia3.py`    | `test_3_3_mudanca_brusca_de_pace`            | 3.3         |
| `testes/testes_historia3.py`    | `test_3_4_dias_seguidos_sem_descanso`        | 3.4         |
| `testes/testes_historia3.py`    | `test_3_5_semanas_sem_historico_suficiente`  | 3.5         |

---

## Referências

### Pesquisa (Sprint 1)
- CAI, Jie; LI, Gang. Exercise or lie down? The impact of fitness app use on users' wellbeing. Frontiers in Public Health, v. 11, p. 1281323, 2024. DOI: 10.3389/fpubh.2023.1281323.
- VARELLA, Drauzio. Correr: O exercício, a cidade e a busca da superação. 1. ed. São Paulo: Companhia das Letras, 2015.
- LABORO. Os benefícios da prática de atividade física orientada via aplicativo. Blog Grupo Laboro, 2021. Disponível em: https://laboro.edu.br/blog/os-beneficios-da-pratica-de-atividade-fisica-orientada-via-aplicativo/. Acesso em: 30 out. 2026.
- VARELLA, Drauzio. Atividade física e metabolismo. Portal Drauzio Varella, UOL. Disponível em: https://drauziovarella.uol.com.br/drauzio/atividade-fisica-e-metabolismo-artigo/. Acesso em: 30 out. 2026.

### História de usuário 3
- GABBETT, Tim J. The training-injury prevention paradox: should athletes be training smarter and harder? British Journal of Sports Medicine, v. 50, n. 5, p. 273-280, 2016. DOI: 10.1136/bjsports-2015-095788.
- NIELSEN, Rasmus O. et al. Classifying running-related injuries based upon etiology, with emphasis on volume and pace. International Journal of Sports Physical Therapy, v. 8, n. 2, p. 172-179, 2013.
