import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / '.agents/skills/cfo-cash-forecast/scripts/forecast.py'
spec = importlib.util.spec_from_file_location('forecast', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture():
    return {'currency': 'JPY', 'start': '2026-12-01', 'end': '2026-12-14',
            'opening': '300000', 'floor': '100000', 'events': [
                {'id': 'a', 'date': '2026-12-04', 'kind': 'out', 'amount': '180000', 'currency': 'JPY', 'status': 'scheduled', 'source': 'fixture-1'},
                {'id': 'b', 'date': '2026-12-08', 'kind': 'in', 'amount': '200000', 'currency': 'JPY', 'status': 'scheduled', 'source': 'fixture-2'},
                {'id': 'c', 'date': '2026-12-11', 'kind': 'out', 'amount': '250000', 'currency': 'JPY', 'status': 'scheduled', 'source': 'fixture-3'}]}


class ForecastTests(unittest.TestCase):
    def test_basic_and_floor(self):
        output = module.forecast(fixture())
        self.assertEqual([row['closing'] for row in output['daily']], ['120000', '320000', '70000'])
        self.assertEqual(output['maximum_floor_gap'], '30000')
        self.assertEqual(output['first_below_floor_date'], '2026-12-11')
        self.assertIsNone(output['first_negative_date'])

    def test_delayed_receipt_moves_outside_horizon(self):
        data = fixture()
        data['events'][1]['date'] = '2026-12-18'
        output = module.forecast(data)
        self.assertEqual(output['closing'], '-130000')
        self.assertEqual(output['excluded_event_ids'], ['b'])
        self.assertEqual(output['first_negative_date'], '2026-12-11')

    def test_intermediate_shortage_not_hidden_by_recovery(self):
        data = fixture()
        data['events'][1]['date'] = '2026-12-14'
        output = module.forecast(data)
        self.assertEqual(output['closing'], '70000')
        self.assertEqual(output['minimum_balance'], '-130000')

    def test_same_day_order_not_claimed_known(self):
        data = fixture()
        data['events'][1]['date'] = '2026-12-11'
        self.assertEqual(module.forecast(data)['intraday_order_unknown_dates'], ['2026-12-11'])

    def test_floor_unset_and_no_events(self):
        data = fixture()
        data.pop('floor')
        data['events'] = []
        output = module.forecast(data)
        self.assertIsNone(output['floor'])
        self.assertIsNone(output['maximum_floor_gap'])
        self.assertEqual(output['closing'], '300000')

    def test_reject_incomplete_and_ambiguous_inputs(self):
        mutations = [('amount', None), ('amount', 1.5), ('amount', True), ('amount', 'NaN'),
                     ('amount', 'Infinity'), ('amount', '-1'), ('currency', 'USD'),
                     ('status', 'unknown'), ('date', 'unknown'), ('source', '')]
        for key, value in mutations:
            with self.subTest(key=key, value=value):
                data = fixture()
                data['events'][0][key] = value
                with self.assertRaises(ValueError):
                    module.forecast(data)
        data = fixture()
        data['events'].append(copy.deepcopy(data['events'][0]))
        with self.assertRaises(ValueError):
            module.forecast(data)

    def test_decimal_arithmetic_and_assumptions(self):
        data = fixture()
        data['opening'] = '0.1'
        data['floor'] = None
        data['events'] = [dict(data['events'][1], amount='0.2', status='assumed')]
        output = module.forecast(data)
        self.assertEqual(output['closing'], '0.3')
        self.assertEqual(output['assumed_event_ids'], ['b'])

    def test_initial_shortage_and_period_boundaries(self):
        data = fixture()
        data['opening'] = '-1'
        data['events'] = [dict(data['events'][1], date=data['end'])]
        output = module.forecast(data)
        self.assertEqual(output['first_negative_date'], data['start'])
        self.assertEqual(output['closing'], '199999')

    def test_supported_precision_preserves_small_movements(self):
        data = fixture()
        data['opening'] = '100000000000000000000000'
        data['floor'] = None
        data['events'] = [dict(data['events'][1], amount='0.00000001')]
        self.assertEqual(module.forecast(data)['closing'], '100000000000000000000000.00000001')

    def test_cli_success_and_error_leave_input_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.json'
            raw = json.dumps(fixture())
            path.write_text(raw)
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['closing'], '70000')
            self.assertEqual(path.read_text(), raw)
            path.write_text('{"opening": null}')
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn('error', json.loads(result.stderr))


if __name__ == '__main__':
    unittest.main()
