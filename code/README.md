# Workflow

## Code Structure
- `code/generate.py`: Generates the set of vertices.
- `code/simplePoly.py`: Generates a simple polygon from the set. (Data output is used in C, referred to as Cinput.)
- Look at the `/figure` folder to choose source and destination.
- Use the C code to triangulate the polygon and generate a sleeve. (Data output is used in `lee.py`, referred to as Coutput.)
- `code/lee.py`: Applies Lee & Preparata's algorithm.

## How to Use

### Generate Set of Vertices
#### If You Already Have a Set of Vertices:
- Ensure you've created a `.txt` file in `code/dataset/vertices` or change the path in `code/simplePoly.py`.
- Proceed to [Generate Simple Polygon](#generate-simple-polygon).

#### If You Do Not Have a Set of Vertices:
- In `code/generate.py`, set your number of vertices `n` or use `nn` to generate multiple sets at once.
- The `.txt` file will be generated in `code/dataset/vertices/`, so you don’t need to modify the path in `code/simplePoly.py`.

### Generate Simple Polygon
#### If You Already Have a Simple Polygon:
- Ensure the order of vertices is counterclockwise, or use the reverse function to correct it.
- Ensure you've created a `.txt` file in `code/dataset/Cinput`. (**Required**)
- Proceed to the C code and output the `.txt` file at `code/dataset/Coutput`.

#### If You Do Not Have a Simple Polygon:
- In `code/simplePoly.py`, modify the path as needed.
- The default script uses `nn` to generate multiple simple polygons at once; adjust as necessary.
- The `.txt` file will appear in `code/dataset/Cinput/`.
- Figures (if desired) will be saved in `code/figure/simplePolygonFig`.
- Proceed to the C code and output the `.txt` file at `code/dataset/Coutput`.

### Look at Figures to Choose Source and Destination
- The `/figure` folder contains visual representations to help select the appropriate source and destination points.

### Run the C Code
- The output file in `code/dataset/Coutput` will contain:
  - `name.txt`: Simple polygon vertices.
  - `name_sleeve.txt`: The second row contains coordinates of source and destination; the rest is a list of diagonals in the sleeve (**Required**).

### Apply Lee & Preparata Algorithm
- Check and modify the path if needed.
- Run the algorithm:
  ```sh
  python code/lee.py
  ```

