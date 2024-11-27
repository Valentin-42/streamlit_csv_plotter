import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
import glob

def get_csv_paths(input_str):
    """
    Get a list of CSV file paths from the input string.
    
    Parameters:
    input_str (str): A string containing paths to CSV files or a directory with a wildcard.
    
    Returns:
    list: A list of CSV file paths.
    """
    if '*' in input_str:
        return glob.glob(input_str, recursive=True)
    else:
        return [path.strip() for path in input_str.split(',')]

def load_data(paths):
    """
    Load data from the provided CSV file paths and merge them into a single DataFrame.
    
    Parameters:
    paths (list): A list of CSV file paths.
    
    Returns:
    DataFrame: A merged DataFrame containing data from all the CSV files.
    """
    dataframes = []
    for idx, path in enumerate(paths):
        if os.path.exists(path):
            df = pd.read_csv(path)
            df['Source'] = f'{idx + 1}'
            df['Original'] = path
            dataframes.append(df)
        else:
            st.error(f"File not found: {path}")
    return pd.concat(dataframes, ignore_index=True) if dataframes else None

def plot_data(merged_df, plot_config, global_smoothing_window):
    """
    Plot data from the merged DataFrame based on the provided plot configuration.
    
    Parameters:
    merged_df (DataFrame): The merged DataFrame containing data from all the CSV files.
    plot_config (dict): A dictionary containing plot configuration (x_axis, y_axis, compute_derivative).
    global_smoothing_window (int): The window size for global smoothing.
    
    Returns:
    None
    """
    
    smoothed_df = merged_df.copy()
    smoothed_df[plot_config['y_axis']] = (
        merged_df.groupby('Source')[plot_config['y_axis']]
        .transform(lambda x: x.rolling(window=global_smoothing_window, min_periods=1).mean())
    )
    smoothed_df[plot_config['x_axis']] = (
        merged_df.groupby('Source')[plot_config['x_axis']]
        .transform(lambda x: x.rolling(window=global_smoothing_window, min_periods=1).mean())
    )

    if plot_config['compute_derivative']:
        smoothed_df['dy_dx'] = np.gradient(smoothed_df[plot_config['y_axis']], smoothed_df[plot_config['x_axis']])
        fig = px.line(smoothed_df, x=plot_config['x_axis'], y='dy_dx', color='Source', 
                      title=f'Derivative of {plot_config["y_axis"]} vs {plot_config["x_axis"]}',
                      labels={'dy_dx': 'dy/dx'},
                      hover_data={'Source': True, plot_config['x_axis']: True, 'dy_dx': True, 'Original': True},
                      color_discrete_sequence=px.colors.qualitative.Plotly)
    else:
        fig = px.line(smoothed_df, x=plot_config['x_axis'], y=plot_config['y_axis'], color='Source', 
                      title=f'{plot_config["y_axis"]} vs {plot_config["x_axis"]}',
                      hover_data={'Source': True, plot_config['x_axis']: True, plot_config['y_axis']: True, 'Original': True},
                      color_discrete_sequence=px.colors.qualitative.Plotly)

    fig.update_layout(
        autosize=False,
        width=800,
        height=800,
        title_x=0.5
    )
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.set_page_config(layout="wide")
    st.title('Specify CSV Paths and Plot Data with Plotly')
    st.write('Enter paths to CSV files or a directory with a wildcard (e.g., mydir/**/*.csv) to merge and plot them interactively.')

    with st.expander("Inputs and Instructions"):
        csv_paths_input = st.text_area('Enter paths to CSV files or a directory (with wildcard)', '')

    if 'plots' not in st.session_state:
        st.session_state.plots = []

    if csv_paths_input:
        paths = get_csv_paths(csv_paths_input)
        merged_df = load_data(paths)
        if merged_df is not None:
            st.write("Merged Data:")
            with st.expander("View Merged Data"):
                st.dataframe(merged_df)

            numeric_columns = merged_df.select_dtypes(include=['number']).columns.tolist()
            if len(numeric_columns) < 2:
                st.error("Error: Not enough numeric columns to plot.")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    x_axis = st.selectbox('Select X-axis', numeric_columns, key='x_axis')
                with col2:
                    y_axis = st.selectbox('Select Y-axis', numeric_columns, key='y_axis')

                global_smoothing_window = st.slider('Select Global Smoothing Window Size', min_value=1, max_value=20, value=1)
                compute_derivative = st.checkbox('Compute Derivative of Y-axis', value=False)

                if st.button('Add Plot'):
                    plot_config = {
                        'x_axis': x_axis,
                        'y_axis': y_axis,
                        'compute_derivative': compute_derivative
                    }
                    st.session_state.plots.append(plot_config)

                for i, plot_config in enumerate(st.session_state.plots):
                    plot_data(merged_df, plot_config, global_smoothing_window)
                    if st.button(f'Remove Plot {i + 1}'):
                        st.session_state.plots.pop(i)
                        st.rerun()

if __name__ == "__main__":
    main()