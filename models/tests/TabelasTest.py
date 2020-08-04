import unittest

from models.tabelas import TabelaFrequncia


class MyTestCase(unittest.TestCase):
    def test_devera_criar_limites_atraves_do_excesso(self):
        TabelaFrequncia()
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
