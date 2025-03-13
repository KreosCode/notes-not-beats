# notes-not-beats
## mapping guide
> [General]
> - song_name<br>
> str<br>
> supported formats: mp3<br>
> name of the file, that contains song<br>

-  bg_type
str <br>
video, image, None <br>

- bg_name
str <br>
if image: suported formats: png, jpeg <br>
if video: suported formats: mp4 <br>
Note: image file need to be included anyway (nameOfImage || nameOfImage_nameOfVideo) <br>

[Difficulty]
- hp_drain <br>
float <br>
value of the lost hp with each missed note <br>

[TimingOptions]
- skipToStream <br>
bool <br>
True - song starts from the beginning and can be skipped to the timing, when the first note appears <br>
False - song starts from the timing, when the first note appears <br>
Default value - True <br>

- skipEnd
bool <br>
True - result screen is appearing in 3 seconds after the last note is being played <br>
False - song is being played till the end, press skip button to move to the result screen <br>
Default value - False <br>

[NoteTimings] <br>
expression = name1, name2, end_timing1, end_timing2, side <br>
EXPRESSION CONTAINS EITHER 3 OR 5 VALUES IN TOTAL <br> <br>

- name1, name2 <br>
str <br>
input is the name of file, that contain desired note / pause <br>
supported formats: wav <br>
name1 is prerequisite, name2 is optional <br>
If you writing only one name, then you put a simple note <br>
Writing two notes means that name1 is the start of the slider note and name2 is end of slider note <br>
Note: if 'pause' value's provided instead of any of notes, then note will appear without any sound <br>

- endTiming1 <br>
int <br>
input in ms <br>
perfect timing for the note1 to be pressed <br>

- endTiming2 <br>
int <br>
input in ms <br>
perfect timing for the note2 to be pressed <br>

- side <br>
str <br>
top / bottom / left / right <br>
side, where the note / slider will appear <br> <br>

All notes are being written in the order from the first one to the last one <br>
expression1 <br>
expression2 <br>
expression3  <br>
...
expressionLast <br>
