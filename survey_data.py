"""Fonte compartilhada: demonstração sintética por padrão, CSV autorizado opcional."""

import os
import random

import pandas as pd


CATEGORICAL_COLUMNS = [
    'Você é um profissional:',
    'Qual sua faixa etaria?',
    'Gênero:',
    'Município onde reside:',
    'Faixa de renda mensal:',
    'Seu canal de compra mais frequente:',
    'Categoria do seu consumo mensal principal:',
    'Gasto mensal não essencial (R$):',
    'Local mais frequente de lazer:',
    'Frequências de lazer semanal:',
    'Estilo de vida predominante:',
    'Plataforma onde acompanha marcas:',
    'Frequência de compras online:',
]


def is_demo():
    return not (os.environ.get('SURVEY_CSV_PATH') or os.environ.get('SURVEY_CSV_URL'))


def load_survey():
    """Lê somente as colunas de análise; não exporta nomes ou contatos do CSV."""
    source = os.environ.get('SURVEY_CSV_PATH') or os.environ.get('SURVEY_CSV_URL')
    if source:
        return pd.read_csv(source, usecols=CATEGORICAL_COLUMNS)

    rng = random.Random(42)
    profiles = [
        ['Estudante', '18-24', 'Não informado', 'Fortaleza', 'Até R$ 2.000',
         'Online', 'Alimentação', '100-200', 'Praia', '1 vez',
         'Ativo', 'Instagram', 'Semanal'],
        ['Autônomo', '25-34', 'Não informado', 'Caucaia', 'R$ 2.000-4.000',
         'Loja física', 'Casa', '300-500', 'Parque', '2 vezes',
         'Tranquilo', 'YouTube', 'Mensal'],
        ['Empregado', '35-44', 'Não informado', 'Maracanaú', 'R$ 4.000-6.000',
         'Online', 'Tecnologia', '500-800', 'Cinema', '1 vez',
         'Digital', 'YouTube', 'Semanal'],
        ['Empregado', '45-54', 'Não informado', 'Fortaleza', 'Acima de R$ 6.000',
         'Loja física', 'Saúde', '800-1200', 'Restaurante', '3 vezes',
         'Social', 'Instagram', 'Mensal'],
    ]
    rows = []
    for profile in profiles:
        for _ in range(20):
            row = profile.copy()
            row[2] = rng.choice(['Feminino', 'Masculino', 'Não informado'])
            if rng.random() < 0.2:
                row[11] = rng.choice(['Instagram', 'YouTube', 'Não acompanha'])
            rows.append(row)
    return pd.DataFrame(rows, columns=CATEGORICAL_COLUMNS)
