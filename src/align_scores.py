"""Align scores to recordings."""
import argparse
import csv
import datetime
import logging
import pathlib
import sys

import librosa
import librosa.display
import librosa.sequence
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial.distance
import tqdm

REF_DATE = datetime.datetime.fromisoformat("2000-01-01T00:00")


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


def sec2datetime(sec):
    """Convert second to datetime."""
    return REF_DATE + datetime.timedelta(seconds=sec)


def sec2num(sec):
    """Convert second to number."""
    return matplotlib.dates.date2num(sec2datetime(sec))


def plot_alignment(
    s1,
    s2,
    sr1,
    sr2,
    hop_length,
    bins_per_octave,
    filename=None,
    warp_path=None,
):
    """Plot the alignment result."""
    # Create figure
    gridspec = {"width_ratios": [1, 4], "height_ratios": [1, 4]}
    fig, axs = plt.subplots(2, 2, gridspec_kw=gridspec, figsize=(10, 10))
    fig.tight_layout()
    axs[0, 0].axis("off")

    # Plot spectrograms
    time_formatter = matplotlib.dates.DateFormatter("%M:%S")
    time_lim1 = (sec2num(0), sec2num(s1.shape[1] * hop_length / sr1))
    extent = (time_lim1[0], time_lim1[1], 0, len(s1))
    axs[0, 1].imshow(
        s1,
        cmap="inferno",
        aspect="auto",
        origin="lower",
        extent=extent,
        interpolation="none",
    )
    axs[0, 1].xaxis.tick_top()
    axs[0, 1].yaxis.tick_right()
    axs[0, 1].set_yticks(np.arange(0, len(s1) + 1, bins_per_octave))
    axs[0, 1].set_yticklabels(
        [f"C{octave+3}" for octave in range(len(s1) // bins_per_octave + 1)],
    )
    axs[0, 1].xaxis_date()
    axs[0, 1].xaxis.set_major_formatter(time_formatter)
    axs[0, 1].xaxis.set_ticks_position("both")
    axs[0, 1].yaxis.set_ticks_position("both")
    axs[0, 1].tick_params(labelleft=True, labelright=True)
    axs[0, 1].set_xlabel("Time")
    axs[0, 1].set_ylabel("Note")
    axs[0, 1].xaxis.set_label_position("top")
    axs[0, 1].yaxis.set_label_position("right")

    time_lim2 = (sec2num(0), sec2num(s2.shape[1] * hop_length / sr2))
    extent2 = (0, len(s2), time_lim2[1], time_lim2[0])
    axs[1, 0].imshow(
        s2.T,
        cmap="inferno",
        aspect="auto",
        extent=extent2,
        interpolation="none",
    )
    axs[1, 0].invert_xaxis()
    axs[1, 0].set_xticks(np.arange(0, len(s2) + 1, bins_per_octave))
    axs[1, 0].set_xticklabels(
        [f"C{octave+3}" for octave in range(len(s2) // bins_per_octave + 1)]
    )
    axs[1, 0].yaxis_date()
    axs[1, 0].yaxis.set_major_formatter(time_formatter)
    axs[1, 0].xaxis.set_ticks_position("both")
    axs[1, 0].yaxis.set_ticks_position("both")
    axs[1, 0].tick_params(
        bottom=True,
        top=True,
        left=True,
        right=True,
        labeltop=True,
        labelbottom=True,
    )
    axs[1, 0].set_xlabel("Note")
    axs[1, 0].set_ylabel("Time")

    # Plot DTW matrix and warping path
    dist = scipy.spatial.distance.cdist(s1.T, s2.T)
    extent_dist = (time_lim1[0], time_lim1[1], time_lim2[1], time_lim2[0])
    axs[1, 1].imshow(
        dist.T,
        cmap="Greys",
        aspect="auto",
        extent=extent_dist,
        interpolation="none",
    )
    axs[1, 1].yaxis.tick_right()
    axs[1, 1].set_xticklabels([])
    axs[1, 1].set_yticklabels([])
    axs[1, 1].xaxis_date()
    axs[1, 1].xaxis.set_major_formatter(time_formatter)
    axs[1, 1].yaxis_date()
    axs[1, 1].yaxis.set_major_formatter(time_formatter)
    axs[1, 1].xaxis.set_ticks_position("both")
    axs[1, 1].yaxis.set_ticks_position("both")
    axs[1, 1].set_xlabel("Time")
    axs[1, 1].set_ylabel("Time")
    axs[1, 1].yaxis.set_label_position("right")

    if filename is not None:
        fig.savefig(filename, bbox_inches="tight")
    if warp_path is not None:
        axs[1, 1].plot(
            [sec2num(x * hop_length / sr1) for x in warp_path[:, 0]],
            [sec2num(y * hop_length / sr2) for y in warp_path[:, 1]],
            "r",
        )
        if filename is not None:
            path_filename = filename.parent / (filename.stem + "_path.png")
            fig.savefig(path_filename, bbox_inches="tight")

    plt.close(fig)


def plot_notes(
    s, sr, pitches, onsets, offsets, hop_length, bins_per_note, filename=None,
):
    """Plot the notes and spectrogram."""
    on_offsets = np.zeros((len(pitches), 2, 2))
    onset_markers = np.zeros((len(pitches), 2, 2))
    for i, (pitch, onset, offset) in enumerate(zip(pitches, onsets, offsets)):
        y_pos = bins_per_note * (pitch - librosa.note_to_midi("C3"))
        on_offsets[i, 0] = (sec2num(onset), y_pos + 0.5)
        on_offsets[i, 1] = (sec2num(offset), y_pos + 0.5)
        onset_markers[i, 0] = (sec2num(onset), y_pos - 0.5)
        onset_markers[i, 1] = (sec2num(onset), y_pos + 1.5)

    fig, ax = plt.subplots(figsize=(20, 2))
    time_lim1 = (sec2num(0), sec2num(s.shape[1] * hop_length / sr))
    extent = (time_lim1[0], time_lim1[1], 0, len(s))
    ax.imshow(s, cmap="inferno", aspect="auto", origin="lower", extent=extent)
    ax.add_collection(
        matplotlib.collections.LineCollection(on_offsets, colors="g", lw=1)
    )
    ax.add_collection(
        matplotlib.collections.LineCollection(
            onset_markers, colors="w", lw=0.5
        )
    )
    ax.set_yticks(np.arange(0, len(s) + 1, 12 * bins_per_note))
    ax.set_yticklabels(
        [
            f"C{octave+3}"
            for octave in range(len(s) // (12 * bins_per_note) + 1)
        ],
    )
    ax.xaxis_date()
    time_formatter = matplotlib.dates.DateFormatter("%M:%S")
    ax.xaxis.set_major_formatter(time_formatter)
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    if filename is not None:
        fig.savefig(filename, dpi=300, bbox_inches="tight")

    plt.close(fig)


def main():
    """Main function."""
    # Parse the command-line arguments
    args = parse_args()

    # Make sure output directory exists
    args.out_dir.mkdir(exist_ok=True)
    (args.out_dir / "alignment").mkdir(exist_ok=True)

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
            / "alignment"
            / row["collection"]
            / (row["filename"] + ".csv")
        )
        if args.skip_existing and out_filename.is_file():
            continue
        out_filename.parent.mkdir(exist_ok=True, parents=True)

        # Load the audio
        y, rate = librosa.load(
            args.input_dir
            / "wav"
            / row["collection"]
            / (row["filename"] + ".wav"),
            sr=None,
        )
        y_synth, rate_synth = librosa.load(
            args.input_dir
            / "synth"
            / row["collection"]
            / (row["filename"] + ".wav"),
            sr=None,
        )
        assert rate == rate_synth

        # Compute spectrograms
        cqt = np.abs(
            librosa.cqt(
                y,
                sr=rate,
                hop_length=args.hop_length,
                fmin=librosa.note_to_hz("C3"),
                n_bins=5 * 12 * args.bins_per_note,
                bins_per_octave=12 * args.bins_per_note,
            )
        )
        cqt_synth = np.abs(
            librosa.cqt(
                y_synth,
                sr=rate_synth,
                hop_length=args.hop_length,
                fmin=librosa.note_to_hz("C3"),
                n_bins=5 * 12 * args.bins_per_note,
                bins_per_octave=12 * args.bins_per_note,
            )
        )

        # Convert amplitude to db
        cqt_db = librosa.amplitude_to_db(cqt, ref=np.max)
        cqt_db_synth = librosa.amplitude_to_db(cqt_synth, ref=np.max)

        # Run the DTW algorithm
        _, warp_path = librosa.sequence.dtw(cqt_db, cqt_db_synth)
        warp_path = warp_path[::-1]
        np.save(out_filename.with_suffix(".npy"), warp_path)

        # Read the notes
        notes = read_csv(
            args.input_dir
            / "notes"
            / row["collection"]
            / (row["filename"] + ".csv"),
        )
        onsets = [int(row["onset"]) for row in notes]
        offsets = [int(row["offset"]) for row in notes]
        pitches = [int(row["pitch"]) for row in notes]

        # Compute starts and ends
        factor = cqt.shape[1] * rate_synth / rate / max(offsets)
        starts_synth = [onset * factor for onset in onsets]
        ends_synth = [offset * factor for offset in offsets]
        starts_indices = np.clip(
            np.searchsorted(warp_path[:, 1], starts_synth, side="right"),
            0,
            len(warp_path) - 1,
        )
        starts = warp_path[starts_indices, 0] * args.hop_length / rate
        ends_indices = np.clip(
            np.searchsorted(warp_path[:, 1], ends_synth) - 1,
            0,
            len(warp_path) - 1,
        )
        ends = warp_path[ends_indices, 0] * args.hop_length / rate
        with open(out_filename, "w") as f:
            f.write("start,end\n")
            for start, end in zip(starts, ends):
                f.write(f"{start},{end}\n")

        # Plot alignment
        if args.save_plot:
            plot_alignment(
                cqt_db,
                cqt_db_synth,
                rate,
                rate_synth,
                hop_length=args.hop_length,
                bins_per_octave=12 * args.bins_per_note,
                filename=out_filename.parent
                / (out_filename.stem + "_dtw.png"),
                warp_path=warp_path,
            )
            plot_notes(
                cqt_db,
                rate,
                pitches,
                onsets,
                offsets,
                hop_length=args.hop_length,
                bins_per_note=args.bins_per_note,
                filename=out_filename.parent
                / (out_filename.stem + "_alignment.png"),
            )


if __name__ == "__main__":
    main()
