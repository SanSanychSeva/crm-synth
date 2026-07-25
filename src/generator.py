from pathlib import Path
import random
import yaml
import pandas as pd


class CRMGenerator:
    """
    Генератор синтетических CRM/NOC комментариев.
    """

    def __init__(self, config_path="../", seed=None):

        if seed is not None:
            random.seed(seed)

        self.base_path = Path(config_path)

        self.services = self._load(
            "dictionaries/services.yaml"
        )

        self.technologies = self._load(
            "dictionaries/technologies.yaml"
        )

        self.symptoms = self._load(
            "dictionaries/symptoms.yaml"
        )

        self.reasons = self._load(
            "dictionaries/reasons.yaml"
        )

        self.degradation = self._load(
            "dictionaries/degradation.yaml"
        )

        self.compatibility = self._load(
            "topology/compatibility.yaml"
        )

        self.probabilities = self._load(
            "topology/probabilities.yaml"
        )

        self.regions = self._load(
            "topology/regions.yaml"
        )

        self.aliases = self._load(
            "language/aliases.yaml"
        )

        self.templates = self._load(
            "language/templates.yaml"
        )

        self.mutations = self._load(
            "language/mutations.yaml"
        )


    def _load(self, filename):

        path = self.base_path / filename

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return yaml.safe_load(f)



    def _weighted_choice(self, data):

        """
        Выбор ключа по весам.

        input:
            {
              key1: 0.7,
              key2: 0.3
            }
        """

        keys = list(data.keys())
        weights = list(data.values())

        return random.choices(
            keys,
            weights=weights,
            k=1
        )[0]



    def _choose_service(self):

        return self._weighted_choice(
            self.probabilities["service"]
        )



    def _choose_technology(self):

        return self._weighted_choice(
            self.probabilities["technology"]
        )



    def _choose_degradation(self):

        return self._weighted_choice(
            self.probabilities["degradation"]
        )



    def _choose_template(self):

        return self._weighted_choice(
            self.probabilities["template"]
        )



    def _choose_region(self):

        return random.choice(
            list(self.regions.keys())
        )



    def _choose_scenario(self):

        """
        Генерация допустимого сочетания:
        service -> technology -> symptom/reason
        """

        while True:

            service = self._choose_service()

            if service not in self.compatibility:
                continue


            technology = random.choice(
                list(
                    self.compatibility[service].keys()
                )
            )


            data = self.compatibility[
                service
            ][technology]


            symptom = random.choice(
                data["symptoms"]
            )


            reason = random.choice(
                data["reasons"]
            )


            return {
                "service": service,
                "technology": technology,
                "symptom": symptom,
                "reason": reason
            }



    def _alias(self, category, key, region=None):

        """
        Выбор текстового представления.
        """

        # региональный override

        if region:

            reg = self.regions.get(
                region,
                {}
            )

            aliases = (
                reg
                .get("aliases", {})
                .get(key)
            )

            if aliases:
                return aliases


        variants = (
            self.aliases
            .get(category, {})
            .get(key)
        )


        if variants:
            return random.choice(
                variants
            )


        return key



    def _apply_mutations(self, text):

        # замена знаков

        if random.random() < self.mutations["punctuation"]["dash"]["probability"]:

            text = text.replace(
                "-",
                random.choice(
                    self.mutations
                    ["punctuation"]
                    ["dash"]
                    ["variants"]
                )
            )


        # добавление финальной фразы

        if random.random() < self.mutations["append_phrase"]["probability"]:

            phrase = random.choice(
                self.mutations
                ["append_phrase"]
                ["variants"]
            )

            text += ". " + phrase


        return text



    def generate_one(self):

        scenario = self._choose_scenario()

        region = self._choose_region()

        degradation = self._choose_degradation()

        template_id = self._choose_template()

        template = self.templates[
            template_id
        ]["text"]


        values = {

            "SERVICE":
                self._alias(
                    "service",
                    scenario["service"],
                    region
                ),

            "TECH":
                self._alias(
                    "technology",
                    scenario["technology"],
                    region
                ),

            "SYMPTOM":
                self._alias(
                    "symptom",
                    scenario["symptom"],
                    region
                ),

            "REASON":
                self._alias(
                    "reason",
                    scenario["reason"],
                    region
                ),

            "DEGRADATION":
                self._alias(
                    "degradation",
                    degradation,
                    region
                )
        }


        text = template.format(
            **values
        )


        text = self._apply_mutations(
            text
        )


        return {

            "comment": text,

            "service":
                scenario["service"],

            "technology":
                scenario["technology"],

            "symptom":
                scenario["symptom"],

            "reason":
                scenario["reason"],

            "degradation":
                degradation,

            "region":
                region,

            "template":
                template_id
        }



    def generate(
        self,
        n=1000
    ):

        rows = []

        for _ in range(n):

            rows.append(
                self.generate_one()
            )


        return pd.DataFrame(rows)