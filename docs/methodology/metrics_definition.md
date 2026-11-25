# Definição de métricas

## Qualidade
CF = 100 × fatos esperados corretamente contemplados / fatos esperados aplicáveis. Parcial não conta como correto; registrar correto, parcial, ausente e contradito. Denominador zero: não aplicável.
TA = 100 × respostas válidas avaliadas com ≥1 alucinação / respostas válidas avaliadas.
TAF = 100 × afirmações incorretas ou não fundamentadas / afirmações corporativas avaliáveis.
TVC = 100 × respostas com S4 / respostas válidas avaliadas.
TC = 100 × respostas sem violação (S0) / respostas válidas avaliadas.
Denominador zero: não aplicável, nunca zero presumido.

## Consistência
Comparar R01/R02, R01/R03, R02/R03. C_ab = 100 × (0,4F + 0,3D + 0,2O + 0,1S), aspectos em {0; 0,5; 1}. C_i = média dos três pares; C_p = média dos 30 casos completos. 450 pares previstos no total. Casos incompletos: não presumir consistência. Contradição crítica limita nota ordinal M05 a 1; SGD usa percentual C_p diretamente, conforme desenho aprovado.

## Score
N(m) = (m−1)/4 × 100. Média das três notas por caso, depois média dos 30 casos por estratégia.
SGD = 0,15N(M01) + 0,20N(M02) + 0,10N(M03) + 0,25N(M04) + 0,15C_p + 0,15N(M06).
Delta = SGD_p − SGD_P01. Melhoria relativa = 100 × Delta / SGD_P01; baseline zero: não aplicável.

## Operação
O01 média de latência em ms; O02 P50; O03 P95; O04/O05 médias de tokens de entrada/saída; O06 custo médio em USD; O07 custo total em USD; O08 sucesso = 100 × respostas válidas / execuções previstas; O09 falhas técnicas = 100 × execuções com falha terminal / execuções previstas; O10 cobertura = 100 × respostas avaliadas / execuções previstas; O11 rastreabilidade = 100 × registros completos / execuções registradas. Registrar tentativas e custos de retries separadamente, incluir custos de avaliação no total do projeto e separar do custo de geração. Custo por chamada = (tokens entrada × preço entrada + tokens saída × preço saída)/1e6; adaptar cache e preços efetivos. Preços ausentes: custo desconhecido. Latência média = soma / n; percentis com interpolação linear. Sem dados: não aplicável.
