#!/bin/bash

# List of file numbers to process
for i in 5 10 15 20 25 50 100 150 200 400 600 1000; do
  # Construct the file name
  input_file="./Cinput/c_case_${i}.txt"
  output_file="./output/triangulation/tri_${i}.txt"
  time_file="./output/triangulation_time/time_${i}.txt"

  # Check if the file exists before processing
  if [[ -f "$input_file" ]]; then
    strace -c -o "$time_file" ./C_code/seidel-1.0/triangulate "$input_file" "$output_file"
    echo "Triangulated $input_file to $output_file"
  else
    echo "$input_file not found!"
  fi
done
