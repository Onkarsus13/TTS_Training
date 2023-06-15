import re
import pandas as pd
from langdetect import detect
import langid
# from TTS.tts.utils.text.DPsaarthi.phonemizer import Phonemizer

class SymbolParser(object):

    # def __init__(self,):
    #     pass
    # @staticmethod
    def readNumber(self, number,language):
        #define indic numberic lexicons
        numLiterals = { 0 : 'zero', 1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four', 5 : 'five',
                6 : 'six', 7 : 'seven', 8 : 'eight', 9 : 'nine'}
        numHindi = {0:'',1:'एक',2:'दो',3:'तीन',4:'चार',5:'पांच',
                        6:'छह',7:'सात',8:'आठ',9:'नौ',10:'दस',11:'ग्यारह',12:'बारह',13:'तेरह',
                        14:'चोदह',15:'पंद्रह',16:'सोलह',17:'सत्त्रह',18:'अट्ठारह',19:'उन्नीस',20:'बीस',
                        21:'इक्कीस',22:'बाइस',23:'तेईस',24:'चौबीस',25:'पच्चीस',26:'छब्बीस',27:'सत्ताइस',
                        28:'अट्ठाइस',29:'उन्तीस',30:'तीस',31:'इकतीस',32:'बत्तीस',33:'तैतीस',34:'चौतीस',
                        35:'पैतीस',36:'छत्तीस',37:'सैतीस',38:'अड़तीस',39:'उन्तालीस',40:'चालीस',41:'इकतालीस',
                        42:'बयालीस',43:'तिरतालिस',44:'चौवालीस',45:'पैतालीस',46:'छयालीस',47:'सैतालिस',
                        48:'अड़तालीस',49:'उनचास',50:'पचास',51:'इक्क्यावन',52:'बावन',53:'तिरपन',54:'चौवन',
                        55:'पचपन',56:'छप्पन',57:'सत्तावन',58:'अट्ठावन',59:'उनसठ',60:'साठ',61:'इकसठ',62:'बासठ',
                        63:'तिरसठ',64:'चौसठ',65:'पैंसठ',66:'छयासठ',67:'सड़सठ',68:'अड़सठ',69:'उनहत्तर',70:'सत्तर',
                        71:'इकहत्तर',72:'बहत्तर',73:'तिरहत्तर',74:'चौहत्तर',75:'पिचहत्तर',76:'छियत्तर',77:'सतत्तर',
                        78:'अठहत्तर',79:'उन्हासी',80:'अस्सी',81:'इक्यासी',82:'बयासी',83:'तिरासी',84:'चौरासी',
                        85:'पिचासी',86:'छयासी',87:'सत्तासी',88:'अट्ठासी',89:'नवासी',90:'नब्बे',91:'इक्यानवे',
                        92:'बानवे',93:'तिरानवे',94:'चौरानवे',95:'पिच्यानवे',96:'छियानवे',97:'सत्तानवे',98:'अट्ठानवे',
                        99:'निन्यानवे',100:'सौ'}
                        #,1000:'हजार',100000:'लाख',10000000:'करोड़',1000000000:'अरब'
        numOdia= {0:'',1:'ଏକ',2:'ଦୁଇ',3:'ତିନି',4:'ଚାରି',5:'ପାଞ୍ଚ',
                6:'ଛଅ',7:'ସାତ',8:'ଆଠ',9:'ନଅ',10:'ଦଶ',11:'ଏଗାର',12:'ବାର',13:'ତେର',
                14:'ଚଉଦ',15:'ପନ୍ଦର',16:'ଷୋହଳ',17:'ସତର',18:'ଅଠର',19:'ଉଣେଇଶ',20:'କୋଡ଼ିଏ',
                21:'ଏକୋଇଶ',22:'ବାଇଶ',23:'ତେଇଶ',24:'ଚବିଶ',25:'ପଚିଶ',26:'ଛବିଶ',27:'ସତେଇଶ',
                28:'ଅଠେଇଶ',29:'ଅଣତିରିଶ',30:'ତିରିଶ',31:'ଏକତିରିଶ',32:'ବତିଶ',33:'ତେତିଶ',34:'ଚଉତରିଶ',
                35:'ପଇଁତିରିଶ',36:'ଛତିଶ',37:'ସଇଁତିରିଶ',38:'ଅଠତିରିଶ',39:'ଅଣଚାଳିଶ',40:'ଚାଳିଶ',41:'ଏକଚାଳିଶ',
                42:'ବୟାଳିଶ',43:'ତେୟାଳିଶ',44:'ଚଉରାଳିଶ',45:'ପଇଁଚାଳିଶ',46:'ଛୟାଳିଶ',47:'ସତଚାଳିଶ',
                48:'ଅଠଚାଳିଶ',49:'ଅଣଚାଶ',50:'ପଚାଶ',51:'ଏକାବନ',52:'ବାବନ',53:'ତେପନ',54:'ଚଉବନ',
                55:'ପଞ୍ଚାବନ',56:'ଛପନ',57:'ସତାବନ',58:'ଅଠାବନ',59:'ଅଣଷଠି',60:'ଷାଠିଏ',61:'ଏକଷଠି',62:'ବାଷଠି',
                63:'ତେଷଠି',64:'ଚଉଷଠି',65:'ପଞ୍ଚଷଠି',66:'ଛଷଠି',67:'ଶତଷଠି',68:'ଅଠଷଠି',69:'ଅଣସ୍ତରି',70:'ସତୁରୀ',
                71:'ଏକସ୍ତରୀ',72:'ବାସ୍ତରୀ',73:'ତେସ୍ତରୀ',74:'ଚଉସ୍ତରୀ',75:'ପଞ୍ଚସ୍ତରୀ',76:'ଛସ୍ତରୀ',77:'ସତସ୍ତରୀ',
                78:'ଅଠସ୍ତରୀ',79:'ଅଣାଅଶୀ',80:'ଅଶୀ',81:'ଏକାଅଶୀ',82:'ବୟାଅଶୀ',83:'ତେୟାଅଶୀ',84:'ଚଉରାଅଶୀ',
                85:'ପଞ୍ଚାଅଶୀ',86:'ଛୟାଅଶୀ',87:'ସତାଅଶୀ',88:'ଅଠାଅଶୀ',89:'ଅଣାନବେ',90:'ନବେ',91:'ଏକାନବେ',
                92:'ବୟାନବେ',93:'ତେୟାନବେ',94:'ଚଉରାନବେ',95:'ପଞ୍ଚାନବେ',96:'ଛୟାନବେ',97:'ସତନାବେ',98:'ଅଠାନବେ',
                99:'ଅନେଶ୍ୱତ',100:'ଶହେ'}
        numMalayalam={0:'',1:'ഒന്ന്',2:'രണ്ട്',3:'മൂന്ന്',4:'നാല്',5:'അഞ്ച്',6:'ആറ്',7:'ഏഴ്',
                8:'എട്ട്',9:'ഒന്‍പത്',10:'പത്ത്',11:'പതിനൊന്ന്',12:'പന്ത്രണ്ട്',13:'പതിമൂന്ന്',14:'പതിനാല്',
                15:'പതിനഞ്ച്',16:'പതിനാറ്',17:'പതിനേഴ്',18:'പതിനെട്ട്',19:'പത്തൊന്‍പത്',20:'ഇരുപത്',
                21:'ഇരുപത്തിയൊന്ന്',22:'ഇരുപത്തിരണ്ട്',23:'ഇരുപത്തിമൂന്ന്',24:'ഇരുപത്തിനാല്',
                25:'ഇരുപത്തിയഞ്ച്',26:'ഇരുപത്തിയാറ്',27:'ഇരുപത്തിയേഴ്',28:'ഇരുപത്തിയെട്ട്',29:'ഇരുപത്തിയൊന്‍പത്',
                30:'മുപ്പത്',31:'മുപ്പത്തിയൊന്ന്',32:'മുപ്പത്തിരണ്ട്',33:'മുപ്പത്തിമൂന്ന്',34:'മുപ്പത്തിനാല്',35:'മുപ്പത്തിയഞ്ച്',
                36:'മുപ്പത്തിയാറ്',37:'മുപ്പത്തിയേഴ്',38:'മുപ്പത്തിയെട്ട്',39:'മുപ്പത്തിയൊന്‍പത്',40:'നാല്‍പത്',41:'നാല്‍പ്പത്തിയൊന്ന്',
                42:'നാല്‍പ്പത്തിരണ്ട്',43:'നാല്‍പ്പത്തിമൂന്ന്',44:'നാല്‍പ്പത്തിനാല്',45:'നാല്‍പ്പത്തിയഞ്ച്',46:'നാല്‍പ്പത്തി ആറ്',
                47:'നാല്‍പ്പത്തി ഏഴ്',48:'നാല്‍പ്പത്തി എട്ട്',49:'നാല്‍പ്പത്തി ഒന്‍പത്',50:'അമ്പത്',51:'അമ്പത്തി ഒന്ന്',
                52:' അമ്പത്തി രണ്ട്',53:'അമ്പത്തി മൂന്ന്',54:'അമ്പത്തി നാല്',55:' അമ്പത്തി അഞ്ച്',56:' അമ്പത്തി ആറ്',
                57:' അമ്പത്തി ഏഴ്',58:' അമ്പത്തി എട്ട്',59:'അമ്പത്തി ഒമ്പത്',60:'അറുപത്',61:'അറുപത്തി ഒന്ന്',
                62:'അറുപത്തി രണ്ട്',63:'അറുപത്തി മൂന്ന്',64:'അറുപത്തി നാല്',65:'അറുപത്തി അഞ്ച്',66:'അറുപത്തി ആറ്',
                67:'അറുപത്തി ഏഴ്',68:'അറുപത്തി എട്ട്',69:'അറുപത്തി ഒമ്പത്',70:'എഴുപത്',71:'എഴുപത്തി ഒന്ന്',
                72:'എഴുപത്തി രണ്ട്',73:'എഴുപത്തി മൂന്ന്',74:'എഴുപത്തി നാല്',75:'എഴുപത്തി അഞ്ച്',76:'എഴുപത്തി ആറ്',
                77:'എഴുപത്തി ഏഴ്',78:'എഴുപത്തി എട്ട്',79:'എഴുപത്തി ഒമ്പത്',80:'എണ്‍പത്',81:'എണ്‍പത്തി ഒന്ന്',
                82:'എണ്‍പത്തി രണ്ട്',83:'എണ്‍പത്തി മൂന്ന്',84:'എണ്‍പത്തി നാല്',85:'എണ്‍പത്തി അഞ്ച്',
                86:'എണ്‍പത്തി ആറ്',87:'എണ്‍പത്തി ഏഴ്',88:'എണ്‍പത്തി എട്ട്',89:'എണ്‍പത്തി ഒമ്പത്',
                90:'തൊണ്ണൂറ്',91:'തൊണ്ണൂറ്റി ഒന്ന്',92:'തൊണ്ണൂറ്റി രണ്ട്',93:'തൊണ്ണൂറ്റി മൂന്ന്',
                94:'തൊണ്ണൂറ്റി നാല്',95:'തൊണ്ണൂറ്റി അഞ്ച്',96:'തൊണ്ണൂറ്റി ആറ്',97:'തൊണ്ണൂറ്റി ഏഴ്',
                98:'തൊണ്ണൂറ്റി എട്ട്',99:'തൊണ്ണൂറ്റി ഒമ്പത്',100:'നൂറ്'}
        numGujarati={0:'',1:'એક',2:'બે',3:'ત્રણ',4:'ચાર',5:'પાંચ',6:'છ',7:'સાત',8:'આઠ',9:'નવ',
                10:'દસ',11:'અગિયાર',12:'બાર',13:'તેર',14:'ચૌદ',15:'પંદર',16:'સોળ',17:'સતર',18:'અઢાર',19:'ઓગણીસ',
                20:'વીસ',21:'એકવીસ',22:'બાવીસ',23:'તેવીસ',24:'ચોવીસ',25:'પચ્ચીસ',26:'છવીસ',27:'સત્તાવીસ',28:'અઠ્ઠાવીસ',
                29:'ઓગણત્રીસ',30:'ત્રીસ',31:'એકત્રીસ',32:'બત્રીસ',33:'તેત્રીસ',34:'ચોત્રીસ',35:'પાંત્રીસ',36:'છત્રીસ',37:'સડત્રીસ',
                38:'અડત્રીસ',39:'ઓગણચાલીસ',40:'ચાલીસ',41:'એકતાલીસ',42:'બેતાલીસ',43:'તેતાલીસ',44:'ચુંમાલીસ',45:'પિસ્તાલીસ',
                46:'છેતાલીસ',47:'સુડતાલીસ',48:'અડતાલીસ',49:'ઓગણપચાસ',50:'પચાસ',51:'એકાવન',52:'બાવન',53:'ત્રેપન',54:'ચોપન',
                55:'પંચાવન',56:'છપ્પન',57:'સત્તાવન',58:'અઠ્ઠાવન',59:'ઓગણસાઠ',60:'સાઈઠ',61:'એકસઠ',62:'બાસઠ',63:'ત્રેસઠ',64:'ચોસઠ',
                65:'પાંસઠ',66:'છાસઠ',67:'સડસઠ',68:'અડસઠ',69:'અગણોસિત્તેર',70:'સીત્તેર',71:'એકોતેર',72:'બોતેર',73:'તોતેર',74:'ચુમોતેર',
                75:'પંચોતેર',76:'છોતેર',77:'સીત્યોતેર',78:'ઇઠ્યોતેર',79:'ઓગણાએંસી',80:'એંસી',81:'એક્યાસી',82:'બ્યાસી',83:'ત્યાસી',
                84:'ચોર્યાસી',85:'પંચાસી',86:'છ્યાસી',87:'સિત્યાસી',88:'ઈઠ્યાસી',89:'નેવ્યાસી',90:'નેવું',91:'એકાણું',92:'બાણું',
                93:'ત્રાણું',94:'ચોરાણું',95:'પંચાણું',96:'છન્નું',97:'સત્તાણું',98:'અઠ્ઠાણું',99:'નવ્વાણું',100:'સો'}
        numBengali={0:'',1:'এক',2:'দুই',3:'তিন',4:'চার',5:'পাঁচ',6:'ছয়',7:'সাত',8:'আট',9:'নয়',10:'দশ',11:'এগার',
                12:'বার',13:'তের',14:'চৌদ্দ',15:'পনের',16:'ষোল',17:'সতের',18:'আঠার',19:'ঊনিশ',20:'বিশ',21:'একুশ',22:'বাইশ',
                23:'তেইশ',24:'চব্বিশ',25:'পঁচিশ',26:'ছাব্বিশ',27:'সাতাশ',28:'আঠাশ',29:'ঊনত্রিশ',30:'ত্রিশ',31:'একত্রিশ',32:'বত্রিশ',
                33:'তেত্রিশ',34:'চৌত্রিশ',35:'পঁয়ত্রিশ',36:'ছত্রিশ',37:'সাঁইত্রিশ',38:'আটত্রিশ',39:'ঊনচল্লিশ',40:'চল্লিশ',41:'একচল্লিশ',
                42:'বিয়াল্লিশ',43:'তেতাল্লিশ',44:'চুয়াল্লিশ',45:'পঁয়তাল্লিশ',46:'ছেচল্লিশ',47:'সাতচল্লিশ',48:'আটচল্লিশ',49:'ঊনপঞ্চাশ',
                50:'পঞ্চাশ',51:'একান্ন',52:'বায়ান্ন',53:'তিপ্পান্ন',54:'চুয়ান্ন',55:'পঞ্চান্ন',56:'ছাপ্পান্ন',57:'সাতান্ন',58:'আটান্ন',
                59:'ঊনষাট',60:'ষাট',61:'একষট্টি',62:'বাষট্টি',63:'তেষট্টি',64:'চৌষট্টি',65:'পঁয়ষট্টি',66:'ছেষট্টি',67:'সাতষট্টি',
                68:'আটষট্টি',69:'ঊনসত্তর',70:'সত্তর',71:'একাত্তর',72:'বাহাত্তর',73:'তিয়াত্তর',74:'চুয়াত্তর',75:'পঁচাত্তর',76:'ছিয়াত্তর',
                77:'সাতাত্তর',78:'আটাত্তর',79:'ঊনআশি',80:'আশি',81:'একাশি',82:'বিরাশি',83:'তিরাশি',84:'চুরাশি',85:'পঁচাশি',
                86:'ছিয়াশি',87:'সাতাশি',88:'আটাশি',89:'ঊননব্বই',90:'নব্বই',91:'একানব্বই',92:'বিরানব্বই',93:'তিরানব্বই',94:'চুরানব্বই',
                95:'পঁচানব্বই',96:'ছিয়ানব্বই',97:'সাতানব্বই',98:'আটানব্বই',99:'নিরানব্বই',100:'এক শো'}
        numTelugu={0:'',1:'ఒకటి',2:'రెండు',3:'మూడు',4:'నాలుగు',5:'అయిదు',6:'ఆరు',7:'ఏడు',
                8:'ఎనిమిది',9:'తొమ్మిది',10:'పది',11:'పదకొండు',12:'పన్నెండు',13:'పదమూడు',14:'పధ్నాలుగు',
                15:'పదునయిదు',16:'పదహారు',17:'పదిహేడు',18:'పధ్ధెనిమిది',19:'పందొమ్మిది',20:'ఇరవై',
                21:'ఇరవై ఒకటి',22:'ఇరవై రెండు',23:'ఇరవై మూడు',24:'ఇరవై నాలుగు',25:'ఇరవై అయిదు',
                26:'ఇరవై ఆరు',27:'ఇరవై ఏడు',28:'ఇరవై ఎనిమిది',29:'ఇరవై తొమ్మిది',30:'ముప్పై',
                31:'ముప్పై ఒకటి',32:'ముప్పై రెండు',33:'ముప్పై మూడు',34:'ముప్పై నాలుగు',35:'ముప్పై ఐదు',
                36:'ముప్పై ఆరు',37:'ముప్పై ఏడు',38:'ముప్పై ఎనిమిది',39:'ముప్పై తొమ్మిది',40:'నలభై',
                41:'నలభై ఒకటి',42:'నలభై రెండు',43:'నలభై మూడు',44:'నలభై నాలుగు',45:'నలభై అయిదు',
                46:'నలభై ఆరు',47:'నలభై ఏడు',48:'నలభై ఎనిమిది',49:'నలభై తొమ్మిది',50:'యాభై',
                51:'యాభై ఒకటి',52:'యాభై రెండు',53:'యాభై మూడు',54:'యాభై నాలుగు',55:'యాభై అయిదు',
                56:'యాభై ఆరు',57:'యాభై ఏడు',58:'యాభై ఎనిమిది',59:'యాభై తొమ్మిది',60:'అరవై',
                61:'అరవై ఒకటి',62:'అరవై రెండు',63:'అరవై మూడు',64:'అరవై నాలుగు',65:'అరవై అయిదు',
                66:'అరవై ఆరు',67:'అరవై ఏడు',68:'అరవై ఎనిమిది',69:'అరవై తొమ్మిది',70:'డెబ్బై',
                71:'డెబ్బై ఒకటి',72:'డెబ్బై రెండు',73:'డెబ్బై మూడు',74:'డెబ్బై నాలుగు',75:'డెబ్బై అయిదు',
                76:'డెబ్బై ఆరు',77:'డెబ్బై ఏడు',78:'డెబ్బై ఎనిమిది',79:'డెబ్బై తొమ్మిది',80:'ఎనభై',
                81:'ఎనభై ఒకటి',82:'ఎనభై రెండు',83:'ఎనభై మూడు',84:'ఎనభై నాలుగు',85:'ఎనభై అయిదు',
                86:'ఎనభై ఆరు',87:'ఎనభై ఏడు',88:'ఎనభై ఎనిమిది',89:'ఎనభై తొమ్మిది',90:'తొంభై',
                91:'తొంభై ఒకటి',92:'తొంభై రెండు',93:'తొంభై మూడు',94:'తొంభై నాలుగు',95:'తొంభై అయిదు',
                96:'తొంభై ఆరు',97:'తొంభై ఏడు',98:'తొంభై ఎనిమిది',99:'తొంభై తొమ్మిది',100:'వంద'}
        numMarathi={0:'',1:'एक',2:'दोन',3:'तीन',4:'चार',5:'पाच',6:'सहा',7:'सात',8:'आठ',9:'नऊ',10:'दहा',
                11:'अकरा',12:'बारा',13:'तेरा',14:'चौदा',15:'पंधरा',16:'सोळा',17:'सतरा',18:'अठरा',19:'एकोणीस',
                20:'वीस',21:'एकवीस',22:'बावीस',23:'तेवीस',24:'चोवीस',25:'पंचवीस',26:'सव्वीस',27:'सत्तावीस',
                28:'अठ्ठावीस',29:'एकोणतीस',30:'तीस',31:'एकतीस',32:'बत्तीस',33:'तेहेतीस',34:'चौतीस',
                35:'पस्तीस',36:'छत्तीस',37:'सदतीस',38:'अडतीस',39:'एकोणचाळीस',40:'चाळीस',41:'एक्केचाळीस',
                42:'बेचाळीस',43:'त्रेचाळीस',44:'चव्वेचाळीस',45:'पंचेचाळीस',46:'सेहेचाळीस',47:'सत्तेचाळीस',
                48:'अठ्ठेचाळीस',49:'एकोणपन्नास',50:'पन्नास',51:'एक्कावन्न',52:'बावन्न',53:'त्रेपन्न',54:'चोपन्न',
                55:'पंचावन्न',56:'छप्पन्न',57:'सत्तावन्न',58:'अठ्ठावन्न',59:'एकोणसाठ',60:'साठ',61:'एकसष्ठ',
                62:'बासष्ठ',63:'त्रेसष्ठ',64:'चौसष्ठ',65:'पासष्ठ',66:'सहासष्ठ',67:'सदुसष्ठ',68:'अडुसष्ठ',
                69:'एकोणसत्तर',70:'सत्तर',71:'एक्काहत्तर',72:'बाहत्तर',73:'त्र्याहत्तर',74:'चौर्‍याहत्तर',75:'पंच्याहत्तर',
                76:'शहात्तर',77:'सत्याहत्तर',78:'अठ्ठ्याहत्तर',79:'एकोण ऐंशी',80:'ऐंशी',81:'एक्क्याऐंशी',82:'ब्याऐंशी',
                83:'त्र्याऐंशी',84:'चौऱ्याऐंशी',85:'पंच्याऐंशी',86:'शहाऐंशी',87:'सत्त्याऐंशी',88:'अठ्ठ्याऐंशी',89:'एकोणनव्वद',
                90:'नव्वद',91:'एक्क्याण्णव',92:'ब्याण्णव',93:'त्र्याण्णव',94:'चौऱ्याण्णव',95:'पंच्याण्णव',96:'शहाण्णव',
                97:'सत्त्याण्णव',98:'अठ्ठ्याण्णव',99:'नव्यान्नव',100:'शंभर'}
        numPunjabi={0:'',1:'ਇੱਕ',2:'ਦੋ',3:'ਤਿੰਨ',4:'ਚਾਰ',5:'ਪੰਜ',6:'ਛੇ',7:'ਸੱਤ',8:'ਅੱਠ',9:'ਨੌ',10:'ਦਸ',
                11:'ਗਿਆਰਾਂ',12:'ਬਾਰਾਂ',13:'ਤੇਰਾਂ',14:'ਚੌਦਾਂ',15:'ਪੰਦਰਾਂ',16:'ਸੋਲਾਂ',17:'ਸਤਾਰਾਂ',18:'ਅਠਾਰਾਂ',19:'ਉੱਨੀ',
                20:'ਵੀਹ',21:'ਇੱਕੀ',22:'ਬਾਈ',23:'ਤੇਈ',24:'ਚੌਬੀ',25:'ਪੱਚੀ',26:'ਛੱਬੀ',27:'ਸਤਾਈ',28:'ਅਠਾਈ',29:'ਉਨੱਤੀ',
                30:'ਤੀਹ',31:'ਇਕੱਤੀ',32:'ਬੱਤੀ',33:'ਤੇਤੀ',34:'ਚੌਂਤੀ',35:'ਪੈਂਤੀ',36:'ਛੱਤੀ',37:'ਸੈਂਤੀ',38:'ਅਠੱਤੀ',39:'ਉਨਤਾਲੀ',
                40:'ਚਾਲੀ',41:'ਇਕਤਾਲੀ',42:'ਬਿਆਲੀ',43:'ਤਰਤਾਈ',44:'ਚੁਤਾਲੀ',45:'ਪਨਤਾਲੀ',46:'ਛਿਆਲੀ',47:'ਸਨਤਾਲੀ',
                48:'ਅਠਤਾਲੀ',49:'ਉਨੰਜਾ',50:'ਪੰਜਾਹ',51:'ਇਕਵੰਜਾ',52:'ਬਵੰਜਾ',53:'ਤਰਵੰਜਾ',54:'ਚਰਵੰਜਾ',55:'ਪਚਵੰਜਾ',
                56:'ਛਪੰਜਾ',57:'ਸਤਵੰਜਾ',58:'ਅਠਵੰਜਾ',59:'ਉਨਾਹਠ',60:'ਸੱਠ',61:'ਇਕਾਹਠ',62:'ਬਾਹਠ',63:'ਤਰੇਂਹਠ',
                64:'ਚੌਂਹਠ',65:'ਪੈਂਹਠ',66:'ਛਿਆਹਠ',67:'ਸਤਾਹਠ',68:'ਅਠਾਹਠ',69:'ਉਨੱਤਰ',70:'ਸੱਤਰ',71:'ਇਕਹੱਤਰ',
                72:'ਬਹੱਤਰ',73:'ਤਹੇਤਰ',74:'ਚਹੱਤਰ',75:'ਪਚੱਤਰ',76:'ਛਿਅੱਤਰ',77:'ਸਤੱਤਰ',78:'ਅਠੱਤਰ',79:'ਉਨਾਸੀ',
                80:'ਅੱਸੀ',81:'ਇਕਆਸੀ',82:'ਬਿਆਸੀ',83:'ਤਿਰਾਸੀ',84:'ਚੌਰਾਸੀ',85:'ਪਚਾਸੀ',86:'ਛਿਆਸੀ',87:'ਸਤਾਸੀ',
                88:'ਅਠਾਸੀ',89:'ਉਨੱਨਵੇਂ',90:'ਨੱਬੇ',91:'ਇਕੱਨਵੇ',92:'ਬੱਨਵੇ',93:'ਤਰੱਨਵੇ',94:'ਚਰੱਨਵੇ',95:'ਪਚੱਨਵੇ',
                96:'ਛਿਅੱਨਵੇ',97:'ਸਤੱਨਵੇ',98:'ਅਠੱਨਵੇ',99:'ਨੜਿੱਨਵੇ',100:'ਸੌ'}
        numKannada={0:'',1:'ಒಂದು',2:'ಎರಡು',3:'ಮೂರು',4:'ನಾಲ್ಕು',5:'ಅಯ್ದು',6:'ಆರು',7:'ಏಳು',8:'ಎಂಟು',
                9:'ಒಂಬತ್ತು',10:'ಹತ್ತು',11:'ಹನ್ನೊಂದು',12:'ಹನ್ನೆರಡು',13:'ಹದಿಮೂರು',14:'ಹದಿನಾಲ್ಕು',15:'ಹದಿನೈದು',
                16:'ಹದಿನಾರು',17:'ಹದಿನೇಳು',18:'ಹದಿನೆಂಟು',19:'ಹತ್ತೊಂಬತ್ತು',20:'ಇಪ್ಪತ್ತು',21:'ಇಪ್ಪತ್ತ್\’ಒಂದು',
                22:'ಇಪ್ಪತ್ತ್\’ಎರಡು',23:'ಇಪ್ಪತ್ತ್\’ಮೂರು',24:'ಇಪ್ಪತ್ತ್\’ನಾಲ್ಕು',25:'ಇಪ್ಪತ್ತ್\’ಐದು',26:'ಇಪ್ಪತ್ತ್\’ಆರು',
                27:'ಇಪ್ಪತ್ತ್\’ಏಳು',28:'ಇಪ್ಪತ್ತ್\’ಎಂಟು',29:'ಇಪ್ಪತ್ತ್\’ಒಂಬತ್ತು',30:'ಮೂವತ್ತು',31:'ಮುವತ್ತ್\’ಒಂದು',
                32:'ಮುವತ್ತ್\’ಎರಡು',33:'ಮುವತ್ತ್\’ಮೂರು',34:'ಮೂವತ್ತ್\’ನಾಲ್ಕು',35:'ಮೂವತ್ತ್\’ಐದು',36:'ಮೂವತ್ತ್\’ಆರು',
                37:'ಮೂವತ್ತ್\’ಏಳು',38:'ಮೂವತ್ತ್\’ಎಂಟು',39:'ಮೂವತ್ತ್\’ಒಂಬತ್ತು',40:'ನಲವತ್ತು',50:'ಐವತ್ತು',
                60:'ಅರುವತ್ತು',70:'ಎಪ್ಪತ್ತು',80:'ಎಂಬತ್ತು',90:'ತೊಂಬತ್ತು',100:'ನೂರು'}
                                                        

#',1000:'ആയിരം',100000:'ലക്ഷം',10000000:'കോടി',1000000000:''ലക്ഷം കോടി) 0:'പൂജ്യം'

#',1000:'ହଜାର',100000:'ଲକ୍ଷ',10000000:'କୋଟି',1000000000:''ଅରବ (ଦଶ କୋଟି)'
        #Indian Counting System
        k=1000
        oneLakh=k*100
        tenLakh=k*1000
        crore=k*10000
        tenCrore=k*100000
        arab=k*1000000
        tenArab=10000000000
        kharab=100000000000
        tenKharab=1000000000000
        neela=10000000000000
        tenNeela=100000000000000
        padma=1000000000000000
        tenPadma=10000000000000000
        shangkha=100000000000000000
        tenShangkha=1000000000000000000
        
        assert(0 <= number)
        
        if number < 100: #and isinstance(number,float)==False
            if language == 'hindi':
                return numHindi[number]
            elif language == 'marathi':
                return numMarathi[number]
            elif language == 'gujarati':
                return numGujarati[number]
            elif language == 'punjabi':
                return numPunjabi[number]
            elif language == 'kannada':
                return numKannada[number]
            elif language == 'malayalam':
                return numMalayalam[number]
            elif language == 'telugu':
                return numTelugu[number]
            elif language == 'odia':
                return numOdia[number]
            elif language == 'bengali':
                return numBengali[number]
            elif language == 'marathi':
                return numMarathi[number]
                
        elif number < 1000:
            if number % 100 == 0:
                if language == 'hindi':
                    return numHindi[number // 100] + ' सौ'
                if language == 'gujarati':
                    return numGujarati[number // 100] + ' સો'
                if language == 'marathi':
                    return numMarathi[number // 100] + ' शंभर'
                if language == 'punjabi':
                    return numPunjabi[number // 100] + ' ਸੌ'
                if language == 'odia':
                    return numOdia[number // 100] + ' ଶହେ'
                if language == 'bengali':
                    return numBengali[number // 100] + ' শত'
                if language == 'telugu':
                    return numTelugu[number // 100] + ' వంద'
                if language == 'malayalam':
                    return numMalayalam[number // 100] + ' നൂറ്'
                if language == 'kannada':
                    return numKannada[number // 100] + ' ನೂರು'
            else:
                if language == 'hindi':
                    return numHindi[number // 100] + ' सौ ' + self.readNumber(number % 100,language)
                if language == 'gujarati':
                    return numGujarati[number // 100] + ' સો ' + self.readNumber(number % 100,language)
                if language == 'marathi':
                    return numMarathi[number // 100] + ' शंभर ' + self.readNumber(number % 100,language)
                if language == 'punjabi':
                    return numPunjabi[number // 100] + ' ਸੌ ' + self.readNumber(number % 100,language)
                if language == 'odia':
                    return numOdia[number // 100] + ' ଶହେ ' + self.readNumber(number % 100,language)
                if language == 'bengali':
                    return numBengali[number // 100] + ' শত ' + self.readNumber(number % 100,language)
                if language == 'telugu':
                    return numTelugu[number // 100] + ' వంద ' + self.readNumber(number % 100,language)
                if language == 'malayalam':
                    return numMalayalam[number // 100] + ' നൂറ് ' + self.readNumber(number % 100,language)
                if language == 'kannada':
                    return numKannada[number // 100] + ' ನೂರು ' + self.readNumber(number % 100,language)
        elif number < 10000: #less than ten thousand
            if language == 'hindi':
                return numHindi[number // 1000] + ' हजार ' + self.readNumber(number % 1000,language)
            elif language == 'marathi':
                return numMarathi[number // 1000] + ' हजार ' + self.readNumber(number % 1000,language)
            elif language == 'gujarati':
                return numGujarati[number // 1000] + ' હજાર ' + self.readNumber(number % 1000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 1000] + ' ਹਜ਼ਾਰ ' + self.readNumber(number % 1000,language)
            elif language == 'kannada':
                return numKannada[number // 1000] + ' ಸಾವಿರ ' + self.readNumber(number % 1000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 1000] + ' ആയിരം ' + self.readNumber(number % 1000,language)
            elif language == 'telugu':
                return numTelugu[number // 1000] + ' వెయ్యి ' + self.readNumber(number % 1000,language)
            elif language == 'odia':
                return numOdia[number // 1000] + ' ହଜାରେ ' + self.readNumber(number % 1000,language)
            elif language == 'bengali':
                return numBengali[number // 1000] + ' হাজার ' + self.readNumber(number % 1000,language)
    
        elif number < oneLakh: #less than one lakh
            if language == 'hindi':
                return numHindi[number // 1000] + ' हजार ' + self.readNumber(number % 1000,language)
            elif language == 'marathi':
                return numMarathi[number // 1000] + ' हजार ' + self.readNumber(number % 1000,language)
            elif language == 'gujarati':
                return numGujarati[number // 1000] + ' हजार ' + self.readNumber(number % 1000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 1000] + ' हजार ' + self.readNumber(number % 1000,language)
            elif language == 'kannada':
                return numKannada[number // 1000] + ' ಸಾವಿರ ' + self.readNumber(number % 1000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 1000] + ' ആയിരം ' + self.readNumber(number % 1000,language)
            elif language == 'telugu':
                return numTelugu[number // 1000] + ' వెయ్యి ' + self.readNumber(number % 1000,language)
            elif language == 'odia':
                return numOdia[number // 1000] + ' ହଜାରେ ' + self.readNumber(number % 1000,language)
            elif language == 'bengali':
                return numBengali[number // 1000] + ' हजार ' + self.readNumber(number % 1000,language)
                      
        elif number < tenLakh: #less than ten lakh
            if language == 'hindi':
                return numHindi[number // 100000] + ' लाख ' + self.readNumber(number % 100000,language)
            elif language == 'marathi':
                return numMarathi[number // 100000] + ' लाख ' + self.readNumber(number % 100000,language)
            elif language == 'gujarati':
                return numGujarati[number // 1000] + ' लाख ' + self.readNumber(number % 100000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 100000] + ' लाख ' + self.readNumber(number % 100000,language)
            elif language == 'kannada':
                return numKannada[number // 100000] + ' ಲಕ್ಷ ' + self.readNumber(number % 100000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 100000] + ' ലക്ഷം ' + self.readNumber(number % 100000,language)
            elif language == 'telugu':
                return numTelugu[number // 100000] + ' లాక్ ' + self.readNumber(number % 100000,language)
            elif language == 'odia':
                return numOdia[number // 100000] + ' ଲକ୍ଷ ' + self.readNumber(number % 100000,language)
            elif language == 'bengali':
                return numBengali[number // 100000] + ' लाख ' + self.readNumber(number % 100000,language)
        
        elif number < crore: #less than one crore
            if language == 'hindi':
                return numHindi[number // 100000] + ' लाख ' + self.readNumber(number % 100000,language)
            elif language == 'marathi':
                return numMarathi[number // 100000] + ' लाख ' + self.readNumber(number % 100000,language)
            elif language == 'gujarati':
                return numGujarati[number // 100000] + ' लाख ' + self.readNumber(number % 100000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 100000] + ' लाख ' + self.readNumber(number % 100000,language)
            elif language == 'kannada':
                return numKannada[number // 100000] + ' ಲಕ್ಷ ' + self.readNumber(number % 100000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 100000] + ' ലക്ഷം ' + self.readNumber(number % 100000,language)
            elif language == 'telugu':
                return numTelugu[number // 100000] + ' లాక్ ' + self.readNumber(number % 100000,language)
            elif language == 'odia':
                return numOdia[number // 100000] + ' ଲକ୍ଷ ' + self.readNumber(number % 100000,language)
            elif language == 'bengali':
                return numBengali[number // 100000] + ' लाख ' + self.readNumber(number % 100000)            
                #return numHindi[number // 100000] + ' लाख ' + self.readNumber(number % 100000,language)
        elif number < tenCrore: #less than
            if language == 'hindi':
                return numHindi[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'marathi':
                return numMarathi[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'gujarati':
                return numGujarati[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'kannada':
                return numKannada[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'telugu':
                return numTelugu[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'odia':
                return numOdia[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'bengali':
                return numBengali[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
                #return numHindi[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000)   
        elif number < arab: #less than
            if language == 'hindi':
                return numHindi[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'marathi':
                return numMarathi[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'gujarati':
                return numGujarati[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'kannada':
                return numKannada[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'telugu':
                return numTelugu[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'odia':
                return numOdia[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'bengali':
                return numBengali[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
                #return numHindi[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
        elif number < tenArab: #less than
            if language == 'hindi':
                return numHindi[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'marathi':
                return numMarathi[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'gujarati':
                return numGujarati[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'kannada':
                return numKannada[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'telugu':
                return numTelugu[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'odia':
                return numOdia[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'bengali':
                return numBengali[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
                #return numHindi[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
        elif number < kharab: #less than
            if language == 'hindi':
                return numHindi[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'marathi':
                return numMarathi[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'gujarati':
                return numGujarati[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'kannada':
                return numKannada[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'telugu':
                return numTelugu[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'odia':
                return numOdia[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'bengali':
                return numBengali[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
                #return numHindi[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
        elif number < tenKharab: #less than
            if language == 'hindi':
                return numHindi[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'marathi':
                return numMarathi[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'gujarati':
                return numGujarati[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'kannada':
                return numKannada[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'telugu':
                return numTelugu[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'odia':
                return numOdia[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'bengali':
                return numBengali[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
 
                #return numHindi[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
        elif number < neela: #less than
            if language == 'hindi':
                return numHindi[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'marathi':
                return numMarathi[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'gujarati':
                return numGujarati[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'kannada':
                return numKannada[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'telugu':
                return numTelugu[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'odia':
                return numOdia[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'bengali':
                return numBengali[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
                #return numHindi[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
        elif number < tenNeela: #less than
            if language == 'hindi':
                return numHindi[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'marathi':
                return numMarathi[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'gujarati':
                return numGujarati[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'kannada':
                return numKannada[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'telugu':
                return numTelugu[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'odia':
                return numOdia[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'bengali':
                return numBengali[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)

                #return numHindi[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
        elif number < padma: #less than
            if language == 'hindi':
                return numHindi[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'marathi':
                return numMarathi[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'gujarati':
                return numGujarati[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'kannada':
                return numKannada[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'telugu':
                return numTelugu[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'odia':
                return numOdia[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'bengali':
                return numBengali[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)

                #return numHindi[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
        elif number < tenPadma: #less than
            if language == 'hindi':
                return numHindi[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'marathi':
                return numMarathi[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'gujarati':
                return numGujarati[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'punjabi':
                return numPunjabi[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'kannada':
                return numKannada[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'malayalam':
                return numMalayalam[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'telugu':
                return numTelugu[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'odia':
                return numOdia[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'bengali':
                return numBengali[number // padma] + ' नील ' + self.readNumber(number % padma,language)

                #return numHindi[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
        elif number < shangkha: #less than
            if language == 'hindi':
                return numHindi[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'marathi':
                return numMarathi[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'gujarati':
                return numGujarati[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'punjabi':
                return numPunjabi[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'kannada':
                return numKannada[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'malayalam':
                return numMalayalam[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'telugu':
                return numTelugu[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'odia':
                return numOdia[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'bengali':
                return numBengali[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
          
                #return numHindi[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
        elif number < tenShangkha: #less than
            if language == 'hindi':
                return numHindi[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'marathi':
                return numMarathi[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'gujarati':
                return numGujarati[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'punjabi':
                return numPunjabi[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'kannada':
                return numKannada[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'malayalam':
                return numMalayalam[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'telugu':
                return numTelugu[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'odia':
                return numOdia[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'bengali':
                return numBengali[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)

                #return numHindi[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
        elif number >= tenShangkha : #less than
            if language == 'hindi':
                return numHindi[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'marathi':
                return numMarathi[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'gujarati':
                return numGujarati[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'punjabi':
                return numPunjabi[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'kannada':
                return numKannada[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'malayalam':
                return numMalayalam[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'telugu':
                return numTelugu[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'odia':
                return numOdia[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'bengali':
                return numBengali[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)

                #return numHindi[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha)
        raise AssertionError('the number is too large: %s' % str(number))
    
    def parseSymbols(self, sentence,language):
        #comma separated 12,300 or 12,300.00
        numWithComma= '[\d]+[.,\d]+'
        #decimal / floats 0.123 or .123
        decimal='[\d]*[.][\d]+'
        #number 1234
        numbers='[\d]+'
        #all types of number
        wholeNumber = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
        
        numbersAll=''.join(re.findall(wholeNumber,sentence))
        # print(numbersAll)
        sentence=sentence.replace(numbersAll,self.readNumber(int(numbersAll),language))
        
        return sentence

class TextProcessor(object):
    def engDevaToEngIPA(self,text,lang='hindi'):
            sp = SymbolParser()
            allTexts=[]
            #mapping phonemes: handle phonemic ligular correspondence
            if lang=='odia':
                matra=''.join(re.findall('[ାି]',text))
                text=text.replace('ଚ଼','ଚ')#old odia
                text=text.replace('କ୍ଷ','ख्य')
                text = text.replace('ଜ୍ଞ'+matra, 'ग्य'+matra+'ँ')
                text = text.replace('ଜ୍ଞ', 'ग्यँ')#ज्ञ
            elif lang=='bengali' or lang=='assamese':
                #re.finditer(r'\bdr', text, re.IGNORECASE)
                #find dr as unique word, use \bdr\b.
                conso = '[কখগঘঙহচছজঝযঞটঠডঢণষরতথদধনলপফবভমশসব]'

                text = text.replace('শ্ম', 'শ')#শ্মশানকালীর = ʃoʃɑnkɑliɾ
                text = text.replace('স্ম', 'স')#smriti = sriti

                text = text.replace('ো','ো')
                text = text.replace('ব্ব', '্-ব')
                text = text.replace('্ব', '')#স্ ব সিব্বল স্বর্ণ	শ্বামী
                text = text.replace('্-ব','ব্ব')
                #মুখস্থ
                dntSa=''.join(re.findall('স্'+conso,text))#dental স্ followed by other consonant
                if len(dntSa)>0:
                    if dntSa[2] != 'ব':
                        dntSa=dntSa.replace(dntSa[0]+'্','s')
                        text=text.replace(''.join(re.findall('স্'+conso,text)),dntSa)

                if text.startswith('ক্ষ'):
                    text = text.replace('ক্ষ','ख',1)
                elif len(text)>=2:
                    if text[1]=='্' and text[2]=='য':
                        text = text.replace('্য', '্æ', 1)
                        text = text.replace('æা', 'æ')

                jya=''.join(re.findall(conso+'্য',text))
                if len(jya)>0:
                    jya=jya.replace(jya[0],jya[0]+'্'+jya[0])
                    #print('jyaa',jya)
                    jya = jya.replace('্য','')
                    text=text.replace(''.join(re.findall(conso+'্য',text)),jya)

                text = text.replace('ক্ষ', 'क्ख')
                text=text.replace('য়','য়')
            elif lang=='gujarati':
                if text.startswith('જ્ઞ'):
                    text.replace('જ્ઞ','ग्य')
                elif text.startswith('ક્ષ'):
                    text.replace('ક્ષ','छ')
                text.replace('જ્ઞ', 'ग्न')

            text=text.replace('ೋ','ೋ')
                #স্বার্থপরের
                #श्बार्थपरेर
                #নিখ ে া ঁ জ
                #নিখ ে া ঁ জ
                #निखेाँज
            #mapping one to one graphemes
            odiToDev={'ଡ଼':'ड़','ଢ଼':'ढ़','଼':'़',
                      'କ':'क','ଖ':'ख','ଗ':'ग','ଘ':'घ','ଙ':'ङ','ହ':'ह',
                      'ଚ':'च','ଛ':'छ','ଜ':'ज','ଝ':'झ','ୟ':'य',
                      'ଞ':'ञ','ଟ':'ट','ଠ':'ठ','ଡ':'ड','ଢ':'ढ',
                      'ଣ':'ण','ଷ':'स','ର':'र','ତ':'त','ଥ':'थ',
                      'ଦ':'द','ଧ':'ध','ନ':'न','ଲ':'ल','ପ':'प',
                      'ଫ':'फ','ବ':'ब','ଭ':'भ','ମ':'म',
                      'ଶ':'स','ସ':'स','ୱ':'व','ଵ':'व','୍':'्',
                      'ା':'ा','ି':'ि','ୀ':'ी','ୁ':'ु','ୂ':'ू','ୃ':'्रु','ୄ':'ॄ','ୢ':'ॢ',
                      'ୣ':'ॣ','େ':'े','ୈ':'इ','ୋ':'ो','ୌ':'ौ','ଁ':'ँ',
                      'ଂ':'ं','ଃ':'ः','ଅ':'अ','ଆ':'आ','ଇ':'इ','ଈ':'ई','ଉ':'उ','ଊ':'ऊ','ଋ':'रु',
                      'ୠ':'ॠ','ଏ':'ए','ଐ':'ऐ','ଓ':'ओ','ଔ':'औ',
                      'ଯ':'य़','ଳ':'ळ','୦':'०','୧':'१','୨':'२','୩':'३','୪':'४','୫':'५','୬':'६'
                      ,'୭':'७','୮':'८','୯':'९'}#দীর্ঘস্থায ় ী
            assmBanglaToDev={'ড়':'र','ঢ়':'ढ़','়':'़',
                      'ক':'क','খ':'ख','গ':'ग','ঘ':'घ','ঙ':'ङ','হ':'ह',
                      'চ':'च','ছ':'छ','জ':'ज','ঝ':'झ','য়':'य',
                      'ঞ':'ञ','ট':'ट','ঠ':'ठ','ড':'ड','ঢ':'ढ',
                      'ণ':'न','স':'श','র':'र','ত':'त','ৎ':'त्','থ':'थ',
                      'দ':'द','ধ':'ध','ন':'न','ল':'ल','প':'प',
                      'ফ':'फ','ব':'ब','ভ':'भ','ম':'म',
                      'শ':'श','ষ':'श','ৱ':'व','্':'्',
                      'া':'ा','ি':'ि','ী':'ी','ু':'ु','ূ':'ू','ৃ':'्रि','ৄ':'ॄ','ৢ':'ॢ',
                      'ৣ':'ॣ','ে':'े','ৈ':'ोइ','ো':'ो','ৌ':'ौ','ঁ':'ँ',
                      'ং':'ं','ঃ':'ः','অ':'अ','আ':'आ','ই':'इ','ঈ':'ई','উ':'उ','ঊ':'ऊ',
                      'ঋ':'रि','ৠ':'ॠ','এ':'ए','ঐ':'ओइ','ও':'ओ','ঔ':'औ',
                      'য':'ज','০':'०','১':'१','২':'२','৩':'३','৪':'४','৫':'५','৬':'६'
                      ,'৭':'७','৮':'८','৯':'९'}#ज palatel affricate
            kannaToDev={'ಕ':'क','ಖ':'ख','ಗ':'ग','ಘ':'घ',
                        'ಙ':'ङ','ಹ':'ह','ಚ':'च','ಛ':'छ','ಜ':'ज','ಝ':'झ','ಯ':'य','ಞ':'ञ',
                        'ಟ':'ट','ಠ':'ठ','ಡ':'ड','ಢ':'ढ','ಣ':'ण','ಷ':'ष','ರ':'र','ತ':'त',
                        'ಥ':'थ','ದ':'द','ಧ':'ध','ನ':'न','ಲ':'ल','ಪ':'प','ಫ':'फ','ಬ':'ब',
                        'ಭ':'भ','ಮ':'म','ಶ':'श','ಸ':'स','ವ':'व','್':'्',
                        'ಾ':'ा','ಿ':'ि','ೀ':'ी','ು':'ु','ೂ':'ू',
                        'ೃ':'रु','ೄ':'रू','ೆ':'ॆ','ೇ':'े','ೈ':'ै','ೋ':'ो',
                        'ೊ':'ॊ','ೌ':'ौ','ಂ':'ं','ಃ':'ः','ಅ':'अ','ಆ':'आ','ಇ':'इ',
                        'ಈ':'ई','ಉ':'उ','ಊ':'ऊ','ಋ':'रु','ಎ':'ऎ','ಏ':'ए','ಐ':'ऐ',
                        'ಒ':'ऒ','ಓ':'ओ','ಔ':'औ','ಳ':'ळ','೦':'०'
                        ,'೧':'१','೨':'२','೩':'३','೪':'४','೫':'५','೬':'६',
                        '೭':'७','೮':'८','೯':'९'} #ಹ ೋ ಗ ು  ಹ ೋ ಗ ು
            #'ೊ':'<short o>' = ॊ
            #'ಒ':'<short o>' = ऒ
            #'ಎ':'<short e>' = ऎ
            #'ೆ':'<short e>' = ॆ
            #ಳ = la (retroflex flap)
            #ಹೋಗು
            #ಒಫ಼್
            #ವಿಧಿಸುತ್ತದೆಯೇ, ಸುಧಾರಣೆಗಳು, ಖಾಜಿ, ೧೯೩೧ क्
            #ಹಲೋನೀವು हलोनिೕवु
            text=text.replace('ై','ై')
            teluguToDev={'క':'क','ఖ':'ख','గ':'ग','ఘ':'घ',
                        'ఙ':'ङ','హ':'ह','చ':'च','ఛ':'छ','జ':'ज','ఝ':'झ','య':'य','ఞ':'ञ',
                        'ట':'ट','ఠ':'ठ','డ':'ड','ఢ':'ढ','ణ':'ण','ష':'ष','ర':'र','త':'त',
                        'థ':'थ','ద':'द','ధ':'ध','న':'न','ల':'ल','ప':'प','ఫ':'फ','బ':'ब',
                        'భ':'भ','మ':'म','శ':'श','స':'स','వ':'व','్':'्',
                        'ా':'ा','ి':'ि','ీ':'ी','ు':'ु','ూ':'ू',
                        'ృ':'रु','ౄ':'रू','ె':'ॆ','ే':'े','ై':'ै','ో':'ो',
                        'ొ':'ॊ','ౌ':'ौ','ఀ':'ँ','ం':'ं','ః':'ः','అ':'अ','ఆ':'आ','ఇ':'इ',
                        'ఈ':'ई','ఉ':'उ','ఊ':'ऊ','ఋ':'रु','ౠ':'रु','ఎ':'ऎ','ఏ':'ए','ఐ':'ऐ',
                        'ఒ':'ऒ','ఓ':'ओ','ఔ':'औ','ళ':'ळ','౦':'०','౧':'१','౨':'२','౩':'३','౪':'४','౫':'५','౬':'६',
                        '౭':'७','౮':'८','౯':'९'}
            malayalamToDev={'ക':'क','ഖ':'ख','ഗ':'ग','ഘ':'घ',
                        'ങ':'ङ','ഹ':'ह','ച':'च','ഛ':'छ','ജ':'ज','ഝ':'झ','യ':'य','ഞ':'ञ',
                        'ട':'ट','ഠ':'ठ','ഡ':'ड','ഢ':'ढ','ണ':'ण','ഷ':'ष','ര':'र','ത':'त',
                        'ഥ':'थ','ദ':'द','ധ':'ध','ന':'न','ല':'ल','പ':'प','ഫ':'फ','ബ':'ब',
                        'ഭ':'भ','മ':'म','ശ':'श','സ':'स','വ':'व','്':'्',
                        'ാ':'ा','ി':'ि','ീ':'ी','ു':'ु','ൂ':'ू',
                        'ൃ':'र','ൄ':'र','െ':'ॆ','േ':'े','ൈ':'ै','ോ':'ो',
                        'ൊ':'ॊ','ൌ':'ौ','ൗ':'ौ','ം':'ं','ഃ':'ः','അ':'अ','ആ':'आ','ഇ':'इ',
                        'പി':'ई','ഉ':'उ','ഊ':'ऊ','ഋ':'र','ൠ':'र','എ':'ऎ','ഏ':'ए','ഐ':'ऐ',
                        'ഒ':'ऒ','ഓ':'ओ','ഔ':'औ','ള':'ळ','റ':'र','ഴ':'l|','ഺ':'r|','൦':'०'
                        ,'൧':'१','൨':'२','൩':'३','൪':'४','൫':'५','൬':'६',
                        '൭':'७','൮':'८','൯':'९'}
                        # ഴ = maḻa/madla generally represented wtih zha. eg mazha = rain
                        # ഺ = stalk ta. kaat =  wind കാറ്റ് = kāṟṟ
                        # ള':'ळ' = പൂള pūḷa
                        #xyxee sdfsdfsdf                        
            gujaratiToDev={'ક':'क','ખ':'ख','ગ':'ग','ઘ':'घ',
                        'ઙ':'ङ','હ':'ह','ચ':'च','છ':'छ','જ':'ज','ઝ':'झ','ય':'य','ઞ':'ञ',
                        'ટ':'ट','ઠ':'ठ','ડ':'ड','ઢ':'ढ','ણ':'ण','ષ':'ष','ર':'र','ત':'त',
                        'થ':'थ','દ':'द','ધ':'ध','ન':'न','લ':'ल','પ':'प','ફ':'फ','બ':'ब',
                        'ભ':'भ','મ':'म','શ':'श','સ':'स','વ':'व','્':'्',
                        'ા':'ा','િ':'ि','ી':'ी','ુ':'ु','ૂ':'ू',
                        'ૃ':'रु','ૄ':'रु','ૅ':'ॆ','ે':'े','ૈ':'ै','ો':'ो',
                        'ૉ':'ॊ','ૌ':'ौ','ં':'ं','ઃ':'ः','અ':'अ','આ':'आ','ઇ':'इ',
                        'ઈ':'ई','ઉ':'उ','ઊ':'ऊ','ઋ':'रु','എ':'ऎ','ઍ':'ए','ઐ':'ऐ',
                        'ഒ':'ऒ','ઓ':'ओ','ઔ':'औ','ળ':'ळ'}
            gurumukhiToDev={'ਁ':'ँ','ਕ':'क','ਖ':'ख','ਖ਼':'ख','ਗ':'ग','ਗ਼':'ग','ਘ':'घ','਼':'़','ੱ':'',
                        'ਙ':'ङ','ਹ':'ह','ਚ':'च','ਛ':'छ','ਜ':'ज','ਜ਼':'ज़','ਝ':'झ','ਯ':'य','ਞ':'ञ',
                        'ਟ':'ट','ਠ':'ठ','ਡ':'ड','ੜ':'ड़','ਢ':'ढ','ਫ਼':'ढ़','ਣ':'ण','`ਰ':'र','ਤ':'त',
                        'ਥ':'थ','ਦ':'द','ਧ':'ध','ਨ':'न','ਲ':'ल','ਲ਼':'ल','ਪ':'प','ਫ':'फ','ਬ':'ब',
                        'ਭ':'भ','ਮ':'म','ਸ਼':'श','ਸ':'स','ਵ':'व','੍':'्',
                        'ਾ':'ा','ਿ':'ि','ੀ':'ी','ੁ':'ु','ੂ':'ू','ੇ':'े','ੈ':'ै','ੋ':'ो',
                        'ੌ':'ौ','ં':'ं','ੰ':'ं','ਃ':'ः','ਅ':'अ','ਆ':'आ','ਇ':'इ',
                        'ਈ':'ई','ਉ':'उ','ਊ':'ऊ','ਏ':'ए','ਐ':'ऐ',
                        'ਓ':'ओ','ਔ':'औ','੦':'०','੧':'१','੨':'२','੩':'३','੪':'४','੫':'५','੬':'६',
                        '੭':'७','੮':'८','੯':'९'}
            # ਸ਼ = sha with nukta 
            # ਲ਼ = la with nukta
            # ਖ਼ = kha with nukta
            # ਗ਼ = ga with nukta
            # ਜ਼ = ja with nukta
            # ੜ = RRA nuktda da
            # ਫ਼ =dha with nukta
            #ਁ =
            #  ਂ = 
            # ੱ = zero mapping

            #murdhanya, talavya sha, short e o
            # ਸ਼ (talavya)
            tamilToDev={'க':'क',
                        'க':'ङ','ஹ':'ह','ச':'च','ஜ':'ज','ய':'य','ஞ':'ञ',
                        'ட':'ट','ண':'ण','ன':'ण','ஶ':'ष','ர':'र','ற':'र्र','த':'त','ந':'न','ல':'ल','ள':'ल|',
                        'ப':'प','ம':'म','ஷ':'श','ஸ':'स','வ':'व','்':'्',
                        'ா':'ा','ி':'ि','ீ':'ी','ு':'ु','ூ':'ू','ெ':'े','ை':'ै','ோ':'ो',
                        'ொ':'ॊ','ௌ':'ौ','ஂ':'ं','ஃ':'ः','அ':'अ','ஆ':'आ','இ':'इ',
                        'ஈ':'ई','உ':'उ','ஊ':'ऊ','எ':'ऎ','ஏ':'ए','ஐ':'ऐ',
                        'ஒ':'ऒ','ஓ':'ओ','ஔ':'औ','ழ':'ळ','௦':'०','௧':'१','௨':'२','௩':'३','௪':'४','௫':'५','௬':'६',
                        '௭':'७','௮':'८','௯':'९'}
            
            #ௗ TAMIL AU LENGTH MARK still to mapped
            #ಅಂ  ə ೈ  əೄ  ə=  ಅಂ ಅಃ
            #getting phonemes 
            for aLetter in text:
                if aLetter in odiToDev:
                    allTexts.append(odiToDev[aLetter])
                elif aLetter in assmBanglaToDev:
                    allTexts.append(assmBanglaToDev[aLetter])
                elif aLetter in kannaToDev:
                    allTexts.append(kannaToDev[aLetter])
                elif aLetter in malayalamToDev:
                    allTexts.append(malayalamToDev[aLetter])
                elif aLetter in gujaratiToDev:
                    allTexts.append(gujaratiToDev[aLetter])
                elif aLetter in gurumukhiToDev:
                    allTexts.append(gurumukhiToDev[aLetter])
                elif aLetter in tamilToDev:
                    allTexts.append(tamilToDev[aLetter])
                elif aLetter in teluguToDev:
                    allTexts.append(teluguToDev[aLetter])
                else:
                    allTexts.append(aLetter)
            text=''.join(allTexts)
            wordInDev=text
            vowelsIndependent = '[अआइईउऊऋॠऌॡ]'
            consoWithNukta = '[क़|क़|ख़|ख़|ग़|ग़|ज़|ज़|झ़|ड़|ड़|फ़|फ़|ढ़|ढ़]'
            conso = '[कखगघङहचछजझञयशटठडढणषरतथदधनलसपफबभमव]'#any one of them

            vowelDiacri = '[ा|ि|ी|ु|ू|ृ|ॄ|ॢ|ॣ|े|ै|ो|ौ|ॉ]'

            #print(sp.parseSymbols('hi i am 507000600000',language='kannada'))
            
            if bool(re.findall('[0-9]', text)) == True:
                # print('number detect',text)
                text=self.engDevaToEngIPA(sp.parseSymbols(text,language=lang),lang)
                text = text.replace('_','')

            if bool(re.search(conso+'$', text)) == True: #ସା ˚ସଦ
                #print('ending with consonant')
                if lang!='odia' and lang!='kannada':
                    text=text+'्' # add this while hindi +'्'
            elif bool(re.search(consoWithNukta + '$', text)) == True:
                text = text # add this while hindi + '्'
            text=text.replace('०','0')
            text = text.replace('१', '1')
            text = text.replace('२', '2')
            text = text.replace('३', '3')
            text = text.replace('४', '4')
            text = text.replace('५', '5')
            text = text.replace('६', '6')
            text = text.replace('७', '7')
            text = text.replace('८', '8')
            text = text.replace('९', '9')
            
            text = text.replace('श़', 'श')#ऑकेश़न्
            text = text.replace('व़', 'व')#क्व़ाक्व़ारेल्ली
            text = text.replace('क़', 'qə')# 0915 क  093C ़ (Nukta)
            text = text.replace('क़', 'qə')# 0958
            text = text.replace('ख़', 'xə')# 0916 ख  093C ़
            text = text.replace('ख़', 'xə')# 0959
            text = text.replace('ग़', 'ɣə')# 0917 ग  093C ़
            text = text.replace('ग़', 'ɣə')# 095A
            text = text.replace('ज़', 'zə')# 091C ज  093C ़
            text = text.replace('ज़', 'zə')# 095B ज़
            text = text.replace('झ़', 'ʒə')#
            text = text.replace('ड़', 'ɽə')# 0921 ड  093C ़
            text = text.replace('ड़', 'ɽə')# 095C
            text = text.replace('फ़', 'fə')# 092B फ  093C ़
            text = text.replace('फ़', 'fə')# 095E
            text = text.replace('ढ़', 'ɽʱə')# 0922 ढ  093C ़
            text = text.replace('ढ़', 'ɽʱə')# 095D
            text = text.replace('ँक', 'ŋक')
            text = text.replace('ंक', 'ŋक')
            text = text.replace('क', 'kə')
            text = text.replace('ँख', 'ŋख')
            text = text.replace('ंख', 'ŋख')
            text = text.replace('ख', 'kʰə')
            text = text.replace('ँग', 'ŋग')# ङ ्
            text = text.replace('ंग', 'ŋग')# ङ
            if bool(re.search('ŋग'+conso, text))==False \
                and bool(re.search('ŋग'+vowelDiacri, text))==False:
                text = text.replace('ŋग', 'ŋ')
            text = text.replace('ग', 'ɡə')
            text = text.replace('य़', '|yə')
            text = text.replace('घ', 'ɡʰə')
            text = text.replace('ङ', 'ŋə')
            text = text.replace('ह', 'hə')
            text = text.replace('च', 't͡ʃə')
            text = text.replace('छ', 't͡ʃʰə')
            text = text.replace('ज', 'd͡ʒə')
            text = text.replace('झ', 'd͡ʒʱə')
            text = text.replace('य', 'jə')
            text = text.replace('ञ', 'ɲə')
            text = text.replace('ट', 'ʈə')
            text = text.replace('ठ', 'ʈʰə')
            text = text.replace('ड', 'ɖə')
            text = text.replace('ढ', 'ɖʱə')
            text = text.replace('ण', 'ɳə')
            text = text.replace('ष', 'ʂə')
            text = text.replace('र', 'ɾə')
            text = text.replace('त', 'tə')
            text = text.replace('थ', 'tʰə')
            text = text.replace('द', 'də')
            text = text.replace('ध', 'dʰə')
            text = text.replace('न', 'nə')
            text = text.replace('ल', 'lə')
            text = text.replace('ळ', '`lə')
            text = text.replace('प', 'pə')
            text = text.replace('फ', 'phə')
            text = text.replace('ब', 'bə')
            text = text.replace('भ', 'bʰə')
            text = text.replace('म', 'mə')
            text = text.replace('श', 'ʃə')
            text = text.replace('स', 'sə')
            text = text.replace('व', 'ʋə')
            text = text.replace('ə्', '')
            text = text.replace('्', '')
            text = text.replace('əा', 'ɑː')
            text = text.replace('ा', 'ɑː')
            text = text.replace('əि', 'i')
            text = text.replace('ि', 'i')
            text = text.replace('əी', 'iː')
            text = text.replace('əु', 'ʊ')
            text = text.replace('ु', 'ʊ')
            text = text.replace('əू', 'uː')
            text = text.replace('əृ', 'r̥')
            text = text.replace('əॄ', '[noMap]ॄ')#exception=============================
            text = text.replace('əॢ', '[noMap]ॢ')#exception=============================
            text = text.replace('əॣ', '[noMap]ॣ')#exception=============================
            text = text.replace('əे', 'eː')
            text = text.replace('əॆ', 'e')
            text = text.replace('əै', 'æː')
            text = text.replace('əो', 'oː')
            text = text.replace('əॊ', 'o')
            text = text.replace('əौ', 'ouː')#
            text = text.replace('ँ', 'n~')
            text = text.replace('ं', 'M')
            text = text.replace('ः', 'h')
            text = text.replace('əॉ', 'ɑː')
            text = text.replace('अ', 'ə')
            text = text.replace('आ', 'ɑː')
            text = text.replace('इ', 'i')
            text = text.replace('ई', 'iː')
            text = text.replace('उ', 'ʊ')
            text = text.replace('ऊ', 'uː')
            text = text.replace('ऋ', 'r̥')
            text = text.replace('ए', 'eː')
            text = text.replace('ऎ', 'e')#short e
            text = text.replace('ऐ', 'æː')
            text = text.replace('ओ', 'oː')
            text = text.replace('ऒ', 'o')#short o
            text = text.replace('औ', 'ouː')#ɔ
            text = text.replace('ऑ', 'ɑː')#exception===
            if lang=='odia':
                text=text.replace('ə','ɔ')
                text = text.replace('ː', '')
            elif lang=='bengali':
                text = text.replace('ə', 'o')
                text = text.replace('ː', '')
            #text+'\t'+wordInDev
            # text = text.replace('_ ', "")
            return text
    def devToCMUDic(self,text,delimiter=False,delimit=''):
        delimit=phoneme_delimiter(delimiting=delimiter,delimit=delimit)

        text = text.replace('क़', 'K'+delimit+'AH'+delimit)  # 0915 क  093C ़ (Nukta)
        text = text.replace('क़', 'K'+delimit+'AH'+delimit)  # 0958
        text = text.replace('ख़', 'K'+delimit+'AH'+delimit)  # 0916 ख  093C ़
        text = text.replace('ख़', 'K'+delimit+'AH'+delimit)  # 0959
        text = text.replace('ग़', 'G'+delimit+'AH'+delimit)  # 0917 ग  093C ़
        text = text.replace('ग़', 'G'+delimit+'AH'+delimit)  # 095A
        text = text.replace('ज़', 'Z'+delimit+'AH'+delimit)  # 091C ज  093C ़
        text = text.replace('ज़', 'Z'+delimit+'AH'+delimit)  # 095B ज़
        text = text.replace('झ़', 'JH'+delimit+'AH'+delimit)  #
        text = text.replace('ड़', 'R'+delimit+'AH'+delimit)  # 0921 ड  093C ़
        text = text.replace('ड़', 'R'+delimit+'AH'+delimit)  # 095C
        text = text.replace('फ़', 'F'+delimit+'AH'+delimit)  # 092B फ  093C ़
        text = text.replace('फ़', 'F'+delimit+'AH'+delimit)  # 095E
        text = text.replace('ढ़', 'R'+delimit+'AH'+delimit)  # 0922 ढ  093C ़
        text = text.replace('ढ़', 'R'+delimit+'AH'+delimit)  # 095D

        text = text.replace('ँक', 'NG'+delimit+'K'+delimit+'AH'+delimit)
        text = text.replace('ंक', 'NG'+delimit+'K'+delimit+'AH'+delimit)
        text = text.replace('क', 'K'+delimit+'AH'+delimit)
        text = text.replace('ँख', 'NG'+delimit+'K'+delimit+'AH'+delimit)
        text = text.replace('ंख', 'NG'+delimit+'K'+delimit+'AH'+delimit)
        text = text.replace('ख', 'K'+delimit+'AH'+delimit)
        text = text.replace('ँग', 'NG'+delimit+'G'+delimit+'AH'+delimit)  # ङ ्
        text = text.replace('ंग', 'NG'+delimit+'G'+delimit+'AH'+delimit)  # ङ
        text = text.replace('ग', 'G'+delimit+'AH'+delimit)
        text = text.replace('घ', 'G'+delimit+'AH'+delimit)
        text = text.replace('ङ', 'NG'+delimit+'AH'+delimit)
        text = text.replace('ह', 'H'+delimit+'AH'+delimit)
        text = text.replace('च', 'CH'+delimit+'AH'+delimit)
        text = text.replace('छ', 'CH'+delimit+'AH'+delimit)
        text = text.replace('ज', 'JH'+delimit+'AH'+delimit)
        text = text.replace('झ', 'JH'+delimit+'AH'+delimit)
        text = text.replace('य', 'Y'+delimit+'AH'+delimit)
        text = text.replace('ञ', 'N'+delimit+'AH'+delimit)
        text = text.replace('ट', 'T'+delimit+'AH'+delimit)
        text = text.replace('ठ', 'T'+delimit+'AH'+delimit)
        text = text.replace('ड', 'D'+delimit+'AH'+delimit)
        text = text.replace('ढ', 'D'+delimit+'AH'+delimit)
        text = text.replace('ण', 'N'+delimit+'AH'+delimit)
        text = text.replace('ष', 'SH'+delimit+'AH'+delimit)
        text = text.replace('र', 'R'+delimit+'AH'+delimit)
        text = text.replace('त', 'TH'+delimit+'AH'+delimit)
        text = text.replace('थ', 'TH'+delimit+'AH'+delimit)
        text = text.replace('द', 'DH'+delimit+'AH'+delimit)
        text = text.replace('ध', 'DH'+delimit+'AH'+delimit)
        text = text.replace('न', 'N'+delimit+'AH'+delimit)
        text = text.replace('ल', 'L'+delimit+'AH'+delimit)
        text = text.replace('प', 'P'+delimit+'AH'+delimit)
        text = text.replace('फ', 'F'+delimit+'AH'+delimit)
        text = text.replace('ब', 'B'+delimit+'AH'+delimit)
        text = text.replace('भ', 'B'+delimit+'AH'+delimit)
        text = text.replace('म', 'M'+delimit+'AH'+delimit)
        text = text.replace('श', 'SH'+delimit+'AH'+delimit)
        text = text.replace('स', 'S'+delimit+'AH'+delimit)
        text = text.replace('व', 'V'+delimit+'AH'+delimit)
        text = text.replace('AH'+delimit+'्', '')
        text = text.replace('्', '')
        text = text.replace('AH'+delimit+'ा', 'AA'+delimit)
        text = text.replace('ा', 'AA'+delimit)
        text = text.replace('AH'+delimit+'ि', 'IH'+delimit)
        text = text.replace('ि', 'IH'+delimit)
        text = text.replace('AH'+delimit+'ी', 'IY'+delimit)
        text = text.replace('AH'+delimit+'ु', 'UH'+delimit)
        text = text.replace('ु', 'UH'+delimit)
        text = text.replace('AH'+delimit+'ू', 'UW'+delimit)
        text = text.replace('AH'+delimit+'ृ', 'R'+delimit)
        text = text.replace('AH'+delimit+'े', 'EY'+delimit)
        text = text.replace('AH'+delimit+'ॆ', 'EH'+delimit)
        text = text.replace('AH'+delimit+'ै', 'AY'+delimit)
        text = text.replace('AH'+delimit+'ो', 'AO'+delimit)
        text = text.replace('AH'+delimit+'ौ', 'OW'+delimit)
        text = text.replace('ँ', 'N'+delimit)
        text = text.replace('ं', 'N'+delimit)
        text = text.replace('AH'+delimit+'ॉ', 'AW'+delimit)
        text = text.replace('अ', 'AH'+delimit)
        text = text.replace('आ', 'AA'+delimit)
        text = text.replace('इ', 'IH'+delimit)
        text = text.replace('ई', 'IY'+delimit)
        text = text.replace('उ', 'UH'+delimit)
        text = text.replace('ऊ', 'UW'+delimit)
        text = text.replace('ऋ', 'R'+delimit)
        text = text.replace('ए', 'EY'+delimit)
        text = text.replace('ऎ', 'EH'+delimit)  # short e
        text = text.replace('ऐ', 'AY'+delimit)
        text = text.replace('ओ', 'AO'+delimit)
        text = text.replace('औ', 'OW'+delimit)
        text = text.replace('ऑ', 'AW'+delimit)  # exception===
        text=text.rstrip()
        return text
    def toDeva(self,text):
        vowels = '[अआइईउऊऋॠऌॡ]'
        consoWithNukta = '[क़|क़|ख़|ख़|ग़|ग़|ज़|ज़|झ़|ड़|ड़|फ़|फ़|ढ़|ढ़]'
        conso = '[कखगघङहचछजझञयशटठडढणषरतथदधनलसपफबभमव]'

        vowelDiacri = '[ा|ि|ी|ु|ू|ृ|ॄ|ॢ|ॣ|े|ै|ो|ौ|ॉ]'
        sufixes = '[\'ing\'|\'hood\'|\'less\'|\'ly\']'

        # अ = a, आ = A,aa, इ = i, ई = I,ee, उ = u, ऊ = U,oo, ऋ = Ru, ॠ = RU, ऌ = ~lu, ॡ = ~lU,
        # ऍ(ॲ) = ~e,~a, ऎ = E, ए = e, ऐ = ai, ऑ = ~o, ऒ = O, ओ = o, औ = au,ou
        # ँ = ~M
        # ं = M
        # ः = H
        # ऽ = &
        # ॐ = oum
        # ₹ = Rs
        text = text.replace('||', '॥')
        text = text.replace('|', '।')
        text = text.replace('&', 'ऽ')
        text = text.replace('OM', 'ॐ')
        text = text.replace('Rs.', '₹')
        text = text.replace('Th','ठ्')
        text = text.replace('Dhx', 'ढ़्')
        text = text.replace('dh','ध्')
        text = text.replace('bh','भ्')
        text = text.replace('sh','श्')
        text = text.replace('ph','फ्')
        text = text.replace('gh','घ्')
        text = text.replace('th','थ्')
        text = text.replace('ng','ङ्')
        text = text.replace('ch','छ्')
        text = text.replace('jh','झ्')
        text = text.replace('Q', 'क़्')
        text = text.replace('X', 'ख़्')
        text = text.replace('G', 'ग़्')
        text = text.replace('Z', 'ज़्')
        text = text.replace('Jh', 'झ़्')
        text = text.replace('Dx', 'ड़्')
        text = text.replace('F', 'फ़्')
        text = text.replace('k', 'क्')
        text = text.replace('g', 'ग्')
        text = text.replace('h','ह्')
        text = text.replace('c','च्')
        text = text.replace('j','ज्')
        text = text.replace('y','य्')
        text = text.replace('J','ञ्')
        text = text.replace('T','ट्')
        text = text.replace('D','ड्')
        text = text.replace('Dh','ढ्')
        text = text.replace('N','ण्')
        text = text.replace('S','ष्')
        text = text.replace('r','र्')
        text = text.replace('t','त्')
        text = text.replace('d','द्')
        text = text.replace('n','न्')
        text = text.replace('l','ल्')
        text = text.replace('p','प्')
        text = text.replace('b','ब्')
        text = text.replace('m','म्')
        text = text.replace('s','स्')
        text = text.replace('v','व्')
        text = text.replace('्aa', 'ा')
        text = text.replace('्ai', 'ै')
        text = text.replace('्au', 'ौ')
        text = text.replace('्a', '')
        text = text.replace('्Ri', 'ृ')#======================
        text = text.replace('्i', 'ि')
        text = text.replace('्ee', 'ी')
        text = text.replace('्u', 'ु')
        text = text.replace('्oo', 'ू')
        text = text.replace('्Ree', 'ॄ')#=====================
        text = text.replace('्Li', 'ॢ')# exception=============================
        text = text.replace('्Lee', 'ॣ') # exception=============================
        text = text.replace('्e', 'े')
        text = text.replace('्o', 'ो')
        text = text.replace('्MM', 'ँ')
        text = text.replace('्M', 'ं')  # exception=============================
        text = text.replace('H', 'ः')  # exception=============================
        text = text.replace('्A', 'ॉ')  # exception=============================
        text = text.replace('MM', 'ँ')
        text = text.replace('M', 'ं')

        text = text.replace('au', 'औ')
        text = text.replace('ai', 'ऐ')
        text = text.replace('aa', 'आ')
        text = text.replace('a', 'अ')
        text = text.replace('i', 'इ')
        text = text.replace('ee', 'ई')
        text = text.replace('u', 'उ')
        text = text.replace('oo', 'ऊ')
        text = text.replace('ri', 'ऋ')
        text = text.replace('e', 'ए')
        text = text.replace('o', 'ओ')
        text = text.replace('A', 'ऑ')  # exception=============================
        return text
    def toSaarthiDevaPhoneme(self,text): #from ipaDIC IPA to Saarthi Devanagari Phonemic
        text = text.replace('ˈ', '')#stress 1
        text = text.replace('ˌ', '')  # stress 2
        #text = text.replace('"', '')

        text = text.replace('eɪ', 'एय्')#two code points
        text = text.replace('e‍ɪ', 'एय्')#three code points
        text = text.replace('e‍ə', 'एअ')
        text = text.replace('ə‍ʊ', 'अव्')
        text = text.replace('aɪ', 'आय्')#two code points
        text = text.replace('a‍ɪ', 'आय्')# tree code points
        text = text.replace('eɪ', 'एय्')
        text = text.replace('aʊ', 'आव्')
        text = text.replace('oʊ', 'आव्')
        text = text.replace('dʒ', 'ज्')
        text = text.replace('tʃ', 'च्')
        text = text.replace('ɜː', 'अ')
        text = text.replace('ɑː', 'आ')
        text = text.replace('ɔː', 'ओ')
        text = text.replace('iː', 'ई')
        text = text.replace('uː', 'ऊ')
        text = text.replace('æ', 'ए')
        text = text.replace('ɝ', 'अर्')
        text = text.replace('ɛ', 'ए')
        text = text.replace('ɑ', 'आ')
        text = text.replace('ə', 'अ')
        text = text.replace('ʌ', 'अ')
        text = text.replace('ɐ', 'अ')
        text = text.replace('ɔ', 'ओ')
        text = text.replace('i', 'ई')
        text = text.replace('ɪ', 'इ')
        text = text.replace('ʊ', 'उ')
        text = text.replace('u', 'उ')
        text = text.replace('ɒ', 'ओ')
        text = text.replace('t', 'ट्')
        text = text.replace('b', 'ब्')
        text = text.replace('ɫ', 'ल्')
        text = text.replace('l', 'ल्')
        text = text.replace('ð', 'द्')
        text = text.replace('d', 'ड्')
        text = text.replace('m', 'म्')
        text = text.replace('n', 'न्')
        text = text.replace('ɹ', 'र्')
        text = text.replace('r', 'र्')
        text = text.replace('ɡ', 'ग्')
        text = text.replace('k', 'क्')
        text = text.replace('ŋ', 'ङ्')
        text = text.replace('θ', 'थ्')
        text = text.replace('v', 'व्')
        text = text.replace('w', 'व्')
        text = text.replace('f', 'फ्')
        text = text.replace('h', 'ह्')
        text = text.replace('p', 'प्')
        text = text.replace('ʃ', 'श्')
        text = text.replace('s', 'स्')
        text = text.replace('z', 'ज़्')
        text = text.replace('ʒ', 'ज्')
        text = text.replace('j', 'य्')
        return text
    def ipaToSaarthiASCII(self,text,delimiter=False,delimit=''): #from Saarthi IPA to Saarthi ASCII 600, 3000 kannada
        delimit=phoneme_delimiter(delimiting=delimiter,delimit=delimit)

        text=text.replace('଼','')#odia gi matamda kakkadaba

        text = text.replace('q', '|k'+delimit)
        text = text.replace('x', '|K'+delimit)
        text = text.replace('ɣ', '|g'+delimit)
        text = text.replace('z', '|j'+delimit)
        text = text.replace('ɽʱ', '|X'+delimit)
        text = text.replace('ɽ', '|x'+delimit)
        text = text.replace('f', 'f'+delimit)
        text = text.replace('kʰ', 'K'+delimit)
        text = text.replace('k', 'k'+delimit)
        text = text.replace('ɡʰ', 'G'+delimit)
        text = text.replace('ɡ', 'g'+delimit)
        text = text.replace('|y', '|y'+delimit)
        text = text.replace('ŋ', 'w'+delimit)
        text = text.replace('h', 'h'+delimit)
        text = text.replace('t͡ʃʰ', 'C'+delimit)
        text = text.replace('t͡ʃ', 'c'+delimit)
        text = text.replace('d͡ʒʱ', 'J'+delimit)
        text = text.replace('j', 'y' + delimit)
        text = text.replace('d͡ʒ', 'j'+delimit)
        text = text.replace('ʒ', '|J'+delimit)
        text = text.replace('ɲ', 'Y'+delimit)
        text = text.replace('ʈʰ', 'V'+delimit)
        text = text.replace('ʈ', 'q'+delimit)
        text = text.replace('ɖʱ',  'X'+delimit)
        text = text.replace('ɖ', 'x'+delimit)
        text = text.replace('ɳ', 'N'+delimit)
        text = text.replace('ʂ', 'S'+delimit)
        text = text.replace('ɾ', 'r'+delimit)
        text = text.replace('tʰ', 'T'+delimit)
        text = text.replace('t', 't'+delimit)
        text = text.replace('dʰ', 'D'+delimit)
        text = text.replace('d', 'd'+delimit)
        text = text.replace('n~', 'n~'+delimit)
        text = text.replace('n', 'n'+delimit)
        text = text.replace('`l', '`l'+delimit)
        text = text.replace('l', 'l'+delimit)
        text = text.replace('ph', 'P'+delimit)
        text = text.replace('p', 'p'+delimit)
        text = text.replace('bʰ', 'B'+delimit)
        text = text.replace('b', 'b'+delimit)
        text = text.replace('m', 'm'+delimit)
        text = text.replace('ʃ', 'z'+delimit)
        text = text.replace('s', 's'+delimit)
        text = text.replace('ʋ', 'v'+delimit)
        text = text.replace('ɑː', 'Aː'+delimit)
        text = text.replace('ɑ', 'A'+delimit)
        text = text.replace('iː', 'Iː'+delimit)
        text = text.replace('i', 'i'+delimit)
        text = text.replace('ʊ', 'u'+delimit)
        text = text.replace('uː', 'Uː'+delimit)
        text = text.replace('U', 'U' + delimit)
        text = text.replace('u', 'u' + delimit)
        text = text.replace('r̥', 'R'+delimit)
        text = text.replace('ouː', 'Oː'+delimit)
        text = text.replace('ou', 'O'+delimit)
        text = text.replace('eː', 'eː'+delimit)
        text = text.replace('e', 'e'+delimit)
        text = text.replace('æː', 'Eː'+delimit)
        text = text.replace('oː', 'oː'+delimit)
        text = text.replace('o', 'o'+delimit)
        text = text.replace('M', 'M'+delimit)
        text = text.replace('h', 'h'+delimit)
        text = text.replace('ə', 'a'+delimit)
        text = text.replace('ɔ', '`a'+delimit)
        text=text.replace('-','-'+delimit)
        #reprocess over aplicable rules : Vipratishede param kaaryam
        text=text.replace(delimit+delimit,delimit)
        text=text.replace(delimit+'~','~')
        text = text.replace(delimit + 'ː', 'ː')

        if len(text)>0:
            if text[-1]=='_':
                text=text[: -1]
                # print('in if')
        '''
        if len(text)>1:
            last=text[-1]
            if last==delimit:
                text=text.replace(text[len(text)-1],'')
        '''
        text = text.rstrip(delimit)
        return text
    def toSaarthiACII(self,text,delimiter=False,delimit=''):

        delimit=phoneme_delimiter(delimiting=delimiter,delimit=delimit)

        text = text.replace('ट्', 'q'+delimit)
        text = text.replace('ब्', 'b'+delimit)
        text = text.replace('ल्', 'l'+delimit)
        text = text.replace('द्', 'd'+delimit)
        text = text.replace('ड्', 'x'+delimit)
        text = text.replace('म्', 'm'+delimit)
        text = text.replace('न्', 'n'+delimit)
        text = text.replace('र्', 'r'+delimit)
        text = text.replace('ग्', 'g'+delimit)
        text = text.replace('क्', 'k'+delimit)
        text = text.replace('ङ्', 'w'+delimit)
        text = text.replace('थ्', 'T'+delimit)
        text = text.replace('व्', 'v'+delimit)
        text = text.replace('फ्', 'P'+delimit)
        text = text.replace('ह्', 'h'+delimit)
        text = text.replace('प्', 'p'+delimit)
        text = text.replace('श्', 'z'+delimit)
        text = text.replace('च्', 'c'+delimit)
        text = text.replace('स्', 's'+delimit)
        text = text.replace('ज़्', '|x'+delimit)
        text = text.replace('ज्', 'j'+delimit)
        text = text.replace('य्', 'y'+delimit)
        text = text.replace('ए', 'eː'+delimit)
        text = text.replace('आ', 'Aː'+delimit)
        text = text.replace('अ', 'a'+delimit)
        text = text.replace('ओ', 'oː'+delimit)
        text = text.replace('ई', 'Iː'+delimit)
        text = text.replace('इ', 'i'+delimit)
        text = text.replace('उ', 'u'+delimit)
        text = text.replace('ऊ', 'Uː'+delimit)

        text = text.replace('्', '')
        #print('in text',text[:-1])
        #print('within func',text)
        if len(text)>0:
            if text[-1]=='_':
                text=text[: -1]
                # print('in if')
        return text

def phoneme_delimiter(delimiting=False,delimit=''):
    if bool(re.findall('[A-Za-z0-9]', delimit)) == True:
        print('delimiter is:', delimit)
        raise SystemExit('number or alphabet cannot be a delimiter')
    elif len(delimit) > 1:
        print('length of delimiter is', len(delimit), delimit)
        raise SystemExit('delimiter must not be more than one letter/character')
    elif delimiting is True:
        delimit = delimit
    else:
        delimit = ''
    return delimit


def get_phonim(text, lang, tp, eng_p):
    if lang == 'en_IN':
        ipaWord = eng_p(text, 'en_saarthi_IN')
    else:
        if lang == 'marathi':
            lang = 'hindi'
        ipaWord=tp.engDevaToEngIPA(text,lang=lang)#get IPA
        ipaWord=tp.ipaToSaarthiASCII(ipaWord,delimiter=True,delimit='_')
    return ipaWord



#indian english lexicon
# ieLex=pd.read_csv('/root/Documents/phonem_inference/TTS_Custom/TTS/tts/utils/text/indian_english_core_lexicon.csv')
# ieLexHeads=ieLex['WordHead'].tolist()
# ieMapped=ieLex['SaarthiASCII'].tolist()
# #odia lexicon
# odiaLex=pd.read_csv('/root/Documents/phonem_inference/TTS_Custom/TTS/tts/utils/text/odia_tts_set.csv')
# odiaLexHeads=odiaLex['WordHead'].tolist()
# odiaMapped=odiaLex['IPA'].tolist()

lang_dict = {
    "bn":'bangali',
    'en':'en_IN',
    'gu':'gujarathi',
    'hi':'hindi',
    'kn':'kannada',
    'ml':'malayalam',
    'mr':'hindi',
    'od':'odia',
    'pa':'punjabi',
    'ta':'tamil',
    'te':'telugu'
}

    
def G2P(sent, language='odia', eng_p=None):

    # print(language, sent)
    tp = TextProcessor()
    phones = []
    sent = sent.split(" ")
    # print(sent)
    for i in sent:
        # try:
        #     language = detect(i)
        #     print(language)
        #     if language in ['hi', 'bn', 'en', 'gu', 'kn', 'ml', 'mr', 'pa', 'ta', 'te']:
        #         pass
        #     elif language == 'ne':
        #         langauge = 'hi'
        #     else:
        #         language = 'en'
        #     language = lang_dict[language]
        # except:
        #     langauge = 'odia'
        try:
    
            if i in ieLexHeads:
                phones.append(ieMapped[ieLexHeads.index(i)])
                # print(ieMapped[ieLexHeads.index(i)])
            elif i in odiaLexHeads:
                i = odiaMapped[odiaLexHeads.index(i)]
                i = tp.ipaToSaarthiASCII(i, delimiter=True, delimit='_')
                phones.append(i)
            else:
                phones.append(get_phonim(i, language, tp, eng_p))
        except:
            phones.append(" ")
    stringg = " ".join(phones)
    # print(stringg)
    return stringg

