from __future__ import absolute_import, division, print_function

import argparse
import logging
import os
import json
import torch


from TTS.tts.utils.synthesis import synthesis
from TTS.utils.audio import AudioProcessor
from TTS.tts.models import setup_model
from TTS.config import load_config
from TTS.tts.models.vits import *
from scipy.io.wavfile import write
import librosa
from pydub import AudioSegment as am
from pydub import AudioSegment, effects 
from TTS.tts.utils.text.DPsaarthi.dp.phonemizer import Phonemizer


import pandas as pd
logger = logging.getLogger(__name__)

class Predict:
    def __init__(self):
      super().__init__()

      self.lang = json.load(open('/root/Documents/phonem_inference/TTS_Custom/capri_config/language_ids.json'))

      
      self.speaker_hi_or_be_mr_gu = torch.load('mallu_male_dp-June-07-2023_07+41AM-c322046/speakers.pth')

      self.model, self.config = self.make_model('mallu_male_dp-June-07-2023_07+41AM-c322046', 'best_model.pth', True)

      self.eng_p = Phonemizer.from_checkpoint('/root/Documents/Audio-Encoder-Pretraining-main/voice_coder/TTS_Custom/TTS/tts/utils/text/DPsaarthi/latest_model.pt')


      df = pd.read_csv("./customer_names.csv")
      self.names = {}
      for i, name in enumerate(df["ROMAN"]):
        if name.lower() not in self.names:
            self.names[name.lower()] = df["DEVANAGARI"][i]
      
      # print(self.names)
      
        
    def inference(self, text, speaker_name='renuka', language=None, sample_rate=16000, length=1.0, file_name="out.wav", name=['saarthi']):
      
   
      speaker =  self.speaker_hi_or_be_mr_gu [speaker_name]
      model = self.model
      C = self.config
      use_cuda = True

      model.length_scale =  length


      #TTS
      if language == 'english':
        language = 'en_IN'

      lang = self.lang[language]
      wav, alignment, _, _ = synthesis(
                          model,
                          text,
                          C,
                          use_cuda=use_cuda,
                          speaker_id=speaker,
                          d_vector=None,
                          style_wav=None,
                          language_id=lang,
                          language_maping=language,
                          eng_p=self.eng_p
                      ).values()
      
      wav_resampled = librosa.resample(wav, orig_sr=16000, target_sr=sample_rate)
      write('saved_wavs/'+file_name, sample_rate, wav_resampled)
      sound = AudioSegment.from_file("saved_wavs/"+file_name, "wav")  
      sound = effects.normalize(sound)
      # sound = am.from_file("saved_wavs/"+file_name,format="wav")
      sound = sound.set_sample_width(2)
      sound.export('saved_wavs/'+file_name,format="wav")

      return 'saved_wavs/'+file_name

    def make_model(self, config_path, model_name, use_cuda):
        MODEL_PATH = config_path+'/'+model_name
        CONFIG_PATH = config_path+'/config.json'
        TTS_LANGUAGES = config_path+'/language_ids.json'
        TTS_SPEAKERS =  config_path+'/speakers.pth'

        USE_CUDA = use_cuda

        # load the config
        C = load_config(CONFIG_PATH)
        C.language_ids_file = TTS_LANGUAGES
        C.speakers_file = TTS_SPEAKERS
        C.model_args.speakers_file = TTS_SPEAKERS
        C.model_args.language_ids_file = TTS_LANGUAGES

        ap = AudioProcessor(**C.audio)

        model = setup_model(C)
        model.speaker_manager.load_ids_from_file(TTS_SPEAKERS)
        model.language_manager.load_ids_from_file(TTS_LANGUAGES)

        cp = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
        # remove speaker encoder
        model_weights = cp['model'].copy()
        for key in list(model_weights.keys()):
            if "speaker_encoder" in key:
                del model_weights[key]

        model.load_state_dict(model_weights)
        model.eval()

        model.inference_noise_scale = 0.3 # defines the noise variance applied to the random z vector at inference.
        model.inference_noise_scale_dp = 0.3 # defines the noise variance applied to the duration predictor z vector at inference.

        if USE_CUDA:
            model = model.cuda()
        return model, C
      

pred_model = Predict()
def get_model():
    # pred_model = Predict('capri_config/language_ids.json', 'capri_config/speakers.pth')
    return pred_model
# text = ['gives me great pleasure to address both Houses of Parliament assembled  together.']# which is due on twenty january. When can you make the payment?'
# text = ['gives me great pleasure to address both Houses of Parliament assembled  together.  A  few  months  back,  our  country  completed  seventy five years of independence and entered the Amrit Kaal.' ]#This ‘Azadi ka Amrit Kaal’ assimilates the pride of thousands of years of our glorious past, the inspirations of Indian freedom struggle and India to resolve for a golden future.']
# text = ['am i talking with onkar, aakash, sanket']
# # text = ['તમે કૃપા કરીને સીએટ ટાયર નહિ ખરીદવાનું કારણ જણાવી શકો છો?']
# text = ['पिछले साल अगस्त में, इंफोसिस का सीईओ बनते ही, विशाल सिक्का ने, हर सोमवार को टाई पहनकर आने की अनिवार्यता समाप्त कर दी थी ।']
# text = ['मैं आधार हाउसिंग फाइनेंस से प्रिया बोल रही हूँ']
# text = ['ନମସ୍କାର ମୁଁ ଶ୍ରୀ ରାମ ହାଉସିଂ ଫାଇନାନ୍ସରୁ କଲ୍ କରୁଛି']
# # text = ['मेरी सरकार को, देश के लोगों ने, जब पहली बार सेवा का अवसर दिया, तब ‘सबका साथ, सबका विकास’ के मंत्र से हमने शुरुआत की थी। समय के साथ इसमें ‘सबका विश्वास’ और ‘सबका प्रयास’ भी जुड़ गया।']
# # text = ['स्थिर और निर्णायक सरकार होने का लाभ हमें साल की सबसे बड़ी आपदा और उसके बाद बनी परिस्थितियों से निपटने में मिल रहा है। दुनिया में जहां भी राजनीतिक अस्थिरता है, वे देश आज भीषण संकटों से घिरे हैं। लेकिन मेरी सरकार ने राष्ट्रहित में जो भी निर्णय किए उससे भारत बाकी दुनिया से बहुत बेहतर स्थिति में है।']
# text = ['We have to build a भारत, which is self-reliant and also able to fulfill its humanitarian obligations.']
# text = ['A india which has no poverty and where the middle class is also prosperous. ']
text = ['A india whose youth and women power will be at the forefront to give direction to the society and the nation, and whose youth are well ahead of time. ']
# text = ['A भारत whose diversity is even more vivid and whose unity becomes even more unshakeable. ']
# text = ['With the passage of time, ‘सब्का विकास् ’ and ‘सब्का प्रयास’ were also added to it. ']
# text = ['This मंत्रा has now become the  inspiration  for  building  a  developed  India.']
# text = ['मुझे आपकी जॉब के लिए दुःख है ।पर मैं आपको रिकमेंड करता हूँ की पैसों की व्यवस्था करें और पेमेंट करें ।']
# text = ['hii nir']o
# text = ['hi i am onkar calling from pune or banglore']
# text = ['समझ गई, क्या आप bhubaneswar में रहते है?']
# text = ['ଯଦି ଆପଣଙ୍କ ପାଖରେ କାନ ଆଉ ବୁଦ୍ଧି ଅଛି। ତ ସେଗୁଡ଼କୁ କାମରେ ଲଗାଅ।']
# text = ['ভালোর জন্যই দিয়েছে. শুনে ভালো লাগছে তদন্তটা ভালো হবে.']
# text = ['আমি অন্য ঋণের কথা বলছি এবং আপনি আমাকে ভুল ঋণের কথা  বলছেন।']
# text = ['ସେଇ ମହିଳା ସବୁ କିଛି ପାୟିଁ ପଇସା ଦେବେ']
# text = ['গ্রুপ স্টেজের শেষে অরেঞ্জ ক্যাপ ধারক খেলতে পারল না ফাইনালে, বারবার তিনবার ঘটল']
# text = ['బంధాలు, అనుబంధాలు రోజురోజుకీ మృగమై పోతున్నాయి. కంటికి రెప్పలా పిల్లలు కాపాడుకోవలసిన తల్లిదండ్రులే పిల్లలను చైల్డ్ ట్రాఫికింగ్ ముఠాలకు అప్పగిస్తున్నారు.']
# text = ['தாய், கார்த்திகா மிகவும் பலவீனமாக இருந்தார்,']
# text = ["हाआय्य्. आयेम् calling from स्मार्ट्कोय्य्न्. एमाय् speaking to पूर्र्वा? As ए privileged customer of, स्मार्ट्कोय्य्न् personal loan एएप्, we have an exclusive offer that's valid only for today."]
# text = ['ଉଦ୍ଧାର କାର୍ଯ୍ୟରେ ଓଡ୍ରାଫ୍ ଟିମ୍ ଓ ଅଗ୍ନିଶମ ବାହିନୀ ନିୟୋଜିତ ହୋଇଛି।']
# text = ['ନିରଞ୍ଜନ ପଟ୍ଟନାୟକଙ୍କ ପୁଅ ନବ୍ୟଜ୍ୟୋତି ପଟ୍ଟନାୟକ ବାଲେଶ୍ୱର ଲୋକସଭା ଆସନରୁ ପ୍ରାର୍ଥୀ ହୋଇଛନ୍ତି . ଏପଟେ ତାଙ୍କ ଭାଇ ସୌମ୍ୟ ରଞ୍ଜନ ପଟ୍ଟନାୟକଙ୍କ ଶଳା ତଥା.']
# text = ['ഒരു ഐഫോണിനെ ട്രെഡ്‌മില്ലിൽ ഒട്ടിപ്പിടിക്കുന്നതിന് ഇത് സഹായിക്കുമോ? ഇത് ഒരു ഫ്ലാറ്റ് സ്‌ക്രീനാണ്, ചെറുതായി കോണാകൃതിയിലുള്ളതാണ്.']
# # text = ['ആര്‍ഷോ മൂന്നാം സെമസ്റ്ററില്‍ പുനഃപ്രവേശനം നേടുകയും പരീക്ഷയ്ക്ക് രജിസ്റ്റര്‍ ചെയ്യുകയും ചെയ്തിരുന്നെന്ന് രാവിലെ നടത്തിയ പ്രസ്താവന പ്രിന്‍സിപ്പല്‍ തിരുത.']
# # text = ['ലെതറിൽ ഇത് പ്രവർത്തിക്കുമോ?']


# pred_model.inference(text = text[0], language='malayalam', speaker_name='malayalam_male_saarthi', file_name='english_female.wav', length=1.0, name=['bhubaneswar'], sample_rate=16000)
