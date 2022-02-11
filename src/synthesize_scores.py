"""Align scores to recordings."""
import argparse
import csv
import logging
import pathlib
import sys

import librosa
import muspy
import numpy as np
import soundfile as sf
import tqdm


def parse_args(args=None, namespace=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--csv_filename",
        type=pathlib.Path,
        required=True,
        help="input CSV filename",
    )
    parser.add_argument(
        "-i",
        "--input_dir",
        type=pathlib.Path,
        required=True,
        help="input data directory",
    )
    parser.add_argument(
        "-o",
        "--out_dir",
        type=pathlib.Path,
        required=True,
        help="output directory",
    )
    parser.add_argument(
        "-s",
        "--skip_existing",
        action="store_true",
        help="whether to skip existing files",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="show warnings only"
    )
    return parser.parse_args(args=args, namespace=namespace)


def read_csv(filename):
    """Read a CSV file into a dictionary."""
    with open(filename) as f:
        reader = csv.DictReader(f)
        data = [
            {field: row[field] for field in reader.fieldnames}
            for row in reader
        ]
    return data


def main():
    """Main function."""
    # Parse the command-line arguments
    args = parse_args()

    # Make sure output directory exists
    args.out_dir.mkdir(exist_ok=True)
    (args.out_dir / "synth").mkdir(exist_ok=True)
    (args.out_dir / "tempo").mkdir(exist_ok=True)

    # Set up the logger
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.ERROR if args.quiet else logging.INFO,
        format="%(levelname)-8s %(message)s",
    )

    # Read the CSV file
    logging.info("Reading the CSV file...")
    data = read_csv(args.csv_filename)

    # Iterate over rows
    logging.info("Iterating over rows...")
    prog_bar = tqdm.tqdm(data, ncols=120)
    for row in prog_bar:
        # Append filename to progress bar
        prog_bar.set_postfix_str(row["filename"])

        # Get directories
        out_filename = (
            args.out_dir
            / "synth"
            / row["collection"]
            / (row["filename"] + ".wav")
        )
        if args.skip_existing and out_filename.is_file():
            continue

        # Read the notes
        notes = read_csv(
            args.input_dir
            / "notes"
            / row["collection"]
            / (row["filename"] + ".csv"),
        )
        muspy_notes = [
            muspy.Note(
                time=int(row["onset"]),
                pitch=int(row["pitch"]),
                duration=int(row["offset"]) - int(row["onset"]),
                velocity=int(row["velocity"]),
            )
            for row in notes
        ]
        track = muspy.Track(notes=muspy_notes)
        music = muspy.Music(resolution=24, tracks=[track])

        # Load the audio
        y, rate = librosa.load(
            args.input_dir
            / "wav"
            / row["collection"]
            / (row["filename"] + ".wav"),
            sr=None,
        )

        # Set a global tempo
        qpm = 60 * rate * music.get_end_time() / music.resolution / len(y)
        music.tempos = [muspy.Tempo(time=0, qpm=qpm)]

        # Synthesize the score
        y_synth = librosa.to_mono(
            muspy.synthesize(music, rate=args.rate).T / np.iinfo(np.int16).max
        )
        out_filename.parent.mkdir(exist_ok=True)
        sf.write(out_filename, y_synth, args.rate)

        # Write the tempo to a txt file
        out_filename_tempo = (
            args.out_dir
            / "tempo"
            / row["collection"]
            / (row["filename"] + ".txt")
        )
        out_filename_tempo.parent.mkdir(exist_ok=True)
        with open(out_filename_tempo, "w") as f:
            f.write(f"{qpm}\n")


if __name__ == "__main__":
    main()
