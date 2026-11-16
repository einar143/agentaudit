"""Rules. Importing a rule module registers its rules."""

from agentaudit.rules import supply_chain  # noqa: F401
from agentaudit.rules.base import Rule, all_rules, register

__all__ = ["Rule", "all_rules", "register"]
