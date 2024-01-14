from transponiraj import razdeli_vrstico


def preberi_akorde_iz_pesmi(niz):
    # vrne vrstice z akordi
    # prazne vrstice vključene
    # prazni stringi pomenijo, da se akord začne z zadnjim akordom prejšnje vrstice

    nizi = niz.split("\n")

    nova_pesem = []
    
    if nizi == []:
        return nova_pesem

    akordi = nizi.pop(0).rstrip()  # predvsem da se znebimo \n-ja
    if len(nizi) == 0:
        pass
    else:
        nizi.pop(0).strip()
    
    while True:
        vrstica = []
        try:
            seznam = razdeli_vrstico(akordi)
        except:
            raise Exception("Preveri, da so lihe vrstice akordi, sode pa besedilo!")
        
        i = 0
        j = 0
        while True:
            if i >= len(seznam):
                break
            akord, položaj = seznam[i]
            if položaj != 0 and i == 0:  # položaj gledamo, pač a se vrstica akordov začne z novim akordom al ne (potem vzamemo starega)
                vrstica += [""]
            vrstica += [akord]
            i += 1
        
            j += 1
        
        nova_pesem.append(vrstica)
        
        if nizi == []:
            break

        akordi = nizi.pop(0).rstrip()
        if len(nizi) == 0:
            pass
        else:
            nizi.pop(0).strip()
    
    # nova_pesem = nova_pesem[:-1]
    if nova_pesem[-1] == []:
        nova_pesem = nova_pesem[:-1]
    return nova_pesem


def uredi_akorde(akordi):
    # sprejme seznam s stringi, vsaka je en akord
    
    novi_akordi = []
    aux = ""
    for a in akordi:
        if a[0] == "(":
            aux += a
            if a[-1] == ")":  # v primeru, da sta uklepaj in zaklepaj v istem akordu (se lahko zgodi, čeprav bi raje, da se to ne more. But it's fine)
                novi_akordi += [aux]    
                aux = ""
        elif a[-1] == ")":
            aux += a
            novi_akordi += [aux]
            aux = ""
        elif aux != "":
            aux += a
        else:
            novi_akordi += [a]
    assert aux == ""  # nezaprt zaklepaj v akordih
    akordi = novi_akordi

    if len(akordi) == 3:
        akordi = [akordi[0]] + akordi
    elif len(akordi) == 5:
        akordi = sum([[i, i] for i in akordi[:3]], []) + akordi[3:]
    return akordi


def uredi_vrstice(vrstice):
    # sprejme seznam seznamov
    # notranji seznami imajo za elemente stringe, vsak predstavlja en akord
    
    # uredi vrstice akordov
    prejšnja = None
    vrste = []
    for vrsta in vrstice:
        # prazne vrstice pustimo prazne zaenkrat. Ne bomo akorda iz prejšnje vrstice jemali.
        if len(vrsta) > 0 and vrsta[0] == "":  # če je prvi akord prazen
            vrsta[0] = prejšnja[-1]
        vrste.append(v := uredi_akorde(vrsta))
        prejšnja = v
    return vrste


def uredi(niz):
    return uredi_vrstice(preberi_akorde_iz_pesmi(niz))


# TODO: naredi, da se enharmonični toni smatrajo kot isti ton, ko primerjamo enakost vrstic akordov
