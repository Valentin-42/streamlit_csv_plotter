
from setuptools import setup, find_packages

setup(
    name='streamlit_csv_plotter',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'streamlit==1.22.0',
        'pandas==2.1.1',
        'plotly==5.17.0',
        'numpy==1.26.0'
    ],
    entry_points={
        'console_scripts': [
            'csv_plotter=main:main',
        ],
    },
    author='Valentin Vial',
    author_email='valentinvial42@gmail.com',
    description='A Streamlit application to plot data from CSV files using Plotly.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Valentin-42/streamlit_csv_plotter',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)