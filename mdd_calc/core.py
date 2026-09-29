"""Core math for MDD (minimum detectable difference) and sample-size planning.

Model: k groups (1 control + k-1 treatments). Each treatment is compared with control,
so there are m = k-1 comparisons. Normal approximation, variance evaluated at the baseline.

    MDD = (z_alpha + z_power) * sqrt(var * (1/n_control + 1/n_treatment))
"""
from math import sqrt

from scipy.stats import norm


def adj_alpha(alpha: float, m: int, method: str = "Bonferroni") -> float:
    """Alpha used for each of the m comparisons."""
    if method == "Bonferroni":
        return alpha / m
    if method == "Sidak":
        return 1 - (1 - alpha) ** (1 / m)
    return alpha  # "None"


def z_sum(alpha: float, power: float, m: int = 1, tails: str = "Two-tailed", method: str = "Bonferroni") -> float:
    """z_alpha + z_power: how many standard errors the true effect must span."""
    a = adj_alpha(alpha, m, method)
    z_alpha = norm.ppf(1 - a / (2 if tails == "Two-tailed" else 1))
    return z_alpha + norm.ppf(power)


def mdd(n: float, k: int, control_share: float, var: float, zs: float) -> float:
    """Absolute MDD. n = analysed sample (all groups), var = variance of one observation."""
    n_control = n * control_share
    n_treat = n * (1 - control_share) / (k - 1)
    return zs * sqrt(var * (1 / n_control + 1 / n_treat))


def required_n(delta: float, k: int, control_share: float, var: float, zs: float) -> float:
    """Total analysed sample needed to detect an absolute difference `delta`."""
    return zs**2 * var * (1 / control_share + (k - 1) / (1 - control_share)) / delta**2
