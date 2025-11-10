#!/bin/bash

# Define environment variables
export TOKENIZERS_PARALLELISM=false

# Define paths
INPUT_CSV="/workspace/codes/STAR/datasets/neemo_mini/neemo_mini_short_1440p.csv"
SAVE_PATH="/workspace/codes/DiffSynth-Studio/data/neemo_mini_1440p_120f"

# Run script on the full CSV file
torchrun --nproc_per_node=1 --master_port "29501" \
    make_paired_data.py \
    --config "./make_data_config.py" \
    --data-path $INPUT_CSV \
    --save_path $SAVE_PATH
