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
from taxes_quebec import calculer_taxes

calculer_taxes(Decimal("100"))
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
