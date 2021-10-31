# Yaspeller Dictionary (Auto)builder

## Usage

```sh
# this sample command generates `./yaspeller_report.json`
# yaspeller --report json --ignore-digits --ignore-text "'.*" --ignore-latin --only-errors --file-extensions ".md" --lang ru

python -m venv env
source env/bin/activate
pip install 
python src/dictionary.py yaspeller_report.json
```

## Why

[Yaspeller](https://github.com/hcodes/yaspeller) is nice, but there are too many anglicisms in a usual documentation.
Normally you just want to ignore that, but there's the only possibility to add a regexp-array to ignore words.

This generates a array of dictionary words including all lexems for all cases like

```
```

from yaspeller errors (in text format looking like)

```
Spelling check:
✗ www.ruby-lang.org/ru/community/ruby-core/index.md 130 ms
-----
Typos: 9
1. патчингом (36:27)
2. коммитить (68:32, suggest: комитет)
3. багах (75:15, suggest: богах, баках, бегах)
4. баги (89:24, suggest: багги)
5. баг (96:25)
6. тикет (107:14, suggest: этикет)
7. дифф (115:18)
8. коммиту (147:24, suggest: комету, комнату)
9. коммита (148:58, suggest: комета)
-----
```