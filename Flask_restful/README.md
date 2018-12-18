# PYTHON API
This is an api for sayit_ctc project.when run, The url is http://localhost/ port 80
# Requirement
* **Linux**
* **python 3.7** 
* download [model file](https://mycostech-my.sharepoint.com/:u:/p/kornkamon/ESnprKY2dq5Mg6c7te79KNgBC-G1rQgWETMG_pLIfP6apg?e=oNK3q1) and put in models\deepspeech\models directory

# Docker
```
docker-compose build
docker-compose up
```
# Installation 
* pytorch-nighlty 
```
pip install torch_nightly -f https://download.pytorch.org/whl/nightly/cu90/torch_nightly.html
```
or
```
conda install pytorch-nightly -c pytorch
``` 

* pytorch audio 
```
sudo apt-get install sox libsox-dev libsox-fmt-all
git clone https://github.com/pytorch/audio.git
cd audio
python setup.py install
```

* pip install requirements
```
pip install -r requirements.txt
```
* run `python main.py`

 
