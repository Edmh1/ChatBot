from difflib import SequenceMatcher

oracion1 = "hola"
oracion2 = "buenos dias"

## C = coincidencias
## T = Total = oracion1 + oracion 2 (incluyendo espacios)
## Relacion = 2C/T
relacion = SequenceMatcher(None, oracion1, oracion2).ratio()
print(f"la relacion es de: {relacion}") 