import os
import sys
from glob import glob
import shutil
import argparse
from tqdm import tqdm
from os.path import join

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--video_dir",
        type=str,
        default="inputs",
    )
    parser.add_argument(
        "-c",
        "--caption_path",
        type=str,
        default="captions/test.txt",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default="outputs"
    )
    return parser.parse_args()

def read_caption(caption_path: str):
    file_name = caption_path.split("/")[-1].split(".")[0]
    print(f"Found caption file: {file_name}")

    with open(caption_path, "r") as f:
        captions = f.readlines()

    captions = [caption.strip() for caption in captions]
    return captions, file_name


def gen_pair_data(video_dir, caption_path, output_dir):
    captions, file_name = read_caption(caption_path)

    video_paths = sorted(os.listdir(video_dir))
    video_paths = [join(video_dir, video_path) for video_path in video_paths]
    print(f"Found {len(video_paths)} videos...")

    csv_path = join(output_dir, f"{file_name}.csv")
    # write csv title head
    with open(csv_path, "a") as fcsv:
        fcsv.write("path,text\n")

    # append data
    with open(csv_path, "a") as fcsv:
        for idx, video_path in enumerate(tqdm(video_paths, desc=f"Generating pair data for {file_name}")):
            if idx >= len(captions):
                caption = captions[0]
            else:
                caption = captions[idx]
            fcsv.write(f"{video_path},{caption}\n")


if __name__ == "__main__":
    args = parse_args()
    gen_pair_data(args.video_dir, args.caption_path, args.output_dir)
