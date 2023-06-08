import argparse
import librosa
import numpy as np
import pygame as pygame

from frequencyband import FrequencyBand

BASS_CUTOFF = 300
TREBLE_CUTOFF = 4000

parser = argparse.ArgumentParser(prog='BouncingBars',
                                 description='Music visualizer that animates the changing amplitudes of configurable '
                                             'frequency bands to chosen sound file.')
parser.add_argument(
    "filename",
    help="Name of audio file to visualize (mp3)"
)
parser.add_argument(
    "--bass_bars",
    help="Number of bass range frequency bars",
    default=20,
    type=int
)
parser.add_argument(
    "--mid_bars",
    help="Number of midrange frequency bars",
    default=20,
    type=int
)
parser.add_argument(
    "--treble_bars",
    help="Number of treble frequency bands",
    default=20,
    type=int
)
parser.add_argument(
    "--bass_color",
    help="Color of bass range bars, 'r,g,b'",
    default="255,0,0",
)
parser.add_argument(
    "--mid_color",
    help="Color of mid range bars, 'r,g,b'",
    default="0,255,0",
)
parser.add_argument(
    "--treble_color",
    help="Color of treble range bars, 'r,g,b'",
    default="0,0,255",
)
parser.add_argument(
    "--background_color",
    help="Color of background, 'r,g,b'",
    default="255,255,255"
)


def get_decibel(target_time, freq, frequencies_index_ratio):
    return spectrogram[int(freq * frequencies_index_ratio)][int(target_time * time_index_ratio)]

if __name__ == '__main__':

    args = parser.parse_args()

    time_series, sample_rate = librosa.load(args.filename)  # getting information from the file

    # getting a matrix which contains amplitude values according to frequency and time indexes
    stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))

    spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix

    frequencies = librosa.core.fft_frequencies(n_fft=2048 * 4)  # getting an array of frequencies

    # split into frequency bands
    bass_frequencies, mid_frequencies, treble_frequencies = np.split(frequencies, [BASS_CUTOFF, TREBLE_CUTOFF])

    # getting an array of time periodic
    times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)

    time_index_ratio = len(times)/times[len(times) - 1]



    pygame.init()

    infoObject = pygame.display.Info()

    screen_w = int(infoObject.current_w)
    screen_h = int(infoObject.current_h / 1.1)

    background_color = pygame.Color(list(map(int, args.background_color.split(","))))

    bass_band = FrequencyBand(lower_bound=0,
                              upper_bound=BASS_CUTOFF,
                              song_frequencies=bass_frequencies,
                              base_color=args.bass_color,
                              min_height=0,
                              max_height= 0.5 * screen_h,
                              screen_w=screen_w,
                              screen_h=screen_h,
                              num_bars=args.bass_bars)

    mid_band = FrequencyBand(lower_bound=BASS_CUTOFF,
                             upper_bound=TREBLE_CUTOFF,
                             song_frequencies=mid_frequencies,
                             base_color=args.mid_color,
                             min_height=screen_h * 0.25,
                             max_height=screen_h * 0.9,
                             screen_w=screen_w,
                             screen_h=screen_h,
                             num_bars=args.mid_bars)

    treble_band = FrequencyBand(lower_bound=TREBLE_CUTOFF,
                                upper_bound=20000,
                                song_frequencies=treble_frequencies,
                                base_color=args.treble_color,
                                min_height=screen_h * 0.5,
                                max_height=screen_h,
                                screen_w=screen_w,
                                screen_h=screen_h,
                                num_bars=args.treble_bars)

    # Set up the drawing window
    screen = pygame.display.set_mode([screen_w, screen_h])

    t = pygame.time.get_ticks()
    getTicksLastFrame = t

    pygame.mixer.music.load(args.filename)
    pygame.mixer.music.play(0)

    # Run until the user asks to quit
    running = True
    while running:

        t = pygame.time.get_ticks()
        deltaTime = (t - getTicksLastFrame) / 1000.0
        getTicksLastFrame = t

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(background_color)

        for treble in treble_band.bars:
            treble.update(deltaTime, get_decibel(pygame.mixer.music.get_pos()/1000.0, treble.freq, treble_band.frequency_index_ratio))
            treble.render(screen)
        for mid in mid_band.bars:
            mid.update(deltaTime, get_decibel(pygame.mixer.music.get_pos()/1000.0, mid.freq, mid_band.frequency_index_ratio))
            mid.render(screen)
        for bass in bass_band.bars:
            bass.update(deltaTime, get_decibel(pygame.mixer.music.get_pos()/1000.0, bass.freq, bass_band.frequency_index_ratio))
            bass.render(screen)

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()
