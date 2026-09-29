import pytest

from mdd_calc import adj_alpha, mdd, required_n, z_sum

VAR = 0.05 * 0.95


def test_two_group_reference_values():
    zs = z_sum(0.05, 0.80, m=1)
    assert zs == pytest.approx(2.8016, abs=1e-3)
    assert mdd(200_000, 2, 0.5, VAR, zs) / 0.05 == pytest.approx(0.0546, abs=1e-4)
    assert required_n(0.05 * 0.05, 2, 0.5, VAR, zs) == pytest.approx(238_606, abs=1)


def test_bonferroni_and_sidak_alpha():
    assert adj_alpha(0.05, 2, "Bonferroni") == pytest.approx(0.025)
    assert adj_alpha(0.05, 2, "Sidak") == pytest.approx(1 - 0.95**0.5)
    assert adj_alpha(0.05, 2, "None") == 0.05


def test_more_groups_means_larger_mdd():
    def rel(k):
        return mdd(200_000, k, 1 / k, VAR, z_sum(0.05, 0.8, k - 1)) / 0.05
    assert rel(2) < rel(3) < rel(4)


def test_one_tailed_is_more_sensitive():
    assert z_sum(0.05, 0.8, 1, "One-tailed") < z_sum(0.05, 0.8, 1, "Two-tailed")


def test_mdd_and_required_n_are_inverses():
    zs = z_sum(0.05, 0.8, 2)
    d = mdd(60_000, 3, 1 / 3, VAR, zs)
    assert required_n(d, 3, 1 / 3, VAR, zs) == pytest.approx(60_000)
