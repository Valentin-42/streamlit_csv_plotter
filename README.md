# Easy Streamlit CSV Plotter

This Streamlit application allows you to specify paths to CSV files or directories with wildcards to merge and plot them interactively using Plotly.

## Usage

1. Enter paths to CSV files or a directory with a wildcard (e.g., `mydir/**/*.csv`) in the text area.
2. The application will merge the CSV files and display the data.
3. Add your plotting configurations to visualize the data.

### On Windows

```sh
run_streamlit.bat
```

### On Linux

```sh
./run_streamlit.sh
```

## Installation

### Using Conda
To create the Conda environment and install the dependencies, run the following command:

```sh
conda env create -f environment.yml
```

### Using pip 

```sh
pip install -r requirements.txt
```