"""Tests du module taxes_quebec."""

from decimal import Decimal

import pytest

from taxes_quebec import (
    MontantInvalideError,
    MontantNonNumeriqueError,
    calculer_ht_depuis_ttc,
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


def test_ht_depuis_ttc_114_98():
    assert calculer_ht_depuis_ttc(Decimal("114.98")) == {
        "ht": Decimal("100.00"),
        "tps": Decimal("5.00"),
        "tvq": Decimal("9.98"),
        "ttc": Decimal("114.98"),
    }


def test_ht_depuis_ttc_zero():
    assert calculer_ht_depuis_ttc(Decimal("0")) == {
        "ht": Decimal("0.00"),
        "tps": Decimal("0.00"),
        "tvq": Decimal("0.00"),
        "ttc": Decimal("0.00"),
    }


def test_ht_depuis_ttc_22_98():
    # 22.98 / 1.14975 = 19.987... -> 19.99 $.
    assert calculer_ht_depuis_ttc(Decimal("22.98")) == {
        "ht": Decimal("19.99"),
        "tps": Decimal("1.00"),
        "tvq": Decimal("1.99"),
        "ttc": Decimal("22.98"),
    }


def test_ht_depuis_ttc_correction_d_un_cent():
    # 1.20 / 1.14975 = 1.0437... -> 1.04 $, mais 1.04 + 0.05 + 0.10 = 1.19 $.
    # Le montant hors taxes est corrige a la hausse d'un cent (1.05 $) pour
    # retrouver exactement 1.20 $.
    assert calculer_ht_depuis_ttc(Decimal("1.20")) == {
        "ht": Decimal("1.05"),
        "tps": Decimal("0.05"),
        "tvq": Decimal("0.10"),
        "ttc": Decimal("1.20"),
    }


def test_ht_depuis_ttc_erreurs():
    for valeur in (Decimal("-1.00"), -1, Decimal("-0.01")):
        with pytest.raises(MontantInvalideError):
            calculer_ht_depuis_ttc(valeur)
    for valeur in ("abc", [100], None, True, False):
        with pytest.raises(MontantNonNumeriqueError):
            calculer_ht_depuis_ttc(valeur)
    with pytest.raises(ValueError):
        calculer_ht_depuis_ttc("abc")
    with pytest.raises(ValueError):
        calculer_ht_depuis_ttc(Decimal("-1.00"))
