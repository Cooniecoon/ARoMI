# AI Robot Mate for Individual

## Abstract

### 1인가구를 위한 소셜로봇

사용자의 자세, 표정을 인식한 후 이를 기반으로 대화 유도

### Environment / Dependencies

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

---
### TODO
- [x] ~~Pose Data 수집 : Input data shape (18,2) -> (1,36)~~
- [x] ~~Pose Classifier 모델 수정~~
- [ ] EyeContact Situation일 때 챗봇 호출 알고리즘 수정
- [ ] Face Expression Recognition 모델 추가
- [ ] Robot UI, Motor Motion Code Merge
- [ ] AWS 환경 설정, 업로드