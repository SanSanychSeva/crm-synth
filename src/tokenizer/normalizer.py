import re


class Normalizer:
    """
    Нормализация кандидатов словаря.

    Выполняет:
        - удаление лишних пробелов;
        - удаление пунктуации по краям;
        - удаление служебных шаблонов;
        - приведение к каноническому виду.
    """


    def __init__(self):

        # шаблоны, которые встречаются в CRM,
        # но не должны попадать в словарь

        self.prefix_patterns = [

            r"^-+\s*",

            r"^причина\s*-\s*",

            r"^по\s+услуге\s+",

            r"^на\s+",

        ]


        self.suffix_patterns = [

            r"\s*причина$",

            r"\s*причина\s*-$",

        ]


        self.stop_phrases = {

            "причина",
            "-",
            "по услуге",
            "зарегистрировано",

        }



    def normalize(
        self,
        phrase
    ):

        if phrase is None:
            return None


        phrase = phrase.lower()


        # пробелы

        phrase = re.sub(
            r"\s+",
            " ",
            phrase
        ).strip()


        # удалить префиксы

        changed = True

        while changed:

            changed = False

            for pattern in self.prefix_patterns:

                new_phrase = re.sub(
                    pattern,
                    "",
                    phrase
                )

                if new_phrase != phrase:

                    phrase = new_phrase.strip()

                    changed = True


        # удалить суффиксы

        changed = True

        while changed:

            changed = False

            for pattern in self.suffix_patterns:

                new_phrase = re.sub(
                    pattern,
                    "",
                    phrase
                )

                if new_phrase != phrase:

                    phrase = new_phrase.strip()

                    changed = True


        # убрать мусорную пунктуацию по краям

        phrase = phrase.strip(
            " .,:;-/()"
        )


        # еще раз убрать лишние пробелы

        phrase = re.sub(
            r"\s+",
            " ",
            phrase
        ).strip()


        if phrase in self.stop_phrases:

            return None


        if len(phrase) == 0:

            return None


        return phrase