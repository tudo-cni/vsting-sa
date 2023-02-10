#!/bin/bash

# write image to sd-card

sdcard_device=$1
gzipped_img=$2

gzip -cd $gzipped_img | pv | sudo dd of=$sdcard_device bs=1M