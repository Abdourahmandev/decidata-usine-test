"""Calcul des taxes de vente du Quebec (TPS et TVQ).

Ce module fournit deux fonctions :

- :func:`calculer_taxes`, qui calcule la TPS (5 %) et la TVQ (9,975 %)
  sur un montant hors taxes ;
- :func:`calculer_ht_depuis_ttc`, qui retrouve le montant hors taxes a
  partir d'un montant toutes taxes comprises.

Les montants sont calcules en Decimal et arrondis au cent (2 decimales)
avec l'arrondi commercial (ROUND_HALF_UP).

Les montants acceptes sont les nombres entiers (int), les nombres a
virgule flottante (float) et les Decimal. Tout autre type, de meme que
tout montant negatif, leve une erreur explicite.
"""

from decimal import Decimal, ROUND_HALF_UP

__all__ = [
    "TAUX_TPS",
    "TAUX_TVQ",
    "MontantInvalideError",
    "MontantNonNumeriqueError",
    "calculer_taxes",
    "calculer_ht_depuis_ttc",
]

TAUX_TPS = Decimal("0.05")
TAUX_TVQ = Decimal("0.09975")

_FACTEUR_TTC = Decimal("1") + TAUX_TPS + TAUX_TVQ  # 1,14975

_DEUX_DECIMALES = Decimal("0.01")


class MontantInvalideError(ValueError):
    """Levee lorsqu'un montant hors taxes est negatif."""


class MontantNonNumeriqueError(ValueError):
    """Levee lorsqu'un montant hors taxes n'est pas un nombre."""


def _vers_decimal(montant):
    """Convertit un montant valide en Decimal.

    Leve :class:`MontantNonNumeriqueError` si le type n'est pas numerique.
    """
    if isinstance(montant, bool):
        raise MontantNonNumeriqueError(
            "Montant invalide : un booleen n'est pas un montant."
        )
    if isinstance(montant, Decimal):
        return montant
    if isinstance(montant, int):
        return Decimal(montant)
    if isinstance(montant, float):
        return Decimal(str(montant))
    raise MontantNonNumeriqueError(
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


def calculer_taxes(montant_ht):
    """Calcule la TPS, la TVQ et le total sur un montant hors taxes.

    Retourne un dictionnaire dont les valeurs sont des :class:`Decimal`
    arrondis au cent avec l'arrondi commercial (ROUND_HALF_UP) :

        {
            "ht":  montant hors taxes arrondi au cent,
            "tps": TPS (5 %) arrondie au cent,
            "tvq": TVQ (9,975 %) arrondie au cent,
            "ttc": montant + TPS + TVQ, arrondi au cent,
        }

    Leve :class:`MontantInvalideError` si le montant est negatif, et
    :class:`MontantNonNumeriqueError` (sous-classe de :class:`ValueError`)
    si le montant n'est pas numerique.
    """
    montant = _arrondir(_valider_montant(montant_ht))
    tps = _arrondir(montant * TAUX_TPS)
    tvq = _arrondir(montant * TAUX_TVQ)
    ttc = _arrondir(montant + tps + tvq)
    return {
        "ht": montant,
        "tps": tps,
        "tvq": tvq,
        "ttc": ttc,
    }


def calculer_ht_depuis_ttc(montant_ttc):
    """Retrouve le montant hors taxes a partir d'un montant TTC.

    Le montant hors taxes est d'abord calcule en divisant le montant TTC
    par le facteur combine TPS + TVQ (1,14975), puis arrondi au cent
    (ROUND_HALF_UP). La TPS et la TVQ sont ensuite recalculees sur ce
    montant avec :func:`calculer_taxes`.

    Si, a cause des arrondis, la somme ``ht + tps + tvq`` differe du
    montant TTC d'un cent, le montant hors taxes est corrige d'un cent
    pour que le total retrouve exactement le montant TTC fourni.

    Retourne le meme dictionnaire ``{"ht", "tps", "tvq", "ttc"}`` que
    :func:`calculer_taxes`, avec des :class:`Decimal` arrondis au cent.

    Leve les memes erreurs que :func:`calculer_taxes` :
    :class:`MontantInvalideError` si le montant est negatif, et
    :class:`MontantNonNumeriqueError` (sous-classe de :class:`ValueError`)
    si le montant n'est pas numerique.
    """
    montant = _arrondir(_valider_montant(montant_ttc))
    ht = _arrondir(montant / _FACTEUR_TTC)
    resultat = calculer_taxes(ht)
    somme = resultat["ht"] + resultat["tps"] + resultat["tvq"]
    if somme != montant:
        if somme < montant:
            ht = ht + _DEUX_DECIMALES
        else:
            ht = ht - _DEUX_DECIMALES
        resultat = calculer_taxes(ht)
    return resultat
