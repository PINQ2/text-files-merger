import logging
import os
import sys
from pathlib import Path


def main():
    output_dir = Path("/tmp/outputs")
    logs_dir = Path("/tmp/logs")
    output_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_file = logs_dir / "text_files_merger.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file),
        ],
    )

    logging.info("Starting Text Files Merger execution...")

    # Step 1: Resolve environment variables
    input_dir = os.getenv("KIT_INPUTS_FILE")
    input1_name = os.getenv("INPUT_1_NAME")
    input2_name = os.getenv("INPUT_2_NAME")

    logging.info(f"KIT_INPUTS_FILE: {input_dir}")
    logging.info(f"INPUT_1_NAME: {input1_name}")
    logging.info(f"INPUT_2_NAME: {input2_name}")

    if not input_dir:
        logging.error("KIT_INPUTS_FILE environment variable is not set")
        sys.exit(1)
    if not input1_name:
        logging.error("INPUT_1_NAME environment variable is not set or empty")
        sys.exit(1)
    if not input2_name:
        logging.error("INPUT_2_NAME environment variable is not set or empty")
        sys.exit(1)

    # Step 2: Resolve and validate input paths
    input1_path = Path(input_dir) / input1_name
    input2_path = Path(input_dir) / input2_name

    if os.path.isdir(input_dir):
        logging.info(f"Input directory exists: {input_dir}")
    else:
        logging.warning(f"Input path is not a directory: {input_dir}")

    # Step 3: Read both input files
    try:
        content1 = input1_path.read_text()
        logging.info(f"Read input file 1: {input1_path}")
    except Exception as e:
        logging.error(f"Failed to read {input1_path}: {e}")
        sys.exit(1)

    try:
        content2 = input2_path.read_text()
        logging.info(f"Read input file 2: {input2_path}")
    except Exception as e:
        logging.error(f"Failed to read {input2_path}: {e}")
        sys.exit(1)

    # Step 4: Merge and write output
    merged = content1 + content2
    output_path = output_dir / "output.txt"
    output_path.write_text(merged)
    logging.info(f"Merged output written to {output_path}")

    logging.info("Text Files Merger execution completed successfully")


if __name__ == "__main__":
    main()
