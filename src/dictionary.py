import os
import json
import pymorphy2
import argparse

morph = pymorphy2.MorphAnalyzer(lang='ru', char_substitutes={})
cases = [{'nomn'}, {'gent'}, {'datv'}, {'accs'}, {'ablt'}, {'loct'}]

# баг, самоорганизованными
noun_prtf_inflection_cases = [
    x | y for x in cases for y in [{'sing'}, {'plur'}]]

# пропатченную
adjf_inflection_cases = [
    x | gender for x in noun_prtf_inflection_cases for gender in [{'masc'}, {'femn'}, set()]]

inflection_cases_by_tag = {
    'NOUN': noun_prtf_inflection_cases,
    'PRTF': noun_prtf_inflection_cases,
    'ADJF': adjf_inflection_cases,
}


def flatten(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


def _remove_prefix(text, prefix):
    '''compat 3.9'''
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def _export_words(file_report):
    return [x['word'] for x in file_report['data']]


def export_all_words(fname):
    with open(fname, 'r') as outfile:
        lst = [_export_words(file_report)
               for file_status, file_report in json.load(outfile)]
        return sorted(set(flatten(lst)))


def _regexp_inflectable(parsed, inflection_cases):
    '''_regexp_inflectable(morph.parse('баг')[0]) #=> "[бБ]аг(а|ам|ами|ах|е|и|ов|ом|у)?"'''
    lexems = list(set([lexem.word for lexem in (parsed.inflect(
        case) for case in inflection_cases) if lexem is not None]))
    prefix = os.path.commonprefix(lexems)
    start = prefix[0].lower()
    suffixes = sorted(set([_remove_prefix(lexem, prefix) for lexem in lexems]))
    optional_regexp_suffix = ''
    if '' in suffixes:
        optional_regexp_suffix = '?'
        suffixes.remove('')
    regexp_suffixes = "(%s)" % ('|'.join(suffixes),)
    if len(suffixes) == 0:
        regexp_suffixes = ''
        optional_regexp_suffix = ''

    regexp = "[%s%s]" % (start, start.upper()) + prefix[1:] + \
        regexp_suffixes + optional_regexp_suffix
    # debug output using this:
    # return "%s | %s | %s" % (regexp, parsed.word, parsed.tag)
    return regexp


def inflections(parsed):
    inflection_cases = inflection_cases_by_tag.get(parsed.tag.POS)
    if inflection_cases:
        return _regexp_inflectable(parsed, inflection_cases)
    else:
        return parsed.word


def process_file(fname):
    cache = {}
    for word in export_all_words(fname):
        parseds = morph.parse(word)
        norms = set([parsed.normalized.word for parsed in parseds])
        if len(norms & cache.keys()) > 0:
            continue  # if a 2nd variant of word is processed as 1st variant earlier
        parsed = sorted(parseds, key=lambda p: p.tag.animacy != 'inan')[
            0]  # non-animals first
        norm = parsed.normalized.word
        if norm not in cache:
            cache[norm] = inflections(parsed)
            # debug output using this:
            # cache[norm] += " [%s | %s]" % (parsed.word, parsed.tag)
    return sorted(set(cache.values()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()
    dict_words = process_file(args.file)
    print(json.dumps(dict_words, ensure_ascii=False, indent=4, sort_keys=True))
