import sys
import string
import functools
import itertools


def incap_wrapper(func):

    @functools.wraps(func)
    def incap(string):
        a = string.upper()[0]
        b = string.lower()[1:]
        a += b
        string = a

        def is_letter(sym):
            if 'a' <= sym <= 'z' or 'A' <= sym <= 'Z' or 'а' <= sym <= 'я' or 'А' <= sym <= 'Я':
                return True
            else:
                return False

        a = ''
        for i in string:
            if not (is_letter(i)):
                break
            else:
                a += i
        a = func(a)
        return a
    return incap


@incap_wrapper
def transliterate(string):
    capital_letters = {u'А': u'A',
                       u'Б': u'B',
                       u'В': u'V',
                       u'Г': u'G',
                       u'Д': u'D',
                       u'Е': u'E',
                       u'Ё': u'E',
                       u'З': u'Z',
                       u'И': u'I',
                       u'Й': u'Y',
                       u'К': u'K',
                       u'Л': u'L',
                       u'М': u'M',
                       u'Н': u'N',
                       u'О': u'O',
                       u'П': u'P',
                       u'Р': u'R',
                       u'С': u'S',
                       u'Т': u'T',
                       u'У': u'U',
                       u'Ф': u'F',
                       u'Х': u'H',
                       u'Ъ': u'',
                       u'Ы': u'Y',
                       u'Ь': u'',
                       u'Э': u'E',}

    capital_to_multiple_translit = dict(Ж=u'Zh', Ц=u'Ts', Ч=u'Ch', Ш=u'Sh', Щ=u'Sch', Ю=u'Yu', Я=u'Ya')

    lower_case_letters = {u'а': u'a',
                       u'б': u'b',
                       u'в': u'v',
                       u'г': u'g',
                       u'д': u'd',
                       u'е': u'e',
                       u'ё': u'e',
                       u'ж': u'zh',
                       u'з': u'z',
                       u'и': u'i',
                       u'й': u'y',
                       u'к': u'k',
                       u'л': u'l',
                       u'м': u'm',
                       u'н': u'n',
                       u'о': u'o',
                       u'п': u'p',
                       u'р': u'r',
                       u'с': u's',
                       u'т': u't',
                       u'у': u'u',
                       u'ф': u'f',
                       u'х': u'h',
                       u'ц': u'ts',
                       u'ч': u'ch',
                       u'ш': u'sh',
                       u'щ': u'sch',
                       u'ъ': u'',
                       u'ы': u'y',
                       u'ь': u'',
                       u'э': u'e',
                       u'ю': u'yu',
                       u'я': u'ya',}

    capital_and_lower_case_letter_pairs = {}

    for capital_letter, capital_letter_translit in iter(capital_to_multiple_translit.items()):
        for lowercase_letter, lowercase_letter_translit in iter(lower_case_letters.items()):
            capital_and_lower_case_letter_pairs[u"%s%s" % (capital_letter, lowercase_letter)] = u"%s%s" % (capital_letter_translit, lowercase_letter_translit)

    for dictionary in (capital_and_lower_case_letter_pairs, capital_letters, lower_case_letters):

        for cyrillic_string, latin_string in iter(dictionary.items()):
            string = string.replace(cyrillic_string, latin_string)

    for cyrillic_string, latin_string in iter(capital_to_multiple_translit.items()):
        string = string.replace(cyrillic_string, latin_string.upper())

    return string


def get_rid_of_stuff(string):
    def is_letter(sym):
        if 'a' <= sym <= 'z' or 'A' <= sym <= 'Z' or 'а' <= sym <= 'я' or 'А' <= sym <= 'Я':
            return True
        else:
            return False
    a = ''
    for i in string:
        if not (is_letter(i)):
            break
        else:
            a += i
    return a

if __name__ == '__main__':
    pass
