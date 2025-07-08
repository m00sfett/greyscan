import argparse
from datetime import datetime



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scan images for gray bars")
    parser.add_argument("path", help="Path to folder containing images")
    parser.add_argument(
        "--band-height",
        type=int,
        default=20,
        help="Height of the analyzed image bands",
    )
    parser.add_argument(
        "--flatness-thresh",
        type=float,
        default=5.0,
        help="Max brightness standard deviation allowed for gray band",
    )
    parser.add_argument(
        "--brightness-min",
        type=float,
        default=30.0,
        help="Minimum brightness for gray band detection",
    )
    parser.add_argument(
        "--brightness-max",
        type=float,
        default=230.0,
        help="Maximum brightness for gray band detection",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress output of detected files",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.verbose:
        print(f"Starting scan in '{args.path}'...\n")
    try:
        from .scanner import batch_scan_images
        found = batch_scan_images(
            args.path,
            band_height=args.band_height,
            flatness_thresh=args.flatness_thresh,
            brightness_min=args.brightness_min,
            brightness_max=args.brightness_max,
            verbose=args.verbose,
        )
    except Exception as e:
        print(f"Error: {e}")
        return 1

    if found:
        logname = f"graybar_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(logname, "w", encoding="utf-8") as f:
            for path, info in found:
                line = f"{path} — {info}"
                if not args.quiet:
                    print("\u26a0\ufe0f ", line)
                f.write(line + "\n")
        print(
            f"\n\U0001F50D Done. {len(found)} suspicious images found. Log: {logname}"
        )
    else:
        if not args.quiet:
            print("\n\u2705 No corrupted images found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
