import unittest

from models.tabelas import TabelFrequncia


class MyTestCase(unittest.TestCase):
    def test_devera_criar_limites_atraves_do_excesso(self):
        TabelFrequncia()
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
