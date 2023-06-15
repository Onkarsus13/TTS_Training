import torch
import os
import torchaudio

xp = torch.load('model_config/speakers.pth')
xp['malayalam_male_saarthi'] = 47
torch.save(xp, 'model_config/speakers_new.pth')
print(xp)
'''
import re
def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

def clean_text(text: str) -> str:
    text = text.lower()
    text = text.replace(u'@', '')
    text = text.replace(u',', '')
    text = text.replace(u'"', '')
    text = text.replace(u'(', '')
    text = text.replace(u')', '')
    text = text.replace(u'"', '')
    text = text.replace(u':', '')
    text = text.replace(u"'", '')
    text = text.replace(u"‘‘", '')
    text = text.replace(u"’’", '')
    text = text.replace(u"''", '')
    text = text.replace(u'-', '')
    text = text.replace(u"\n","")
    text = text.replace(u'.', '')
    text = text.replace(u"?","")
    text = text.replace(u"\\n","")
    text = text.replace(u"£","")
    text = text.replace(u"[", "")
    text = text.replace(u']', '')
    text = text.replace(u'&', '')
    text = remove_emojis(text)
    text = re.sub(r'[^\w]', ' ', text)
    return text


f = open('custom_data/en_IN/base/metadata.csv', 'r')
with open('cmetadata.csv', 'w') as f1:
    for i in f.readlines():
        # print(i)
        i = i.split('|')
        w = i[0].split('.')[0]
        t = clean_text(i[1][1:])

        nt = w+'|'+t+'\n'
        f1.write(nt)
f1.close()
'''

# import soundfile as sf
# import glob
# files = glob.glob('custom_data/en_IN/base/wavs/*.wav')
# from pydub import AudioSegment as am

# f = sf.SoundFile(files[0])
# print(f.samplerate)

# count = 0
# for i in files:

#     sound = am.from_file(i, format='wav', frame_rate=22050)
#     sound = sound.set_frame_rate(16000)
#     name = i.split('/')[-1]
#     sound.export('custom_data/en_IN/base/wavs/'+name, format='wav')



# print(count)

# dir = os.listdir('../data/bilingual_en_hi/hi')

# for i in dir:
#     os.remove('../data/bilingual_en_hi/hi/{}/metadata.csv'.format(i))
#     f = open('../data/bilingual_en_hi/hi/{}/old_metadata.csv'.format(i), 'r')
#     with open('../data/bilingual_en_hi/hi/{}/metadata.csv'.format(i), 'w') as f1:
#         for j, data in enumerate(f.readlines()):
#             f1.write(data)

#             if j == 1500:
#                 break
#     # os.rename('../data/bilingual_en_hi/te/{}/metadata.csv'.format(i), '../data/bilingual_en_hi/te/{}/old_metadata.csv'.format(i))
#     # os.rename('../data/bilingual_en_hi/te/{}/cmetadata.csv'.format(i), '../data/bilingual_en_hi/te/{}/metadata.csv'.format(i))
#     f1.close()
#     f.close()

# import glob

# def load_audio(file_path):
#     """Load the audio file normalized in [-1, 1]

#     Return Shapes:
#         - x: :math:`[1, T]`
#     """
#     x, sr = torchaudio.load(file_path)
    
#     # x = csr(x)
#     assert (x > 1).sum() + (x < -1).sum() == 0
#     return x, sr

# files = glob.glob('/root/Documents/Audio-Encoder-Pretraining-main/voice_coder/TTS_Custom/bengali_male/bengali/bengali_male_saarthi/wavs/*.wav')
# count = 0
# t = 0
# for i in files:
#     x, sr = torchaudio.load(i)
#     t +=  (sr/16000)


# print(t/3600)
    

