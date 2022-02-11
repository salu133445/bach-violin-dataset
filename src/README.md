# Source code for the alignment process

The source code for creating this dataset can be found in the `src` directory. Below is its file organization.

```text
├─ README.md               README file
├─ slice_audio.py          Script that slices the audio into clips
├─ compute_ssm.py          Script that computes the self-similarity matrices
├─ process_scores.py       Script that processes the scores
├─ synthesize_scores.py    Script that synthesizes the scores into audios
├─ align_scores.py         Script that aligns the scores to the recordings
├─ LICENSE                 License of the code
├─ requirements.txt        Dependencies
├─ environment.yml         Conda environment file
├─ environment.dev.yml     Conda environment file (for development)
├─ pyproject.toml          Project configuration
├─ setup.cfg               Project configuration
└─ data
   ├─ audio.xlsx           Worksheet for `audio.csv`
   ├─ info.xlsx            Worksheet for `info.csv`
   ├─ scores.csv           Metadata of the original scores
   ├─ scores.xlsx          Worksheet for `scores.csv`
   └─ scores
      ├─ bwv1001.mscz      Original score file
      └─ ...
```

## Environment setup

Please run the following to create a conda environment.

```sh
conda env create -f environment.yml
```

For development environment, please also run the following.

```sh
conda env update -f environment.dev.yml -n synthesis
```

## Slice the audio recordings by movement

We first slice the audio recordings into clips by movement.

```sh
python slice_audio.py -c audio.csv -i bach-violin/audio/ -o processed/
```

## Process the scores

We then transform the musical scores into note sequences, stored as CSV files.

```sh
python process_scores.py -c audio.csv -i bach-violin/ -o processed/
```

## Synthesize the scores

We then synthesize the scores using [FluidSynth](https://www.fluidsynth.org/), an open-source software synthesizer, with the [MuseScore General SoundFont](https://musescore.org/en/handbook/3/soundfonts-and-sfz-files).

```sh
python synthesize_scores.py -c audio.csv -i bach-violin/ -o processed/
```

## Align the scores to the recordings

Finally, we perform dynamic time warping (DTW) on the constant-Q spectrograms of the synthesized audios and those of the recordings to obtain the alignments.

```sh
python align_scores.py -c info.csv -i processed/ -o processed/ -p
```
