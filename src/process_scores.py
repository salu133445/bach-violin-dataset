"""Process scores into JSON files."""
import argparse
import csv
import logging
import pathlib
import sys

import music21
import muspy
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
        "-l", "--hop_length", type=int, default=512, help="hop length for CQT"
    )
    parser.add_argument(
        "-b",
        "--bins_per_note",
        type=int,
        default=3,
        help="number of bins per note for CQT",
    )
    parser.add_argument(
        "-a",
        "--adjust_tuning_pitches",
        action="store_true",
        help="whether to adjust pitches for Baroque tuning",
    )
    parser.add_argument(
        "-p", "--save_plot", action="store_true", help="save alignment plots"
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
    (args.out_dir / "notes").mkdir(exist_ok=True)

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
    pbar = tqdm.tqdm(data, ncols=120)
    for row in pbar:
        # Get directories
        out_filename = (
            args.out_dir
            / "notes"
            / row["collection"]
            / (row["filename"] + ".csv")
        )
        if args.skip_existing and out_filename.is_file():
            continue
        out_filename.parent.mkdir(exist_ok=True)

        # Read the score
        m21 = music21.converter.parse(
            args.input_dir
            / "scores"
            / row["work"].lower()
            / (row["score_filename"] + ".mxl")
        )
        music = muspy.from_music21_score(m21.expandRepeats())
        assert len(music) == 1

        # Collect the notes
        notes = []
        for note in music[0].notes:
            notes.append(
                (
                    int(note.time),
                    int(note.end),
                    int(note.pitch),
                    int(note.velocity),
                )
            )

        # Collect the chords
        for chord in music[0].chords:
            for pitch in chord.pitches:
                notes.append(
                    (
                        int(chord.time),
                        int(chord.end),
                        int(pitch),
                        int(chord.velocity),
                    )
                )
        notes.sort()

        # Adjust the tuning
        if args.adjust_tuning_pitches and row["baroque_tuning"] == "1":
            for note in notes:
                note[2] -= 1

        # Write the CSV file
        with open(out_filename, "w") as f:
            f.write("onset,offset,pitch,velocity\n")
            for onset, offset, pitch, velocity in notes:
                f.write(f"{onset},{offset},{pitch},{velocity}\n")


if __name__ == "__main__":
    main()
