"""Slice audio files into clips using FFmpeg."""
import argparse
import csv
import logging
import pathlib
import subprocess
import sys

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
        "-r", "--rate", type=int, default=16000, help="sampling rate"
    )
    parser.add_argument(
        "-m",
        "--save_mp3",
        action="store_true",
        help="whether to save MP3 files",
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
    (args.out_dir / "wav-original").mkdir(exist_ok=True)
    (args.out_dir / "wav").mkdir(exist_ok=True)
    if args.save_mp3 is not None:
        (args.out_dir / "mp3").mkdir(exist_ok=True)

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
        pbar.set_postfix_str(row["filename"])
        source_filename = (
            args.input_dir / row["collection"] / row["source_filename"]
        )
        out_filename = (
            args.out_dir
            / "wav-original"
            / row["collection"]
            / (row["filename"] + ".wav")
        )
        if args.skip_existing and out_filename.is_file():
            continue

        # Slice and convert to WAV
        out_filename.parent.mkdir(exist_ok=True)
        subprocess.check_output(
            [
                "ffmpeg",
                "-loglevel",
                "error",
                "-y",
                "-ss",
                row["start"],
                "-to",
                row["end"],
                "-i",
                source_filename,
                out_filename,
            ]
        )

        # Downmix to mono and downsample to 16 kHz
        downsampled_filename = (
            args.out_dir
            / "wav"
            / row["collection"]
            / (row["filename"] + ".wav")
        )
        downsampled_filename.parent.mkdir(exist_ok=True)
        subprocess.check_output(
            [
                "sox",
                out_filename,
                downsampled_filename,
                "remix",
                "-",
                "rate",
                "-s",
                str(args.rate),
            ]
        )

        # Encode into MP3
        if args.save_mp3 is not None:
            mp3_filename = (
                args.out_dir
                / "mp3"
                / row["collection"]
                / (row["filename"] + ".mp3")
            )
            mp3_filename.parent.mkdir(exist_ok=True)
            subprocess.check_output(
                [
                    "ffmpeg",
                    "-loglevel",
                    "error",
                    "-y",
                    "-i",
                    downsampled_filename,
                    "-b:a",
                    "192k",
                    mp3_filename,
                ]
            )


if __name__ == "__main__":
    main()
