import random
from aqt import gui_hooks
from aqt.qt import QFontDatabase

def prepare(html, card, context):
    qf = QFontDatabase()
    thefont = random.choice(qf.families(QFontDatabase.Japanese))
    return html + '''
    <script>
        el = document.getElementsByClassName("randomfont")
        for(var i = 0; i < el.length; i++) {
            el[i].style.fontFamily = "''' + thefont + '''";
        }
    </script>
    '''
    
gui_hooks.card_will_show.append(prepare)
