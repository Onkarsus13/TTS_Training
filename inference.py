import os
from glob import glob
import torch
from trainer import Trainer, TrainerArgs
import numpy as np
from scipy.io.wavfile import write
from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.tts.configs.vits_config import VitsConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.vits import CharactersConfig, Vits, VitsArgs, VitsAudioConfig
from TTS.tts.utils.languages import LanguageManager
from TTS.tts.utils.speakers import SpeakerManager
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio import AudioProcessor
import soundfile as sf

output_path = os.path.dirname(os.path.abspath(__file__))

mailabs_path = "../data/bilingual_en_hi/**"
dataset_paths = glob(mailabs_path)

dataset_config = [
    BaseDatasetConfig(name="mailabs", meta_file_train=None, path=path, language=path.split("/")[-1])
    for path in dataset_paths
]


speaker = 24

audio_config = VitsAudioConfig(
    sample_rate=16000,
    win_length=1024,
    hop_length=256,
    num_mels=80,
    mel_fmin=0,
    mel_fmax=None,
)

vitsArgs = VitsArgs(
    # use_language_embedding=True,
    # embedded_language_dim=512,
    use_speaker_embedding=True,
    speaker_embedding_channels=256,
    use_sdp=False,
    num_speakers=25,
    # speakers_file = 'bilingual_en_hi_te-September-07-2022_12+17PM-096b35f6/speakers.pth',
    # use_speaker_file=Truet

)

config = VitsConfig(
    model_args=vitsArgs,
    audio=audio_config,
    speaker_embedding_channels=256,
    run_name="bilingual_en_hi_te",
    batch_size=64,
    eval_batch_size=64,
    batch_group_size=0,
    num_loader_workers=4,
    num_eval_loader_workers=4,
    run_eval=True,
    test_delay_epochs=-1,
    epochs=1000,
    save_step=5,
    save_n_checkpoints=10,
    text_cleaner="multilingual_cleaners",

    use_phonemes=False,
    phoneme_language="en-us",
    phoneme_cache_path=os.path.join(output_path, "phoneme_cache"),
    compute_input_seq_cache=True,
    use_language_weighted_sampler=True,
    print_eval=False,
    mixed_precision=False,
    # sort_by_audio_len=True,
    min_audio_len=32 * 256 * 4,
    max_audio_len=160000,
    output_path=output_path,
    datasets=dataset_config,
    characters=CharactersConfig(
        pad="<PAD>",
        eos="<EOS>",
        bos="<BOS>",
        blank="<BLNK>",
        characters= "abcdefghijklmnopqrstuvwxyzप्रसिदकबीअधयेताुषोमगवलहशआखउनंजैडफ़एणभइचईँथछूज़औटफ़घढृॉऊओड़झठढ़ऐौक़ॅञःङख़ग़ऑऋऱఆయనభార్జలకషమిటంతవగోసథచెపదీేుొఉధడఅఇృహఛైూశబఈఎఒణఏఘఖళఐఫఓౌఠఊఢఞఔఋఙ‌!¡'(),-.:;¿""'?1234567890",
        punctuations= "",
        phonemes= None,
        
    ),
    test_sentences=[
        [
            "It took me quite a long time to develop a voice, and now that I have it I'm not going to be silent.",
            "saarthi_voice_A",
            None,
            "en_IN",
        ],
        [
            "मेरा नाम सारथी है। तुम कौन हो?",
            "saarthi_voice_A",
            None,
            "hi",
        ],
        [
            "నా పేరు సారథి. నీవెవరు?",
            "saarthi_telugu_female",
            None,
            "te",
        ],
    ],
    num_speakers=25,
    use_speaker_embedding = True,
    # speakers_file = 'bilingual_en_hi_te-September-07-2022_12+17PM-096b35f6/speakers.pth'
#     use_d_vector_file=True,
#     d_vector_file="../speaker Embeddings/speaker.pth",
#     d_vector_dim=768
)

config.from_dict(config.to_dict())

# init audio processor
ap = AudioProcessor(**config.audio.to_dict())

# load training samples
train_samples, eval_samples = load_tts_samples(
    dataset_config,
    eval_split=True,
    eval_split_max_size=config.eval_split_max_size,
    eval_split_size=config.eval_split_size,
)

speaker_manager = SpeakerManager()
speaker_manager.set_ids_from_data(train_samples + eval_samples, parse_key="speaker_name")
speaker_manager.load_ids_from_file('speaker_id/speakers.pth')
config.model_args.num_speakers = 25

language_manager = LanguageManager(config=config)
config.model_args.num_languages = 3
language_manager.load_ids_from_file('bilingual_en_hi_te-September-17-2022_01+22PM-096b35f6/language_ids.json')

tokenizer, config = TTSTokenizer.init_from_config(config)


model = Vits(config, ap, tokenizer, speaker_manager, language_manager)

if speaker >= 23:
    model.load_checkpoint(config, 'bilingual_en_hi_te-October-03-2022_03+15PM-096b35f6/checkpoint_6995.pth', 
    eval=True)
else:
    model.load_checkpoint(config, 'bilingual_en_hi_te-September-07-2022_12+17PM-096b35f6/akash_model.pth')
    model.length_scale = 0.8

# text = "नमस्ते ओंकार आप कैसे हैं"
text = 'नमस्ते ओंकार आप कैसे हैं'

text = torch.tensor(tokenizer.text_to_ids(text)).to(torch.int64).unsqueeze(0)
print(text)

# dvec= torch.load('../speaker Embeddings/speaker.pth')['text_01011.wav']['embedding'].unsqueeze(0)[:, :256]
# print(dvec.shape)

aux_input= {"x_lengths": None, "d_vectors":None , "speaker_ids":torch.Tensor([24]).to(torch.int64), "language_ids": torch.Tensor([0]).to(torch.int64), "durations": None}

output = model.inference(text, aux_input)
output = output['model_outputs'].cpu().squeeze(0).squeeze(0).numpy()

scaled = np.int16(output/np.max(np.abs(output)) * 32767)
write('onkar_test_base_hi_30_new.wav', 16000, scaled)


