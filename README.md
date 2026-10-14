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
from taxes_quebec import calculer_tps, calculer_tvq, calculer_total

montant = Decimal("100")

calculer_tps(montant)    # Decimal('5.00')
calculer_tvq(montant)    # Decimal('9.98')
calculer_total(montant)  # Decimal('114.98')
```

### Erreurs

- `MontantInvalideError` (sous-classe de `ValueError`) : montant negatif.
- `TypeMontantInvalideError` (sous-classe de `TypeError`) : montant non
  numerique (ex. chaine de caracteres, liste, `None`).

Les montants acceptes sont `int`, `float` et `Decimal`.

### Tests

```bash
pip install pytest
pytest -v
```
