word_pairs = [
    ("envanglion", "navgionlen"),  # Evangelion
    ("chrollolucifer", "rllcholucrefi"),  # Chrollo Lucifer
    ("ryougi", "yirgou"),  # Ryougi (Shiki)
    ("okabe", "beako"),  # Okabe (Rintarou)
    ("kamado", "amkado"),  # Kamado (Tanjirou)
    ("remuru", "umrure"),  # Rimuru (Tempest)
    ("rengoku", "kuronge"),  # Rengoku (Kyojuro)
    ("zoldyck", "dlykocz"),  # Zoldyck (Family)
    ("sakuragi", "ugarsaki"),  # Sakuragi (Hanamichi)
    ("guts", "tugs"),  # Guts (Berserk)
    ("getou", "ogtue"),  # Getou (Suguru)
    ("hollows", "wllhoos"),  # Hollows (Bleach)
    ("kurapika", "krupakia"),  # Kurapika
    ("shinigami", "mgaihinsi"),  # Shinigami
    ("homunculus", "nlumushocu"),  # Homunculus
    ("zangetsu", "sangetzu"),  # Zangetsu
    ("senju", "ujens"),  # Senju
    ("shibata", "bhsitaa"),  # Shibata
    ("ryomen", "menory"),  # Ryomen Sukuna
    ("esdeath", "ethsaed"),  # Esdeath
    ("vashthestampede", "tpdshevamhsaet"),  # Vash The Stampede
    ("rezero", "erorez"),  # Re:Zero
    ("tokiwadai", "awdiatok"),  # Tokiwadai (Railgun)
    ("hachiman", "namchiah"),  # Hachiman
    ("mikazuki", "zukakimi"),  # Mikazuki (Augus)
    ("byakuya", "akyuyba"),  # Byakuya
    ("yoruichi", "ichruoyi"),  # Yoruichi
    ("mitsuri", "ruimtsi"),  # Mitsuri (Kanroji)
    ("izaya", "aayiz"),  # Izaya (Orihara)
    ("shiba", "bahsi"),  # Shiba (Ichigo’s family)
    ("arceuid", "iduacer"),  # Arcueid (Brunestud)
    ("gilgamesh", "hsagilmge"),  # Gilgamesh
    ("lancaster", "tarsnacle"),  # Lancaster (Weiss)
    ("francoise", "cosafiren"),  # Francoise (009)
    ("tsukishima", "tmahisuiks"),  # Tsukishima
    ("fushiguro", "higurusfo"),  # Fushiguro (Megumi)
    ("benimaru", "mibaneur"),  # Benimaru
    ("mugen", "engmu"),  # Mugen (Samurai Champloo)
    ("hiyori", "rihyoi"),  # Hiyori (Iki)
    ("tohsaka", "shatoak"),  # Tohsaka (Rin)
    ("fujimaru", "ufaimrju"),  # Fujimaru (Ritsuka)
    ("roswaal", "larowas"),  # Roswaal
    ("ichimaru", "urimaich"),  # Ichimaru (Gin)
    ("toji", "ojti"),  # Toji (Fushiguro)
    ("shiba", "hbsia"),  # Shiba (Kaien)
    ("escanor", "aesnroc"),  # Escanor
    ("charlotte", "ltorcetha"),  # Charlotte
    ("akabane", "akaenab"),  # Akabane (Kurodo)
    ("hollowfication", "llwhofictoiain"),  # Hollowfication
    ("rukh", "hukr"),  # Rukh (Magi)
    ("sasaki", "kaisast"),  # Sasaki (Haise)
    ("rayleigh", "yiglreah"),  # Rayleigh (Silvers)
    ("kobayashi", "bkosayahi"),  # Kobayashi
    ("netero", "tereno"),  # Netero (Isaac)
    ("kaguya", "gaukya"),  # Kaguya (Ōtsutsuki)
    ("fateapocrypha", "teapcryohfapa"),  # Fate/Apocrypha
    ("kisaragi", "grsakiai"),  # Kisaragi (Saya)
    ("hinamizawa", "wahianzmia"),  # Hinamizawa (Higurashi)
    ("chamber", "ehmcrab"),  # Chamber (Suisei no Gargantia)
    ("codegeass", "esgdoca"),  # Code Geass
    ("hoshigaki", "oighishak"),  # Hoshigaki (Kisame)
    ("himura", "urmhai"),  # Himura (Kenshin)
    ("edolas", "soldea"),  # Edolas (Fairy Tail)
    ("amaterasu", "mtersaaau"),  # Amaterasu
    ("darkcontinent", "rontdaentick"),  # Dark Continent (HxH)
    ("balmung", "lubmgna"),  # Balmung
    ("touka", "kaout"),  # Touka (Tokyo Ghoul)
    ("hanekawa", "khaweana"),  # Hanekawa (Tsubasa)
    ("kizuna", "zaukni"),  # Kizuna
    ("shiranui", "nisuhari"),  # Shiranui
    ("berserker", "rsrreekeb"),  # Berserker
    ("argonavis", "gsaonravi"),  # Argonavis
    ("osamu", "maosu"),  # Osamu (Dazai)
    ("umineko", "unomike"),  # Umineko
    ("pannacotta", "acnpttoana"),  # Pannacotta (Fugo)
    ("femto", "mftoe"),  # Femto (Berserk)
    ("hellsalemslot", "llhestmoslel"),  # Hellsalem’s Lot
    ("sakurafubuki", "kufasurubki"),  # Sakura Fubuki
    ("amuro", "mruoa"),  # Amuro (Toru)
    ("shichibukai", "isibckahuh"),  # Shichibukai
    ("cocytus", "ytucosc"),  # Cocytus (Overlord)
    ("genjutsu", "sgunetju"),  # Genjutsu
    ("euphie", "peuhie"),  # Euphemia
    ("hokuto", "tuhoko"),  # Hokuto (Hyoudou)
    ("grimoire", "irmgioer"),  # Grimoire
    ("chaldea", "chdleaa"),  # Chaldea
    ("reichswein", "isrchiwene"),  # Reichswein
    ("iskandar", "rknaisda"),  # Iskandar (Fate)
    ("celestia", "leseatci"),  # Celestia
    ("altair", "itral"),  # Altair (Re:Creators)
    ("python", "nohtyp"),
    ("banana", "ananab"),
    ("computer", "putermoc"),
    ("keyboard", "draboyek"),
    ("elephant", "tnahpele"),
    ("programming", "gnimmargorp"),
    ("telephone", "enohpelet"),
    ("network", "krowten"),
    ("algorithm", "mhtirogla"),
    ("software", "erawtfos"),
    ("developer", "relopedev"),
    ("database", "esabatad"),
    ("security", "yticures"),
    ("interface", "ecafretni"),
    ("debugging", "gniggubed"),
    ("iteration", "noitaretI"),
    ("variable", "elbairav"),
    ("function", "noitcnuf"),
    ("documentation", "noitatnemucod"),
    ("naruto", "arnotu"),
    ("bleach", "lehbac"),
    ("goku", "kugo"),
    ("sakura", "rkuaas"),
    ("titan", "tatin"),
    ("nami", "imna"),
    ("pikachu", "icpkhau"),
    ("yugi", "iguy"),
    ("totoro", "orotot"),
    ("tanjiro", "rojanit"),
    ("luffy", "yfluf"),
    ("shonen", "nnsoeh"),
    ("seiyuu", "eiyuus"),
    ("vegeta", "etgave"),
    ("shikamaru", "rakmuhasi"),
    ("ichigo", "goiich"),
    ("natsu", "stun"),
    ("hinata", "taniah"),
    ("alchemist", "lthimcaes"),
    ("kenshin", "neiknsh"),
    ("sora", "osar"),
    ("shinobi", "ioshinb"),
    ("demon", "node"),
    ("saitama", "tasamia"),
    ("inuyasha", "anuiysah"),
    ("akira", "rikaa"),
    ("sao", "oas"),
    ("baka", "akab"),
    ("otaku", "tkuao"),
    ("kirito", "otkiri"),
    ("asuna", "nsasu"),
    ("zoro", "oroz"),
    ("kaguya", "akugya"),
    ("lelouch", "louelch"),
    ("edward", "wardde"),
    ("mustang", "tansgum"),
    ("alucard", "rcaldua"),
    ("dragon", "ngrdao"),
    ("gohan", "hagon"),
    ("trunks", "runtsk"),
    ("mecha", "acehm"),
    ("anime", "imena"),
    ("mangaka", "kmangaa"),
    ("studio", "idoust"),
    ("kaiju", "iujak"),
    ("yamcha", "mhacya"),
    ("madara", "raamad"),
    ("gon", "nog"),
    ("hisoka", "koshia"),
    ("ciel", "lcei"),
    ("rem", "mer"),
    ("ryuk", "ukyr"),
    ("light", "thilg"),
    ("ghoul", "louhg"),
    ("urameshi", "hrusmeia"),
    ("kaneki", "eknkai"),
    ("mikasa", "asakim"),
    ("shanks", "akshns"),
    ("usopp", "suopp"),
    ("sanji", "janis"),
    ("broly", "lryob"),
    ("piccolo", "colopic"),
    ("bulma", "malub"),
    ("jiraiya", "irijyaa"),
    ("kankuro", "ankkoru"),
    ("anbu", "banu"),
    ("konoha", "onkhoa"),
    ("edo", "doe"),
    ("hokage", "okhega"),
    ("rinnegan", "ginnenar"),
    ("sharingan", "rganashn"),
    ("tsunade", "ensutda"),
    ("akatsuki", "taksuaki"),
    ("obito", "btooi"),
    ("tobi", "ibot"),
    ("pain", "inap"),
    ("yahiko", "kyoaih"),
    ("nagato", "atogan"),
    ("jutsu", "tsuju"),
    ("chuunin", "nchuniu"),
    ("kunai", "ukain"),
    ("shuriken", "renshuki"),
    ("rasengan", "rsnegaan"),
    ("chidori", "rdchii"),
    ("kurama", "akmrua"),
    ("shisui", "sshiu"),
    ("yato", "atoy"),
    ("tooru", "oruot"),
    ("frieza", "raifze"),
    ("shenron", "hrnones"),
    ("cell", "lcle"),
    ("jiren", "nrjie"),
    ("beerus", "ebruse"),
    ("whis", "hswi"),
    ("android", "noridda"),
    ("chichi", "hcicih"),
    ("goten", "teong"),
    ("videl", "ldvei"),
    ("pan", "nap"),
    ("babidi", "ibadib"),
    ("dabura", "bruada"),
    ("nimbus", "busnim"),
    ("kamehameha", "ehamkmhaaa"),
    ("kaioken", "oenkkai"),
    ("super", "perus"),
    ("saiyan", "yasain"),
    ("kaioshin", "hnokiais"),
    ("zenoh", "hezon"),
    ("kushina", "inhkas"),
    ("minato", "atmion"),
    ("neji", "ijen"),
    ("tenten", "entnet"),
    ("gai", "iag"),
    ("asuma", "suama"),
    ("kurenai", "raunkie"),
    ("kiba", "abik"),
    ("shino", "hosni"),
    ("boruto", "orbut"),
    ("sarada", "darasa"),
    ("mitsuki", "kistmui"),
    ("orochimaru", "cmruaiohr"),
    ("kabuto", "bakotu"),
    ("karin", "irakn"),
    ("suigetsu", "giustes"),
    ("jugo", "uojg"),
    ("yamato", "otmaay"),
    ("hanabi", "biahna"),
    ("shikaku", "ksuahki"),
    ("ino", "oni"),
    ("chouji", "iocjhu"),
    ("konohamaru", "ouhnkmar"),
    ("moegi", "geimo"),
    ("udon", "onud"),
    ("suzume", "umezsu"),
    ("yugao", "ouagy"),
    ("choza", "czhao"),
    ("gaara", "aagra"),
    ("temari", "amirte"),
    ("matsuri", "tsurima"),
    ("ebisu", "ieusb"),
    ("raikage", "kgeaair"),
    ("darui", "rduai"),
    ("samui", "uamsi"),
    ("killerbee", "ilbekrlee"),
    ("c", "ec"),
    ("ay", "ya"),
    ("onoki", "okoin"),
    ("kurotsuchi", "ckroihtsu"),
    ("akatsuchi", "akictsuh"),
    ("tsuchikage", "gsuhicekta"),
    ("mizukage", "kemaugzi"),
    ("mei", "iem"),
    ("ao", "oa"),
    ("chojuro", "hcurooj"),
    ("yagura", "agruya"),
    ("kirigakure", "gariekruki"),
    ("konan", "nanko"),
    ("zabuza", "aubazz"),
    ("haku", "kiah"),
    ("kimimaro", "rokmiami"),
    ("jigen", "ngije"),
    ("amado", "oadma"),
    ("kashin", "hnsiak"),
    ("shin", "niish"),
    ("denki", "inekd"),
    ("iwabe", "wabie"),
    ("sumire", "eirsum"),
    ("shikadai", "ikishada"),
    ("chocho", "oohcch"),
    ("inojin", "jiinon"),
    ("metal", "latem"),
    ("kawaki", "wikaka"),
    ("eida", "ieda"),
    ("daemon", "noamed"),
    ("code", "deoc"),
    ("boros", "osbor"),
    ("tanktop", "tkpaton"),
    ("fubuki", "kufbik"),
    ("garou", "rugao"),
    ("genos", "sogne"),
    ("sonic", "cison"),
    ("bang", "angb"),
    ("bomb", "obmb"),
    ("child", "lhidc"),
    ("emperor", "rpeemro"),
    ("tornado", "ontdora"),
    ("king", "gink"),
    ("prisioner", "nrieprso"),
    ("puri", "uirp"),
    ("blizzard", "dziralbz"),
    ("umbrella", "allerbmu"),
    ("chocolate", "etalocohc"),
    ("giraffe", "effarig"),
    ("butterfly", "ylfrettub"),
    ("pyramid", "dimaryp"),
    ("horizon", "noziroh"),
    ("galaxy", "yxalag"),
    ("volcano", "onaclov"),
    ("parachute", "etuhcarap"),
    ("fireworks", "skrowerif"),
    ("astronaut", "tuonortsa"),
    ("backpack", "kcapkcab"),
    ("carousel", "leusorac"),
    ("dinosaur", "ruasonid"),
    ("eclipse", "eslipce"),
    ("fountain", "niatnuof"),
    ("guitar", "ratiug"),
    ("harbor", "robrah"),
    ("jigsaw", "wagsij"),
    ("kayaking", "gnikayak"),
    ("landscape", "epacsdnal"),
    ("marathon", "nohtaram"),
    ("nebula", "aluben"),
    ("octopus", "supotco"),
    ("puzzle", "elzzup"),
    ("quicksand", "dnasciuq"),
    ("rainbow", "wobniar"),
    ("sapphire", "erihppas"),
    ("tornado", "odanrot"),
    ("universe", "esrevinu"),
    ("vortex", "xetrov"),
    ("whirlpool", "looplihw"),
    ("xylophone", "enohpolyx"),
    ("zeppelin", "nilpezep"),
    ("yacht", "thcay"),
    ("zigzag", "gazzig"),
]
