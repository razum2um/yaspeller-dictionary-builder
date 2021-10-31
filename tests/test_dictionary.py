import unittest
import os
import pymorphy2
from dictionary import export_all_words, inflections, process_file

curdir = os.path.abspath(os.path.dirname(__file__))
fixture_file = os.path.abspath(os.path.join(curdir, './yaspeller_report.json'))

morph = pymorphy2.MorphAnalyzer(lang='ru', char_substitutes={})


class TestDictionary(unittest.TestCase):

    def test_export_all_words(self):
        expected = [
            'баг',
            'багах',
            'баги',
            'дифф',
            'коммита',
            'коммитить',
            'коммиту',
            'патчингах',
            'патчингом',
            'рубистами',
            'самоорганизованными',
            'тикет'
        ]
        actual = export_all_words(fixture_file)
        self.assertEqual(actual, expected)

    def test_inflections(self):
        parsed = morph.parse('баг')[0]
        self.assertEqual('[бБ]аг(а|ам|ами|ах|е|и|ов|ом|у)?',
                         inflections(parsed))
        parsed = morph.parse('коммита')[0]
        self.assertEqual(
            '[кК]оммит(а|ам|ами|ах|е|ов|ом|у|ы)?', inflections(parsed))

        parsed = morph.parse('рубистами')[0]
        self.assertEqual(
            '[рР]убист(а|ам|ами|ах|е|ов|ом|у|ы)?', inflections(parsed))

        parsed = morph.parse('тикет')[0]
        self.assertEqual('[тТ]икет(а|ам|ами|ах|е|ой|у|ы)?',
                         inflections(parsed))

        parsed = morph.parse('дифф')[0]
        self.assertEqual('[дД]ифф(а|ам|ами|ах|е|ов|ом|у|ы)?',
                         inflections(parsed))

        parsed = morph.parse('самоорганизованными')[0]
        self.assertEqual(
            '[сС]амоорганизованн(ого|ом|ому|ую|ые|ый|ым|ыми|ых)', inflections(parsed))

        parsed = morph.parse('коммитить')[0]
        self.assertEqual('коммитить', inflections(parsed))

        parsed = morph.parse('сгенеренную')[0]
        self.assertEqual(
            '[сС]генеренн(ая|ого|ой|ом|ому|ую|ые|ый|ым|ыми|ых)', inflections(parsed))

        parsed = morph.parse('несимвольные')[0]
        self.assertEqual(
            '[нН]есимвольн(ая|ого|ой|ом|ому|ую|ые|ый|ым|ыми|ых)', inflections(parsed))

        parsed = morph.parse('ноду')[0]
        self.assertEqual(
            '[нН]од(а|ам|ами|ах|е|ой|у|ы)?', inflections(parsed))

    def test_process_file(self):
        expected = [
            '[бБ]аг(а|ам|ами|ах|е|и|ов|ом|у)?',
            '[дД]ифф(а|ам|ами|ах|е|ов|ом|у|ы)?',
            '[кК]оммит(а|ам|ами|ах|е|ов|ом|у|ы)?',
            '[пП]атчинг(а|ам|ами|ах|е|и|ов|ом|у)?',
            '[рР]убист(а|ам|ами|ах|е|ов|ом|у|ы)?',
            '[сС]амоорганизованн(ого|ом|ому|ую|ые|ый|ым|ыми|ых)',
            '[тТ]икет(а|ам|ами|ах|е|ов|ом|у|ы)?',
            'коммитить'
        ]
        self.assertEqual(expected, process_file(fixture_file))


if __name__ == '__main__':
    unittest.main()
