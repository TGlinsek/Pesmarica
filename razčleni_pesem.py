from preberi_akorde import uredi


def vrni_dele_pesmi(niz):
    # sprejme en niz samih akordov
    # najde največji kos, ki se ponovi
    # razdeli pesem glede na ta kos

    urejene_vrstice = uredi(niz)

    max_stevec = 0
    max_kitica = None
    for i, x in enumerate(urejene_vrstice):
        for j, y in enumerate(urejene_vrstice):
            if j <= i:
                continue
            i_ = i
            j_ = j
            # x_ = x
            # y_ = y
            stevec = 0
            while True:
                if i_ == j or j_ >= len(urejene_vrstice):
                    break
                x_ = urejene_vrstice[i_]
                y_ = urejene_vrstice[j_]
                if x_ == y_ != []:  # prazne vrstice naj pomenijo, da je to break med kiticami oz. med kitico in refrenom
                    stevec += 1
                    i_ += 1
                    j_ += 1
                    continue
                else:
                    break
            if stevec > max_stevec:
                max_kitica = urejene_vrstice[i:i_]
            max_stevec = max(max_stevec, stevec)
    refren = max_kitica
    return refren
