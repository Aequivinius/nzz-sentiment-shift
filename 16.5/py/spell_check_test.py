# -*- coding: utf-8 -*-
import xml.etree.ElementTree as et
import re
import enchant
from enchant.checker import SpellChecker
text = u' Weil Feuerbach heimlehrte von seinen Ausfl\xfcgen in die Campagna, und ebenso, wenn er nachdenklich durch die Vanne der vatikanischen Sammlungen !,e wandelt und langsam, die m\xe4chtigen Eindr\xfccke w\xe4gend und vergleichend, seinem bescheidenen Melier ugcckiritten war, ordneten sich in feiner Phantasie die regeln\xfc\xdfiaen, nicht etwa theatralisch gelegten, sondern durch die ernste Pose des antiken Menschen gegebenen, majest\xe4tisch herabfallenden, lichten Gl wander und Ueberni\xfcrfe. In ihrer Vornehmheit ud Ruhe, die an die Sch\xf6nheit klassischer Statuen er innert, treffen wir sie wieder auf dem meisterlichen Vilde des Orstheu und der Eurydike, in der ergrei sende Hoheit der Stuttgarter Iphigenie, der Plato nisch neinnsiiatcn Lebensheilerleit des Gastmahle. Es ist die aus tiefstem Innerlichem Verh\xe4ltnis er kl\xe4rte Vergeistigung der Natur, dl durch die Gluten de pers\xf6nlichen Temperament gel\xe4utert, under sa,l im Rhythmus de antil.llasstsch Sch\xf6nen  schaute Wirklichkeit und Wahrheit, dl un in, wl Anselm Fe,ieU,ich entgegen!!. '

#spell checking
chkr = SpellChecker("de_CH",text)
Nerr = 0
for err in chkr:
    Nerr += 1
    repl = ''
    repl = err.suggest()
    try:
        err.replace(repl[0])
    except:
        err.replace('Error')

    newtext = err.get_text()