import essentia
import essentia.standard as es
import essentia.streaming
import IPython
# from pylab import plot, show, figure, imshow
import matplotlib.pyplot as plt
from tempfile import TemporaryDirectory

loader = es.MonoLoader(
    filename='OST/53 - Cars/Rascal Flatts - Life is a Highway.mp3')
audio = loader()
# IPython.display.Audio('OST/Cars/Rascal Flatts - Life is a Highway.mp3')

print(audio)

plt.rcParams['figure.figsize'] = (
    15, 6)  # set plot sizes to something larger than default

plt.plot(audio[1 * 44100:2 * 44100])
plt.title("This is how the 2nd second of this audio looks like:")
plt.savefig('audio')

rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(
    audio[:60 * 44100])

print("BPM:", bpm)
print("Beat positions (sec.):", beats[:10])
print("Beat estimation confidence:", beats_confidence)

marker = es.AudioOnsetsMarker(onsets=beats, type='beep')
marked_audio = marker(audio)

temp_dir = TemporaryDirectory()
#es.MonoWriter(filename=temp_dir.name + '/dubstep_beats.flac')(marked_audio)

peak1_bpm, peak1_weight, peak1_spread, peak2_bpm, peak2_weight, peak2_spread, histogram = \
    es.BpmHistogramDescriptors()(beats_intervals)

print("Overall BPM (estimated before): %0.1f" % bpm)
print("First histogram peak: %0.1f bpm" % peak1_bpm)
print("Second histogram peak: %0.1f bpm" % peak2_bpm)

fig, ax = plt.subplots()
ax.bar(range(len(histogram)), histogram, width=1)
ax.set_xlabel('BPM')
ax.set_ylabel('Frequency of occurrence')
plt.title("BPM histogram")
ax.set_xticks([20 * x + 0.5 for x in range(int(len(histogram) / 20))])
ax.set_xticklabels([str(20 * x) for x in range(int(len(histogram) / 20))])
plt.savefig('bpm')