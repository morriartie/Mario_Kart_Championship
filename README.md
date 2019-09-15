# About
This tool takes the races info of Time Trials in Mario Kart (or any race) and build graphs and rankings. See an example of the txt in the files.
Data must be inserted manually

# Requirements
matplotlib
numpy

# Usage
* Fill the txt with player name, race time, best lap and worse lap each time a fried plays. Incrementing the index accordingly (last parameter)

## Example
python3 mario_kart_board.py baby_park_times.txt

# Etc
* The first line of the txt must contain the track name; a path for it will be created for saving the images
* Lines can be ignored by adding '#' to it (unless its the first line)
* Lines containing '--:--:--.---' as data will be ignored as well
* Lines can be left blank
