import random
from english_words import get_english_words_set

WORDS_LIST = ['leguminaceae', 'cruciferae', 'ceres', 'alliaceae', 'asparagus', 'crotalaria', 'pendimethalin', 'leucaena', 'lignification', 'scrobiculatum', 'synergistic', 'overlapping', 'ulmaceae', 'chrococcum', 'tetragonoloba', 'convolvulus', 'eleucine', 'sterilization', 'fluchloralin', 'intertilled', 'parthenocarpy', 'gibberellic', 'arboriculture', 'micropropagation', 'Quincunx', 'caesalpinia', 'vermiculite', 'cumbersome', 'antiphlogistic', 'mucilage', 'xerophthalmia', 'keratomalacia', 'urolithasis', 'antirachitic', 'keratinization', 'osteomalacia', 'osteodystrophy', 'antihaemorrhagic', 'phospholipid', 'dinitrobenzene', 'tetracarbocyclic', 'ketogluconic', 'trinitrostarch', 'amylopectin', 'oligosaccharides', 'ergotine', 'allelopathic', 'flavidum', 'aristolochia', 'enneaphylla', 'solipsism', 'nihilism', 'hedonism', 'coppice', 'lundburg', 'hominidae', 'acrasiomycetes', 'leishmania', 'sexduction', 'holothuria', 'eucoelomate', 'frugivorous', 'chondrichthyes', 'neoceratodus', 'enterocoelous', 'calyciflorae', 'fabaceae', 'spermatheca', 'dimorphism', 'methionine', 'devernalisation', 'auxanometers', 'photoperiodism', 'pancreozymin', 'villikinin', 'chymotrypsinogen', 'histidine', 'undernourishment', 'buccopharyngeal', 'schneiderian', 'maxilloturbinals', 'mediastinum', 'rhythmicity', 'hypocapnia', 'emphysema', 'bronchiodilators', 'oxyhaemoglobin', 'agranulocytes', 'erythroblastosis', 'adventitia', 'thebesius', 'myogenic', 'neurogenic', 'atherosclerosis', 'anastomosis', 'guanotelism', 'mesorchium', 'juxtamedullary', 'uropoiesis', 'argininosuccinic']

for x in get_english_words_set(["web2"]):
    if len(x) == 10:
        WORDS_LIST.append(x.lower())
        
five = []
        
def five_letter_words():
    global five
    if not five:
        for x in get_english_words_set(["web2"]):
            if len(x) == 5:
                five.append(x.lower())
    return five

def Word():
  x = random.choice(WORDS_LIST)
  return x
