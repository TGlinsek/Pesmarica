import os
from preberi_akorde import uredi
from razčleni_pesem import vrni_dele_pesmi


dir_path = os.path.dirname(os.path.realpath(__file__))

naslov = "Hazard - Vsak je sam"

with open(dir_path + f"\\pesmi\\{naslov}.txt", encoding="utf-8") as f:
    vrstice = f.readlines()

vrstice = vrstice[vrstice.index("\n"):]
while True:
    if vrstice[0] == "\n":
        vrstice = vrstice[1:]
    else:
        break


akordi = vrstice[::2]
niz = "\n".join(akordi)

print(uredi(niz))
print(vrni_dele_pesmi(niz))
