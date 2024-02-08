# Installation
`segpy` is a Python module specifically designed for segregation analysis, developed on Python 3.10.2, the module can be easily downloaded using `pip` package manager:  

```
pip install 'git+https://github.com/neurobioinfo/segpy#subdirectory=segpy'
```

Segregation analysis can be conducted utilizing the segpy scheduler, `segpy.pip`. If you have access to an HPC or Linux workstation, you can automate the process using `segpy.pip`. The scheduler script is written in Bash, making it compatible with systems such as Slurm or a Linux workstation.

```
wget https://github.com/neurobioinfo/segpy/releases/download/v0.2.2.3/segpy.pip.zip
unzip segpy.pip.zip 
```

To obtain a brief guidance of the pipeline, execute the following code.
```
bash ./segpy.pip/launch_segpy.sh -h
```
