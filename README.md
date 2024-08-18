# museair-python
Python version of https://github.com/eternal-io/museair

## What's this?
It's a simple implementation of museair [薄纱！高中生编写的哈希算法超越了先前的所有算法！(合作 K--Aethiax&Twilight-Dream) 王一大佬你在看嘛？ [2024-08-16]
](https://www.bilibili.com/video/BV1vTeuefEHN).

Completely converted from the original Rust code, no optimizations were made to the Python version of the code.

## How to use?
1. Move museair.py to your project root and add this code to your code:
```python
import museair
```
or
```python
from museair import hash,hash128,hash_BFAST,hash128_BFAST
```
2. Example
```python
from museair import hash
data = bytes(range(1,17))
seed = 0x12345678ABCDEF
result = hash(data,seed)
print(hex(result)[2:])
```

## Benchmark
Run test.py
python3.10.5 32bit:
```python
64bits without B-Fast:0.011997222900390625
128bits without B-Fast:0.011997699737548828
64bits with B-Fast:0.013997793197631836
128bits with B-Fast:0.014001607894897461
```
pypy3.10 64bit:
```python
64bits without B-Fast:0.04000043869018555
128bits without B-Fast:0.04499554634094238
64bits with B-Fast:0.02600240707397461
128bits with B-Fast:0.036004066467285156
```
