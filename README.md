# notes-not-beats
## mapping guide
**[General]**
- song_name
    - str
    - supported formats: mp3
    - name of the file, that contains song

- bg_type
    - str
    - video, image, None

- bg_name
    - str
    - if image: suported formats: png, jpeg 
    - if video: suported formats: mp4 
*Note*: image file need to be included anyway (nameOfImage || nameOfImage_nameOfVideo) 

**[Difficulty]**
- hp_drain
    - float
    - value of the lost hp with each missed note

**[TimingOptions]**
- skipToStream
    - bool
    - True - song starts from the beginning and can be skipped to the timing, when the first note appears 
    - False - song starts from the timing, when the first note appears 
    - Default value - True

- skipEnd
    - bool
    - True - result screen is appearing in 3 seconds after the last note is being played 
    - False - song is being played till the end, press skip button to move to the result screen 
    - Default value - False 

**[NoteTimings]**
- expression = name1, name2, end_timing1, end_timing2, side 
- EXPRESSION CONTAINS EITHER 3 OR 5 VALUES IN TOTAL  

- name1, name2
    - str 
    - input is the name of file, that contain desired note / pause 
    - supported formats: wav 
    - name1 is prerequisite, name2 is optional 
    - If you writing only one name, then you put a simple note 
    - Writing two notes means that name1 is the start of the slider note and name2 is end of slider note 
*Note*: if 'pause' value's provided instead of any of notes, then note will appear without any sound 

- endTiming1 
    - int 
    - input in ms 
    - perfect timing for the note1 to be pressed 

- endTiming2 
    - int 
    - input in ms 
    - perfect timing for the note2 to be pressed 

- side 
    - str 
    - top / bottom / left / right 
    - side, where the note / slider will appear  

*Note*: All notes are being written in the order from the first one to the last one 
expression1<br>
expression2<br>
expression3<br>
...<br>
expressionLast