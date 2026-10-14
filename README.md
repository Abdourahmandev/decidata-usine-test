# decidata-usine-test

## Module `taxes_quebec.py`

Calcul des taxes de vente du Quebec sur un montant hors taxes :

| Taxe | Taux    |
| ---- | ------- |
| TPS  | 5 %     |
| TVQ  | 9,975 % |

### Arrondi

Les montants sont calcules en `Decimal` et arrondis au cent (2 decimales)
avec l'arrondi commercial `ROUND_HALF_UP` : un demi-cent est arrondi au
cent superieur (ex. `9,975 $` devient `9,98 $`).

### Usage

```python
from decimal import Decimal
from taxes_quebec import calculer_taxes, calculer_ht_depuis_ttc

calculer_taxes(Decimal("100"))
# {
#     "ht": Decimal("100.00"),
#     "tps": Decimal("5.00"),
#     "tvq": Decimal("9.98"),
#     "ttc": Decimal("114.98"),
# }

calculer_ht_depuis_ttc(Decimal("114.98"))
# {
#     "ht": Decimal("100.00"),
#     "tps": Decimal("5.00"),
#     "tvq": Decimal("9.98"),
#     "ttc": Decimal("114.98"),
# }
```

`calculer_taxes` retourne un dictionnaire dont les valeurs sont des
`Decimal` arrondis au cent : `ht` (montant hors taxes), `tps`, `tvq` et
`ttc` (total = montant + TPS + TVQ).

`calculer_ht_depuis_ttc` retrouve le montant hors taxes a partir d'un
montant TTC : il divise le montant par le facteur combine TPS + TVQ
(`1,14975`), arrondit au cent, puis recalcule la TPS et la TVQ avec
`calculer_taxes`. Si la somme `ht + tps + tvq` differe du montant TTC d'un
cent a cause des arrondis, le montant hors taxes est corrige d'un cent
pour que le total corresponde exactement au montant TTC fourni. La
fonction retourne le meme dictionnaire que `calculer_taxes`.

### Erreurs

- `MontantInvalideError` (sous-classe de `ValueError`) : montant negatif.
- `MontantNonNumeriqueError` (sous-classe de `ValueError`) : montant non
  numerique (ex. chaine de caracteres, liste, `None`, booleen).

Les montants acceptes sont `int`, `float` et `Decimal`.

### Tests

```bash
pip install pytest
python -m pytest -v
```
