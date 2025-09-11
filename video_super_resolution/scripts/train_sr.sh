#!/bin/bash

torchrun \
  --nnodes=1 \
  --nproc_per_node=2 \
  ./video_super_resolution/scripts/train_sr.py \
  --pretrained_model_path '/workspace/codes/STAR/pretrained_weight/VEnhancer/venhancer_v2.pt' \
  --train_data_dir '/workspace/codes/STAR/datasets/neemo_mini_720p_res' \
  --output_dir '/workspace/codes/STAR/outputs/neemo_mini_720p_res' \
  --train_batch_size 1 \
  --max_train_steps 15000 \
  --checkpointing_steps 500 \
  --learning_rate 5e-5 \
  --num_frames 32
