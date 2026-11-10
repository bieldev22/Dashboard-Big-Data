import math
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import matplotlib
matplotlib.use('Agg')

from analysis_utils import faixa_to_numeric
from survey_data import CATEGORICAL_COLUMNS, is_demo, load_survey


class AnalysisTests(unittest.TestCase):
    def test_monetary_ranges_and_missing_values(self):
        for value, expected in [('100-200', 150), ('R$ 1.000-2.000', 1500),
                                ('até 200', 200), ('acima de 2000', 2000),
                                ('2000+', 2000), ('R$ 250,50', 250.5)]:
            with self.subTest(value=value):
                self.assertEqual(faixa_to_numeric(value), expected)
        self.assertTrue(math.isnan(faixa_to_numeric(None)))
        self.assertTrue(math.isnan(faixa_to_numeric('Não informado')))

    def test_demo_is_reproducible_and_has_only_analysis_columns(self):
        with patch.dict(os.environ, {'SURVEY_CSV_PATH': '', 'SURVEY_CSV_URL': ''}):
            self.assertTrue(is_demo())
            frame = load_survey()
            self.assertEqual(frame.shape, (80, 13))
            self.assertEqual(list(frame.columns), CATEGORICAL_COLUMNS)
            self.assertTrue(frame.equals(load_survey()))
            self.assertFalse(frame.isna().any().any())

    def test_authorized_csv_excludes_identifying_columns(self):
        with patch.dict(os.environ, {'SURVEY_CSV_PATH': '', 'SURVEY_CSV_URL': ''}):
            frame = load_survey()
        frame['email'] = 'pessoa@example.invalid'
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'survey.csv'
            frame.to_csv(source, index=False)
            with patch.dict(os.environ, {'SURVEY_CSV_PATH': str(source), 'SURVEY_CSV_URL': ''}):
                self.assertFalse(is_demo())
                self.assertNotIn('email', load_survey().columns)

    def test_streamlit_pages_and_per_cluster_statistics(self):
        from streamlit.testing.v1 import AppTest
        with patch.dict(os.environ, {'SURVEY_CSV_PATH': '', 'SURVEY_CSV_URL': ''}):
            app = AppTest.from_file('app.py', default_timeout=60).run()
            self.assertEqual(len(app.exception), 0)
            self.assertEqual(len(app.dataframe), 1)
            self.assertIn('Dados fictícios', app.caption[0].value)
            app.switch_page('graf.py').run()
            self.assertEqual(len(app.exception), 0)
            app.switch_page('models.py').run()
            self.assertEqual(len(app.exception), 0)
            cards = [item.value for item in app.markdown if '<div class="persona-id">' in item.value]
            self.assertEqual(len(cards), 4)
            self.assertTrue(all('Número de membros: 20' in card for card in cards))
            for median in ['150.00', '400.00', '650.00', '1000.00']:
                self.assertTrue(any(median in card for card in cards))


if __name__ == '__main__':
    unittest.main()
