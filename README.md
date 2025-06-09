# VISION

*VISualize your ambitION*

## I. Introduction

VISION is a python package is designed for quick visualization of scientific data. It is based on the popular matplotlib library, but with a more user-friendly interface.

## II. Environment Set-up

### i. Pre-requisites

Recommended python version: 3.12 (which is used by myself). Anyway, in theory it should work with any python version >= 3.0.

Highly recommending using [anaconda](https://www.anaconda.com/) to manage your python environment. It is a free and open-source distribution 
of python and R programming languages for scientific computing, that aims to simplify package management and deployment.

Required packages:
- *Data acquisition*: [Pandas](https://pandas.pydata.org/) & [Xlrd](https://xlrd.readthedocs.io/en/latest/)
- *Scientific calculus*: [Numpy](https://numpy.org/) & [Scipy](https://www.scipy.org/)
- *Machine learning & statistical analysis*: [Scikit-learn](https://scikit-learn.org/stable/)
- *Visualization*: [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/)
- *Notebook interface for python*: [JupyterLab](https://jupyter.org/install)

### ii. Managing python environment via anaconda

Using anaconda, we can easily manage our python environment and packages through the command line interface (CLI).

(1) Creating new anaconda environment
```Shell
conda create --name yourENV python=3.12
```
where `yourEnv` is the name of your environment.

(2) Activating the environment
```Shell
conda activate yourENV
```

(3) Installing packages

Part of the required packages can be quickly installed by calling the `requirements.txt` file, which is located in the 
root directory of this repository. The installation can be done via `conda` by the following command:
```Shell
conda install --yes --file requirements.txt
```
or `pip` by the following command:
```Shell
pip install -r requirements.txt
```
(***Reminding***: *When setting up virtual environments by anaconda, using `conda install` before `pip install` is usually beneficial for environment management.*)


## III. Installation
```shell
```
