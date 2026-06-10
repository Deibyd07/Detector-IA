"""
Rule-based humanizer — no API key required.
Supports English (EN) and Spanish (ES) with auto-detection.

Transformation pipeline (aggressive → balanced → subtle):
  1. AI-phrase removal & formal-word substitution
  2. Contraction injection (EN)
  3. Informal sentence starters (~25-30% of sentences)
  4. Personal-voice hedge injection
  5. Extreme sentence splitting (burstiness)
  6. Punch sentence insertion (very short sentences)
  7. Cleanup
"""
import re

from app.models.schemas import HumanizeResponse

try:
    from nltk.tokenize import sent_tokenize as _nltk_sent
    def sent_tokenize(text: str, lang: str = "en") -> list[str]:
        try:
            locale = "spanish" if lang == "es" else "english"
            return _nltk_sent(text, language=locale)
        except Exception:
            return re.split(r"(?<=[.!?])\s+", text)
except ImportError:
    def sent_tokenize(text: str, lang: str = "en") -> list[str]:  # type: ignore[misc]
        return re.split(r"(?<=[.!?])\s+", text)


# ===========================================================================
# ENGLISH DATA
# ===========================================================================

_CONTRACTIONS_EN: list[tuple[str, str]] = [
    ("cannot", "can't"), ("will not", "won't"), ("shall not", "shan't"),
    ("do not", "don't"), ("does not", "doesn't"), ("did not", "didn't"),
    ("would not", "wouldn't"), ("could not", "couldn't"), ("should not", "shouldn't"),
    ("is not", "isn't"), ("are not", "aren't"), ("was not", "wasn't"),
    ("were not", "weren't"), ("have not", "haven't"), ("has not", "hasn't"),
    ("had not", "hadn't"),
    ("I am", "I'm"), ("I have", "I've"), ("I will", "I'll"), ("I would", "I'd"),
    ("you are", "you're"), ("you have", "you've"), ("you will", "you'll"),
    ("you would", "you'd"), ("he is", "he's"), ("she is", "she's"),
    ("it is", "it's"), ("it will", "it'll"), ("it would", "it'd"),
    ("we are", "we're"), ("we have", "we've"), ("we will", "we'll"), ("we would", "we'd"),
    ("they are", "they're"), ("they have", "they've"), ("they will", "they'll"),
    ("they would", "they'd"), ("that is", "that's"), ("that will", "that'll"),
    ("there is", "there's"), ("let us", "let's"), ("who is", "who's"),
    ("what is", "what's"), ("how is", "how's"), ("where is", "where's"),
]

_AI_REPLACEMENTS_EN: list[tuple[str, str]] = [
    # Remove epistemic filler
    ("it's worth noting that ", ""), ("it is worth noting that ", ""),
    ("it's worth noting, ", ""), ("it is worth noting, ", ""),
    ("it's worth noting ", ""), ("it is worth noting ", ""),
    ("it's important to note that ", ""), ("it is important to note that ", ""),
    ("it's important to note, ", ""), ("it is important to note, ", ""),
    ("it's important to note ", ""), ("it is important to note ", ""),
    ("it goes without saying that ", ""), ("it goes without saying ", ""),
    ("needless to say, ", ""), ("needless to say ", ""),
    ("suffice it to say, ", ""), ("suffice it to say ", ""),
    ("rest assured, ", ""), ("rest assured ", ""),
    ("it should be noted that ", ""), ("it should be noted ", ""),
    ("it bears mentioning that ", ""), ("it bears mentioning ", ""),
    ("it cannot be overstated that ", ""), ("it cannot be overstated ", ""),
    ("as previously mentioned, ", ""), ("as previously mentioned ", ""),
    ("as mentioned above, ", ""), ("as mentioned above ", ""),
    ("as mentioned earlier, ", ""), ("as mentioned earlier ", ""),
    ("as noted above, ", ""), ("as noted above ", ""),
    ("as discussed above, ", ""), ("as discussed above ", ""),
    ("one must keep in mind that ", ""), ("keep in mind that ", ""),
    ("bear in mind that ", ""),
    ("it's crucial to acknowledge that ", ""), ("it is crucial to acknowledge that ", ""),
    ("it's essential to recognize that ", ""), ("it is essential to recognize that ", ""),
    ("it is widely accepted that ", ""), ("it's widely accepted that ", ""),
    ("it is generally agreed that ", ""), ("it's generally agreed that ", ""),
    ("it is commonly known that ", ""), ("it's commonly known that ", ""),
    # Transition replacements
    ("furthermore, ", "also, "), ("furthermore ", "also "),
    ("moreover, ", "plus, "), ("moreover ", "plus "),
    ("additionally, ", "and "), ("additionally ", "and "),
    ("consequently, ", "so, "), ("consequently ", "so "),
    ("subsequently, ", "then, "), ("subsequently ", "then "),
    ("in conclusion, ", "so, "), ("in conclusion ", "so "),
    ("to summarize, ", "in short, "), ("to summarize ", "in short "),
    ("in summary, ", "in short, "), ("in summary ", "in short "),
    ("to sum up, ", "in short, "), ("to sum up ", "in short "),
    ("in closing, ", "finally, "), ("in closing ", "finally "),
    ("first and foremost, ", "first, "), ("first and foremost ", "first "),
    ("last but not least, ", "finally, "), ("last but not least ", "finally "),
    ("that being said, ", "that said, "), ("that being said ", "that said "),
    ("with that said, ", "that said, "), ("with that said ", "that said "),
    ("having said that, ", "that said, "), ("having said that ", "that said "),
    ("by and large, ", "mostly, "), ("by and large ", "mostly "),
    ("all in all, ", "overall, "), ("all in all ", "overall "),
    ("all things considered, ", "overall, "), ("all things considered ", "overall "),
    ("on the other hand, ", "but "), ("on the other hand ", "but "),
    ("by extension, ", "so, "), ("by extension ", "so "),
    ("therefore, ", "so, "), ("therefore ", "so "),
    ("hence, ", "so, "), ("hence ", "so "),
    ("thus, ", "so, "), ("thus ", "so "),
    ("as such, ", "so, "), ("as such ", "so "),
    ("nevertheless, ", "still, "), ("nevertheless ", "still "),
    ("nonetheless, ", "still, "), ("nonetheless ", "still "),
    ("in contrast, ", "but "), ("in contrast ", "but "),
    ("on the contrary, ", "but actually, "), ("on the contrary ", "but actually "),
    ("conversely, ", "but "), ("conversely ", "but "),
    ("notwithstanding, ", "that said, "), ("notwithstanding ", "that said "),
    ("henceforth, ", "from now on, "), ("henceforth ", "from now on "),
    ("in other words, ", "basically, "), ("in other words ", "basically "),
    ("to put it simply, ", "simply, "), ("to put it simply ", "simply "),
    ("to put it another way, ", "or rather, "),
    ("in essence, ", "basically, "), ("in essence ", "basically "),
    # Framing phrases
    ("in today's digital age, ", "today, "), ("in today's digital age ", "today "),
    ("in today's fast-paced world, ", "today, "), ("in today's fast-paced world ", "today "),
    ("in today's world, ", "today, "), ("in today's world ", "today "),
    ("in the modern era, ", "today, "), ("in the modern era ", "today "),
    ("in contemporary society, ", "today, "), ("in contemporary society ", "today "),
    ("in modern society, ", "today, "), ("in modern society ", "today "),
    ("in the realm of ", "in "), ("in the world of ", "in "),
    ("at its core, ", "basically, "), ("at its core ", "basically "),
    ("at the heart of ", "central to "),
    ("moving forward, ", "from here, "), ("moving forward ", "from here "),
    ("going forward, ", "from here, "), ("going forward ", "from here "),
    ("looking ahead, ", "going forward, "), ("looking ahead ", "going forward "),
    ("throughout history, ", "historically, "), ("throughout history ", "historically "),
    ("in the grand scheme of things, ", "overall, "), ("in the grand scheme of things ", "overall "),
    ("when all is said and done, ", "in the end, "), ("when all is said and done ", "in the end "),
    ("at the end of the day, ", "ultimately, "), ("at the end of the day ", "ultimately "),
    ("in the long run, ", "over time, "), ("in the long run ", "over time "),
    ("in this day and age, ", "today, "), ("in this day and age ", "today "),
    # AI exploration verbs
    ("let's delve into", "let's look at"), ("delve into", "look at"),
    ("delves into", "looks at"), ("delving into", "looking at"),
    ("a deep dive into", "a close look at"), ("deep dive into", "look at"),
    ("deep dive", "close look"), ("let's explore", "let's look at"),
    ("as we explore", "as we look at"), ("as we navigate", "as we go through"),
    ("shed light on", "explain"), ("sheds light on", "explains"),
    ("shedding light on", "explaining"),
    ("unpack this", "break this down"), ("unpack the ", "break down the "),
    ("unpack ", "break down "),
    # Certainty phrases
    ("it is clear that ", "clearly, "), ("it's clear that ", "clearly, "),
    ("it is evident that ", "clearly, "), ("it's evident that ", "clearly, "),
    ("it is safe to say ", "we can say "), ("it's safe to say ", "we can say "),
    ("without a doubt, ", "obviously, "), ("without a doubt ", "obviously "),
    ("undoubtedly, ", "no question, "), ("undoubtedly ", "no question "),
    ("there is no denying that ", "let's be honest, "),
    ("there is no denying ", "honestly "),
    ("without question, ", "of course, "), ("without question ", "of course "),
    # Role / importance
    ("plays a crucial role", "is crucial"), ("plays a pivotal role", "plays a key role"),
    ("plays an integral role", "plays a key role"), ("plays a significant role", "plays a major role"),
    ("plays an important role", "is important"), ("crucial role in", "key role in"),
    ("pivotal role in", "key role in"),
    ("of paramount importance", "really important"),
    ("of utmost importance", "really important"), ("of great importance", "very important"),
    ("highly significant", "really significant"), ("highly effective", "really effective"),
    # Redundant preposition clusters
    ("in order to ", "to "), ("due to the fact that ", "because "),
    ("in the event that ", "if "), ("at the present time, ", "now, "),
    ("at the present time ", "now "), ("at this point in time, ", "now, "),
    ("at this point in time ", "now "), ("in the near future, ", "soon, "),
    ("in the near future ", "soon "), ("for the purpose of ", "to "),
    ("with the exception of ", "except for "), ("prior to ", "before "),
    ("subsequent to ", "after "), ("in addition to ", "besides "),
    ("as a result of ", "because of "), ("with regard to ", "about "),
    ("with respect to ", "about "), ("pertaining to ", "about "),
    ("in light of ", "given "), ("in view of ", "given "),
    ("on account of ", "because of "), ("by means of ", "through "),
    ("in the absence of ", "without "), ("in accordance with ", "following "),
    ("in conjunction with ", "along with "), ("in close proximity to ", "near "),
    ("at this juncture, ", "now, "), ("at this juncture ", "now "),
    ("under these circumstances, ", "given this, "), ("under these circumstances ", "given this "),
    ("under the circumstances, ", "given this, "), ("under the circumstances ", "given this "),
    ("in the context of ", "in "), ("in terms of ", "for "),
    ("a wide range of ", "many "), ("a variety of ", "various "),
    ("a number of ", "several "), ("a large number of ", "many "),
    ("a significant number of ", "many "), ("a growing number of ", "more and more "),
    # Formal vocabulary → casual
    ("utilization", "use"), ("utilized", "used"), ("utilizes", "uses"), ("utilize", "use"),
    ("facilitate", "help"), ("facilitates", "helps"), ("facilitated", "helped"),
    ("endeavoring", "trying"), ("endeavored", "tried"), ("endeavors", "tries"),
    ("endeavor to", "try to"), ("endeavor", "try"),
    ("strive to", "try to"), ("strives to", "tries to"), ("strived to", "tried to"),
    ("commenced", "started"), ("commences", "starts"), ("commence", "start"),
    ("terminated", "ended"), ("terminates", "ends"), ("terminate", "end"),
    ("ascertain", "find out"), ("elucidate", "explain"),
    ("elucidates", "explains"), ("elucidated", "explained"),
    ("paradigm shift", "big change"), ("paradigm", "model"),
    ("holistic approach", "overall approach"), ("holistic view", "overall view"),
    ("holistic", "overall"), ("synergistic", "collaborative"), ("synergy", "teamwork"),
    ("multifaceted", "complex"), ("tapestry", "mix"),
    ("plethora of", "lots of"), ("plethora", "lots"),
    ("a myriad of", "many"), ("myriad of", "many"), ("myriad", "many"),
    ("nuanced approach", "careful approach"), ("nuanced understanding", "deeper understanding"),
    ("nuanced perspective", "thoughtful perspective"), ("nuanced", "subtle"),
    ("groundbreaking", "innovative"), ("revolutionizes", "transforms"),
    ("revolutionized", "transformed"), ("revolutionize", "transform"),
    ("cutting-edge", "latest"), ("state-of-the-art", "advanced"),
    ("seamlessly", "smoothly"), ("streamlined", "simplified"),
    ("streamlines", "simplifies"), ("streamline", "simplify"),
    ("scalable", "flexible"), ("comprehensive overview", "overview"),
    ("comprehensive guide", "guide"), ("comprehensive analysis", "full analysis"),
    ("comprehensive", "thorough"), ("leveraging ", "using "), ("leverage ", "use "),
    ("obtained ", "got "), ("obtaining ", "getting "), ("obtain ", "get "),
    ("purchased ", "bought "), ("purchase ", "buy "),
    ("requires ", "needs "), ("required ", "needed "), ("require ", "need "),
    ("possesses ", "has "), ("possessed ", "had "), ("possess ", "have "),
    ("inquired ", "asked "), ("inquires ", "asks "), ("inquire ", "ask "),
    ("demonstrates ", "shows "), ("demonstrated ", "showed "), ("demonstrate ", "show "),
    ("indicates ", "shows "), ("indicated ", "showed "), ("indicate ", "show "),
    ("illustrates ", "shows "), ("illustrated ", "showed "), ("illustrate ", "show "),
    ("comprehends ", "understands "), ("comprehended ", "understood "), ("comprehend ", "understand "),
    ("assists ", "helps "), ("assisted ", "helped "), ("assist ", "help "),
    ("provides ", "gives "), ("provided ", "gave "), ("provide ", "give "),
    ("enhances ", "improves "), ("enhanced ", "improved "), ("enhance ", "improve "),
    ("ensures ", "makes sure "), ("ensured ", "made sure "), ("ensure ", "make sure "),
    ("maintains ", "keeps "), ("maintained ", "kept "), ("maintain ", "keep "),
    ("achieves ", "reaches "), ("achieved ", "reached "), ("achieve ", "reach "),
    ("addresses ", "deals with "), ("addressed ", "dealt with "), ("address ", "deal with "),
    ("incorporates ", "includes "), ("incorporated ", "included "), ("incorporate ", "include "),
    ("establishes ", "sets up "), ("established ", "set up "), ("establish ", "set up "),
    ("generates ", "creates "), ("generated ", "created "), ("generate ", "create "),
    ("emphasizes ", "stresses "), ("emphasized ", "stressed "), ("emphasize ", "stress "),
    ("highlights ", "points out "), ("highlighted ", "pointed out "), ("highlight ", "point out "),
    ("acknowledges ", "recognizes "), ("acknowledged ", "recognized "), ("acknowledge ", "recognize "),
    ("significantly ", "a lot "), ("substantial ", "big "), ("substantially ", "a lot "),
    ("numerous ", "many "), ("sufficient ", "enough "), ("sufficiently ", "enough "),
    ("initiates ", "starts "), ("initiated ", "started "), ("initiate ", "start "),
    ("implements ", "applies "), ("implemented ", "applied "), ("implement ", "apply "),
    ("optimizes ", "improves "), ("optimized ", "improved "), ("optimize ", "improve "),
    ("maximizes ", "makes the most of "), ("maximize ", "make the most of "),
    ("prioritizes ", "focuses on "), ("prioritize ", "focus on "),
    ("concerning ", "about "), ("regarding ", "about "),
    ("mitigates ", "reduces "), ("mitigated ", "reduced "), ("mitigate ", "reduce "),
    ("alleviates ", "eases "), ("alleviated ", "eased "), ("alleviate ", "ease "),
    ("disseminates ", "shares "), ("disseminated ", "shared "), ("disseminate ", "share "),
    ("ameliorates ", "improves "), ("ameliorated ", "improved "), ("ameliorate ", "improve "),
    ("culminates in", "ends in"), ("culminated in", "ended in"), ("culminate in", "end in"),
    ("paves the way for", "makes room for"), ("paved the way for", "made room for"),
    ("pave the way for", "make room for"),
    ("very unique", "unique"), ("absolutely essential", "essential"),
    ("completely eliminate", "eliminate"), ("truly remarkable", "remarkable"),
    ("highly recommend", "recommend"), ("extremely important", "important"),
    ("very important", "important"), ("very significant", "significant"),
    ("entirely new", "new"), ("robust", "solid"),
    # Additional high-signal words
    ("fundamentally ", "deeply "), ("fundamental ", "core "),
    ("remarkable ", "impressive "), ("remarkably ", "really "),
    ("crucial ", "key "), ("crucially ", "importantly "),
    ("thoroughly ", "carefully "), ("thorough ", "careful "),
    ("stakeholders", "people involved"),
    ("harnessing ", "using "), ("harness ", "use "),
    ("empower ", "help "), ("empowers ", "helps "), ("empowered ", "helped "),
    ("innovative ", "new "), ("innovatively ", "newly "),
    ("transformative ", "powerful "), ("transformatively ", "powerfully "),
    ("unprecedented ", "new "), ("complex ", "tricky "),
    ("pivotal ", "key "), ("integral ", "key "),
    ("rigorous ", "careful "), ("rigorously ", "carefully "),
    ("substantial ", "big "), ("substantially ", "a lot "),
    ("contemporary ", "modern "), ("sophisticated ", "advanced "),
    ("streamlined ", "simplified "), ("streamline ", "simplify "),
]

# Sentence splitting: (regex, connector_word_for_part2)
_SPLIT_PATTERNS_EN: list[tuple[str, str]] = [
    (r",\s+but\s+", "But"), (r",\s+and\s+", "And"),
    (r",\s+while\s+", ""), (r",\s+which\s+", "This"),
    (r",\s+although\s+", "Although"), (r",\s+though\s+", "Though"),
    (r";\s+", ""), (r",\s+so\s+", "So"), (r",\s+yet\s+", "But"),
    (r",\s+because\s+", "Because"), (r",\s+when\s+", "When"),
    (r"\s+—\s+", ""),
]

# Personal-voice hedges
_HEDGES_EN = [
    "I think ", "I believe ", "I'd say ", "Personally, ",
    "In my view, ", "Honestly, ", "To be fair, ", "Frankly, ",
    "If you ask me, ", "Actually, ",
]

# Informal sentence starters (prepend to whole sentence)
_INFORMAL_EN = [
    "Look, ", "Here's the thing: ", "And honestly, ",
    "Thing is, ", "Worth noting: ", "To be clear: ",
    "And here's why that matters: ", "Simply put: ",
    "And this is where it gets interesting: ",
]

# Short "punch" sentences injected after long sentences
_PUNCH_EN = [
    "And that matters.", "That's the point.", "Think about it.",
    "It's that simple.", "Worth keeping in mind.",
    "That's the key part.", "And that's huge.", "Pretty wild, right?",
    "And it shows.", "Simple as that.",
]

# AI-typical openers that benefit from hedging
_HEDGEABLE_EN = {
    "the", "this", "these", "those", "it", "there", "studies",
    "research", "evidence", "data", "analysis", "such", "one",
    "many", "most", "some", "based", "according",
}

# Openers that benefit from informal starters
_FORMAL_OPENERS_EN = {
    "The", "This", "These", "Those", "It", "There",
    "Such", "One", "Many", "Most", "Some", "Based",
    "According", "Research", "Studies", "Evidence", "Data",
}


# ===========================================================================
# SPANISH DATA
# ===========================================================================

_AI_REPLACEMENTS_ES: list[tuple[str, str]] = [
    # Article+noun concordance (must come before single-word replacements)
    ("la utilización de", "el uso de"), ("la utilización", "el uso"),
    ("la implementación de", "la aplicación de"), ("la implementación", "la aplicación"),
    ("la optimización de", "la mejora de"), ("la optimización", "la mejora"),
    ("la facilitación de", "la ayuda con"), ("la facilitación", "la ayuda"),
    ("la maximización de", "el aprovechamiento máximo de"),
    # Remove epistemic filler
    ("es importante destacar que ", ""), ("es importante señalar que ", ""),
    ("es importante mencionar que ", ""), ("cabe destacar que ", ""),
    ("cabe señalar que ", ""), ("cabe mencionar que ", ""), ("cabe resaltar que ", ""),
    ("vale la pena destacar que ", ""), ("vale la pena mencionar que ", ""),
    ("vale la pena señalar que ", ""), ("resulta fundamental señalar que ", ""),
    ("resulta importante destacar que ", ""), ("resulta importante señalar que ", ""),
    ("es fundamental reconocer que ", ""), ("es crucial reconocer que ", ""),
    ("es esencial reconocer que ", ""),
    ("hay que tener en cuenta que ", ""), ("es importante tener en cuenta que ", ""),
    ("cabe tener en cuenta que ", ""), ("debemos tener en cuenta que ", ""),
    ("teniendo en cuenta lo anterior, ", ""), ("teniendo en cuenta lo anteriormente expuesto, ", ""),
    ("como se mencionó anteriormente, ", ""), ("tal como se mencionó anteriormente, ", ""),
    ("como se indicó previamente, ", ""), ("como se ha mencionado, ", ""),
    ("como se ha señalado, ", ""), ("como se mencionó antes, ", ""),
    ("en este sentido, ", ""), ("en este contexto, ", ""),
    ("en este marco, ", ""), ("en este ámbito, ", ""),
    ("de hecho, ", ""), ("en efecto, ", ""), ("efectivamente, ", ""),
    ("ciertamente, ", ""), ("indudablemente, ", ""), ("innegablemente, ", ""),
    # Transitions
    ("adicionalmente, ", "además, "), ("adicionalmente ", "además "),
    ("asimismo, ", "también, "), ("asimismo ", "también "),
    ("así como ", "y "), ("sin embargo, ", "pero "), ("sin embargo ", "pero "),
    ("no obstante, ", "pero "), ("no obstante ", "pero "),
    ("por otro lado, ", "y "), ("por otro lado ", "y "),
    ("a pesar de ello, ", "aunque "), ("a pesar de esto, ", "aunque "),
    ("a pesar de ello ", "aunque "), ("a pesar de esto ", "aunque "),
    ("por el contrario, ", "al contrario, "), ("por el contrario ", "al contrario "),
    ("en consecuencia, ", "entonces, "), ("en consecuencia ", "entonces "),
    ("por consiguiente, ", "entonces, "), ("por consiguiente ", "entonces "),
    ("en definitiva, ", "en fin, "), ("en definitiva ", "en fin "),
    ("en conclusión, ", "entonces, "), ("en conclusión ", "entonces "),
    ("para concluir, ", "para terminar, "), ("para concluir ", "para terminar "),
    ("a modo de conclusión, ", "en fin, "), ("a modo de cierre, ", "para terminar, "),
    ("en resumen, ", "en pocas palabras, "), ("en resumen ", "en pocas palabras "),
    ("para resumir, ", "en pocas palabras, "), ("para resumir ", "en pocas palabras "),
    ("en última instancia, ", "al final, "), ("en última instancia ", "al final "),
    ("a fin de cuentas, ", "al final, "), ("a fin de cuentas ", "al final "),
    ("dicho esto, ", "así que, "), ("dicho lo anterior, ", "así que, "),
    ("dado lo anterior, ", "entonces, "), ("en ese sentido, ", "así que, "),
    # Framing
    ("en el mundo actual, ", "hoy, "), ("en el mundo actual ", "hoy "),
    ("en el mundo moderno, ", "hoy, "), ("en el mundo moderno ", "hoy "),
    ("en la actualidad, ", "hoy, "), ("en la actualidad ", "hoy "),
    ("en la era digital, ", "hoy, "), ("en la era digital ", "hoy "),
    ("en la sociedad actual, ", "hoy, "), ("en la sociedad actual ", "hoy "),
    ("en la sociedad moderna, ", "hoy, "), ("en la sociedad moderna ", "hoy "),
    ("en el contexto actual, ", "hoy, "), ("en el contexto actual ", "hoy "),
    ("en el contexto contemporáneo, ", "hoy, "), ("en el contexto contemporáneo ", "hoy "),
    ("en los tiempos actuales, ", "hoy, "), ("en los tiempos actuales ", "hoy "),
    ("en estos tiempos, ", "hoy, "), ("en estos tiempos ", "hoy "),
    ("en el mundo contemporáneo, ", "hoy, "), ("en el mundo contemporáneo ", "hoy "),
    ("en la era moderna, ", "hoy, "), ("en la era moderna ", "hoy "),
    ("en los últimos tiempos, ", "recientemente, "), ("en los últimos tiempos ", "recientemente "),
    ("en los últimos años, ", "recientemente, "), ("en los últimos años ", "recientemente "),
    ("a lo largo de la historia, ", "históricamente, "), ("a lo largo de la historia ", "históricamente "),
    ("a lo largo de los años, ", "con el tiempo, "), ("a lo largo de los años ", "con el tiempo "),
    ("con el paso del tiempo, ", "con el tiempo, "), ("con el paso del tiempo ", "con el tiempo "),
    ("de cara al futuro, ", "a futuro, "), ("de cara al futuro ", "a futuro "),
    ("a largo plazo, ", "con el tiempo, "), ("a largo plazo ", "con el tiempo "),
    ("en el largo plazo, ", "con el tiempo, "), ("en el largo plazo ", "con el tiempo "),
    # AI exploration verbs
    ("vamos a explorar", "vamos a ver"), ("vamos a analizar", "vamos a ver"),
    ("vamos a profundizar en", "vamos a ver"),
    ("exploraremos", "veremos"), ("analizaremos", "veremos"),
    ("profundizaremos en", "veremos más sobre"),
    ("arrojar luz sobre", "explicar"), ("arroja luz sobre", "explica"),
    ("arrojando luz sobre", "explicando"), ("dilucidar", "explicar"),
    ("dilucida", "explica"), ("adentrarnos en", "ver"), ("adentrémonos en", "veamos"),
    # Certainty phrases
    ("es evidente que ", "claramente, "), ("resulta evidente que ", "claramente, "),
    ("está claro que ", "claramente, "), ("queda claro que ", "claramente, "),
    ("es innegable que ", "sin duda, "), ("no hay duda de que ", "sin duda, "),
    ("es indudable que ", "sin duda, "), ("es incuestionable que ", "sin duda, "),
    ("no cabe duda de que ", "sin duda, "), ("resulta obvio que ", "claramente, "),
    ("es obvio que ", "claramente, "),
    # Role / importance
    ("juega un papel crucial", "es crucial"), ("juega un papel fundamental", "es fundamental"),
    ("juega un papel importante", "es importante"), ("juega un papel esencial", "es esencial"),
    ("juega un papel clave", "es clave"), ("juega un papel central", "es central"),
    ("desempeña un papel crucial", "es crucial"), ("desempeña un papel fundamental", "es fundamental"),
    ("desempeña un papel importante", "es importante"), ("desempeña un papel esencial", "es esencial"),
    ("desempeña un papel clave", "es clave"),
    ("de suma importancia", "muy importante"), ("de vital importancia", "muy importante"),
    ("de gran importancia", "muy importante"), ("de capital importancia", "muy importante"),
    ("de primordial importancia", "muy importante"),
    # Long prepositional phrases
    ("con el objetivo de ", "para "), ("con el propósito de ", "para "),
    ("con el fin de ", "para "), ("a fin de ", "para "), ("con miras a ", "para "),
    ("por medio de ", "con "), ("a través del uso de ", "usando "),
    ("con respecto a ", "sobre "), ("con relación a ", "sobre "),
    ("en lo que respecta a ", "sobre "), ("en lo que se refiere a ", "sobre "),
    ("en términos de ", "en cuanto a "), ("en virtud de ", "debido a "),
    ("en materia de ", "en cuanto a "),
    ("una amplia gama de ", "muchos "), ("una variedad de ", "varios "),
    ("una gran cantidad de ", "muchos "), ("un gran número de ", "muchos "),
    ("un número significativo de ", "muchos "), ("un número considerable de ", "muchos "),
    ("una serie de ", "varios "),
    # Formal vocabulary → casual (with word boundaries via code)
    ("utilización", "uso"), ("utilizar", "usar"), ("utilizado", "usado"),
    ("utilizada", "usada"), ("utiliza", "usa"), ("utilizan", "usan"),
    ("facilitar", "ayudar"), ("facilita", "ayuda"), ("facilitan", "ayudan"),
    ("facilitado", "ayudado"), ("facilitada", "ayudada"),
    ("implementar", "aplicar"), ("implementa", "aplica"), ("implementan", "aplican"),
    ("implementado", "aplicado"), ("implementación", "aplicación"),
    ("optimizar", "mejorar"), ("optimiza", "mejora"), ("optimizan", "mejoran"),
    ("optimizado", "mejorado"), ("optimización", "mejora"),
    ("maximizar", "aprovechar al máximo"), ("maximiza", "aprovecha al máximo"),
    ("paradigma", "modelo"), ("paradigmático", "representativo"),
    ("holístico", "general"), ("holística", "general"),
    ("sinérgico", "colaborativo"), ("sinérgica", "colaborativa"),
    ("sinergia", "trabajo en equipo"), ("multifacético", "complejo"), ("multifacética", "compleja"),
    ("vanguardista", "de punta"), ("de vanguardia", "de punta"),
    ("de última generación", "avanzado"),
    ("sin precedentes", "sin igual"), ("sin parangón", "sin igual"),
    ("revolucionario", "innovador"), ("revolucionaria", "innovadora"),
    ("revolucionar", "transformar"), ("catalizador", "impulsor"),
    ("robusto", "sólido"), ("robusta", "sólida"), ("escalable", "adaptable"),
    ("exhaustivo", "completo"), ("exhaustiva", "completa"),
    ("meticuloso", "cuidadoso"), ("meticulosa", "cuidadosa"),
    ("minucioso", "detallado"), ("minuciosa", "detallada"),
    ("significativo", "importante"), ("significativa", "importante"),
    ("considerable", "importante"), ("sustancial", "importante"),
    ("sustancialmente", "bastante"), ("notablemente", "bastante"),
    ("significativamente", "bastante"), ("indispensable", "necesario"),
    ("imprescindible", "necesario"), ("imperativo", "necesario"),
    ("primordial", "fundamental"),
    # More formal → casual (ES)
    ("garantizar", "asegurar"), ("garantiza", "asegura"),
    ("garantizan", "aseguran"), ("garantizado", "asegurado"),
    ("evidenciar", "mostrar"), ("evidencia", "muestra"),
    ("evidencian", "muestran"), ("evidenciado", "mostrado"),
    ("constatar", "ver"), ("constata", "muestra"),
    ("mediante", "con"), ("llevar a cabo", "hacer"),
    ("dar lugar a", "generar"), ("da lugar a", "genera"),
    ("por ende, ", "así que, "), ("por ende ", "así que "),
    ("en base a ", "basado en "), ("en base a", "con base en"),
    ("a nivel de ", "en "), ("a nivel ", "en "),
    ("lo anterior", "esto"), ("lo anteriormente", "lo"),
    ("en términos generales", "en general"),
    ("de manera efectiva", "bien"), ("de forma efectiva", "bien"),
    ("de manera eficiente", "bien"), ("de forma eficiente", "bien"),
    ("de manera adecuada", "bien"), ("de forma adecuada", "bien"),
    ("de manera significativa", "bastante"), ("de forma significativa", "bastante"),
    ("de manera considerable", "bastante"), ("de forma considerable", "bastante"),
    ("en la medida en que", "cuando"), ("en la medida que", "cuando"),
    ("con el paso del tiempo", "con el tiempo"),
    ("llevar adelante", "seguir"), ("poner en marcha", "iniciar"),
    ("dar respuesta a", "responder"), ("hacer frente a", "enfrentar"),
    ("poner de manifiesto", "mostrar"), ("pone de manifiesto", "muestra"),
    ("hacer hincapié en", "destacar"), ("hace hincapié en", "destaca"),
]

_SPLIT_PATTERNS_ES: list[tuple[str, str]] = [
    (r",\s+pero\s+", "Pero"), (r",\s+aunque\s+", "Aunque"),
    (r",\s+sino\s+", "Sino"), (r",\s+mientras\s+", ""),
    (r",\s+ya que\s+", "Ya que"), (r",\s+puesto que\s+", "Puesto que"),
    (r";\s+", ""), (r",\s+por lo que\s+", "Por lo que"),
    (r",\s+y\s+", "Y"), (r",\s+lo que\s+", "Esto "), (r"\s+—\s+", ""),
]

_HEDGES_ES = [
    "Creo que ", "Pienso que ", "En mi opinión, ",
    "Sinceramente, ", "La verdad es que ", "Personalmente, ",
    "Diría que ", "A mi parecer, ", "Si me preguntas, ",
]

_INFORMAL_ES = [
    "Mira, ", "Pues, ", "O sea, ", "Bueno, ",
    "Y aquí está lo importante: ", "Ojo, ",
    "Para ser claros: ", "Y esto es clave: ",
    "Seamos honestos: ", "La verdad es que ",
]

_PUNCH_ES = [
    "Y eso importa.", "Así de simple.", "Hay que pensarlo.",
    "Y es clave.", "Vale la pena recordarlo.",
    "Ahí está la clave.", "No es poca cosa.",
    "Y se nota.", "Hay que tenerlo claro.",
]

_HEDGEABLE_ES = {
    "el", "la", "los", "las", "este", "esta", "estos", "estas",
    "muchos", "algunos", "varios", "según", "dado",
}

_FORMAL_OPENERS_ES = {
    "El", "La", "Los", "Las", "Este", "Esta", "Estos", "Estas",
    "Muchos", "Algunos", "Varios", "Según", "Dado",
    "Los estudios", "La investigación", "Los datos",
}


# ===========================================================================
# LANGUAGE DETECTION
# ===========================================================================

def _detect_language(text: str) -> str:
    es_common = {
        "que", "de", "la", "el", "en", "es", "con", "un", "una",
        "los", "las", "del", "por", "para", "como", "más", "también",
        "pero", "sin", "sobre", "ya", "hay", "puede", "cuando", "muy",
        "al", "le", "su", "se", "si", "no", "lo", "me", "te", "nos",
        "son", "está", "era", "ser", "han", "fue", "este",
    }
    words = re.findall(r"\b[a-záéíóúüñ]+\b", text.lower())[:100]
    if not words:
        return "en"
    es_count = sum(1 for w in words if w in es_common)
    if any(c in text for c in "áéíóúüñ¿¡"):
        es_count += 8
    return "es" if es_count / len(words) > 0.12 else "en"


# ===========================================================================
# CORE HELPERS
# ===========================================================================

def _apply_contractions(text: str) -> tuple[str, int]:
    count = 0
    for full, contracted in _CONTRACTIONS_EN:
        pattern = re.compile(r"\b" + re.escape(full) + r"\b", re.IGNORECASE)
        matches = pattern.findall(text)
        if matches:
            count += len(matches)
            text = pattern.sub(contracted, text)
    return text, count


def _cap(orig: str, repl: str) -> str:
    """Capitalize repl if orig starts with uppercase."""
    if orig and orig[0].isupper() and repl and repl[0].islower():
        return repl[0].upper() + repl[1:]
    return repl


def _apply_replacements(text: str, replacements: list[tuple[str, str]]) -> tuple[str, int]:
    count = 0
    for phrase, replacement in replacements:
        stripped = phrase.strip()
        if re.fullmatch(r"[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ][a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\-]*", stripped):
            # Single pure-alpha/hyphenated word: word boundaries prevent partial matches
            pat = re.compile(r"\b" + re.escape(stripped) + r"\b", re.IGNORECASE)

            def _mk_simple(r: str):
                return lambda m: _cap(m.group(0), r)

            new_text = pat.sub(_mk_simple(replacement), text)
        else:
            # Multi-word or punctuated phrase.
            # Strip trailing comma/space from both phrase and replacement separately,
            # then match the base with a capture group for the trailing context.
            # When the tail IS captured (mid-sentence), use the full replacement as-is.
            # When the tail is NOT captured (end-of-sentence lookahead), use base replacement.
            base = phrase.rstrip(", ")
            tail = phrase[len(base):]           # e.g. ", " or " " or ""
            base_repl = replacement.rstrip(", ")

            if tail:
                pat = re.compile(
                    re.escape(base) + r"(" + re.escape(tail) + r"|(?=[.!?;:\n]|$))",
                    re.IGNORECASE,
                )

                def _mk_flex(full_r: str, base_r: str):
                    def fn(m: re.Match) -> str:
                        orig = m.group(0)
                        captured = m.group(1) or ""
                        # Full replacement includes its own trailing (e.g. "and ", "today, ")
                        # Use it when tail matched; use base (stripped) when at end-of-sentence
                        r = full_r if captured else base_r
                        return _cap(orig, r)
                    return fn

                new_text = pat.sub(_mk_flex(replacement, base_repl), text)
            else:
                pat = re.compile(re.escape(phrase), re.IGNORECASE)

                def _mk_exact(r: str):
                    return lambda m: _cap(m.group(0), r)

                new_text = pat.sub(_mk_exact(replacement), text)

        if new_text != text:
            count += 1
            text = new_text
    return text, count


def _force_split(sent: str, lang: str) -> list[str]:
    """Split a long sentence at the best conjunction even without a preceding comma."""
    words = sent.split()
    if len(words) < 14:
        return [sent]
    mid = len(words) // 2
    # Only conjunctions that reliably separate main clauses
    conjunctions_en = {"and", "but", "while", "although", "whereas", "because"}
    conjunctions_es = {"y", "pero", "mientras", "aunque", "porque", "sino"}
    conjunctions = conjunctions_es if lang == "es" else conjunctions_en
    # Use a higher minimum for Spanish "y" splits to prevent bad fragments
    min_words = 9 if lang == "es" else 7

    best_pos = -1
    best_dist = len(words)
    for i in range(4, len(words) - 4):
        w = words[i].lower().rstrip(".,;:")
        if w in conjunctions:
            prev = words[i - 1].lower().rstrip(".,;:")
            next_w = words[i + 1].lower().rstrip(".,;:") if i + 1 < len(words) else ""
            # Good split: substantial word before AND after the conjunction
            if len(prev) > 3 and len(next_w) > 3:
                dist = abs(i - mid)
                if dist < best_dist:
                    best_dist = dist
                    best_pos = i

    if best_pos == -1:
        return [sent]

    part1 = " ".join(words[:best_pos]).rstrip() + "."
    connector = words[best_pos][0].upper() + words[best_pos][1:]
    rest = " ".join(words[best_pos + 1:]).strip()
    part2 = (connector + " " + rest) if rest else ""
    if not part2 or len(part1.split()) < min_words or len(part2.split()) < min_words:
        return [sent]
    return [part1, part2]


def _split_sentences(text: str, max_words: int, lang: str) -> tuple[str, int]:
    patterns = _SPLIT_PATTERNS_ES if lang == "es" else _SPLIT_PATTERNS_EN
    sentences = sent_tokenize(text, lang)
    result: list[str] = []
    splits = 0

    for sent in sentences:
        if len(sent.split()) <= max_words:
            result.append(sent)
            continue

        split_done = False
        for pat, connector in patterns:
            matches = list(re.finditer(pat, sent, re.IGNORECASE))
            if not matches:
                continue
            mid = len(sent) // 2
            best = min(matches, key=lambda m: abs(m.start() - mid))
            part1 = sent[: best.start()].rstrip()
            rest = sent[best.end():].strip()
            part2 = (connector + " " + rest) if connector else rest
            if part2:
                part2 = part2[0].upper() + part2[1:]
                # Skip if either side would be a very short fragment
                if len(part1.split()) < 4 or len(part2.split()) < 4:
                    continue
                result.append(part1 + ".")
                result.append(part2)
                splits += 1
                split_done = True
                break

        if not split_done:
            # Fallback: force-split at any conjunction near the midpoint
            parts = _force_split(sent, lang)
            if len(parts) > 1:
                result.extend(parts)
                splits += 1
            else:
                result.append(sent)

    return " ".join(result), splits


def _inject_hedges(text: str, intensity: str, lang: str) -> tuple[str, int]:
    """Prepend first-person hedges to AI-typical impersonal sentence openers."""
    if intensity == "subtle":
        return text, 0
    hedges = _HEDGES_ES if lang == "es" else _HEDGES_EN
    starters = _HEDGEABLE_ES if lang == "es" else _HEDGEABLE_EN

    sentences = sent_tokenize(text, lang)
    n = len(sentences)
    if n < 3:
        return text, 0

    candidates = [
        i for i in range(1, n)
        if len(sentences[i].split()) >= 5
        and not sentences[i].endswith("?")
        and sentences[i].split()[0].lower().rstrip(".,;:") in starters
    ]
    if not candidates:
        return text, 0

    num = {"balanced": 1, "aggressive": min(3, len(candidates))}.get(intensity, 1)
    picks: set[int] = {candidates[0]}
    if num >= 2 and len(candidates) > 2:
        picks.add(candidates[len(candidates) // 2])
    if num >= 3 and len(candidates) > 4:
        picks.add(candidates[len(candidates) * 3 // 4])

    result: list[str] = []
    injected = 0
    for i, sent in enumerate(sentences):
        if i in picks:
            hedge = hedges[i % len(hedges)]
            if sent and sent[0].isupper():
                sent = sent[0].lower() + sent[1:]
            result.append(hedge + sent)
            injected += 1
        else:
            result.append(sent)
    return " ".join(result), injected


def _inject_informal_starters(text: str, intensity: str, lang: str) -> tuple[str, int]:
    """Add informal openers like 'Look,' / 'Mira,' by sentence position."""
    if intensity != "aggressive":
        return text, 0
    starters_pool = _INFORMAL_ES if lang == "es" else _INFORMAL_EN

    sentences = sent_tokenize(text, lang)
    n = len(sentences)
    if n < 4:
        return text, 0

    # Pick non-first, non-last sentences of sufficient length, spaced apart
    # Skip sentences that already start with a conjunction to avoid "And honestly, and..."
    conjunction_starts = {"and", "but", "yet", "so", "or", "nor", "pero", "sino", "aunque"}
    max_starters = 3 if lang == "es" else 2
    picks: list[int] = []
    for i in range(2, n - 1):
        first_word = sentences[i].split()[0].lower().rstrip(".,;:") if sentences[i].split() else ""
        if (len(sentences[i].split()) >= 7
                and not sentences[i].endswith("?")
                and first_word not in conjunction_starts):
            if not picks or i - picks[-1] >= 2:
                picks.append(i)
        if len(picks) >= max_starters:
            break

    result: list[str] = []
    injected = 0
    for i, sent in enumerate(sentences):
        if i in picks:
            starter = starters_pool[i % len(starters_pool)]
            if sent and sent[0].isupper():
                sent = sent[0].lower() + sent[1:]
            result.append(starter + sent)
            injected += 1
        else:
            result.append(sent)
    return " ".join(result), injected


def _insert_punch_sentences(text: str, intensity: str, lang: str) -> tuple[str, int]:
    """Insert short punch sentences after long ones to maximize burstiness."""
    if intensity != "aggressive":
        return text, 0
    punches = _PUNCH_ES if lang == "es" else _PUNCH_EN
    sentences = sent_tokenize(text, lang)
    n = len(sentences)
    if n < 4:
        return text, 0

    # Find long sentences (>18 words) that could use a punch after them
    # Include first sentence (index 0) as valid punch point — creates strong opening contrast
    candidates = [
        i for i in range(n - 1)
        if len(sentences[i].split()) > 18
    ]
    if not candidates:
        return text, 0

    # Pick 1-3 spots — allow consecutive long sentences to each get a punch
    max_punches = 3 if lang == "es" else 2
    picks: list[int] = []
    for idx in candidates:
        if not picks or idx - picks[-1] >= 1:
            picks.append(idx)
        if len(picks) >= max_punches:
            break

    result: list[str] = []
    inserted = 0
    for i, sent in enumerate(sentences):
        result.append(sent)
        if i in picks:
            result.append(punches[i % len(punches)])
            inserted += 1
    return " ".join(result), inserted


def _clean(text: str) -> str:
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\s+([.,;:!?¡¿])", r"\1", text)
    text = re.sub(r"([.!?])\s*([a-záéíóúüñA-ZÁÉÍÓÚÜÑ])",
                  lambda m: m.group(1) + " " + m.group(2).upper(), text)
    text = re.sub(r"^\s+|\s+$", "", text, flags=re.MULTILINE)
    return text.strip()


# ===========================================================================
# PUBLIC ENTRY POINT
# ===========================================================================

def humanize_rules(text: str, intensity: str = "balanced") -> HumanizeResponse:
    """
    Rule-based humanizer. intensity: 'subtle' | 'balanced' | 'aggressive'
    Supports English and Spanish (auto-detected).
    """
    lang = _detect_language(text)
    result = text
    replacement_count = 0
    contraction_count = 0
    split_count = 0
    hedge_count = 0
    informal_count = 0
    punch_count = 0

    replacements = _AI_REPLACEMENTS_ES if lang == "es" else _AI_REPLACEMENTS_EN

    if intensity in ("balanced", "aggressive"):
        result, replacement_count = _apply_replacements(result, replacements)
    else:
        # Subtle: small targeted subset
        if lang == "es":
            subtle: list[tuple[str, str]] = [
                ("es importante destacar que ", ""), ("cabe destacar que ", ""),
                ("sin embargo, ", "pero "), ("no obstante, ", "pero "),
                ("asimismo, ", "también, "), ("en consecuencia, ", "entonces, "),
                ("en conclusión, ", "entonces, "), ("en resumen, ", "en pocas palabras, "),
                ("en la actualidad, ", "hoy, "), ("en el contexto actual, ", "hoy, "),
                ("utilización", "uso"), ("utilizar", "usar"),
                ("significativamente", "bastante"), ("en definitiva, ", "en fin, "),
            ]
        else:
            subtle = [
                ("it's worth noting that ", ""), ("it is worth noting that ", ""),
                ("furthermore, ", "also, "), ("moreover, ", "plus, "),
                ("additionally, ", "and "), ("consequently, ", "so, "),
                ("therefore, ", "so, "), ("thus, ", "so, "),
                ("utilization", "use"), ("utilized", "used"), ("utilize", "use"),
                ("in order to ", "to "), ("due to the fact that ", "because "),
                ("paradigm shift", "big change"), ("leverage ", "use "),
                ("leveraging ", "using "), ("comprehensive", "thorough"),
                ("groundbreaking", "innovative"), ("seamlessly", "smoothly"),
                ("a wide range of ", "many "), ("significantly ", "a lot "),
                ("numerous ", "many "), ("furthermore ", "also "),
            ]
        result, replacement_count = _apply_replacements(result, subtle)

    # Contractions only for English
    if lang == "en":
        result, contraction_count = _apply_contractions(result)

    # Personal-voice hedges
    result, hedge_count = _inject_hedges(result, intensity, lang)

    # Sentence splitting — split BEFORE informal starters to prevent fragment issues
    # Spanish aggressive uses 10 (tighter) to maximize burstiness
    if intensity == "aggressive" and lang == "es":
        max_w = 10
    else:
        max_w = {"aggressive": 12, "balanced": 20, "subtle": 999}.get(intensity, 999)
    if max_w < 999:
        result, split_count = _split_sentences(result, max_words=max_w, lang=lang)

    # Informal starters applied to already-split sentences (avoids fragments)
    result, informal_count = _inject_informal_starters(result, intensity, lang)

    # Punch sentences (aggressive only)
    result, punch_count = _insert_punch_sentences(result, intensity, lang)

    result = _clean(result)

    # Build change list
    changes: list[str] = []
    if replacement_count > 0:
        changes.append(f"Replaced {replacement_count} AI-signature phrases and formal words")
    if contraction_count > 0:
        changes.append(f"Added {contraction_count} natural contractions")
    if hedge_count > 0:
        changes.append(f"Injected personal voice in {hedge_count} sentence(s)")
    if informal_count > 0:
        changes.append(f"Added {informal_count} informal sentence opener(s)")
    if split_count > 0:
        orig_n = len(sent_tokenize(text, lang))
        new_n = len(sent_tokenize(result, lang))
        changes.append(
            f"Restructured sentence count ({orig_n} → {new_n}) for natural burstiness"
        )
    if punch_count > 0:
        changes.append(f"Inserted {punch_count} short punch sentence(s) for rhythm")
    changes.append({
        "subtle":     "Applied subtle polish — minimal structural changes",
        "balanced":   "Rewrote for natural human tone and varied rhythm",
        "aggressive": "Fully restructured — new expression, same ideas",
    }[intensity])

    original_score = _estimate_score(text)
    estimated_score = _estimate_score(result)

    return HumanizeResponse(
        original=text,
        humanized=result,
        changes_made=[c for c in changes if c],
        estimated_ai_score=estimated_score,
        original_ai_score=original_score,
    )


def _estimate_score(text: str) -> float:
    from app.services.detector import (
        _burstiness, _get_sentences, _get_words,
        _ai_phrase_density, _personal_pronoun_ratio,
        _transition_density, _formal_word_ratio,
        _contraction_ratio, _calibrate,
    )
    sentences = _get_sentences(text)
    words = _get_words(text)
    if not sentences or not words:
        return 50.0
    burst = _burstiness(sentences)
    phrase_density, _ = _ai_phrase_density(text.lower(), len(words))
    pron_ratio = _personal_pronoun_ratio(words)
    trans_density = _transition_density(words)
    formal_ratio = _formal_word_ratio(words)
    contr_ratio = _contraction_ratio(text, len(words))

    burst_ai  = max(0.0, min(100.0, (0.68 - burst) / 0.52 * 100))
    phrase_ai = min(100.0, phrase_density * 55)
    pron_ai   = max(0.0, min(100.0, (0.055 - pron_ratio) / 0.055 * 88))
    trans_ai  = min(100.0, trans_density * 4000)
    formal_ai = min(100.0, formal_ratio * 900)
    contr_ai  = max(0.0, min(100.0, (0.028 - contr_ratio) / 0.028 * 85))

    raw = (burst_ai * 0.22 + phrase_ai * 0.25 + pron_ai * 0.12 +
           trans_ai * 0.13 + formal_ai * 0.12 + contr_ai * 0.16)
    return round(max(0.0, min(100.0, _calibrate(raw))), 1)
