import sys
sys.path.append("/connection")
from flask import jsonify
from util import constants
from Connection import Connection

connection = Connection()

# Função que organiza a resposta das queries da rota ativos e elabora um json com todos
## as chaves e valores correspondentes.
def response_json_to_active_route(dados):
  json_return = []

  for registro in dados:
    periodos_integralizados = int(registro[1])

    if (registro[2] == None):
      cred_obrig_int = 0
    else:
      cred_obrig_int = int(registro[2])

    if (registro[3] == None):
      cred_opt_int = 0
    else:
      cred_opt_int = int(registro[3])
    
    if (registro[4] == None):
      cred_comp_int = 0
    else:
      cred_comp_int = int(registro[4]) 

    cred_comp_int = get_percent(cred_obrig_int, cred_opt_int, cred_comp_int)
    
    json_return.append({ 
      "matricula": registro[0], 
      "periodo_ingresso": registro[5],
      "periodos_integralizados": periodos_integralizados, 
      "porcentagem_concluida": round(cred_comp_int, 2)
    })

  return jsonify(json_return)


# Calcula o percentual do curso concluído de cada aluno a partir dos créditos.
def get_percent(cred_obrig_int, cred_opt_int, cred_comp_int):
  result = 0
  if (cred_comp_int == 0):
    pass
  elif (cred_comp_int == 4):
    result = 4
  elif (cred_comp_int == 8):
    result = 8
  else:
    result = max(0, min(8, cred_comp_int - 22))

  porcentagem = min(cred_obrig_int, 132) + min(cred_opt_int, 56) + result

  return (porcentagem / int(constants.TOTAL_CREDITOS)) * 100


# Função que formata o json de resposta das rotas que geram os dados de alunos
## ativos e egressos  para exportar para o arquivo .csv.
def response_json_to_csv_actives_export(dados):
  json_return = []
  
  for registro in dados:
    json_return.append({
      "matricula": registro[0],
      "periodo_ingresso": registro[1],
      "periodos_integralizados": registro[2],
      "cred_obrig_int": registro[3],
      "cred_opt_int": registro[4],
      "cred_comp_int": registro[5],
      "cota": registro[6],
      "genero": registro[7],
      "estado_civil": registro[8],
      "curriculo": registro[9],
      "cra": registro[10],
      "mc": registro[11],
      "iea": registro[12],
      "trancamentos_totais": registro[13],
      "matriculas_institucionais": registro[14],
      "mobilidade_estudantil": registro[15],
      "media_geral_ingresso": registro[16]
    })
  
  return jsonify(json_return)


# Função que formata o json de resposta das rotas que geram os dados de alunos
## egressos  para exportar para o arquivo .csv.
def response_json_to_csv_graduates_export(dados):
  json_return = []
  
  for registro in dados:
    json_return.append({
      "matricula": registro[0],
      "periodo_conclusao": registro[1],
      "periodos_integralizados": registro[2],
      "cred_obrig_int": registro[3],
      "cred_opt_int": registro[4],
      "cred_comp_int": registro[5],
      "cota": registro[6],
      "genero": registro[7],
      "estado_civil": registro[8],
      "curriculo": registro[9],
      "cra": registro[10],
      "mc": registro[11],
      "iea": registro[12],
      "trancamentos_totais": registro[13],
      "matriculas_institucionais": registro[14],
      "mobilidade_estudantil": registro[15],
      "media_geral_ingresso": registro[16]
    })
  
  return jsonify(json_return)


# Função que formata o json de resposta das rotas que geram os dados de alunos
## evadidos para exportar para o arquivo .csv.
def response_json_to_csv_escaped_export(dados):
  json_return = []
  
  for registro in dados:
    json_return.append({
      "matricula": registro[0],
      "periodo_evasao": registro[1],
      "motivo_evasao": registro[2],
      "periodos_integralizados": registro[3],
      "cred_obrig_int": registro[4],
      "cred_opt_int": registro[5],
      "cred_comp_int": registro[6],
      "cota": registro[7],
      "genero": registro[8],
      "estado_civil": registro[9],
      "curriculo": registro[10],
      "cra": registro[11],
      "mc": registro[12],
      "iea": registro[13],
      "trancamentos_totais": registro[14],
      "matriculas_institucionais": registro[15],
      "mobilidade_estudantil": registro[16],
      "media_geral_ingresso": registro[17]
    })
  
  return jsonify(json_return)


# Função auxiliar que retorna estatísticas sobre os egressos, informações como o total 
## de graduados em um determinado intervalo de tempo, média de graduados, períodos que
### tiveram mais e menos graduados e seus números, respectivamente.
def get_statistics(results):
  total_graduados = 0
  media_graduados = 0
  periodo_max_graduados = results[0][0]
  periodo_min_graduados = results[0][0]
  max_graduados = results[0][1]
  min_graduados = results[0][1]
  soma_cras = 0

  for i in range(len(results)):
    if (results[i][1] < min_graduados):
      periodo_min_graduados = results[i][0]
      min_graduados = results[i][1]

    elif (results[i][1] > max_graduados):
      periodo_max_graduados = results[i][0]
      max_graduados = results[i][1]

    total_graduados += results[i][1]
    soma_cras += results[i][2]

  media_graduados = total_graduados / len(results)
  media_cras = soma_cras / len(results)

  return [total_graduados, round(media_graduados, 2), periodo_min_graduados, 
    periodo_max_graduados, min_graduados, max_graduados, round(media_cras, 2)]


# Função auxiliar que monta a estrutura json para os alunos egressos (graduados), 
## retorna um array de objetos, onde cada objeto contém o período de vínculo e a
### quantidade de egressos daquele período.
def response_json_to_graduates_route(periods):
  response = []
  for i in range(len(periods)):
    response.append({
      "periodo_conclusao": periods[i][0], 
      "qtd_egressos": periods[i][1],
      "cra_medio": round(periods[i][2], 2),
    })

  return response


# Função que retorna o número de alunos evadidos por período (a partir do id do motivo
## de cancelamento da matrícula) de um único período passado.
def process_query_of_one_period(id_curso, id, periodo):

  query = 'SELECT periodo_situacao, count(*) AS qtd_evadidos \
    FROM "DiscenteVinculo" \
    INNER JOIN "Discente" \
      ON "DiscenteVinculo".cpf = "Discente".cpf \
    WHERE id_curso=' + id_curso + ' \
    AND id_situacao_vinculo=' + str(id) + ' \
    AND periodo_situacao=\'' + str(periodo) + '\' \
    GROUP BY periodo_situacao \
    ORDER BY periodo_situacao'

  result = connection.select(query)
  
  retorno = []
  for i in range(len(result)):
    retorno.append({"periodo": result[i][0], "tag"+str(id): result[i][1]})

  return retorno


# Função que retorna o número de alunos evadidos por período (a partir do id do motivo
## de cancelamento da matrícula) de um intervalo de períodos passados.
def process_query_of_interval_of_the_periods(id_curso, id, minimo, maximo):

  query = 'SELECT periodo_situacao, count(*) AS qtd_egressos \
    FROM "DiscenteVinculo" \
    INNER JOIN "Discente" \
    ON "DiscenteVinculo".cpf = "Discente".cpf \
    WHERE id_curso=' + id_curso + \
    'AND id_situacao_vinculo=' + str(id) + \
    'AND periodo_situacao BETWEEN \'' + str(minimo) + '\' AND \'' + str(maximo) + '\' \
    GROUP BY periodo_situacao \
    ORDER BY periodo_situacao'

  result = connection.select(query)
  
  retorno = []
  for i in range(len(result)):
    retorno.append({"periodo": result[i][0], "tag"+str(id): result[i][1]})

  return retorno


# Função que retorna o número de alunos evadidos por período, a partir do id do motivo
## de cancelamento da matrícula, de todos os períodos registrados.
def process_query_of_escaped(id_curso, id):

  query = 'SELECT periodo_situacao, count(*) AS qtd_evadidos \
    FROM "DiscenteVinculo" \
    INNER JOIN "Discente" \
      ON "DiscenteVinculo".cpf = "Discente".cpf \
    WHERE id_curso=' + id_curso + '\
    AND id_situacao_vinculo=' + str(id) + '\
    GROUP BY periodo_situacao \
    ORDER BY periodo_situacao'

  result = connection.select(query)
  
  retorno = []
  for i in range(len(result)):
    retorno.append({"periodo": result[i][0], "tag"+str(id): result[i][1]})

  return retorno


# Fazendo a junção entre os 10 arrays de evadidos pelos motivos de 1 a 9 e 13, para que o
## array tenha o formato { "periodo": { "tag1": 0, "tag2": 0, ..., "tag13": 0 }, ... },
### onde tag(i) significa o número de evadidos pelo motivo (i) naquele período, sendo
#### "i" um valor entre 1 e 9 e também 13.
def join_results_of_escaped_query(results):
  dic_periodos = {}
  for i in range(len(results)):
    for j in range(len(results[i])):
      if (results[i][j]['periodo'] in dic_periodos):
        if (i == 9):
          dic_periodos[str(results[i][j]['periodo'])]['tag'+str(i+4)] = results[i][j]['tag'+str(i+4)]
        else:
          dic_periodos[str(results[i][j]['periodo'])]['tag'+str(i+1)] = results[i][j]['tag'+str(i+1)]
      else:
        if (i == 9):
          dic_periodos[str(results[i][j]['periodo'])] = { 'tag'+str(i+4): results[i][j]['tag'+str(i+4)] }
        else:
          dic_periodos[str(results[i][j]['periodo'])] = { 'tag'+str(i+1): results[i][j]['tag'+str(i+1)] }

  return dic_periodos


# Função responsável por adicionar a resposta json os períodos do intervalo que não possui
## alunos evadidos de nenhum dos tipos. periodo_min e max têm valores padrão para o caso de
### a função ser chamadas sem os parâmetros 'de' e 'ate', ou seja, todo o intervalo.
def add_periods_without_escaped(periodo_min='1987.1', periodo_max=constants.PERIODO_ATUAL, *, dados):
  ano_ini = int(periodo_min[:4])
  ano_fim = int(periodo_max[:4])
  semestre_ini = int(periodo_min[5])
  semestre_fim = int(periodo_max[5])

  for ano in range(ano_ini, ano_fim+1):
    for semestre in range(1, 3):
      if (ano == ano_fim and semestre > semestre_fim):
        pass
      elif (ano == ano_ini and semestre < semestre_ini):
        pass
      else:
        periodo = str(ano) + '.' + str(semestre)
        if (periodo not in dados):
          dados[str(ano)+'.'+str(semestre)] = {}
    
  return dados


# Preenchendo com 0 as tags que não existem no objeto de cada período. Exemplo: caso o
## período X só tenha evadidos em "tag1", "tag2" e "tag3", o trecho abaixo irá preencher
### o objeto com o restante das tags até a 9 e também a 13, todas com o valor 0.    
def fill_tag_list_with_zeros(json):
  for i in json:
    for j in range(1,14):
      if (j <= 9 or j >=13):
        if ('tag'+str(j) in json[i]):
          pass
        else:
          json[i]['tag'+str(j)] = 0
  
  return json


# Função que prepara o json para retorno, onde cada objeto irá possui a chave 'periodo' com
## o período e outra chave tags, que correspondem as 9 tags que representam a quantidade
### de evadidos pelo motivo i, onde i é um número entre 1 e 9, inclusive.
def response_json_to_escaped_route(json):
  json_response = []
  for i in json:
    json_response.append({ "periodo": i, "tags": json[i] })
  
  return json_response


def get_escaped_statistics(joined_results, args):
  total_evadidos = 0
  qtd_ingressos_mesmo_curso = 0
  for periodo in joined_results:
    for tag in joined_results[periodo]:
      if (tag == 'tag2'):
        qtd_ingressos_mesmo_curso += joined_results[periodo][tag]
    total_evadidos += sum(joined_results[periodo].values())
  
  total_evadidos_liquido = total_evadidos - qtd_ingressos_mesmo_curso

  if (len(args) == 1):
    qtd_ingressos_query = 'SELECT COUNT(*) FROM "DiscenteVinculo" \
      WHERE periodo_ingresso = \'' + args.get('de') + '\''

    qtd_egressos_query = 'SELECT COUNT(*) FROM "DiscenteVinculo" \
      WHERE id_situacao_vinculo = 11 AND periodo_situacao = \'' + args.get('de') + '\''
  
  elif (len(args) == 2):
    qtd_ingressos_query = 'SELECT COUNT(*) FROM "DiscenteVinculo" \
      WHERE periodo_ingresso BETWEEN \'' + args.get('de') + '\' AND \'' + args.get('ate') + '\''

    qtd_egressos_query = 'SELECT COUNT(*) FROM "DiscenteVinculo" \
      WHERE id_situacao_vinculo = 11 \
      AND periodo_situacao BETWEEN \'' + args.get('de') + '\' AND \'' + args.get('ate') + '\''

  else:
    qtd_ingressos_query = 'SELECT COUNT(*) FROM "DiscenteVinculo"'

    qtd_egressos_query = 'SELECT COUNT(*) FROM "DiscenteVinculo" WHERE id_situacao_vinculo = 11'
  
  qtd_ingressos = connection.select(qtd_ingressos_query)[0][0]
  qtd_egressos = connection.select(qtd_egressos_query)[0][0]

  evadidos_ingressos = round(total_evadidos / qtd_ingressos, 2)
  evadidos_egressos = round(total_evadidos / qtd_egressos, 2)

  return [total_evadidos, total_evadidos_liquido, evadidos_ingressos, evadidos_egressos]
