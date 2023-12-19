import re

from solution.part import Part
from solution.rule import Rule


class Workflow:
    def __init__(self, rules: str):
        self.rules: list[Rule] = []
        rule_regex = re.compile(r"^(?P<parameter>[xmas])(?P<operator>[<>])(?P<value>[0-9]*):(?P<next>[a-zAR]*)$")
        end_rule_regex = re.compile(r"^(?P<next>[a-zAR]*)$")
        for rule in rules.split(","):
            if match := re.match(rule_regex, rule):
                self.rules.append(Rule(match["parameter"], match["operator"], match["value"], match["next"]))
            elif match := re.match(end_rule_regex, rule):
                self.rules.append(Rule(None, None, None, match["next"]))
            else:
                assert False

    def process(self, part: Part) -> str:
        for rule in self.rules:
            result: str | None = rule.apply(part)
            if result:
                return result

        assert False
