# ProjetoFinal_Engenharia_Software
Repositório Público destinado para o projeto final da disciplina de engenharia de software.

## Estrutura do repositório

A entrega do trabalho é um `.zip` com **um arquivo de código** (`sistema_corrida.py`) e **um arquivo de testes** (`testes_sistema.py`). Por isso o código das três histórias está reunido nesses dois arquivos, na raiz do repositório. As pastas `src/` e `testes/` mantêm o mesmo código separado por história, e a pasta `backup/` guarda as versões de antes da refatoração, para comparar o que foi alterado.

```
ProjetoFinal_Engenharia_Software/
├── README.md
├── sistema_corrida.py             # código completo do sistema (HUs 1, 2 e 3 + relatório) - entregue no .zip
├── testes_sistema.py              # todos os testes automatizados - entregue no .zip
├── treinos.csv                    # exemplo de histórico com 16 treinos
├── src/                           # mesmo código refatorado, separado por história
│   ├── historia1.py               # leitura do CSV e cálculo do pace com Template Method (HU 1)
│   ├── historia2.py               # semanas, volume semanal e recordes com Strategy (HU 2)
│   └── analisador_lesoes.py       # alertas de lesão na classe AnalisadorLesoes com Observer (HU 3)
├── testes/                        # testes separados por história
│   ├── testes_historia1.py
│   ├── testes_historia2.py
│   ├── testes_historia3.py        # testes da versão da Sprint 3 da HU 3
│   └── testes_analisador_lesoes.py
├── backup/                        # código antes da refatoração da Sprint 4
│   ├── historia1.py
│   ├── historia2.py
│   └── historia3.py
└── docs/
    ├── TrabalhoFinal.pdf          # documentação do trabalho (gerada a partir do LaTeX)
    ├── Diagramas/
    │   ├── DiagramaArquiteturaDeSoftware.pdf    # arquitetura do sistema
    │   ├── Fluxograma_Eng_Software.drawio       # fluxograma da aplicação (CSV único) + .png
    │   ├── diagramaUMLPP1.png                   # padrão Template Method (HU 1)
    │   ├── Diagrama_UML_HU2.png                 # padrão Strategy (HU 2)
    │   └── Diagrama_UML_HU3.drawio              # padrão Observer (HU 3) + .png
    ├── latex/
    │   └── TrabalhoFinal.tex      # fonte do documento
    └── enunciado/
        └── Enunciado_Trabalho_Final_ES_26-2.pdf
```

## Como executar

A partir da raiz do repositório, passando o caminho do CSV:

```
python sistema_corrida.py treinos.csv
```

Sem o argumento, o programa pergunta o caminho do arquivo. O relatório é mostrado no terminal e gravado em `relatorio_final.txt`, com o resumo semanal, os recordes pessoais, a análise de carga (ACWR) de cada semana e os alertas preventivos.

O CSV deve ter um cabeçalho e uma linha por treino, com as colunas `data` (DD/MM/AAAA), `distancia_km`, `tempo_minutos` e `frequencia_cardiaca`.

## Como rodar os testes

Todos os testes, a partir da raiz do repositório:

```
python -m unittest testes_sistema -v
```

O arquivo tem uma classe de testes por história: `TestHistorialPace` (HU 1), `TestHistorialVolume` (HU 2) e `TestAnalisadorLesoes` (HU 3). Para rodar só uma história:

```
python -m unittest testes_sistema.TestHistorialPace -v
```

Os testes separados por história, na pasta `testes/`, também podem ser rodados um a um, por exemplo:

```
python -m unittest testes.testes_historia1 -v
```

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
- **3.3:** O sistema deve calcular o pace de cada treino (tempo / distância), o pace médio da semana (média dos paces dos treinos da semana) e o pace crônico (média dos paces dos treinos das últimas 4 semanas, incluindo a atual). Semana sem treino não tem pace médio e não gera alerta de ritmo. Se o pace da semana for 15% ou mais rápido que o crônico, pela fórmula ((pace crônico − pace da semana) / pace crônico) × 100 arredondada para 1 casa decimal, o sistema deve gerar o alerta, pois mudanças bruscas de ritmo estão ligadas a lesões no tendão de Aquiles, na panturrilha e na fáscia plantar (Nielsen et al., 2013). Exemplo:
  - “ALERTA (ritmo): pace médio da semana de 4:48 min/km, 15.8% mais rápido que a média das últimas 4 semanas (5:42 min/km).”
- **3.4:** Para cada sequência de 3 ou mais dias seguidos com treino, o sistema deve gerar um único alerta de recuperação com o primeiro e o último dia da sequência. Dois treinos no mesmo dia contam como um dia só. Exemplo:
  - “ALERTA (recuperação): treinos em 3 dias seguidos, de 02/11/2026 a 04/11/2026. Agende um dia de descanso.”
- **3.5:** Se a semana não tiver 4 semanas de histórico (contando a partir da primeira semana com treino), o sistema não calcula o ACWR nem a diferença de pace, classifica a semana como “Sem base de comparação” e não gera alertas de volume nem de ritmo.

### Relação entre testes e critérios

Todos os testes estão em `testes_sistema.py`. O nome de cada teste começa pelo número do critério que ele verifica.

| Classe de teste         | Teste                                          | Critério |
|-------------------------|------------------------------------------------|----------|
| `TestHistorialPace`     | `test_1_1_leitura_dados_validos`               | 1.1      |
| `TestHistorialPace`     | `test_1_2_calculo_pace`                        | 1.2      |
| `TestHistorialPace`     | `test_1_3_ignorar_linhas_invalidas`            | 1.3      |
| `TestHistorialPace`     | `test_1_4_formatacao_pace`                     | 1.4      |
| `TestHistorialVolume`   | `test_2_1_agrupamento_semanal`                 | 2.1      |
| `TestHistorialVolume`   | `test_2_2_calculo_volumeSemanal`               | 2.2      |
| `TestHistorialVolume`   | `test_2_3_recordePessoal`                      | 2.3      |
| `TestHistorialVolume`   | `test_2_4_identificacao_agrupamentos_semanais` | 2.4      |
| `TestAnalisadorLesoes`  | `test_3_1_volume_semanal_e_acwr`               | 3.1      |
| `TestAnalisadorLesoes`  | `test_3_2_classificacao_e_alertas_de_volume`   | 3.2      |
| `TestAnalisadorLesoes`  | `test_3_3_mudanca_brusca_de_pace`              | 3.3      |
| `TestAnalisadorLesoes`  | `test_3_4_dias_seguidos_sem_descanso`          | 3.4      |
| `TestAnalisadorLesoes`  | `test_3_5_semanas_sem_historico_suficiente`    | 3.5      |

---

## Sprint 3

- Diagrama da arquitetura: `docs/Diagramas/DiagramaArquiteturaDeSoftware.pdf`.
- Diagrama de fluxo da HU 3 (versão treino por treino), substituído na Sprint 4 pelo fluxograma da aplicação.
- Desenvolvimento inicial das histórias 1, 2 e 3, com os testes da Sprint 2 passando. Essas versões estão em `backup/`.

---

## Sprint 4

### Mudança na entrada do sistema

O sistema passou a receber **um único arquivo CSV com o histórico completo** de treinos, em vez de receber treino por treino. Com isso a HU 3 não precisa mais do cache de treinos nem de ir montando o banco de semanas a cada entrada: o histórico é lido de uma vez, as semanas são montadas (incluindo as semanas sem treino) e cada semana é analisada em sequência. O novo fluxo está no fluxograma da aplicação: `docs/Diagramas/Fluxograma_Eng_Software.drawio` (e `.png`).

### Refatoração e padrões de projeto

| História | Padrão          | Classe principal           | Arquivo separado           | Diagrama                              |
|----------|-----------------|----------------------------|----------------------------|---------------------------------------|
| 1        | Template Method | `ProcessadorArquivoTreino` | `src/historia1.py`         | `docs/Diagramas/diagramaUMLPP1.png`   |
| 2        | Strategy        | `EstrategiaRecorde`        | `src/historia2.py`         | `docs/Diagramas/Diagrama_UML_HU2.png` |
| 3        | Observer        | `AnalisadorLesoes`         | `src/analisador_lesoes.py` | `docs/Diagramas/Diagrama_UML_HU3.png` |

As três classes também estão em `sistema_corrida.py`. As versões de antes da refatoração estão em `backup/`.

**HU 1 - Template Method:** a classe abstrata `ProcessadorArquivoTreino` define o fluxo de leitura no método `processar` (ler as linhas → extrair e validar cada linha → montar o registro com o pace). A subclasse `ProcessadorCSV` implementa só o que depende do formato: `ler_linhas` abre o arquivo e descarta o cabeçalho, e `extrair_e_validar` usa `processar_linha_csv` para descartar linhas inválidas. Para aceitar outro formato basta criar outra subclasse. O histórico inteiro é lido com `ProcessadorCSV().processar("treinos.csv")`. A versão anterior está em `backup/historia1.py`.

**HU 2 - Strategy:** a comparação dos recordes pessoais saiu da classe `RecordPessoal` e foi para as estratégias `MaiorRecorde` e `MenorRecorde` (interface `EstrategiaRecorde`). A classe continua responsável por guardar e atualizar os recordes, e a regra de comparação fica separada. A versão anterior está em `backup/historia2.py`.

**HU 3 - Observer:** as funções soltas de `backup/historia3.py` (versão da Sprint 3) viraram os métodos da classe `AnalisadorLesoes` (`src/analisador_lesoes.py`), com a mesma lógica de cálculo. Na versão da Sprint 3 cada função imprimia o alerta direto no terminal, o que prendia o cálculo à saída. Agora a classe só calcula e chama `notificar(semana, mensagem)`, que avisa os observadores cadastrados:

- `AlertaTerminal`: imprime o alerta no terminal (mesmo comportamento da Sprint 3);
- `ColetorAlertas`: guarda os alertas em uma lista, usada nos testes e na geração do relatório final.

Para uma nova saída basta criar outro observador que implemente `ObservadorAlerta.atualizar`, sem mexer na classe de análise.

**O que mudou na HU 3 além da estrutura:**

- A entrada é o CSV inteiro (`AnalisadorLesoes.de_csv`), lido com a `ProcessadorCSV` da HU 1; o agrupamento por semana usa `agruparSemana` e `indentificarDomingo` da HU 2.
- Cada semana gera um perfil com `volume_agudo`, `pace_agudo`, `volume_cronico`, `pace_cronico`, `acwr` e `classificacao`.
- "Sem base de comparação" passou a ser a classificação da semana e não é mais impresso como alerta (critério 3.5).
- O alerta de recuperação sai uma vez para cada sequência de dias seguidos (critério 3.4), e não mais a cada novo treino.
- Correção: semana sem treino ficava com pace 0.0 e gerava um alerta de ritmo de 100%. Agora o pace dessa semana fica `None` e não gera alerta.

Os testes da versão refatorada (classe `TestAnalisadorLesoes` em `testes_sistema.py`, e `testes/testes_analisador_lesoes.py`) usam os mesmos cenários e as mesmas mensagens dos testes da Sprint 3, mas montando um CSV com o histórico completo.


### Junção para a entrega

Como a entrega é um `.zip` com um arquivo de código e um de testes, o código das três histórias foi reunido em `sistema_corrida.py`, junto com a função `gerar_relatorio`, que monta o relatório final em `.txt`, e os testes foram reunidos em `testes_sistema.py`. Na junção, a leitura do CSV passou também a descartar linhas com data fora do formato DD/MM/AAAA e a aceitar arquivos salvos com BOM (`utf-8-sig`, como os exportados pelo Excel).

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
