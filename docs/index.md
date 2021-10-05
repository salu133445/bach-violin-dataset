The Bach Violin Dataset is a collection of high-quality public recordings of Bach's sonatas and partitas for solo violin (BWV 1001–1006). It contains roughly 400 minutes of recordings from 17 violinists in various recording environments. All recordings are collected from the web. Source url to each file can be found in `info.csv`. Reference scores for the six pieces are also provided. The dataset can be downloaded [here](https://github.com/salu133445/bach-violin/releases).

## File organization

```text
├─ README.md                          README file
├─ info.csv                           Metadata of the audio files
├─ audio
│  ├─ emil-telmanyi
│  │  ├─ emil-telmanyi_bwv1001.mp3    Audio file
│  │  └─ ...
│  └─ ...
├─ scores
│  ├─ bwv1001
│  │  ├─ bwv1001.mxl                  Reference score (whole piece)
│  │  ├─ bwv1001_mov1.mxl             Reference score (single movement)
│  │  └─ ...
│  └─ ...
└─ .dev
   ├─ info.xlsx                       Worksheet for `info.csv`
   ├─ scores.csv                      Metadata of the scores
   ├─ scores.xlsx                     Worksheet for `scores.csv`
   └─ scores
      ├─ bwv1001.mscz                 Original score file
      └─ ...
```

## Notes

- Each folder in the `audio` directory corresponds to a _collection_ that contains recordings with similar recording setups except the `misc` folder.
- Due to copyright concern, audio files in the collections _shunske-sato_ and _young-talents_ need to be downloaded from YouTube.
- Audio files come in either MP3 or OPUS format, depending on their sources. They can be converted into WAV files with [FFmpeg](http://ffmpeg.org/).
- Reference scores come in MusicXML format. They can be opened with [MuseScore](https://musescore.org/), [music21](https://web.mit.edu/music21/) and [MusPy](https://salu133445.github.io/muspy/).

## License

All audio files in this dataset are public recordings downloaded from various
sources. License for each audio file can be found in the associated CSV file
(`info.csv`). All reference scores are in public domain.

Please cite the project website (<https://salu133445.github.io/bach-violin/>) if you use this dataset in your work.
