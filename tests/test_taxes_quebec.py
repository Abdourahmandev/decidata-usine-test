"""Tests du module taxes_quebec."""

from decimal import Decimal

import pytest

from taxes_quebec import (
    MontantInvalideError,
    TypeMontantInvalideError,
    calculer_total,
    calculer_tps,
    calculer_tvq,
)


def test_montant_100_dollars():
    assert calculer_tps(Decimal("100")) == Decimal("5.00")
    assert calculer_tvq(Decimal("100")) == Decimal("9.98")
    assert calculer_total(Decimal("100")) == Decimal("114.98")


def test_montant_zero():
    assert calculer_tps(Decimal("0")) == Decimal("0.00")
    assert calculer_tvq(Decimal("0")) == Decimal("0.00")
    assert calculer_total(Decimal("0")) == Decimal("0.00")


def test_arrondi_commercial_demi_cent():
    # 0.10 $ * 5 % = 0.005 $ -> arrondi commercial (HALF_UP) = 0.01 $.
    assert calculer_tps(Decimal("0.10")) == Decimal("0.01")
    # 0.30 $ * 5 % = 0.015 $ -> arrondi commercial (HALF_UP) = 0.02 $.
    assert calculer_tps(Decimal("0.30")) == Decimal("0.02")


def test_montant_negatif_leve_erreur():
    with pytest.raises(MontantInvalideError):
        calculer_tps(Decimal("-1.00"))
    with pytest.raises(MontantInvalideError):
        calculer_tvq(-1)
    with pytest.raises(MontantInvalideError):
        calculer_total(Decimal("-0.01"))


def test_type_non_numerique_leve_erreur():
    for valeur in ("abc", [100], None):
        with pytest.raises(TypeMontantInvalideError):
            calculer_tps(valeur)
        with pytest.raises(TypeMontantInvalideError):
            calculer_tvq(valeur)
        with pytest.raises(TypeMontantInvalideError):
            calculer_total(valeur)


def test_accepte_int_float_et_decimal():
    assert calculer_tps(100) == Decimal("5.00")
    assert calculer_tvq(100.0) == Decimal("9.98")
    assert calculer_total(Decimal("100")) == Decimal("114.98")
