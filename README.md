# competition-music-analysis

Analysis of the evolution of the partecipating song in the competition of Sanremo (IT) and Eurovision (EU)

## Setup

Create a virtual enviroment with `conda`

```bash
conda create --name music-venv python=3.9
```

Activate the virtual enviroment

```bash
conda activate music-venv
```

Install `pip`

```bash
conda install pip
```

Install the packages

```bash
pip install -r requirements.txt
```

Install FFmpeg

```bash
sudo apt install ffmpeg
```

### Install tensorflow

Install CUDA and cuDNN

```bash
conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0
```

Configure system path

```bash
mkdir -p $CONDA_PREFIX/etc/conda/activate.d
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/' > $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
```

Upgrade pip

```bash
pip install --upgrade pip
```

Install tensorflow

```bash
pip install tensorflow
```

**FIX successful NUMA node read from SysFS had negative value (-1)** `for a in /sys/bus/pci/devices/*; do echo 0 | sudo tee -a $a/numa_node; done`
