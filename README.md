

TTS is a library for advanced Text-to-Speech generation. It's built on the latest research, and was designed to achieve the best trade-off between ease-of-training, speed, and quality.
TTS comes with pre-trained models, and tools for measuring dataset quality and is already used in **20+ languages** for products and research projects.


- Efficient, flexible, lightweight but feature complete `Trainer API`.
- Released and ready-to-use models.
- Tools to curate Text2Speech datasets under```dataset_analysis```.
- Utilities to use and test your models.
- Modular (but not too much) code base enabling easy implementation of new ideas.



### End-to-End Models (Customized VITS with VQ-FLOW)
- VITS: [paper](https://arxiv.org/pdf/2106.06103)

## Install TTS
TTS is tested on Ubuntu 20.04 with **python >= 3.7, < 3.11.**.

If you plan to code or train models, clone TTS and install it locally.

```
git clone https://github.com/coqui-ai/TTS
pip install -e .[all,dev,notebooks]  # Select the relevant extras
```


## Directory Structure
```
|- notebooks/       (Jupyter Notebooks for model evaluation, parameter selection and data analysis.)
|- utils/           (common utilities.)
|- TTS
    |- bin/             (folder for all the executables.)
      |- train*.py                  (train your target model.)
      |- distribute.py              (train your TTS model using Multiple GPUs.)
      |- compute_statistics.py      (compute dataset statistics for normalization.)
      |- ...
    |- tts/             (text to speech models)
        |- layers/          (model layer definitions)
        |- models/          (model definitions)
        |- utils/           (model specific utilities.)
    |- speaker_encoder/ (Speaker Encoder models.)
        |- (same)
    |- vocoder/         (Vocoder models.)
        |- (same)
```
