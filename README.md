# Bach Violin Dataset

The Bach Violin Dataset is a collection of high-quality public recordings of Bach's sonatas and partitas for solo violin (BWV 1001–1006). The dataset consists of 6.5 hours of professional recordings from 17 violinists recorded in various recording setups. Reference scores and estimated alignments are also provided. All recordings are collected from the web, and their source URLs can be found in `audio.csv`. The dataset can be downloaded [here](https://github.com/salu133445/bach-violin/releases).

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

## Notes

- Each folder in the `audio` directory corresponds to a _collection_ that contains recordings with similar recording setups except the `misc` folder.
- Due to copyright concern, audio files in the collections _shunske-sato_ and _young-talents_ need to be downloaded from YouTube.
- Audio files come in either MP3 or OPUS format, depending on their sources, which can be converted into WAV files with [FFmpeg](http://ffmpeg.org/).
- The corresponding reference score for each recording can be found in `info.csv`.
- Reference scores come in MusicXML format, which can be opened with [MuseScore](https://musescore.org/), [music21](https://web.mit.edu/music21/) and [MusPy](https://salu133445.github.io/muspy/).

## License

ALl audio files in this dataset are public recordings collected from various sources. License information for each audio file can be found in their subdirectory. All reference scores are in public domain. All code and derived annotations are licensed under MIT.

## Citing

Please cite the following paper if you use the code or derived annotations provided in this repository.

__Deep Performer: Score-to-Audio Music Performance Synthesis__<br>
Hao-Wen Dong, Cong Zhou, Taylor Berg-Kirkpatrick and Julian McAuley<br>
_Proceedings of the IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)_, 2022<br>
[[homepage](https://github.com/salu133445/deepperformer)]
