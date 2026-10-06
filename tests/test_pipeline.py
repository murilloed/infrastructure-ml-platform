import unittest,asyncio,tempfile
from pathlib import Path
from mlplatform.core import ingest,validate
class Tests(unittest.TestCase):
    def test_idempotency_survives_restart(self):
        e={'id':'a','asset':'x','timestamp':'2026-01-01T00:00:00Z','cpu':10}
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'db.sqlite'
            r=asyncio.run(ingest([e,e,{'cpu':999}],p))
            self.assertEqual((r['accepted'],r['duplicate'],r['rejected']),(1,1,1))
            again=asyncio.run(ingest([e],p)); self.assertEqual(again['duplicate'],1)
    def test_nonfinite(self):
        with self.assertRaises(ValueError): validate({'id':'a','asset':'x','timestamp':'x','cpu':float('nan')})
