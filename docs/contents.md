# Contents

- All recordings are collected from the web. Their source URLs can be found in `audio.csv`. They come in either MP3 or OPUS format, depending on their sources, which can be converted into WAV files with [FFmpeg](http://ffmpeg.org/)
- Each folder in the `audio` directory corresponds to a _collection_ that contains recordings with similar recording setups except the `misc` folder. (Due to copyright concern, audio files in the collections _shunske-sato_ and _young-talents_ need to be downloaded from YouTube.)
- The corresponding reference score for each recording can be found in `info.csv`. They come in MusicXML format, which can be opened with [MuseScore](https://musescore.org/), [music21](https://web.mit.edu/music21/) and [MusPy](https://salu133445.github.io/muspy/).

## File organization

```text
├─ README.md                               README file
├─ audio.csv                               Metadata of the audio files
├─ info.csv                                Metadata of the processed files
├─ audio
│  ├─ emil-telmanyi
│  │  ├─ emil-telmanyi_bwv1001.mp3         Recording
│  │  └─ ...
│  └─ ...
├─ notes
│  ├─ emil-telmanyi
│  │  ├─ emil-telmanyi_bwv1001_mov1.csv    Score as a note sequence
│  │  └─ ...
│  └─ ...
├─ alignments
│  ├─ emil-telmanyi
│  │  ├─ emil-telmanyi_bwv1001_mov1.csv    Estimated alignment
│  │  └─ ...
│  └─ ...
├─ tempos
│  ├─ emil-telmanyi
│  │  ├─ emil-telmanyi_bwv1001_mov1.txt    Average tempo
│  │  └─ ...
│  └─ ...
├─ scores
│  ├─ bwv1001
│  │  ├─ bwv1001.mxl                       Reference score (whole piece)
│  │  ├─ bwv1001_mov1.mxl                  Reference score (single movement)
│  │  └─ ...
│  └─ ...
└─ .dev
   ├─ audio.xlsx                           Worksheet for `audio.csv`
   ├─ info.xlsx                            Worksheet for `info.csv`
   ├─ scores.csv                           Metadata of the original scores
   ├─ scores.xlsx                          Worksheet for `scores.csv`
   └─ scores
      ├─ bwv1001.mscz                      Original score file
      └─ ...
```
