def razdeli_vrstico(niz):
    akordi = []
    akord = ""
    for h, i in enumerate(niz):
        if i != " " and i != "\t":  # tt tab je sam za zlo redke edge case, ampak lj, zaka pa ne
            if len(akord) >= 3:
                j = i.lower()
                if i.isdigit() or j in "ijklmnopqrsštuvwxyzž" or (j == "a" and akord[-1] == "m"):
                    pass
                else:
                    akordi.append((akord, h - len(akord)))  # drugi člen je samo indeks, kjer se je niz začel
                    akord = ""
            """
            elif len(akord) == 1:  # tu ni >= 1, ker drugače bi se "cmaj7" spremenil v "cm" in "aj7"
                j = i.lower()
                if j in "abcdefgh":
                    akordi.append(akord)
                    akord = ""
            """  # to je zato, da recimo loči niz "Cfis" v "c" in "fis"
            akord += i
        else:
            if akord != "":
                akordi.append((akord, h - len(akord)))
                akord = ""
    akordi += [(akord, len(niz) - len(akord))] * (len(akord) > 0)
    return akordi

"""
primeri = [
    "C    d   ",
    "D    C",
    "Fis    D",
    "fisis   d",
    "fiSDUR   CMAJ7CMOL",
    "fis7cfisfsf3f3f3",
    "fis7cdur  fisC"
]

pravi_primeri = [
    " C    d   ",
    "C    d",
    "Cmaj7  D7  A",
    "FisD   A G",
    "F d fismaj7A7",
    "" 
]
"""


tonalitete = {
    "c" : 0,
    "des" : 1,
    "cis" : 1,
    "d" : 2,
    "dis" : 3,
    "es" : 3,
    "e" : 4,
    "f" : 5,
    "ges" : 6,
    "fis" : 6,
    "g" : 7,
    "gis" : 8,
    "as" : 8,
    "a" : 9,
    "ais" : 10,
    "b" : 10,
    "h" : 11
}

obrnjen_slovar = {v: k for k, v in tonalitete.items()}


def transponiraj(akord, offset=0):  # 0 pomeni, da se nič ne spremeni
    # akord je lahko ali dur ali mol, odvisno od kapitalizacije, ki jo ta funkcija ohranja
    if len(akord) == 0:
        return ""
    dur = akord[0].upper() == akord[0]
    star = tonalitete[akord.lower()]
    nov = (star + offset) % 12
    nov_akord = obrnjen_slovar[nov]
    if dur:
        return nov_akord[0].upper() + nov_akord[1:]
    return nov_akord


def spremenjeni(akordi, razlika):
    # razlika je število poltonov, za kolikor gremo višje

    novi_akordi = []
    
    for akord, indeks in akordi:
        glava = ""
        koren = ""
        kontrola = False
        
        for i in akord:
            if i.lower() in "abcdefgh" and not kontrola:
                glava += i
            else:
                kontrola = True
                koren += i
        # print("glava: '" + glava + "'")
        # print("koren: '" + koren + "'")
        
        novi_akordi.append(
            (
                transponiraj(glava, offset=razlika) + koren, 
                indeks
            )
        )
        
    return novi_akordi
        

        
def spremeni_niz(niz, razlika):
    # razlika je število poltonov, za kolikor gremo višje

    nizi = niz.split("\n")

    nova_pesem = ""
    
    if nizi == []:
        return nova_pesem

    akordi = nizi.pop(0).rstrip()  # predvsem da se znebimo \n-ja
    if len(nizi) == 1:
        besedilo = ""
    else:
        besedilo = nizi.pop(0).strip()
    
    while True:
        vrstica = ""
        try:
            seznam = spremenjeni(razdeli_vrstico(akordi), razlika)
        except:
            raise Exception("Preveri, da so lihe vrstice akordi, sode pa besedilo!")
        
        i = 0
        j = 0
        while True:
            if i >= len(seznam):
                break
            akord, položaj = seznam[i]
            """
            if j == 0:
                print(1)
                vrstica += položaj * " "
            """
            if položaj == j:
                vrstica = (vrstica + " " * j)[:j]
                vrstica += akord
                i += 1
            
            j += 1
        
        nova_pesem += vrstica + "\n"
        nova_pesem += besedilo + "\n"
        
        if nizi == []:  # oz. len(nizi) == 0
            break

        akordi = nizi.pop(0).rstrip()
        if len(nizi) == 1:
            besedilo = ""
        else:
            besedilo = nizi.pop(0).strip()
    
    nova_pesem = nova_pesem[:-1]
    return nova_pesem


