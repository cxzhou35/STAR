import os
import sys
from glob import glob
import shutil
import argparse
from tqdm import tqdm
from os.path import join

def generate_video(input_path, output_path, frame_ranges=None, fps=30):
    """
    Generate a video from a sequence of images.
    :param input_path: Path to the input images (e.g., "path/to/images/*.jpg").
    :param output_path: Path to save the output video (e.g., "path/to/output/video.mp4").
    :param fps: Frames per second for the output video.
    """
    import glob
    import cv2

    s, e, p = frame_ranges
    images = sorted(os.listdir(input_path))
    images = [os.path.join(input_path, img) for img in images]
    images = images[s:e:p]

    if not images:
        print(f"No images found in {input_path}")
        return

    # Get the width and height of the first image
    img = cv2.imread(images[0])
    height, width, layers = img.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for image in tqdm(images, desc="Generating video"):
        img = cv2.imread(image)
        out.write(img)

    out.release()
    print(f"Video saved to {output_path}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_dir",
        type=str,
        default="input",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default="output",
    )
    parser.add_argument("-fr", "--frame_range", type=list, default=[0, 119, 1])
    return parser.parse_args()

def reorganize_images(image_dir, output_dir):
    image_paths = sorted(os.listdir(image_dir))
    for image_path in tqdm(image_paths):
        view_id = image_path.split("_")[0]
        frame_id = image_path.split("_")[1].split(".")[0]
        img_ext = image_path.split(".")[1]
        os.makedirs(join(output_dir, view_id), exist_ok=True)
        # copy image
        shutil.copy(join(image_dir, image_path), join(output_dir, view_id, f"{frame_id}.{img_ext}"))


if __name__ == "__main__":
    args = parse_args()
    # reorganize_images(args.input_dir, args.output_dir)
    os.makedirs(args.output_dir, exist_ok=True)
    view_dirs = sorted(os.listdir(args.input_dir))
    print(f"Found {len(view_dirs)} views...")
    fr = args.frame_range
    for view in view_dirs:
        assert os.path.isdir(
            join(args.input_dir, view)
        ), f"View dir {view} not found"
        input_dir = join(args.input_dir, view)
        result_path = join(args.output_dir, f"{view}_{fr[0]:06d}_{fr[1]:06d}.mp4")
        generate_video(input_dir, result_path, frame_ranges=fr, fps=60)
    print(f"Merge images finished...")
