# ProjetoFinal_Engenharia_Software
Repositório Público destinado para o projeto final da disciplina de engenharia de software.

Sprint 1
Trio:
Gustavo Ferreira da Fonseca, RA: 2669510
Gustavo Henrique Gonçalves, RA: 2669528
João Francisco, RA: 

Em busca do terceiro.
Tema: Analisador de Desempenho e Rotinas de Treino para Corrida. Esse será um sistema em que corredores poderão registrar seus treinos, além de acompanhar sua evolução ao longo das semanas de uso. Primeiramente, receberemos um arquivo CSV com todo o histórico de treino (data, tempo, distância, carga, frequência cardíaca). Pegamos esses dados, processaremos para obter pace médio, volume semanal acumulado e recordes pessoais. Além disso, iremos realizar análises para verificar se não houve um aumento abrupto de volume que pode gerar lesões. Por fim, gerará um relatório em txt consolidando sua evolução semanal, destaques de desempenho e alertas de risco de lesões.

Fontes de referência:
CAI, Jie; LI, Gang. Exercise or lie down? The impact of fitness app use on users' wellbeing. Frontiers in Public Health, v. 11, p. 1281323, 2024. DOI: 10.3389/fpubh.2023.1281323.
VARELLA, Drauzio. Correr: O exercício, a cidade e a busca da superação. 1. ed. São Paulo: Companhia das Letras, 2015.
LABORO. Os benefícios da prática de atividade física orientada via aplicativo. Blog Grupo Laboro, 2021. Disponível em: https://laboro.edu.br/blog/os-beneficios-da-pratica-de-atividade-fisica-orientada-via-aplicativo /. Acesso em: 30 out. 2026.
VARELLA, Drauzio. Atividade física e metabolismo. Portal Drauzio Varella, UOL. Disponível em: https://drauziovarella.uol.com.br/drauzio/atividade-fisica-e-metabolismo-artigo/. Acesso em: 30 out. 2026.
As referências acima sustentam a importância da atividade física e, mais especificamente, os artigos “Exercise or lie down? The impact of fitness app use on users' wellbeing. Frontiers in Public Health” e “Os benefícios da prática de atividade física orientada via aplicativo. Blog Grupo Laboro, 2021” sustentam que o monitoramento da evolução por meio de aplicativos podem auxiliar os praticantes a começarem e a manterem a disciplina nos exercícios físicos.

Sprint 2:

Histórias de Usuário:

1 - Como usuário eu quero carregar um arquivo csv com meu histórico de corrida e obter o cálculo do meu pace médio por treino para acompanhar minha evolução nos meus treinos.


2 - Como usuário eu quero agrupar os meus treinos semanalmente, e a partir disso calcular o volume de treino e meus recordes.

Critérios de Aceitação:


1.1: O sistema deve ler o arquivo csv e ler a distância e o tempo total de cada corrida. Em quilômetros e minutos respectivamente.

1.2: Para cada corrida registrada, o sistema deve calcular corretamente o pace em minutos por quilômetro, dividindo o tempo decorrido pela distância, se atentando a conversão da parte decimal para segundos.

1.3: Se o arquivo csv contiver distância igual ou inferior a 0 ou tempo igual ou inferior a 0, o sistema deve ignorar essa linha.

1.4: O pace resultante deve ser formatado seguindo o seguinte exemplo: 5:30 min/km.


2.1: O sistema, ao receber os dados dos treinos, deve organizá-los por semana e ordená-los por data caso não esteja ordenado.

2.2: Ao analisar os treinos, o sistema irá calcular a somatória das distâncias percorridas na semana para determinar o volume semanal.

2.3: O sistema deverá identificar e atualizar os recordes pessoais do usuário, que possui 4 campos de recorde pessoal: 
Maior distância (km).
Maior volume semanal acumulado (km).
Maior número de treinos realizados em uma semana.
Menor pace médio registrado em um treino (min/km).  

2.4: Cada agrupamento semanal deve ser identificado pelo primeiro dia da semana (Domingo), seguindo com o padrão DD/MM/AAAA. Como exemplo: “semana 01/11/2026:”.
