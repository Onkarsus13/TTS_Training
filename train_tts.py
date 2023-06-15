import os
from glob import glob
# from test import *
from trainer import Trainer, TrainerArgs
import torch
from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.tts.configs.vits_config import VitsConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.vits import CharactersConfig, Vits, VitsArgs, VitsAudioConfig
from TTS.tts.utils.languages import LanguageManager
from TTS.tts.utils.speakers import SpeakerManager
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio import AudioProcessor
from TTS.config import load_config
from TTS.tts.models import setup_model

# output_path = os.path.dirname(os.path.abspath(__file__))
output_path = '/root/Documents/Audio-Encoder-Pretraining-main/voice_coder/TTS_Custom'

mailabs_path = "mallu_temp/**"
dataset_paths = glob(mailabs_path)
dataset_config = [
    BaseDatasetConfig(name="mailabs", meta_file_train=None, path=path, language=path.split("/")[-1])
    for path in dataset_paths
]

phonems = '|k_|K_|g_|j_|J_|X_|x_f_K_k_G_g_|y_w_h_C_c_J_i_y_Y_V_q_x_X_N_S_r_T_t_D_d_n~_n_`I_I_P_p_B_b_m_z_s_Aː_A_Iː_i_u_Uː_R_Oː_O_eː_e_Eː_oː_o_M_h_a_`a_v_j_l_`l'

# dev = ''.join([chr(i) for i in range(0x0900, 0x097F)])
# odi = ''.join([chr(i) for i in range(0x0B00, 0x0B7F)])
# guj = ''.join([chr(i) for i in range(0x0A80, 0x0AFF)])
# ben = ''.join([chr(i) for i in range(0x0980, 0x09FF)])
# pun = ''.join([chr(i) for i in range(0x0A00, 0x0A7F)])
# tam = ''.join([chr(i) for i in range(0x0B80, 0x0BFF)])
# tel = ''.join([chr(i) for i in range(0x0C00, 0x0C7F)])
# mal = ''.join([chr(i) for i in range(0x0D00, 0x0D7F)])
# kan = ''.join([chr(i) for i in range(0x0C80, 0x0CFF)])
# character = dev+odi+guj+ben+pun+tam+tel+mal+kan


audio_config = VitsAudioConfig(
    sample_rate=16000,
    win_length=1024,
    hop_length=256,
    num_mels=80,
    mel_fmin=0,
    mel_fmax=None,
)

vitsArgs = VitsArgs(
    use_speaker_embedding=True,
    speaker_embedding_channels=512,
    use_language_embedding=True,
    embedded_language_dim=512,
    use_sdp=False,
    num_speakers=50,
    # freeze_encoder=True,
    # freeze_PE=True,
    # freeze_DP=True,
    # freeze_flow_decoder=True,
    # freeze_waveform_decoder=True

)

config = VitsConfig(
    model_args=vitsArgs,
    audio=audio_config,
    speaker_embedding_channels=512,
    run_name="mallu_male_dp",
    batch_size=48,
    eval_batch_size=16,
    batch_group_size=0,
    num_loader_workers=4,
    num_eval_loader_workers=4,
    run_eval=True,
    test_delay_epochs=-1,
    epochs=1000,
    save_step=100,
    save_n_checkpoints=10,
    text_cleaner=None,
    use_phonemes=True,
    phoneme_language="en-us",
    phoneme_cache_path=os.path.join(output_path, "phoneme_cache"),
    compute_input_seq_cache=False,
    use_language_weighted_sampler=False,
    print_eval=False,
    mixed_precision=False,
    # sort_by_audio_len=True,
    min_audio_len=16 * 64 * 4,
    max_audio_len=160000,
    output_path=output_path,
    datasets=dataset_config,
    characters=CharactersConfig(
        pad="<PAD>",
        eos="<EOS>",
        bos="<BOS>",
        blank="<BLNK>",
        characters= phonems,#"abcdefghijklmnopqrstuvwxyzप्रसिदकबीअधयेताुषोमगवलहशआखउनंजैडफ़एणभइचईँथछूज़औटफ़घढृॉऊओड़झठढ़ऐौक़ॅञःङख़ग़ऑऋऱఆయనభార్జలకషమిటంతవగోసథచెపదీేుొఉధడఅఇృహఛైూశబఈఎఒణఏఘఖళఐఫఓౌఠఊఢఞఔఋఙ‌!¡'(),-.:;¿""'?1234567890",
        punctuations= ",?.!;:'‘¡",
        phonemes= phonems,
        
    ),
    test_sentences=[
        # [
        #     # 'ਕੀ ਤੁਸੀਂ ਨਿਰਧਾਰਤ ਮਿਤੀ ਜਾਂ ਇਸ ਤੋਂ ਪਹਿਲਾਂ ਭੁਗਤਾਨ ਕਰਨ ਦੇ ਯੋਗ ਹੋਵੋਗੇ?',
        #     # "punjabi_female_saarthi",
        #     # None,
        #     # "punjabi",
        # ],
        # [
        #     "হ্যাঁ সকালে পরে ফোন করুন, তখন কথা বলতে পারি।",
        #     "bengali_female_saarthi",
        #     None,
        #     "bengali",
        # ],
        [
            "അല്ല, ക്ഷമിക്കണം, പക്ഷേ അത് ഉപകരണത്തിലേക്ക് പ്ലഗിൻ ചെയ്യണം.",
            "malayalam_male_saarthi",
            None,
            "malayalam",
        ],
    ],
    num_speakers=50,
    use_speaker_embedding = True,

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

# print(eval_samples)
speaker_manager = SpeakerManager()
speaker_manager.load_ids_from_file('model_config/speakers_new.pth')
speaker_manager = SpeakerManager(speaker_id_file_path='model_config/speakers_new.pth')
# speaker_manager.set_ids_from_data(train_samples + eval_samples, parse_key="speaker_name")
config.model_args.num_speakers = 50

language_manager = LanguageManager(config=config)
config.model_args.num_languages = 11
language_manager.load_ids_from_file('model_config/language_ids.json')
tokenizer, config = TTSTokenizer.init_from_config(config)

model = Vits(config, ap, tokenizer, speaker_manager, language_manager)
cp = torch.load('model_config/checkpoint_1433000.pth', 
                map_location=torch.device('cuda'))

model_weights = cp['model'].copy()
for key in list(model_weights.keys()):
  if "speaker_encoder" in key:
    del model_weights[key]
model.load_state_dict(model_weights)


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

print("Number of parameters ", count_parameters(model))

trainer = Trainer(
    TrainerArgs(), config, output_path, model=model, train_samples=train_samples, eval_samples=eval_samples
)

trainer.fit()
