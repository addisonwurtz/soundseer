# Soundseer: 
By Addison Wurtz

***

## Description: 
Soundseer is a music visualizer that uses python animation libraries in conjunction with librosa to generate and play
custom animations for mp3 files. 
Soundseer 

## Example Configurations 
I've included some screenshots along with the commands to generate that configuration. I have included a few example 
songs in the repository to ensure that these examples will run out-of-the-box.
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

## Dependencies
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Roadmap

- Beat detection visualizer + pyarcade radar sweet
- Keys to notes visualizer using colors for notes ... "raindrops" (pyarcare lights tutorial??)
- Pyarcade glow shader???
- Make a sidescrolling animation?

## References 
https://gitlab.com/avirzayev/medium-audio-visualizer-code/-/blob/master/main.py

https://api.arcade.academy/en/stable/examples/radar_sweep.html#radar-sweep

## License
[MIT License](/LICENSE)