from pydub import AudioSegment as am
from pydub import AudioSegment, effects
import numpy as np
from scipy.io.wavfile import write
from math import ceil


# names = {"anusha":"अनुषा","nirali":"निराली","prashna":"प्रसन्ना","sushant":"सुशांत","sneha":"स्नेहा", "sanchit":"संचित","arvind":"अर्विन्द","digant":"दिगंत"}


def loudness_normalization(sound,target_dBFS=-15):
    loudness_difference = target_dBFS - sound.dBFS
    normalized_audio = sound + loudness_difference
    return normalized_audio

# for k,v in names.items():
# 	first_statement = am.from_file("first_response.wav")
# 	second_statement = am.from_file('names/{}.wav'.format(k))

# 	second_statement = second_statement.set_frame_rate(8000)
# 	second_statement = loudness_normalization(second_statement,first_statement.dBFS)

# 	new_au = first_statement+second_statement

# 	new_au.export("stitched_names/{}.wav".format(k),format="wav")



first_statement = am.from_file("saved_wavs/saarthi_meghana_english1.wav")
second_statement = am.from_file("saved_wavs/saarthi_meghana_english2.wav")
thrid_segment = am.from_file("saved_wavs/saarthi_meghana_english3.wav")
fourth_seg = am.from_file("saved_wavs/saarthi_meghana_english4.wav")
fifth_seg = am.from_file("saved_wavs/saarthi_meghana_english5.wav")
sixth_seg = am.from_file("saved_wavs/saarthi_meghana_english6.wav")

# first_statement = first_statement.set_frame_rate(8000)
# second_statement = second_statement.set_frame_rate(8000)
# second_statement = loudness_normalization(second_statement,first_statement.dBFS)

new_au = first_statement+second_statement + thrid_segment + fourth_seg  + fifth_seg  + sixth_seg
normalizedsound = effects.normalize(new_au)
# norm_audio = effects.normalize(second_statement)
# samples = np.array(normalizedsound.get_array_of_samples())

# au_1 = samples[:ceil(8000*3.7075)]

# write('louaded_1st_part.wav', 8000, au_1)
normalizedsound.export("concat_english_new.wav",format="wav")

