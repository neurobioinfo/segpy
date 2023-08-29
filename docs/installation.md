# Installation
`segpy` is a python module developed on Python 3.10.2 to run the segregation analysis, the module can be easily downloaded using `pip`:  
```
pip install 'git+https://github.com/neurobioinfo/segpy#subdirectory=segpy'
```

The segregation can do done using the segpy module, if you have access to HPC, you can automate it using segpy.slurm
The `segpy.slurm` is written in the bash, so it can be used with any slurm system. To download  `segpy.slurm`, run the below comments 
```
wget https://github.com/neurobioinfo/segpy/releases/download/v0.2.1/segpy.slurm.zip
unzip segpy.slurm.zip 
```

To obtain a brief guidance of the pipeline, execute the following code.
```
bash ./scrnabox.slurm/launch_segpy.sh -h
```
