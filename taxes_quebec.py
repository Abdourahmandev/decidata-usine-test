"""Calcul des taxes de vente du Quebec (TPS et TVQ).

Ce module fournit des fonctions de calcul de la TPS (5 %) et de la TVQ
(9,975 %) sur un montant hors taxes, avec un arrondi commercial
(Decimal, ROUND_HALF_UP) a deux decimales.

Les montants acceptes sont les nombres entiers (int), les nombres a
virgule flottante (float) et les Decimal. Tout autre type, de meme que
tout montant negatif, leve une erreur explicite.
"""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

__all__ = [
    "TAUX_TPS",
    "TAUX_TVQ",
    "MontantInvalideError",
    "TypeMontantInvalideError",
    "calculer_tps",
    "calculer_tvq",
    "calculer_total",
]

TAUX_TPS = Decimal("0.05")
TAUX_TVQ = Decimal("0.09975")

_DEUX_DECIMALES = Decimal("0.01")


class MontantInvalideError(ValueError):
    """Levee lorsqu'un montant hors taxes est negatif."""


class TypeMontantInvalideError(TypeError):
    """Levee lorsqu'un montant hors taxes n'est pas un nombre."""


def _vers_decimal(montant):
    """Convertit un montant valide en Decimal.

    Leve :class:`TypeMontantInvalideError` si le type n'est pas numerique.
    """
    if isinstance(montant, bool):
        raise TypeMontantInvalideError(
            "Montant invalide : un booleen n'est pas un montant."
        )
    if isinstance(montant, Decimal):
        return montant
    if isinstance(montant, int):
        return Decimal(montant)
    if isinstance(montant, float):
        return Decimal(str(montant))
    raise TypeMontantInvalideError(
        "Montant invalide : type %r non numerique." % type(montant).__name__
    )


def _valider_montant(montant):
    """Valide un montant hors taxes et retourne son Decimal.

    Leve :class:`MontantInvalideError` si le montant est negatif.
    """
    valeur = _vers_decimal(montant)
    if valeur < 0:
        raise MontantInvalideError(
            "Montant invalide : %s est negatif." % valeur
        )
    return valeur


def _arrondir(valeur):
    """Arrondit un Decimal au cent avec l'arrondi commercial (HALF_UP)."""
    return valeur.quantize(_DEUX_DECIMALES, rounding=ROUND_HALF_UP)


def calculer_tps(montant_ht):
    """Retourne la TPS (5 %) arrondie au cent sur le montant hors taxes."""
    return _arrondir(_valider_montant(montant_ht) * TAUX_TPS)


def calculer_tvq(montant_ht):
    """Retourne la TVQ (9,975 %) arrondie au cent sur le montant hors taxes."""
    return _arrondir(_valider_montant(montant_ht) * TAUX_TVQ)


def calculer_total(montant_ht):
    """Retourne le total (montant + TPS + TVQ) arrondi au cent."""
    montant = _valider_montant(montant_ht)
    tps = _arrondir(montant * TAUX_TPS)
    tvq = _arrondir(montant * TAUX_TVQ)
    return _arrondir(montant + tps + tvq)
