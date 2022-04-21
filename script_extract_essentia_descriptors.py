import essentia
import essentia.standard as es
from os import listdir
import os.path
#from os.path import isfile, join
import json_to_csv
import pandas as pd
import librosa
import soundfile as sf


DIR_WAV_FILES = '/Users/luca/Documents/Development/datasets/my_datasets/emotional_EEG_audio_Barry/Music_Files_trimmed/DONE'
DIR_SPLITTED_WAV_FILES = '/Users/luca/Documents/Development/datasets/my_datasets/emotional_EEG_audio_Barry/Music_Files_splitted_in_3_parts'
DIR_RESULTS_FILES = '/Users/luca/Documents/Development/datasets/my_datasets/emotional_EEG_audio_Barry/Music_Files_Results'


def compute_all_features(audiofilename):
    # Compute all features.
    # Aggregate 'mean' and 'stdev' statistics for all low-level, rhythm, and tonal frame features.
    features, features_frames = es.MusicExtractor(lowlevelStats=['mean', 'stdev'], 
                                                  rhythmStats=['mean', 'stdev'], 
                                                  tonalStats=['mean', 'stdev'])(audiofilename)
    return features


def write_features(features,audiofilename):
    # Write the aggregated features into a temporary directory.
    #from tempfile import TemporaryDirectory
    #temp_dir = TemporaryDirectory()
    #results_file = temp_dir.name + '/results.json'

    results_file = DIR_RESULTS_FILES + "/" + audiofilename + '_results.json'
    #print(results_file)
    es.YamlOutput(filename=results_file, format="json")(features)

    #Here I remove the line starting with beats_position as this is a variable lenght feature
    with open(results_file, "r") as f:
        lines = f.readlines()
    
    lines_to_write = [line for line in lines if not line.startswith('    "beats_position"')]
    
    with open(results_file, "w") as f:    
        f.write(''.join(lines_to_write))


def slice_files(audiofilenames_full, slices_number):

    #slices_number = 3
    for f in audiofilenames_full:
        print(f"slicing file {f}")
        
        y, sr = librosa.load(os.path.join(DIR_WAV_FILES, f))
        slice_length = int(y.size/slices_number) 

        for i in range(3):
            audio_data = y[i*slice_length:(i+1)*slice_length]
            slice_filename = os.path.join(DIR_SPLITTED_WAV_FILES, f + '_00' + str(i) + '.wav')
            sf.write(slice_filename, audio_data, sr, subtype='PCM_24')
       
    audiofilenames = [f for f in listdir(DIR_SPLITTED_WAV_FILES) if (os.path.isfile(os.path.join(DIR_SPLITTED_WAV_FILES, f)) and f.endswith(".wav"))]
    return audiofilenames




if __name__ == '__main__':
    
    # Uncomment if slicing is not performed
    #
    #audiofilenames_full = [f for f in listdir(DIR_WAV_FILES) if (os.path.isfile(os.path.join(DIR_WAV_FILES, f)) and (f.endswith(".wav") or f.endswith(".mp3")))]
    #
    # Split each file in 3 equal parts; rename each file part with _000, _001, _002.
    #slices_number = 3
    #audiofilenames = slice_files(audiofilenames_full, slices_number)

    # Comment if slicing is not performed:
    audiofilenames = [f for f in listdir(DIR_SPLITTED_WAV_FILES) if (os.path.isfile(os.path.join(DIR_SPLITTED_WAV_FILES, f)) and (f.endswith(".wav") or f.endswith(".mp3")))]


    order_processed_files = []
    emotion_labels = []

    """
    emotion_labels_dict = {
                            "ms01_1.wav": "Angry",
                            "ms01_2.wav": "Happy",
                            "ms01_3.wav": "Relaxed",
                            "ms01_4.wav": "Relaxed",
                            "ms01_5.wav": "Sad",
                            "ms01_6.wav": "Sad",
                            "ms02_1.wav": "Relaxed",
                            "ms02_2.wav": "Angry",
                            "ms02_3.wav": "Angry",
                            "ms02_4.wav": "Relaxed",
                            "ms02_5.wav": "Happy",
                            "ms02_6.wav": "Sad",
                            "ms03_1.wav": "Happy",
                            "ms03_2.wav": "Angry",
                            "ms03_3.wav": "Sad",
                            "ms03_4.wav": "Relaxed",
                            "ms04_1.wav": "Relaxed",
                            "ms04_2.wav": "Relaxed",
                            "ms04_3.wav": "Happy",
                            "ms04_4.wav": "Happy",
                            "ms04_5.wav": "Angry",
                            "ms04_6.wav": "Angry",
                            "ms04_7.wav": "Sad",
                            "ms04_8.wav": "Sad",
                            "ms05_1.wav": "Relaxed",
                            "ms05_2.wav": "Happy",
                            "ms05_3.wav": "Angry",
                            "ms05_4.wav": "Angry",
                            "ms05_5.wav": "Sad",
                            "ms06_1.wav": "Angry",
                            "ms06_2.wav": "Happy",
                            "ms06_3.wav": "Relaxed",
                            "ms06_4.wav": "Sad",
                            "ms06_5.wav": "Relaxed",
                            "ms06_6.wav": "Sad",
                            "ms06_7.wav": "Happy",
                            "ms06_8.wav": "Angry",
                            "ms07_1.wav": "Relaxed",
                            "ms07_2.wav": "Sad",
                            "ms07_3.wav": "Happy",
                            "ms07_4.wav": "Angry",
                            "ms08_1.wav": "Happy",
                            "ms08_2.wav": "Relaxed",
                            "ms08_3.wav": "Sad",
                            "ms08_4.wav": "Angry",
                            "ms08_5.wav": "Relaxed",
                            "ms09_1.wav": "Happy",
                            "ms09_2.wav": "Relaxed",
                            "ms09_3.wav": "Angry",
                            "ms09_4.wav": "Relaxed",
                            "ms09_5.wav": "Happy",
                            "ms10_1.wav": "Happy",
                            "ms10_2.wav": "Relaxed",
                            "ms10_3.wav": "Sad",
                            "ms10_4.wav": "Angry",
                            "ms11_1.wav": "Relaxed",
                            "ms11_2.wav": "Happy",
                            "ms11_3.wav": "Angry",
                            "ms11_4.wav": "Sad"
                            }

    """

    #Angry: 0, Happy: 1, Relaxed: 2, Sad: 3 
    ''' 
    emotion_labels_dict = {
                            "ms01_1.wav": 0,
                            "ms01_2.wav": 1,
                            "ms01_3.wav": 2,
                            "ms01_4.wav": 2,
                            "ms01_5.wav": 3,
                            "ms01_6.wav": 3,
                            "ms02_1.wav": 2,
                            "ms02_2.wav": 0,
                            "ms02_3.wav": 0,
                            "ms02_4.wav": 2,
                            "ms02_5.wav": 1,
                            "ms02_6.wav": 3,
                            "ms03_1.wav": 1,
                            "ms03_2.wav": 0,
                            "ms03_3.wav": 3,
                            "ms03_4.wav": 2,
                            "ms04_1.wav": 2,
                            "ms04_2.wav": 2,
                            "ms04_3.wav": 1,
                            "ms04_4.wav": 1,
                            "ms04_5.wav": 0,
                            "ms04_6.wav": 0,
                            "ms04_7.wav": 3,
                            "ms04_8.wav": 3,
                            "ms05_1.wav": 2,
                            "ms05_2.wav": 1,
                            "ms05_3.wav": 0,
                            "ms05_4.wav": 0,
                            "ms05_5.wav": 3,
                            "ms06_1.wav": 0,
                            "ms06_2.wav": 1,
                            "ms06_3.wav": 2,
                            "ms06_4.wav": 3,
                            "ms06_5.wav": 2,
                            "ms06_6.wav": 3,
                            "ms06_7.wav": 1,
                            "ms06_8.wav": 0,
                            "ms07_1.wav": 2,
                            "ms07_2.wav": 3,
                            "ms07_3.wav": 1,
                            "ms07_4.wav": 0,
                            "ms08_1.wav": 1,
                            "ms08_2.wav": 2,
                            "ms08_3.wav": 3,
                            "ms08_4.wav": 0,
                            "ms08_5.wav": 2,
                            "ms09_1.wav": 1,
                            "ms09_2.wav": 2,
                            "ms09_3.wav": 0,
                            "ms09_4.wav": 2,
                            "ms09_5.wav": 1,
                            "ms10_1.wav": 1,
                            "ms10_2.wav": 2,
                            "ms10_3.wav": 3,
                            "ms10_4.wav": 0,
                            "ms11_1.wav": 2,
                            "ms11_2.wav": 1,
                            "ms11_3.wav": 0,
                            "ms11_4.wav": 3
                            }
    '''
    emotion_labels_dict = {
                            "ms01_1.wav_000.wav": 0,
                            "ms01_2.wav_000.wav": 1,
                            "ms01_3.wav_000.wav": 2,
                            "ms01_4.wav_000.wav": 2,
                            "ms01_5.wav_000.wav": 3,
                            "ms01_6.wav_000.wav": 3,
                            "ms02_1.wav_000.wav": 2,
                            "ms02_2.wav_000.wav": 0,
                            "ms02_3.wav_000.wav": 0,
                            "ms02_4.wav_000.wav": 2,
                            "ms02_5.wav_000.wav": 1,
                            "ms02_6.wav_000.wav": 3,
                            "ms03_1.wav_000.wav": 1,
                            "ms03_2.wav_000.wav": 0,
                            "ms03_3.wav_000.wav": 3,
                            "ms03_4.wav_000.wav": 2,
                            "ms04_1.wav_000.wav": 2,
                            "ms04_2.wav_000.wav": 2,
                            "ms04_3.wav_000.wav": 1,
                            "ms04_4.wav_000.wav": 1,
                            "ms04_5.wav_000.wav": 0,
                            "ms04_6.wav_000.wav": 0,
                            "ms04_7.wav_000.wav": 3,
                            "ms04_8.wav_000.wav": 3,
                            "ms05_1.wav_000.wav": 2,
                            "ms05_2.wav_000.wav": 1,
                            "ms05_3.wav_000.wav": 0,
                            "ms05_4.wav_000.wav": 0,
                            "ms05_5.wav_000.wav": 3,
                            "ms06_1.wav_000.wav": 0,
                            "ms06_2.wav_000.wav": 1,
                            "ms06_3.wav_000.wav": 2,
                            "ms06_4.wav_000.wav": 3,
                            "ms06_5.wav_000.wav": 2,
                            "ms06_6.wav_000.wav": 3,
                            "ms06_7.wav_000.wav": 1,
                            "ms06_8.wav_000.wav": 0,
                            "ms07_1.wav_000.wav": 2,
                            "ms07_2.wav_000.wav": 3,
                            "ms07_3.wav_000.wav": 1,
                            "ms07_4.wav_000.wav": 0,
                            "ms08_1.wav_000.wav": 1,
                            "ms08_2.wav_000.wav": 2,
                            "ms08_3.wav_000.wav": 3,
                            "ms08_4.wav_000.wav": 0,
                            "ms08_5.wav_000.wav": 2,
                            "ms09_1.wav_000.wav": 1,
                            "ms09_2.wav_000.wav": 2,
                            "ms09_3.wav_000.wav": 0,
                            "ms09_4.wav_000.wav": 2,
                            "ms09_5.wav_000.wav": 1,
                            "ms10_1.wav_000.wav": 1,
                            "ms10_2.wav_000.wav": 2,
                            "ms10_3.wav_000.wav": 3,
                            "ms10_4.wav_000.wav": 0,
                            "ms11_1.wav_000.wav": 2,
                            "ms11_2.wav_000.wav": 1,
                            "ms11_3.wav_000.wav": 0,
                            "ms11_4.wav_000.wav": 3,
                            "ms01_1.wav_001.wav": 0,
                            "ms01_2.wav_001.wav": 1,
                            "ms01_3.wav_001.wav": 2,
                            "ms01_4.wav_001.wav": 2,
                            "ms01_5.wav_001.wav": 3,
                            "ms01_6.wav_001.wav": 3,
                            "ms02_1.wav_001.wav": 2,
                            "ms02_2.wav_001.wav": 0,
                            "ms02_3.wav_001.wav": 0,
                            "ms02_4.wav_001.wav": 2,
                            "ms02_5.wav_001.wav": 1,
                            "ms02_6.wav_001.wav": 3,
                            "ms03_1.wav_001.wav": 1,
                            "ms03_2.wav_001.wav": 0,
                            "ms03_3.wav_001.wav": 3,
                            "ms03_4.wav_001.wav": 2,
                            "ms04_1.wav_001.wav": 2,
                            "ms04_2.wav_001.wav": 2,
                            "ms04_3.wav_001.wav": 1,
                            "ms04_4.wav_001.wav": 1,
                            "ms04_5.wav_001.wav": 0,
                            "ms04_6.wav_001.wav": 0,
                            "ms04_7.wav_001.wav": 3,
                            "ms04_8.wav_001.wav": 3,
                            "ms05_1.wav_001.wav": 2,
                            "ms05_2.wav_001.wav": 1,
                            "ms05_3.wav_001.wav": 0,
                            "ms05_4.wav_001.wav": 0,
                            "ms05_5.wav_001.wav": 3,
                            "ms06_1.wav_001.wav": 0,
                            "ms06_2.wav_001.wav": 1,
                            "ms06_3.wav_001.wav": 2,
                            "ms06_4.wav_001.wav": 3,
                            "ms06_5.wav_001.wav": 2,
                            "ms06_6.wav_001.wav": 3,
                            "ms06_7.wav_001.wav": 1,
                            "ms06_8.wav_001.wav": 0,
                            "ms07_1.wav_001.wav": 2,
                            "ms07_2.wav_001.wav": 3,
                            "ms07_3.wav_001.wav": 1,
                            "ms07_4.wav_001.wav": 0,
                            "ms08_1.wav_001.wav": 1,
                            "ms08_2.wav_001.wav": 2,
                            "ms08_3.wav_001.wav": 3,
                            "ms08_4.wav_001.wav": 0,
                            "ms08_5.wav_001.wav": 2,
                            "ms09_1.wav_001.wav": 1,
                            "ms09_2.wav_001.wav": 2,
                            "ms09_3.wav_001.wav": 0,
                            "ms09_4.wav_001.wav": 2,
                            "ms09_5.wav_001.wav": 1,
                            "ms10_1.wav_001.wav": 1,
                            "ms10_2.wav_001.wav": 2,
                            "ms10_3.wav_001.wav": 3,
                            "ms10_4.wav_001.wav": 0,
                            "ms11_1.wav_001.wav": 2,
                            "ms11_2.wav_001.wav": 1,
                            "ms11_3.wav_001.wav": 0,
                            "ms11_4.wav_001.wav": 3,
                            "ms01_1.wav_002.wav": 0,
                            "ms01_2.wav_002.wav": 1,
                            "ms01_3.wav_002.wav": 2,
                            "ms01_4.wav_002.wav": 2,
                            "ms01_5.wav_002.wav": 3,
                            "ms01_6.wav_002.wav": 3,
                            "ms02_1.wav_002.wav": 2,
                            "ms02_2.wav_002.wav": 0,
                            "ms02_3.wav_002.wav": 0,
                            "ms02_4.wav_002.wav": 2,
                            "ms02_5.wav_002.wav": 1,
                            "ms02_6.wav_002.wav": 3,
                            "ms03_1.wav_002.wav": 1,
                            "ms03_2.wav_002.wav": 0,
                            "ms03_3.wav_002.wav": 3,
                            "ms03_4.wav_002.wav": 2,
                            "ms04_1.wav_002.wav": 2,
                            "ms04_2.wav_002.wav": 2,
                            "ms04_3.wav_002.wav": 1,
                            "ms04_4.wav_002.wav": 1,
                            "ms04_5.wav_002.wav": 0,
                            "ms04_6.wav_002.wav": 0,
                            "ms04_7.wav_002.wav": 3,
                            "ms04_8.wav_002.wav": 3,
                            "ms05_1.wav_002.wav": 2,
                            "ms05_2.wav_002.wav": 1,
                            "ms05_3.wav_002.wav": 0,
                            "ms05_4.wav_002.wav": 0,
                            "ms05_5.wav_002.wav": 3,
                            "ms06_1.wav_002.wav": 0,
                            "ms06_2.wav_002.wav": 1,
                            "ms06_3.wav_002.wav": 2,
                            "ms06_4.wav_002.wav": 3,
                            "ms06_5.wav_002.wav": 2,
                            "ms06_6.wav_002.wav": 3,
                            "ms06_7.wav_002.wav": 1,
                            "ms06_8.wav_002.wav": 0,
                            "ms07_1.wav_002.wav": 2,
                            "ms07_2.wav_002.wav": 3,
                            "ms07_3.wav_002.wav": 1,
                            "ms07_4.wav_002.wav": 0,
                            "ms08_1.wav_002.wav": 1,
                            "ms08_2.wav_002.wav": 2,
                            "ms08_3.wav_002.wav": 3,
                            "ms08_4.wav_002.wav": 0,
                            "ms08_5.wav_002.wav": 2,
                            "ms09_1.wav_002.wav": 1,
                            "ms09_2.wav_002.wav": 2,
                            "ms09_3.wav_002.wav": 0,
                            "ms09_4.wav_002.wav": 2,
                            "ms09_5.wav_002.wav": 1,
                            "ms10_1.wav_002.wav": 1,
                            "ms10_2.wav_002.wav": 2,
                            "ms10_3.wav_002.wav": 3,
                            "ms10_4.wav_002.wav": 0,
                            "ms11_1.wav_002.wav": 2,
                            "ms11_2.wav_002.wav": 1,
                            "ms11_3.wav_002.wav": 0,
                            "ms11_4.wav_002.wav": 3
                            }

    for f in audiofilenames:
        print(60*"-")
        print(f"filename: {f}")
        audiofilename = os.path.join(DIR_SPLITTED_WAV_FILES, f)
        features = compute_all_features(audiofilename)
        write_features(features,f)
        order_processed_files.append(f)
        emotion_labels.append(emotion_labels_dict[f])


    resultsfilenames = [f for f in listdir(DIR_RESULTS_FILES) if (os.path.isfile(os.path.join(DIR_RESULTS_FILES, f)) and f.endswith(".json"))]
    print(60*"-")
    print(f"resultsfilenames: {resultsfilenames}")

    args_input = [DIR_RESULTS_FILES + "/" + f for f in resultsfilenames]
    args_output = DIR_RESULTS_FILES + "/" + "temp.csv"
    args_include = "metadata.audio_properties.* metadata.tags.musicbrainz_recordingid.0 lowlevel.* rhythm.* tonal.*"    
    args_ignore = None
    args_add_filename = None
    json_to_csv.convert_all(args_input, args_output, args_include, args_ignore, args_add_filename)

    print(order_processed_files)


 
    csv_input = pd.read_csv(args_output)

    
    csv_input['AudioFilenames'] = order_processed_files
    cols = list(csv_input.columns)
    cols = [cols[-1]] + cols[:-1]
    csv_input = csv_input[cols]


    csv_input['Emotion'] = emotion_labels
    cols = list(csv_input.columns)
    cols = [cols[-1]] + cols[:-1]
    csv_input = csv_input[cols]

    csv_input.to_csv(DIR_RESULTS_FILES + "/" + 'all_results.csv', index=False)

