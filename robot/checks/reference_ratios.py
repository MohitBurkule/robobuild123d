"""`reference.feature_ratio`: design proportions measured on reference photos vs the model.

Runs last so `metric:` terms can use any metric computed by earlier groups (archetype, spinner, mass...).
The spec format and terms are documented in reference.py (`feature_ratios`).
"""

from .reference import feature_ratios


def run(ctx):
    return feature_ratios(ctx)
