# Soundseer 
### By Addison Wurtz

***

## Description 
Soundseer is a music visualizer that uses librosa to analyze sound files and create custom animations for mp3 files. 
Soundseer includes visualizers from pygame and python arcade. 

The "bouncing bars" visualizer uses a spectrogram for each animation frame. The amplitude of various frequency "buckets" 
are then animated in the form of three audio bars--representing the bass, mid, and treble frequencies. Each audio bar
has a configurable number of frequency bars. Additionally, all the colors are configurable.

While working on my first animation, it became clear that pygame offered fairly limited options for expansion. After 
some searching I came across python arcade. It has much more visually complex rendering capabilities and build in tools.
At this time, I am working on building a visualizer in arcade using librosa's beat and note detection tools. 

## Pygame Examples
I've included some screenshots along with the commands to generate that configuration. There are example 
songs in the repository to ensure that these commands will run out-of-the-box.

### Default:
```
python bouncingbars.py Songs\Moby-Porcelain.mp3
```
![Screenshot from visualizer with default settings](screenshots/default.jpg)

### Shades of purple with custom number of frequency bars:
```
python bouncingbars.py Songs\DietMountainDewInstrumental.mp3 --bass_bars 15 --mid_bars 30 --treble_bars 60 
--bass_color 55,0,55 --mid_color 155,0,155 --treble_color 255,0,255 --background_color 5,0,5     
```
![Screenshot from visualizer with custom purple settings](screenshots/custom_purple.jpg)

### Playing with colors and number of bars:
```
python bouncingbars.py Songs\MKDomDolla-RhymeDust.mp3 --bass_bars 12 --mid_bars 60 --treble_bars 36 --bass_color 
155,50,0 --mid_color 200,100,0 --treble_color 255,200,0 --background_color 0,100,240                                   
```
![Screenshot from visualizer with custom colors](screenshots/yellow.jpg)

## Python Arcade Examples

### Beat Radar:

***

## Dependencies
Soundseer uses librosa, pygame, Python Arcade, PyGame, and NumPy

`pip install librosa`

`pip install pygame`

`pip install arcade`

`pip install numpy`

***

## Roadmap

- Beat detection visualizer + pyarcade radar sweep
- Keys to notes visualizer using colors for notes ... "raindrops" (arcade lights)
- Arcade glow shader???
- Make a side-scrolling animation?

***

## References 
[Music Visualizer Tutorial](https://gitlab.com/avirzayev/medium-audio-visualizer-code/-/blob/master/main.py)

[Arcade Radar Tutorial](https://api.arcade.academy/en/stable/examples/radar_sweep.html#radar-sweep)

## License
[MIT License](/LICENSE.md)