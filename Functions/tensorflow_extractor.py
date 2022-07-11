import json
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from essentia.standard import (
    MonoLoader,
    TensorflowPredictMusiCNN,
    TensorflowPredictVGGish,
)
import numpy as np
import matplotlib.pyplot as plt

AUTO_TAGGING = "msd-musicnn-1"
GENDER = "gender-musicnn-msd-2"
DANCEABILITY = "danceability-musicnn-msd-2"
VOICE_INSTRUMENTAL = "voice_instrumental-musicnn-msd-2"
MOODS = [
    "mood_acoustic-musicnn-msd-2",
    "mood_aggressive-musicnn-msd-2",
    "mood_electronic-musicnn-msd-2",
    "mood_happy-musicnn-msd-2",
    "mood_party-musicnn-msd-2",
    "mood_relaxed-musicnn-msd-2",
    "mood_sad-musicnn-msd-2",
]
GENRES = [
    "genre_dortmund-musicnn-msd-2",
    "genre_electronic-musicnn-msd-2",
    "genre_rosamerica-musicnn-msd-2",
]


def plot_activations(ax, metadata):
    ax.set_yticks(range(len(metadata["classes"])))
    ax.set_yticklabels(metadata["classes"])
    ax.set_xlabel("patch number")
    ax.xaxis.set_ticks_position("bottom")
    plt.title("Tag activations")
    plt.show()


def get_model_results(audio_file, model_name):
    out = {}

    with open("../Models/" + model_name + ".json", "r") as json_file:
        metadata = json.load(json_file)

    # audio_file = "Music/ESC_wav/66 - ESC_2021/23-Måneskin - Zitti E Buoni - Italy 🇮🇹 - Grand Final - Eurovision 2021-RVH5dn1cxAQ.wav"
    audio = MonoLoader(sampleRate=16000, filename=audio_file)()

    activations = TensorflowPredictMusiCNN(
        graphFilename="../Models/" + model_name + ".pb"
    )(audio)

    ig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.matshow(activations.T, aspect="auto")

    print(model_name)

    predictions = np.mean(activations, axis=0)

    order = predictions.argsort()[::-1]
    for i in order[:3]:
        out[metadata["classes"][i]] = predictions[i]
        # "{}: {:.3f}".format(metadata["classes"][i], predictions[i])

    return model_name.split("-")[0], out


def get_multiple_models_results(audio_file, models=[]):
    out = {}
    for model in models:
        name, values = get_model_results(audio_file, model)
        out[name] = values
    return out


def all_models():
    models = [AUTO_TAGGING, GENDER, DANCEABILITY, VOICE_INSTRUMENTAL]
    for genre in GENRES:
        models.append(genre)
    for mood in MOODS:
        models.append(mood)
    return models


# audio_file = "Music/ESC_wav/66 - ESC_2021/23-Måneskin - Zitti E Buoni - Italy 🇮🇹 - Grand Final - Eurovision 2021-RVH5dn1cxAQ.wav"
# res = get_multiple_models_results(audio_file, all_models())
# print(res)
