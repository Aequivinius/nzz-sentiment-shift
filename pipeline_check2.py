# -*- coding: utf-8 -*-
import xml.etree.ElementTree as et
import re
import enchant
from enchant.checker import SpellChecker

#filename = "/Users/Simon/UNI VII/bigdata/nzz/NZZ_1910_1920-with-uuid/1910-01/JM20121222000301997.xml"
filename = "/Users/tabris/Downloads/NZZ_1910_1920-with-uuid/1910-08/JM20121222000281742.xml"

clist = []
craw = []
letter_ratio = []
error_ratio = []
lengths = []
oldtext = u' Weil Feuerbach heimlehrte von seinen Ausfl\xfcgen in die Campagna, und ebenso, wenn er nachdenklich durch die Vanne der vatikanischen Sammlungen !,e wandelt und langsam, die m\xe4chtigen Eindr\xfccke w\xe4gend und vergleichend, seinem bescheidenen Melier ugcckiritten war, ordneten sich in feiner Phantasie die regeln\xfc\xdfiaen, nicht etwa theatralisch gelegten, sondern durch die ernste Pose des antiken Menschen gegebenen, majest\xe4tisch herabfallenden, lichten Gl wander und Ueberni\xfcrfe. In ihrer Vornehmheit ud Ruhe, die an die Sch\xf6nheit klassischer Statuen er innert, treffen wir sie wieder auf dem meisterlichen Vilde des Orstheu und der Eurydike, in der ergrei sende Hoheit der Stuttgarter Iphigenie, der Plato nisch neinnsiiatcn Lebensheilerleit des Gastmahle. Es ist die aus tiefstem Innerlichem Verh\xe4ltnis er kl\xe4rte Vergeistigung der Natur, dl durch die Gluten de pers\xf6nlichen Temperament gel\xe4utert, under sa,l im Rhythmus de antil.llasstsch Sch\xf6nen  schaute Wirklichkeit und Wahrheit, dl un in, wl Anselm Fe,ieU,ich entgegen!!. '
alttext = u' II. II. Da dieses Thema schon fr\xfcher \xf6ffent\xbb \xbbich be\'.mndclt \xbbnorden ist, wobei recht widersvre\xbb . Ansichten zum Vorschein kamen, so d\xfcrfte die Lcser interessieren, etwas eingebender zu .,\'rnci\xfciie!!, zu welchen Veschliissen die kantonale ^erzie-Gesellschaft gekonuneu ist. Zum bessern l\'rslni\'.dins mag kurz wiederholt werden, dafz ^ie arge Ucberb\xfcrdiiug der Medizinstudenten -\'.,\'tcht. das; neue wichtige Kapitel in das iiber- ^os^c Pensum an genommen werden sollten und \xe4s; dies N\'om\xf6<;ilich geschehen sollte ohne Ver^ \'"ncierii\xfcg des ZtudiuuiB. Der Versammlung l l\'irn einzelne Thesen von Dr. Kaufmann vor, \' .lch? in einleitendem Votum begr\xfcndet >;vur\xab >;n, 3ci\xbbe Antrage gingen in der Hauptsache ^bi,!: 1. T>;a3 prop\xe4deutische Studium durch ^in\'i^\'N\xfcn des Obligatoriums von Botanik, Irr! \',,!l>; und vergleichender Anatomie zu entla\xbb !i,\'i!, so d!ih es in Zukunft wieder in vier anstalt in f\xfcnf semestern absolviert werden k\xf6nnte. \'.\'. die Unfallmedizin als neues Unterrichts\' und \'^!\',"!fmi\'\'?fach aufzunehmen, welche Mehrbe\xbb asiiinss dis Fachstudium bei einer Dauer von such\xbb? 3\',\',!!?steril ertragen k\xf6nnte, fofern die v^vgeschli\'iiencn V^rbrsserungcn, wi? \'^ernuut^ru\xfcg der Studentenzahl, Verteilung tvs i\xfcniscke\xbb Nnterrickns wom\xf6glich auf je -,\'vei .<;Ni,iiken (vrov\xe4deulische und Hauptklinik), anaeuomineu w\xfcrde!,. Dann k\xf6nnte anch das !\'ou linderer Seite in ?lu?s!cht genommene prak- tische ^l,r fassen gelassen werden. '

for i in range(0,1):
    #use either of the rawtext definitions for pipeline check
    #rawtext = oldtext
    rawtext = oldtext
    text = rawtext
    
    #check string length
    txlen = len(text)
    lengths.append(txlen)
    if txlen < 1000:
        clist.append('length')
        #continue
       
    #check for string size to amount of letters ratio  
    Nchar = 0
    for char in text:
        if char.isalpha() == True or char == u" ":
            Nchar += 1
    lr = Nchar/ float(txlen)
    letter_ratio.append(lr)     
    if lr < 0.7:
        clist.append('letter_ratio')
        continue
    
    #remove all special characters apart from characterset below    
    text = re.sub('[^A-Za-z0-9.,!?\s\\xf6\\xfc\\xe4\\xdf]', '', text)
    
    #remove all special characters apart from characterset below    
    text2 = re.sub('[^A-Za-z0-9.,!?\s\\xf6\\xfc\\xe4\\xdf]', '', text)
    
    ##spell checking
    chkr = SpellChecker("de_CH",text)
    Nerr = 0
    for err in chkr:
        Nerr += 1
        repl = err.suggest()
        try:
            err.replace(repl[0])
        except:
            repl = [u""]
            err.replace(u"wort_das_der_spellchecker_nicht_kennt")
        
        # pesky bug in enchant, where the remainder of a corrected word being the same as it's own replacement
        # will cause trouble
        if len(err.word) > len(repl[0]):
            l = err.word[len(repl[0]):].lower()
            r = chkr.suggest(err.word[len(repl[0]):])
            
            if (len(r) > 0) and (l == r[0].lower()):
                err.replace(u"wort_das_dem_spellchecker_aerger_macht")
                
        if len(err.word) == 2 and len(repl[0]) == 2:
            err.replace(u"wort_das_dem_spellchecker_aerger_macht")
    text = chkr.get_text()  
    
    #check error ratio
    Nwords = text.count(' ')
    try:
        er = Nerr/float(Nwords)  
    except:
        er = 0 
    error_ratio.append(er)
    if er > 0.7:
        clist.append('error_ratio')
        continue

#compare processing        
print "before ", rawtext
print "after  ", text
print "alt    ", text2