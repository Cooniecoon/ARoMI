# AI Robot Mate for Individual

## 1인가구를 위한 소셜로봇

사용자의 자세, 표정을 인식한 후 이를 기반으로 대화 유도

### Dependency

- Python 3.6
- CUDA 11.1
- cuDNN 8.0.5
- TensorFlow 2.4

```bash
$ pip3 install -r requirments.txt
```
```bash
$ conda install swig
$ cd tf_pose/pafprocess
$ swig -python -c++ pafprocess.i
$ python3 setup.py build_ext --inplace
```