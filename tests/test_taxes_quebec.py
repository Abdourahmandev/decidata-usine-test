"""Tests du module taxes_quebec."""

from decimal import Decimal

import pytest

from taxes_quebec import (
    MontantInvalideError,
    MontantNonNumeriqueError,
    calculer_taxes,
)


def test_montant_100_dollars():
    assert calculer_taxes(Decimal("100")) == {
        "ht": Decimal("100.00"),
        "tps": Decimal("5.00"),
        "tvq": Decimal("9.98"),
        "ttc": Decimal("114.98"),
    }


def test_montant_zero():
    assert calculer_taxes(Decimal("0")) == {
        "ht": Decimal("0.00"),
        "tps": Decimal("0.00"),
        "tvq": Decimal("0.00"),
        "ttc": Decimal("0.00"),
    }


def test_arrondi_19_99():
    # 19.99 $ * 5 % = 0.9995 $ -> 1.00 $ ; 19.99 $ * 9.975 % = 1.994... -> 1.99 $.
    resultat = calculer_taxes(Decimal("19.99"))
    assert resultat["tps"] == Decimal("1.00")
    assert resultat["tvq"] == Decimal("1.99")
    assert resultat["ttc"] == Decimal("22.98")


def test_arrondi_commercial_demi_cent():
    # 0.10 $ * 5 % = 0.005 $ -> arrondi commercial (HALF_UP) = 0.01 $.
    assert calculer_taxes(Decimal("0.10"))["tps"] == Decimal("0.01")
    # 0.30 $ * 5 % = 0.015 $ -> arrondi commercial (HALF_UP) = 0.02 $.
    assert calculer_taxes(Decimal("0.30"))["tps"] == Decimal("0.02")


def test_montant_negatif_leve_erreur():
    for valeur in (Decimal("-1.00"), -1, Decimal("-0.01")):
        with pytest.raises(MontantInvalideError):
            calculer_taxes(valeur)


def test_type_non_numerique_leve_erreur():
    for valeur in ("abc", [100], None, True, False):
        with pytest.raises(MontantNonNumeriqueError):
            calculer_taxes(valeur)


def test_erreurs_sont_des_value_error():
    assert issubclass(MontantInvalideError, ValueError)
    assert issubclass(MontantNonNumeriqueError, ValueError)
    with pytest.raises(ValueError):
        calculer_taxes("abc")
    with pytest.raises(ValueError):
        calculer_taxes(Decimal("-1.00"))


def test_accepte_int_float_et_decimal():
    assert calculer_taxes(100)["ttc"] == Decimal("114.98")
    assert calculer_taxes(100.0)["tvq"] == Decimal("9.98")
    assert calculer_taxes(Decimal("100"))["tps"] == Decimal("5.00")
