from bdb import effective
import csv
from email.mime import audio
import os.path
from os import listdir

import essentia
import essentia.standard as es
import essentia.streaming as ess
import librosa
import pandas as pd
import soundfile as sf
from tqdm import tqdm
import numpy as np

# from os.path import isfile, join


DIR_WAV_FILES = "/home/riccardo/Tesi/disney-ost-analysis/Music/ESC_wav"
DIR_SPLITTED_WAV_FILES = "/home/riccardo/Tesi/disney-ost-analysis/Music/ESC_splitted"
DIR_RESULTS_FILES = "/home/riccardo/Tesi/disney-ost-analysis/Music/ESC_results"
RESULT_CSV = "OST_results/results.csv"


def compute_all_features(audiofilename):
    # Compute all features.
    # Aggregate 'mean' and 'stdev' statistics for all low-level, rhythm, and tonal frame features.
    essentia.log.infoActive = False
    features, features_frames = es.MusicExtractor(
        lowlevelStats=["mean", "stdev"],
        rhythmStats=["mean", "stdev"],
        tonalStats=["mean", "stdev"],
    )(audiofilename)
    return features


def slice_files(audiofilenames_full, slices_number):
    idx = "0000"
    j = 0
    # slices_number = 3
    pbar = tqdm(
        audiofilenames_full,
        unit="files",
        bar_format="slicing:\t{percentage:.0f}%|{bar:100}{r_bar}",
    )
    for f in pbar:
        pbar.set_postfix({"song": (f.split("/")[1]).split("-")[1][:20]})
        y, sr = librosa.load(os.path.join(DIR_WAV_FILES, f))
        slice_length = int(y.size / slices_number)
        f = f.split("/")[1]

        for i in range(3):
            try:
                j += 1
                global_index = idx[: -len(str(j))] + str(j)
                audio_data = y[i * slice_length : (i + 1) * slice_length]
                slice_filename = os.path.join(
                    DIR_SPLITTED_WAV_FILES,
                    global_index + "-" + f + "_00" + str(i) + ".wav",
                )
                sf.write(slice_filename, audio_data, sr, subtype="PCM_24")
            except:
                err_str = global_index + " " + f + " " + "00" + str(i) + "\n"
                print(err_str)

    audiofilenames = [
        f
        for f in listdir(DIR_SPLITTED_WAV_FILES)
        if (
            os.path.isfile(os.path.join(DIR_SPLITTED_WAV_FILES, f))
            and f.endswith(".wav")
        )
    ]
    return audiofilenames


def extract_files():
    audiofilenames_full = []
    folders = [f for f in sorted(listdir(DIR_WAV_FILES))]
    for folder in folders:
        for f in sorted(listdir(DIR_WAV_FILES + "/" + folder)):
            if os.path.isfile(os.path.join(DIR_WAV_FILES, folder, f)) and (
                f.endswith(".wav") or f.endswith(".mp3")
            ):
                audiofilenames_full.append(folder + "/" + f)
    return audiofilenames_full


def init_csv(fname):
    start_row = [
        "track_title",
        "lowlevel.average_loudness",
        "lowlevel.barkbands.mean",
        "lowlevel.barkbands.stdev",
        "lowlevel.barkbands_crest.mean",
        "lowlevel.barkbands_crest.stdev",
        "lowlevel.barkbands_flatness_db.mean",
        "lowlevel.barkbands_flatness_db.stdev",
        "lowlevel.barkbands_kurtosis.mean",
        "lowlevel.barkbands_kurtosis.stdev",
        "lowlevel.barkbands_skewness.mean",
        "lowlevel.barkbands_skewness.stdev",
        "lowlevel.barkbands_spread.mean",
        "lowlevel.barkbands_spread.stdev",
        "lowlevel.dissonance.mean",
        "lowlevel.dissonance.stdev",
        "lowlevel.dynamic_complexity",
        "lowlevel.erbbands.mean",
        "lowlevel.erbbands.stdev",
        "lowlevel.erbbands_crest.mean",
        "lowlevel.erbbands_crest.stdev",
        "lowlevel.erbbands_flatness_db.mean",
        "lowlevel.erbbands_flatness_db.stdev",
        "lowlevel.erbbands_kurtosis.mean",
        "lowlevel.erbbands_kurtosis.stdev",
        "lowlevel.erbbands_skewness.mean",
        "lowlevel.erbbands_skewness.stdev",
        "lowlevel.erbbands_spread.mean",
        "lowlevel.erbbands_spread.stdev",
        "lowlevel.gfcc.cov",
        "lowlevel.gfcc.icov",
        "lowlevel.gfcc.mean",
        "lowlevel.hfc.mean",
        "lowlevel.hfc.stdev",
        "lowlevel.loudness_ebu128.integrated",
        "lowlevel.loudness_ebu128.loudness_range",
        "lowlevel.loudness_ebu128.momentary.mean",
        "lowlevel.loudness_ebu128.momentary.stdev",
        "lowlevel.loudness_ebu128.short_term.mean",
        "lowlevel.loudness_ebu128.short_term.stdev",
        "lowlevel.melbands.mean",
        "lowlevel.melbands.stdev",
        "lowlevel.melbands128.mean",
        "lowlevel.melbands128.stdev",
        "lowlevel.melbands_crest.mean",
        "lowlevel.melbands_crest.stdev",
        "lowlevel.melbands_flatness_db.mean",
        "lowlevel.melbands_flatness_db.stdev",
        "lowlevel.melbands_kurtosis.mean",
        "lowlevel.melbands_kurtosis.stdev",
        "lowlevel.melbands_skewness.mean",
        "lowlevel.melbands_skewness.stdev",
        "lowlevel.melbands_spread.mean",
        "lowlevel.melbands_spread.stdev",
        "lowlevel.mfcc.cov",
        "lowlevel.mfcc.icov",
        "lowlevel.mfcc.mean",
        "lowlevel.pitch_salience.mean",
        "lowlevel.pitch_salience.stdev",
        "lowlevel.silence_rate_20dB.mean",
        "lowlevel.silence_rate_20dB.stdev",
        "lowlevel.silence_rate_30dB.mean",
        "lowlevel.silence_rate_30dB.stdev",
        "lowlevel.silence_rate_60dB.mean",
        "lowlevel.silence_rate_60dB.stdev",
        "lowlevel.spectral_centroid.mean",
        "lowlevel.spectral_centroid.stdev",
        "lowlevel.spectral_complexity.mean",
        "lowlevel.spectral_complexity.stdev",
        "lowlevel.spectral_contrast_coeffs.mean",
        "lowlevel.spectral_contrast_coeffs.stdev",
        "lowlevel.spectral_contrast_valleys.mean",
        "lowlevel.spectral_contrast_valleys.stdev",
        "lowlevel.spectral_decrease.mean",
        "lowlevel.spectral_decrease.stdev",
        "lowlevel.spectral_energy.mean",
        "lowlevel.spectral_energy.stdev",
        "lowlevel.spectral_energyband_high.mean",
        "lowlevel.spectral_energyband_high.stdev",
        "lowlevel.spectral_energyband_low.mean",
        "lowlevel.spectral_energyband_low.stdev",
        "lowlevel.spectral_energyband_middle_high.mean",
        "lowlevel.spectral_energyband_middle_high.stdev",
        "lowlevel.spectral_energyband_middle_low.mean",
        "lowlevel.spectral_energyband_middle_low.stdev",
        "lowlevel.spectral_entropy.mean",
        "lowlevel.spectral_entropy.stdev",
        "lowlevel.spectral_flux.mean",
        "lowlevel.spectral_flux.stdev",
        "lowlevel.spectral_kurtosis.mean",
        "lowlevel.spectral_kurtosis.stdev",
        "lowlevel.spectral_rms.mean",
        "lowlevel.spectral_rms.stdev",
        "lowlevel.spectral_rolloff.mean",
        "lowlevel.spectral_rolloff.stdev",
        "lowlevel.spectral_skewness.mean",
        "lowlevel.spectral_skewness.stdev",
        "lowlevel.spectral_spread.mean",
        "lowlevel.spectral_spread.stdev",
        "lowlevel.spectral_strongpeak.mean",
        "lowlevel.spectral_strongpeak.stdev",
        "lowlevel.zerocrossingrate.mean",
        "lowlevel.zerocrossingrate.stdev",
        "metadata.audio_properties.analysis.downmix",
        "metadata.audio_properties.analysis.equal_loudness",
        "metadata.audio_properties.analysis.length",
        "metadata.audio_properties.analysis.sample_rate",
        "metadata.audio_properties.analysis.start_time",
        "metadata.audio_properties.bit_rate",
        "metadata.audio_properties.codec",
        "metadata.audio_properties.length",
        "metadata.audio_properties.lossless",
        "metadata.audio_properties.md5_encoded",
        "metadata.audio_properties.number_channels",
        "metadata.audio_properties.replay_gain",
        "metadata.audio_properties.sample_rate",
        "metadata.tags.file_name",
        "metadata.version.essentia",
        "metadata.version.essentia_git_sha",
        "metadata.version.extractor",
        "rhythm.beats_count",
        "rhythm.beats_loudness.mean",
        "rhythm.beats_loudness.stdev",
        "rhythm.beats_loudness_band_ratio.mean",
        "rhythm.beats_loudness_band_ratio.stdev",
        "rhythm.beats_position",
        "rhythm.bpm",
        "rhythm.bpm_histogram",
        "rhythm.bpm_histogram_first_peak_bpm",
        "rhythm.bpm_histogram_first_peak_weight",
        "rhythm.bpm_histogram_second_peak_bpm",
        "rhythm.bpm_histogram_second_peak_spread",
        "rhythm.bpm_histogram_second_peak_weight",
        "rhythm.danceability",
        "rhythm.onset_rate",
        "tonal.chords_changes_rate",
        "tonal.chords_histogram",
        "tonal.chords_key",
        "tonal.chords_number_rate",
        "tonal.chords_scale",
        "tonal.chords_strength.mean",
        "tonal.chords_strength.stdev",
        "tonal.hpcp.mean",
        "tonal.hpcp.stdev",
        "tonal.hpcp_crest.mean",
        "tonal.hpcp_crest.stdev",
        "tonal.hpcp_entropy.mean",
        "tonal.hpcp_entropy.stdev",
        "tonal.key_edma.key",
        "tonal.key_edma.scale",
        "tonal.key_edma.strength",
        "tonal.key_krumhansl.key",
        "tonal.key_krumhansl.scale",
        "tonal.key_krumhansl.strength",
        "tonal.key_temperley.key",
        "tonal.key_temperley.scale",
        "tonal.key_temperley.strength",
        "tonal.thpcp",
        "tonal.tuning_diatonic_strength",
        "tonal.tuning_equal_tempered_deviation",
        "tonal.tuning_frequency",
        "tonal.tuning_nontempered_energy_ratio",
    ]
    f = open(fname, "w")
    writer = csv.writer(f)
    writer.writerow(start_row)
    f.close()


# def write_csv(fname, song, feature):
#     features_names = sorted(features.descriptorNames())
#     row = []
#     row.append(song)
#     for name in features_names:
#         if type(feature[name]) == type(0) or type(feature[name]) == type(0.1):
#             row.append(feature[name])
#         else:
#             row.append(0)
#
#     f = open(fname, "a")
#     writer = csv.writer(f)
#     writer.writerow(row)
#     f.close()


def compute_time(audio):
    duration = es.Duration()(audio)
    effectiveDuration = es.EffectiveDuration()(audio)
    dynamicComplexity, loudness = es.DynamicComplexity()(audio)
    intensity = es.Intensity()(audio)
    return {
        "duration": duration,
        "effective_duration": effectiveDuration,
        "dynamicComplexity": dynamicComplexity,
        "loudness": loudness,
        "intensity": intensity,
    }


def compute_tempo(audio):
    bpm = es.PercivalBpmEstimator()(audio)
    bpm2, beats, beats_confidence, _, beats_intervals = es.RhythmExtractor2013(
        method="multifeature"
    )(audio)
    loudness, loudnessBandRatio = es.BeatsLoudness(beats=beats)(audio)
    danceability, dfa = es.Danceability()(audio)
    loudness = float(np.mean(loudness))

    return {
        "bpm": int(bpm),
        "bpm_loudness": loudness,
        "danceability": int((danceability * 100) / 3),
    }


def compute_tonal(fname):
    loader = ess.MonoLoader(filename=fname)
    framecutter = ess.FrameCutter(frameSize=4096, hopSize=2048, silentFrames="noise")
    windowing = ess.Windowing(type="blackmanharris62")
    spectrum = ess.Spectrum()
    spectralpeaks = ess.SpectralPeaks(
        # orderBy="magnitude",
        magnitudeThreshold=0.00001,
        minFrequency=20,
        maxFrequency=3500,
        maxPeaks=60,
    )

    # Use default HPCP parameters for plots, however we will need higher resolution
    # and custom parameters for better Key estimation

    hpcp = ess.HPCP()
    hpcp_key = ess.HPCP(
        size=36,  # we will need higher resolution for Key estimation
        # assume tuning frequency is 44100.
        referenceFrequency=440,
        bandPreset=False,
        minFrequency=20,
        maxFrequency=3500,
        weightType="cosine",
        nonLinear=False,
        windowSize=1.0,
    )

    key = ess.Key(
        profileType="edma",  # Use profile for electronic music
        numHarmonics=4,
        pcpSize=36,
        slope=0.6,
        usePolyphony=True,
        useThreeChords=True,
    )

    inharmonicity = ess.Inharmonicity()
    harmonicPeaks = ess.HarmonicPeaks()
    pitchYinFFT = ess.PitchYinFFT()
    dissonance = ess.Dissonance()

    # Use pool to store data
    pool = essentia.Pool()

    # Connect streaming algorithms
    loader.audio >> framecutter.signal
    framecutter.frame >> windowing.frame >> spectrum.frame
    spectrum.spectrum >> spectralpeaks.spectrum
    spectralpeaks.magnitudes >> hpcp.magnitudes
    spectralpeaks.frequencies >> hpcp.frequencies
    spectralpeaks.magnitudes >> hpcp_key.magnitudes
    spectralpeaks.frequencies >> hpcp_key.frequencies
    hpcp_key.hpcp >> key.pcp
    hpcp.hpcp >> (pool, "tonal.hpcp")
    key.key >> (pool, "tonal.key_key")
    key.scale >> (pool, "tonal.key_scale")
    key.strength >> (pool, "tonal.key_strength")

    spectrum.spectrum >> pitchYinFFT.spectrum
    pitchYinFFT.pitch >> harmonicPeaks.pitch
    pitchYinFFT.pitchConfidence >> None
    spectralpeaks.frequencies >> harmonicPeaks.frequencies
    spectralpeaks.magnitudes >> harmonicPeaks.magnitudes
    harmonicPeaks.harmonicFrequencies >> inharmonicity.frequencies
    harmonicPeaks.harmonicMagnitudes >> inharmonicity.magnitudes
    harmonicPeaks.harmonicFrequencies >> dissonance.frequencies
    harmonicPeaks.harmonicMagnitudes >> dissonance.magnitudes
    inharmonicity.inharmonicity >> (pool, "tonal.inharmonicity_inharmonicity")
    dissonance.dissonance >> (pool, "tonal.dissonance_dissonance")

    # Run streaming network
    essentia.run(loader)

    chords, strenght = es.ChordsDetection(hopSize=2048, windowSize=2)(
        pool["tonal.hpcp"]
    )

    (
        chordHistogram,
        chordsNumberRate,
        chordsChangesRate,
        chordsKey,
        chordsScale,
    ) = es.ChordsDescriptors()(chords, pool["tonal.key_key"], pool["tonal.key_scale"])

    inharm = sum(pool["tonal.inharmonicity_inharmonicity"])
    diss = sum(pool["tonal.dissonance_dissonance"])
    chords_set = set(chords)
    chordsNumber = len(chords_set)

    return {
        # "chords": chords,
        "key": pool["tonal.key_key"] + " " + pool["tonal.key_scale"],
        "chordsChangesRate": chordsChangesRate,
        "chordsNumber": chordsNumber,
        "inharmonicity": inharm,
        "dissonance": diss,
    }


# if __name__ == "__main__":
#
#     # Uncomment if slicing is not performed
#     #
#     # audiofilenames_full = [f for f in listdir(DIR_WAV_FILES) if (os.path.isfile(os.path.join(DIR_WAV_FILES, f)) and (f.endswith(".wav") or f.endswith(".mp3")))]
#     audiofilenames_full = extract_files()
#     #
#     # Split each file in 3 equal parts; rename each file part with _000, _001, _002.
#     slices_number = 3
#     audiofilenames = slice_files(audiofilenames_full, slices_number)
#
#     # Comment if slicing is not performed:
#     audiofilenames = [
#         f
#         for f in sorted(listdir(DIR_SPLITTED_WAV_FILES))
#         if (
#             os.path.isfile(os.path.join(DIR_SPLITTED_WAV_FILES, f))
#             and (f.endswith(".wav") or f.endswith(".mp3"))
#         )
#     ]
#
#     order_processed_files = []
#
#     init_csv(RESULT_CSV)
#     pbar = tqdm(
#         total=len(audiofilenames),
#         unit="files",
#         bar_format="extracting:\t{percentage:.0f}%|{bar:100}{r_bar}",
#     )
#     for f in audiofilenames:
#         pbar.set_postfix({"filename": f[:20]})
#         try:
#             audiofilename = os.path.join(DIR_SPLITTED_WAV_FILES, f)
#             features = compute_all_features(audiofilename)
#
#             write_csv(RESULT_CSV, f, features)
#             order_processed_files.append(f)
#         except:
#             print("\n > Fail", audiofilename)
#
#         pbar.update(1)
#
