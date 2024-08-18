import time
from os import urandom
def test(hash_func,num=10):
    data = urandom(1024) # 在计时前生成
    s = time.time()
    for i in range(num):
        hash_func(data,0xACEDCAFE+i)
    e = time.time()
    return e-s
if __name__ == '__main__':
    import museair
    print('64bits without B-Fast:'+str(test(museair.hash)))
    print('128bits without B-Fast:'+str(test(museair.hash_128)))
    print('64bits with B-Fast:'+str(test(museair.hash_BFAST)))
    print('128bits with B-Fast:'+str(test(museair.hash_128_BFAST)))
