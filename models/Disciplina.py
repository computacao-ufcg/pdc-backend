# coding: utf-8
import sys
sys.path.append("./connection")
from Connection import Connection
from flask import jsonify

class Disciplina():

  def __init__(self):
    self.connection = Connection()

  def get_rates_of_subjects(self):
    base_query = 'SELECT "Disciplina".codigo, COUNT("DiscenteDisciplina".*) \
      FROM "DiscenteDisciplina" \
      INNER JOIN "Turma" \
        ON "DiscenteDisciplina".id_turma = "Turma".id \
      INNER JOIN "Disciplina" \
        ON "Turma".id_disciplina = "Disciplina".id \
      INNER JOIN "Curriculo" \
        ON "Disciplina".codigo = "Curriculo".codigo_disciplina \
      AND "Curriculo".id_tipo_disciplina = 1'

    matriculas_totais = base_query + 'GROUP BY "Disciplina".codigo'
 
    total = self.connection.select(matriculas_totais)

    matriculas_aprovadas = base_query + 'AND "DiscenteDisciplina".id_situacao = 1 \
      GROUP BY "Disciplina".codigo'

    aprovadas = self.connection.select(matriculas_aprovadas)

    success_rates = []
    for i in range(len(total)):
      success_rate = aprovadas[i][1] / total[i][1]
      success_rates.append(round(success_rate, 2) * 100)

    success_rates.append(100.0)
    success_rates.sort()

    print(success_rates)
    if(len(success_rates) % 2 != 0):
      mid = len(success_rates) // 2
      mid_right = (len(success_rates) - mid) - 1

      minimo = success_rates[0]
      maximo = success_rates[len(success_rates) - 1]

      q2 = success_rates[mid]

      q1 = (success_rates[mid // 2] + success_rates[(mid // 2) + 1]) / 2

      q3 = (success_rates[mid + (mid_right // 2)] + success_rates[mid + (mid_right // 2) + 1]) / 2

    else:
      mid = (len(success_rates) // 2) - 1

      minimo = success_rates[0]
      maximo = success_rates[len(success_rates) - 1]

      q2 = (success_rates[mid] + success_rates[mid + 1]) / 2

      print(minimo, maximo)

      print(q2)

      





