#!/bin/bash

# List of file numbers to process
for i in 200 400 600 1000 1200 1400 1600 1800 2000 2200 2400; do
  # Construct the file name
  input_file="code/dataset/Cinput/c_case_${i}.txt"
  # 2_point_file="code/dataset/Cinput/2_point/2_point_${i}.txt"
  output_file="output/triangulation/sleeve_${i}.txt"

  # time_file="./output/triangulation_time/time_${i}.txt"

  # Check if the file exists before processing
  if [[ -f "$input_file" ]]; then
    # strace -c -o "$time_file" ./C_code/seidel-1.0/triangulate "$input_file" "$output_file"
    ./C_code/dcel/sleeve "$input_file" "code/dataset/Cinput/2_point/2_point_${i}.txt" "$output_file"
    echo "Triangulated $input_file to $output_file"
  else
    echo "$input_file not found!"
  fi
done
