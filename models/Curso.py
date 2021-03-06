# coding: utf-8
import sys
sys.path.append("./connection")
from Connection import Connection
from flask import jsonify
from util import constants

sys.path.append("./models/util")
from StatisticsExternalFunctions import (response_json_to_active_route, get_percent,
  response_json_to_csv_actives_export, get_statistics, response_json_to_graduates_route,
  process_query_of_one_period, join_results_of_escaped_query, fill_tag_list_with_zeros,
  response_json_to_escaped_route, process_query_of_escaped, process_query_of_interval_of_the_periods,
  response_json_to_csv_escaped_export, add_periods_without_escaped, response_json_to_csv_graduates_export,
  get_escaped_statistics)

class Curso():

  # Construtor da classe
  def __init__(self):
    # Instância da conexão ao banco de dados.
    self.connection = Connection()

    # Queries para setar os id's das constantes que são usadas nas consultas realizadas
    ## na Classe.
    query_id_curso = 'SELECT "Curso".id FROM "Curso" \
      WHERE "Curso".nome=\'' + str(constants.COMPUTACAO_VALUE) + '\''

    query_id_regular = 'SELECT "SituacaoVinculo".id FROM "SituacaoVinculo" \
      WHERE "SituacaoVinculo".descricao=\'' + str(constants.REGULAR_VALUE) + '\''

    query_id_aprovado = 'SELECT "SituacaoDisciplina".id FROM "SituacaoDisciplina" \
      WHERE "SituacaoDisciplina".descricao=\'' + constants.APROVADO_VALUE + '\''

    query_id_graduado = 'SELECT "SituacaoVinculo".id FROM "SituacaoVinculo" \
      WHERE "SituacaoVinculo".descricao=\'' + str(constants.GRADUADO_VALUE) + '\''

    query_id_ativo = 'SELECT "SituacaoDiscente".id FROM "SituacaoDiscente" \
      WHERE "SituacaoDiscente".descricao=\'' + str(constants.ATIVO_VALUE) + '\''

    query_id_concluido_nao_colou_grau = 'SELECT "SituacaoVinculo".id FROM "SituacaoVinculo" \
      WHERE "SituacaoVinculo".descricao=\'' + str(constants.CONCLUIDO_VALUE) + '\''

    # id's das constantes
    self.id_computacao = str(self.connection.select(query_id_curso)[0][0])
    self.id_regular = str(self.connection.select(query_id_regular)[0][0])
    self.id_aprovado = str(self.connection.select(query_id_aprovado)[0][0])
    self.id_graduado = str(self.connection.select(query_id_graduado)[0][0])
    self.id_ativo = str(self.connection.select(query_id_ativo)[0][0])
    self.id_concluido = str(self.connection.select(query_id_concluido_nao_colou_grau)[0][0])
    

  def get_period(self, args):
      periodo = args.get('from')

      result = 'AND "DiscenteVinculo".periodo_ingresso=\'' + str(periodo) + '\''
      return result


  # Função que retorna informações sobre os alunos ativos do curso de Computação,
  ## informações estas que são a matrícula do aluno e a cred_comp_int concluída do 
  ### curso com base na quantidade de créditos que o aluno já possui.
  def get_actives(self, args):
    base_query = 'SELECT "DiscenteVinculo".matricula, "DiscenteVinculo".per_int, \
      "DiscenteVinculo".cred_obrig_int, "DiscenteVinculo".cred_opt_int, "DiscenteVinculo".cred_comp_int, \
      "DiscenteVinculo".periodo_ingresso \
      FROM "DiscenteVinculo" \
      INNER JOIN "Discente" \
        ON "DiscenteVinculo".cpf = "Discente".cpf \
      WHERE "DiscenteVinculo".id_curso = ' + self.id_computacao + ' \
      AND "DiscenteVinculo".id_situacao = ' + self.id_ativo + ' \
      AND "DiscenteVinculo".id_situacao_vinculo = ' + self.id_regular + ' \
      AND "DiscenteVinculo".per_int > 0'

    if (len(args) == 1):
      base_query += self.get_period(args)

    elif (len(args) == 2):
      minimo = args.get('from')
      maximo = args.get('to')

      # Caso o periodo minimo do intervalo seja maior que o maximo, retorna
      ## uma mensagem de erro com código 404 not found.
      if (minimo > maximo):
        return { "error": "Parameters or invalid request" }, 404

      # Caso sejam iguais
      if(minimo == maximo):
        base_query += self.get_period(args)
      # Caso normal, minimo < maximo
      else:
        base_query += 'AND periodo_ingresso BETWEEN \'' + str(minimo) + '\' AND \'' + str(maximo) + '\' \
          ORDER BY periodo_ingresso'

    else:
      base_query += 'ORDER BY periodo_ingresso'

    result = self.connection.select(base_query)
    return response_json_to_active_route(result)

  
  # Função que retorna os dados para geração do arquivo csv de alunos ativos.
  def export_to_csv_actives(self, args):

    base_query = 'SELECT "DiscenteVinculo".matricula, periodo_ingresso, per_int, \
      cred_obrig_int, cred_opt_int, cred_comp_int, "Cota".descricao, "Genero".descricao, \
      "EstadoCivil".descricao, curriculo, cra, mc, iea, tranc, mat_inst, \
      mob_estudantil, media_geral_ingresso \
      FROM "DiscenteVinculo" \
      INNER JOIN "Discente" \
        ON "DiscenteVinculo".cpf = "Discente".cpf \
      INNER JOIN "Cota" \
        ON "DiscenteVinculo".id_cota = "Cota".id \
      INNER JOIN "Genero" \
        ON "Discente".id_genero = "Genero".id \
      INNER JOIN "EstadoCivil" \
        ON "Discente".id_estado_civil = "EstadoCivil".id \
      WHERE "DiscenteVinculo".id_curso = ' + self.id_computacao + '\
      AND "DiscenteVinculo".id_situacao = ' + self.id_ativo + '\
      AND "DiscenteVinculo".id_situacao_vinculo = ' + self.id_regular + ' \
      AND "DiscenteVinculo".per_int > 0'

    if (len(args) == 1):
      base_query += self.get_period(args)

    elif (len(args) == 2):
      minimo = args.get('from')
      maximo = args.get('to')

      # Caso o periodo minimo do intervalo seja maior que o maximo, retorna
      ## uma mensagem de erro com código 404 not found.
      
      # Caso sejam iguais
      if(minimo == maximo):
        base_query += self.get_period(args)
      # Caso normal, minimo < maximo
      else:
        base_query += 'AND periodo_ingresso BETWEEN \'' + str(minimo) + '\' AND \'' + str(maximo) + '\' \
          ORDER BY periodo_ingresso'

    else:
      base_query += 'ORDER BY periodo_ingresso'

    result = self.connection.select(base_query)
    return response_json_to_csv_actives_export(result)


  # Função responsável por retornar o número de alunos egressos (formados) do curso de 
  ## Computação e suas estatísticas de todos os períodos.
  def get_graduates(self, args):

    base_query = 'SELECT periodo_situacao, count(*) AS qtd_egressos, avg(cra) AS cra_medio \
      FROM "DiscenteVinculo" \
      INNER JOIN "Discente" \
        ON "DiscenteVinculo".cpf = "Discente".cpf \
      WHERE id_curso=' + self.id_computacao + '\
      AND id_situacao_vinculo=' + self.id_graduado

    # Para rotas do tipo /api/estatisticas/egressos?de=2019.2, por exemplo.
    ## Retorna o número de egressos que o período informado na rota obteve.
    if (len(args) == 1):
      periodo = args.get('from')

      base_query += 'AND periodo_situacao=\'' + str(periodo) + '\' \
        GROUP BY periodo_situacao \
        ORDER BY periodo_situacao'

      result = self.connection.select(base_query)

      # Caso não hajam registros que correspondam a query passada.
      if (len(result) == 0):
        return { 
          "completion_period": periodo, 
          "amount_graduates": 0,
          "avg_cra": 0 
        }
      else:
        return jsonify(response_json_to_graduates_route(result))
    
    # Para rotas do tipo '.../api/estatisticas/egressos?de=1999.1&ate=2010.2', por exemplo.
    ## retornam o número de egressos por período na faixa que foi especificada na rota, além
    ### de suas estatísticas.
    elif (len(args) == 2):
      minimo = args.get('from')
      maximo = args.get('to')

      # Caso o periodo minimo do intervalo seja maior que o maximo ou então igual, retorna
      ## uma mensagem de erro com código 404 not found.
      if (minimo > maximo or minimo == maximo):
        return { "error": "Parameters or invalid request" }, 404

      base_query += 'AND periodo_situacao BETWEEN \'' + str(minimo) + '\' AND \'' + str(maximo) + '\'\
        GROUP BY periodo_situacao \
        ORDER BY periodo_situacao'

    # Para rotas do tipo '.../api/estatisticas/egressos', que retornam o número de egressos de
    ## todos os períodos até então cadastrados.
    else:
      base_query += 'GROUP BY periodo_situacao \
        ORDER BY periodo_situacao'

    result = self.connection.select(base_query)
    statistics = get_statistics(result)

    return jsonify(
      total_graduates=statistics[0], 
      avg_graduates=statistics[1], 
      bottom_period=statistics[2], 
      top_period=statistics[3],
      min_graduates=statistics[4], 
      max_graduates=statistics[5],
      avg_cra=statistics[6], 
      content=response_json_to_graduates_route(result)
    )
  

  # Função responsável por buscar os dados dos alunos egressos e retorná-los para que o
  ## arquivo .csv possa ser gerado.
  def export_to_csv_graduates(self, args):

    # Query base que trás as informações que são comuns às rotas que possuem parâmetros,
    ## e para cada parâmetro, a condição específica é adicionada a essa string de consulta
    ### base.
    base_query = 'SELECT matricula, periodo_situacao, per_int, cred_obrig_int, \
      cred_opt_int, cred_comp_int, "Cota".descricao, "Genero".descricao, "EstadoCivil".descricao, \
      curriculo, cra, mc, iea, tranc, mat_inst, mob_estudantil, media_geral_ingresso \
      FROM "DiscenteVinculo" \
      INNER JOIN "Discente" \
        ON "DiscenteVinculo".cpf = "Discente".cpf \
      INNER JOIN "Cota" \
        ON "DiscenteVinculo".id_cota = "Cota".id \
      INNER JOIN "Genero" \
        ON "Discente".id_genero = "Genero".id \
      INNER JOIN "EstadoCivil" \
        ON "Discente".id_estado_civil = "EstadoCivil".id \
      WHERE id_curso = ' + self.id_computacao + ' \
      AND id_situacao_vinculo = ' + self.id_graduado

    if (len(args) == 1):
      periodo = args.get('from')

      base_query += 'AND periodo_situacao=\'' + str(periodo) + '\' \
        ORDER BY periodo_situacao'

    elif (len(args) == 2):
      minimo = args.get('from')
      maximo = args.get('to')

      # Caso o periodo minimo do intervalo seja maior que o maximo ou então igual, retorna
      ## uma mensagem de erro com código 404 not found.
      if (minimo > maximo or minimo == maximo):
        return { "error": "Parameters or invalid request" }, 404

      base_query += 'AND periodo_situacao BETWEEN \'' + str(minimo) + '\' AND \'' + str(maximo) + '\'\
        ORDER BY periodo_situacao'

    else:
      base_query += 'ORDER BY periodo_situacao'

    result = self.connection.select(base_query)
    return response_json_to_csv_graduates_export(result)


  # Função que retorna um json com todos os números de evadidos por período de todos os 
  ## motivos, que podem ter do id 1 ao 9, inclusive.
  def get_escaped(self, args):
    # Verifica se foi passado somente um parâmetro na rota, que no caso, é o período
    ## a ser consultado o número de evadidos.
    if (len(args) == 1):
      periodo = args.get('from')

      # Processando queries com os ID's de 1 a 9 e armazenando todos os resultados em uma lista,
      ## para posteriormente fazer um merge dos resultados.
      evadidos_por_motivo = []
      for i in range(1, 14):
        if (i != int(self.id_concluido) and i != int(self.id_graduado) and i != int(self.id_regular)):
          evadidos_por_motivo.append(process_query_of_one_period(self.id_computacao, i, periodo))

      joined_results = join_results_of_escaped_query(evadidos_por_motivo)

      statistics = get_escaped_statistics(joined_results, args, self.id_computacao, self.id_graduado)

      # Caso não hajam resultados para o periodo especificado, é retornado um json com
      ## todas as tags zeradas.
      if (len(joined_results) == 0):
        retorno =  {"period": periodo, "tags": { "tag1": 0, "tag2": 0, "tag3": 0, 
          "tag4": 0, "tag5": 0, "tag6": 0, "tag7": 0, "tag8": 0, "tag9": 0, "tag13": 0 } }
        
        return jsonify(retorno)

      joined_results_with_zeros = fill_tag_list_with_zeros(joined_results)

      json_return = response_json_to_escaped_route(joined_results_with_zeros)

      return jsonify(
        content=json_return,
        gross_total_dropouts=statistics[0],
        net_total_dropouts=statistics[1],
        relationship_escaped_by_begginers=statistics[2],
        relationship_escaped_by_graduates=statistics[3]
      )

    # Verifica se foram passados dois parâmetro na rota, que no caso, é o período de início
    ## e fim para a consulta nesse intervalo sobre o número de evadidos por período por todos
    ### os tipos de evasão.
    elif (len(args) == 2):
      minimo = args.get('from')
      maximo = args.get('to')

      # Caso o periodo minimo do intervalo seja maior que o maximo ou então igual, retorna
      ## uma mensagem de erro com código 404 not found.
      if (minimo > maximo):
        return { "error": "Parameters or invalid request" }, 404

      evadidos_por_motivo = []
      for i in range(1, 14):
        if (i != int(self.id_concluido) and i != int(self.id_graduado) and i != int(self.id_regular)):
          evadidos_por_motivo.append(process_query_of_interval_of_the_periods(self.id_computacao, i, minimo, maximo))

      joined_results = join_results_of_escaped_query(evadidos_por_motivo)

      statistics = get_escaped_statistics(joined_results, args, self.id_computacao, self.id_graduado)

      joined_results_all = add_periods_without_escaped(periodo_min=minimo, periodo_max=maximo, dados=joined_results)

      joined_results_with_zeros = fill_tag_list_with_zeros(joined_results_all)

      json_return = response_json_to_escaped_route(joined_results_with_zeros)

      sorted_json = sorted(json_return, key=lambda k: k['period'])

      return jsonify(
        content=sorted_json, 
        gross_total_dropouts=statistics[0],
        net_total_dropouts=statistics[1],
        relationship_escaped_by_begginers=statistics[2],
        relationship_escaped_by_graduates=statistics[3]
      )
      
    # Caso não seja passado parâmetro algum na rota, são trazidos os dados de todos os períodos
    ## já cadastrados
    else:
      evadidos_por_motivo = []
      for i in range(1, 14):
        if (i != int(self.id_concluido) and i != int(self.id_graduado) and i != int(self.id_regular)):
          evadidos_por_motivo.append(process_query_of_escaped(self.id_computacao, i))

      joined_results = join_results_of_escaped_query(evadidos_por_motivo)

      statistics = get_escaped_statistics(joined_results, args, self.id_computacao, self.id_graduado)

      joined_results_all = add_periods_without_escaped(dados=joined_results)

      joined_results_with_zeros = fill_tag_list_with_zeros(joined_results_all)

      json_return = response_json_to_escaped_route(joined_results_with_zeros)

      sorted_json = sorted(json_return, key=lambda k: k['period'])
      
      return jsonify(
        content=sorted_json, 
        gross_total_dropouts=statistics[0],
        net_total_dropouts=statistics[1],
        relationship_escaped_by_begginers=statistics[2],
        relationship_escaped_by_graduates=statistics[3]
      )  

  
  # Função responsável por buscar os dados para a geração do arquivo .csv de alunos evadidos.
  def export_to_csv_escaped(self, args):

    # Query base que trás as informações que são comuns às rotas que possuem parâmetros,
    ## e para cada parâmetro, a condição específica é adicionada a essa string de consulta
    ### base.
    base_query = 'SELECT matricula, periodo_situacao, "SituacaoVinculo".descricao, \
      per_int, cred_obrig_int, cred_opt_int, cred_comp_int, "Cota".descricao, \
      "Genero".descricao, "EstadoCivil".descricao, curriculo, cra, mc, iea, tranc, \
      mat_inst, mob_estudantil, media_geral_ingresso \
      FROM "DiscenteVinculo" \
      INNER JOIN "Discente" \
        ON "DiscenteVinculo".cpf = "Discente".cpf \
      INNER JOIN "Cota" \
        ON "DiscenteVinculo".id_cota = "Cota".id \
      INNER JOIN "Genero" \
        ON "Discente".id_genero = "Genero".id \
      INNER JOIN "EstadoCivil" \
        ON "Discente".id_estado_civil = "EstadoCivil".id \
      INNER JOIN "SituacaoVinculo" \
        ON "DiscenteVinculo".id_situacao_vinculo = "SituacaoVinculo".id \
      AND id_curso = ' + self.id_computacao + '\
      AND id_situacao_vinculo <> ' + self.id_concluido + '\
      AND id_situacao_vinculo <> ' + self.id_graduado + ' \
      AND id_situacao_vinculo <> ' + self.id_regular

    if (len(args) == 1):
      periodo = args.get('from')

      base_query += 'AND periodo_situacao=\'' + str(periodo) + '\' \
        ORDER BY id_situacao_vinculo' 
    
    elif (len(args) == 2):
      minimo = args.get('from')
      maximo = args.get('to')

      # Caso o periodo minimo do intervalo seja maior que o maximo ou então igual, retorna
      ## uma mensagem de erro com código 404 not found.
      if (minimo > maximo or minimo == maximo):
        return { "error": "Parameters or invalid request" }, 404

      base_query += 'AND periodo_situacao BETWEEN \'' + str(minimo) + '\' AND \'' + str(maximo) + '\'\
        ORDER BY periodo_situacao' 
    
    else:
      base_query += 'ORDER BY periodo_situacao'

    result = self.connection.select(base_query)

    return response_json_to_csv_escaped_export(result)

  
  # Função responsável por calcular a velocidade média dos alunos ativos do curso de Computação
  ## na UFCG com no mínimo 1 período integralizado.
  def get_average_speed(self):
    query = 'SELECT matricula, cred_obrig_int, cred_opt_int, per_int \
      FROM "DiscenteVinculo" \
      WHERE id_curso = ' + self.id_computacao + ' \
      AND id_situacao = ' + self.id_ativo + ' \
      AND id_situacao_vinculo = ' + self.id_regular + ' \
      AND per_int > 0'

    result = self.connection.select(query)

    qtd_ativos = len(result)
    alunos_velocidades = []
    acumulador_velocidades = 0
    for registro in result:
      matricula = registro[0]
      cred_obrig = registro[1]
      cred_opt = registro[2]

      if(cred_obrig == None):
        cred_obrig = 0
      if(cred_opt == None):
        cred_opt = 0

      creditos_totais = cred_obrig + cred_opt
      periodos_integralizados = registro[3]

      velocidade_media_aluno = creditos_totais / periodos_integralizados

      acumulador_velocidades += velocidade_media_aluno

      alunos_velocidades.append({
        "enrollment": matricula,
        "avg_speed": round(velocidade_media_aluno, 2),
      })

    return jsonify(
      active_students=alunos_velocidades,
      amount_actives=qtd_ativos,
      actives_avg_speed=round(acumulador_velocidades / qtd_ativos, 2),
    )

  # Função que calcula a exequibilidade de todos os alunos ativos do curso de Computação na
  ## UFCG e que possuem no mínimo 1 período integralizado e no máximo 14 períodos.
  def get_practicability(self):
    query = 'SELECT matricula, cred_obrig_int, cred_opt_int, per_int \
      FROM "DiscenteVinculo" \
      WHERE id_curso = ' + self.id_computacao + ' \
      AND id_situacao = ' + self.id_ativo + ' \
      AND id_situacao_vinculo = ' + self.id_regular + ' \
      AND per_int > 0 \
      AND per_int < ' + str(constants.PERIODOS_MAXIMO)

    result = self.connection.select(query)

    alunos_exequibilidades = []
    for registro in result:
      matricula = registro[0]
      cred_obrig = registro[1]
      cred_opt = registro[2]

      if(cred_obrig == None):
        cred_obrig = 0
      if(cred_opt == None):
        cred_opt = 0

      creditos_totais = cred_obrig + cred_opt
      periodos_integralizados = registro[3]

      exequibilidade = (constants.TOTAL_CREDITOS - creditos_totais) / \
        ((constants.PERIODOS_MAXIMO - 1 - periodos_integralizados) * constants.CREDITOS_MAXIMO + constants.CREDITOS_CONCLUINTE)

      alunos_exequibilidades.append({
        "enrollment": matricula,
        "exequibility": round(exequibilidade, 2)
      })
    
    return jsonify(alunos_exequibilidades)

  
  # Função que calcula a taxa de sucesso de todos os alunos do curso de Computação na
  ## UFCG que possuem mais de 0 créditos integralizados.
  def get_success_rate(self):
    query = 'SELECT "DiscenteVinculo".matricula, SUM("Disciplina".creditos) AS creditos_totais_matriculados, \
        "DiscenteVinculo".cred_obrig_int, "DiscenteVinculo".cred_opt_int \
      FROM "DiscenteVinculo" \
      INNER JOIN "DiscenteDisciplina" \
        ON "DiscenteVinculo".matricula = "DiscenteDisciplina".matricula \
      INNER JOIN "Turma" \
        ON "DiscenteDisciplina".id_turma = "Turma".id \
      INNER JOIN "Disciplina" \
        ON "Turma".id_disciplina = "Disciplina".id \
      WHERE cred_obrig_int IS NOT NULL \
      GROUP BY "DiscenteVinculo".matricula, "DiscenteVinculo".cred_obrig_int, "DiscenteVinculo".cred_opt_int \
      ORDER BY "DiscenteVinculo".matricula'

    result = self.connection.select(query)

    alunos_taxas_de_sucesso = []
    for registro in result:
      matricula = registro[0]
      cred_totais_matriculados = registro[1]
      cred_obrig_int = registro[2]
      cred_opt_int = registro[3]

      if(cred_opt_int == None):
        cred_opt_int = 0

      creditos_totais = cred_obrig_int + cred_opt_int
      if (creditos_totais > 0):
        taxa_sucesso = cred_totais_matriculados / creditos_totais
      else:
        taxa_sucesso = 0

      alunos_taxas_de_sucesso.append({
        "enrollment": matricula,
        "success_rate": round(taxa_sucesso, 2)
      })

    return jsonify(alunos_taxas_de_sucesso)
