#  script token from the essentia website
#  https://essentia.upf.edu/essentia_python_examples.html#tonality-analysis-hpcp-key-and-scale
#  and adapted for the usecase

import essentia.streaming as ess
import essentia


def get_song_key(fname):
    # Initialize algorithms we will use
    loader = ess.MonoLoader(filename=fname)
    framecutter = ess.FrameCutter(frameSize=4096, hopSize=2048, silentFrames="noise")
    windowing = ess.Windowing(type="blackmanharris62")
    spectrum = ess.Spectrum()
    spectralpeaks = ess.SpectralPeaks(
        orderBy="magnitude",
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

    # Run streaming network
    essentia.run(loader)

    # print("Estimated key and scale:", pool['tonal.key_key'] + " " + pool['tonal.key_scale'])
    return pool["tonal.key_key"] + " " + pool["tonal.key_scale"]
