var razdeli_vrstico = function(niz) {
    var akordi = [];
    var akord = "";
    for (var h = 0; h < niz.length; h++) {
        var i = niz[h];
        if (i !== " " && i !== "\t") {  // tt tab je sam za zlo redke edge case, ampak lj, zaka pa ne
            if (akord.length >= 3) {
                j = i.toLowerCase();
                if (("0".charCodeAt() <= i.charCodeAt() && i.charCodeAt() <= "9".charCodeAt()) || "ijklmnopqrsštuvwxyzž".includes(j) || (j === "a" && akord[akord.length - 1] === "m")) {
                    
                }
                else {
                    akordi.push([akord, h - akord.length]);  // drugi člen je samo indeks, kjer se je niz začel
                    akord = "";
                }
            }
            // /*
            else if (akord.length === 1) {  // tu ni >= 1, ker drugače bi se "cmaj7" spremenil v "cm" in "aj7"
                j = i.toLowerCase();
                if ("abcdefgh".includes(j)) {
                    akordi.push([akord, h - akord.length]);
                    akord = "";
                }
            }
            // */  // to je zato, da recimo loči niz "Cfis" v "c" in "fis"
            akord += i;
        } else {
            if (akord !== "") {
                akordi.push([akord, h - akord.length]);
                akord = "";
            }
        }
    }
    if (akord.length > 0) {
        akordi.push([akord, niz.length - akord.length]);
    }
    return akordi;
};

/*
var primeri = [
    "C    d   ",
    "D    C",
    "Fis    D",
    "fisis   d",
    "fiSDUR   CMAJ7CMOL",
    "fis7cfisfisf3f3f3",
    "fis7cdur  fisC"
];

var pravi_primeri = [
    " C    d   ",
    "C    d",
    "Cmaj7  D7  A",
    "FisD   A G",
    "F d fismaj7A7",
    "(H, C, D)",
    "((H, C, D))",
    "" 
];


for (var i = 0; i < pravi_primeri.length; i++) {
    console.log(razdeli_vrstico(pravi_primeri[i]));
}
*/

var tonalitete = {
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
};

// var obrnjen_slovar = {v: k for k, v in tonalitete.items()};
var obrnjen_slovar = ["c", "cis", "d", "es", "e", "f", "fis", "g", "as", "a", "b", "h"];

var transponiraj = function(akord, offset=0) {  // 0 pomeni, da se nič ne spremeni
    // akord je lahko ali dur ali mol, odvisno od kapitalizacije, ki jo ta funkcija ohranja
    if (akord.length === 0) {
        return "";
    }
    var dur = akord[0].toUpperCase() === akord[0];
    var star = tonalitete[akord.toLowerCase()];
    var nov = ((star + offset) % 12 + 12) % 12;
    var nov_akord = obrnjen_slovar[nov];
    if (dur) {
        return nov_akord[0].toUpperCase() + nov_akord.slice(1);
    }
    return nov_akord;
};


var spremenjeni = function(akordi, razlika) {
    // razlika je število poltonov, za kolikor gremo višje

    var novi_akordi = [];
    
    for (var j = 0; j < akordi.length; j++) {
        var akord = akordi[j][0];
        var indeks = akordi[j][1];

        var glava = "";
        var koren = "";
        var predglava = "";
        var kontrola = false;
        var kontrola2 = false;
        
        for (var k = 0; k < akord.length; k++) {
            var i = akord[k];
            if ("abcdefghis".includes(i.toLowerCase()) && !kontrola) {
                glava += i;
                kontrola2 = true;
                if (i === "s") {  // tu je konec akorda, naprej so sam številke, al pa "maj" oz. podobno
                    kontrola = true;
                }
            } else {
                if (!("abcdefghijklmnopqrstuvwxyz0123456789".includes(i.toLowerCase())) && !kontrola2) {
                    predglava += i;
                }
                else {
                    kontrola = true;
                    koren += i;
                }
            }
        }
        // console.log("glava: '" + glava + "'");
        // console.log("koren: '" + koren + "'");
        
        novi_akordi.push(
            [
                predglava + transponiraj(glava, offset=razlika) + koren, 
                indeks
            ]
        );
    }
    return novi_akordi;
};

        
var spremeni_niz = function(niz, razlika) {
    // razlika je število poltonov, za kolikor gremo višje

    var nizi = niz.split("\n");

    var nova_pesem = "";
    
    if (nizi.length === 0) {
        return nova_pesem;
    }

    var akordi = nizi.shift().replace(/\s+$/, '');  // predvsem da se znebimo \n-ja
    // https://stackoverflow.com/questions/37864460/javascript-remove-trailing-spaces-only

    if (nizi.length === 0) {
        var besedilo = "";
    }
    else {
        var besedilo = nizi.shift().trim();
    }

    while (true) {
        var vrstica = "";
        try {
            var seznam = spremenjeni(razdeli_vrstico(akordi), razlika);
        }
        catch {
            throw "Preveri, da so lihe vrstice akordi, sode pa besedilo!";
        }

        var i = 0;
        var j = 0;
        while (true) {
            if (i >= seznam.length) {
                break;
            }
            var akord = seznam[i][0];
            var položaj = seznam[i][1];
            /*
            if (j === 0) {
                console.log(1);
                vrstica += " ".repeat(položaj);
            }
            */
            if (položaj === j) {
                vrstica = (vrstica + " ".repeat(j)).slice(0, j);
                vrstica += akord;
                i += 1;
            }
            
            j += 1;
        }
        nova_pesem += vrstica + "\n";
        nova_pesem += besedilo + "\n";
        
        if (nizi.length === 0) {  // nizi.length === [] ne gre
            break;
        }

        akordi = nizi.shift().replace(/\s+$/, '')
        if (nizi.length === 0) {
            besedilo = "";
        }
        else {
            besedilo = nizi.shift().trim();
        }
    }
    nova_pesem = nova_pesem.slice(0, -1);
    return nova_pesem;
};

/*
for (var i = 0; i < pravi_primeri.length; i++) {
    console.log(spremenjeni(razdeli_vrstico(pravi_primeri[i]), 1));
}
*/