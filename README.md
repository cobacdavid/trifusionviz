# trifusionviz

## Usage

``` python
import trifusionviz as tfv
import random

liste = list(range(13))
random.shuffle(liste)

t = tfv.trifusionviz(liste)
# sortie pdf
t.sortie("exemple_sortie")

u = tfv.trifusionviz(liste)
u.fonction_ordre = lambda x, y: str(x) < str(y)
# sortie png
u.sortie("exemple_sortie_lexico", "png")

```

## Licence
CC-BY-NC-SA
