# ``AiryAi(0)`` calculated by Y-Cruncher. (0..48)
DEFAULT_SECRET =  [0x5ae31e589c56e17a,
    0x96d7bb04e64f6da9,
    0x7ab1006b26f9eb64,
    0x21233394220b8457,
    0x047cb9557c9f3b43,
    0xd24f2590c0bcee28]
# ``AiryAi(0)`` calculated by Y-Cruncher. (48..56)
INIT_RING_PREV = 0x33ea8f71bb6016d8
seg = lambda s:s*8
def rotate_left(num, k):  
    bits = 64 
    return (num << k) | (num >> (bits - k))

def rotate_right(num, k):  
    bits = 64
    return (num >> k) | (num << (bits - k))

def wrapping_add(a,b,bits=64):
    mask = (1 << bits) - 1
    return (a + b) & mask

def wrapping_sub(a, b, bits=64):  
    mask = (1 << bits) - 1  
    if b > a:  
        return ((a + (1 << bits) - b) & mask)  
    else: 
        return (a - b) & mask

def read_u32(b):
    return int.from_bytes(b[:4],'little')

def read_u64(b):
    return int.from_bytes(b[:8],'little')

def read_short(b):
    leng = len(b)
    if leng >= 4:
        off = (leng & 24) >> (leng >> 3)
        return (read_u32(b) << 32) | read_u32(b[leng-4:leng]),(read_u32(b[off:leng]) << 32) | read_u32(b[leng-4-off:leng])
    elif leng > 0:
        # [0] [0] [0] @ len == 1 (0b01)
        # [0] [1] [1] @ len == 2 (0b10)
        # [0] [1] [2] @ len == 3 (0b11)
        return (b[0]<<48)|(b[leng>>1]<<24)|b[leng-1],0
    else:
        return 0,0
# convert from lib.rs
def u128_to_u64s(x):
    return x & 0xFFFFFFFFFFFFFFFF,(x >> 64) & 0xFFFFFFFFFFFFFFFF

def u64s_to_u128(lo,hi):
    return ((hi << 64) | lo) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

def wmul(a,b):
    return u128_to_u64s(a*b)
# --+=+-----+=+-----+=+-----+=+---
def _frac_6(a,b,BFAST):
    s,t = a
    v,w = b
    s ^= v
    t ^= w
    if not BFAST:
        lo,hi = wmul(s,t)
        return s ^ lo, t ^ hi
    else:
        return wmul(s, t)
    
def _frac_3(a,v,BFAST):
    s,t = a
    t ^= v
    if not BFAST:
        lo,hi = wmul(s,t)
        return s ^ lo, t ^ hi
    else:
        return wmul(s, t)

def _chixx(t,u,v):
    return (t ^ (~u & v), u ^ (~v & t), v ^ (~t & u))

def _tower_layer_12(state,b,ring_prev,BFAST):
    if not BFAST:
        state[0] ^= read_u64(b[seg(0):len(b)])
        state[1] ^= read_u64(b[seg(1):len(b)])
        lo0,hi0 = wmul(state[0], state[1])
        state[0] = wrapping_add(state[0],ring_prev ^ hi0)
        
        state[1] ^= read_u64(b[seg(2):len(b)])
        state[2] ^= read_u64(b[seg(3):len(b)])
        lo1, hi1 = wmul(state[1], state[2])
        state[1] = wrapping_add(state[1],lo0 ^ hi1)
        
        state[2] ^= read_u64(b[seg(4):len(b)])
        state[3] ^= read_u64(b[seg(5):len(b)])
        lo2, hi2 = wmul(state[2], state[3])
        state[2] = wrapping_add(state[2],lo1 ^ hi2)

        state[3] ^= read_u64(b[seg(6):len(b)])
        state[4] ^= read_u64(b[seg(7):len(b)])
        lo3, hi3 = wmul(state[3], state[4])
        state[3] = wrapping_add(state[3],lo2 ^ hi3)

        state[4] ^= read_u64(b[seg(8):len(b)])
        state[5] ^= read_u64(b[seg(9):len(b)])
        lo4, hi4 = wmul(state[4], state[5])
        state[4] = wrapping_add(state[4],lo3 ^ hi4)

        state[5] ^= read_u64(b[seg(10):len(b)])
        state[0] ^= read_u64(b[seg(11):len(b)])
        lo5, hi5 = wmul(state[5], state[0])
        state[5] = wrapping_add(state[5],lo4 ^ hi5)
    else:
        state[0] ^= read_u64(b[seg(0):len(b)])
        state[1] ^= read_u64(b[seg(1):len(b)])
        lo0,hi0 = wmul(state[0], state[1])
        state[0] = ring_prev ^ hi0
        
        state[1] ^= read_u64(b[seg(2):len(b)])
        state[2] ^= read_u64(b[seg(3):len(b)])
        lo1, hi1 = wmul(state[1], state[2])
        state[1] = lo0 ^ hi1
        
        state[2] ^= read_u64(b[seg(4):len(b)])
        state[3] ^= read_u64(b[seg(5):len(b)])
        lo2, hi2 = wmul(state[2], state[3])
        state[2] = lo1 ^ hi2

        state[3] ^= read_u64(b[seg(6):len(b)])
        state[4] ^= read_u64(b[seg(7):len(b)])
        lo3, hi3 = wmul(state[3], state[4])
        state[3] = lo2 ^ hi3

        state[4] ^= read_u64(b[seg(8):len(b)])
        state[5] ^= read_u64(b[seg(9):len(b)])
        lo4, hi4 = wmul(state[4], state[5])
        state[4] = lo3 ^ hi4

        state[5] ^= read_u64(b[seg(10):len(b)])
        state[0] ^= read_u64(b[seg(11):len(b)])
        lo5, hi5 = wmul(state[5], state[0])
        state[5] = lo4 ^ hi5
    return state, lo5

def _tower_layer_6(state,b,BFAST):
    state[0],state[1] = _frac_6((state[0],state[1]),(read_u64(b[seg(0):len(b)]),read_u64(b[seg(1):len(b)])),BFAST)
    state[2],state[3] = _frac_6((state[2],state[3]),(read_u64(b[seg(2):len(b)]),read_u64(b[seg(3):len(b)])),BFAST)
    state[4],state[5] = _frac_6((state[4],state[5]),(read_u64(b[seg(4):len(b)]),read_u64(b[seg(5):len(b)])),BFAST)
    return state

def _tower_layer_3(state,b,BFAST):
    state[0],state[3] = _frac_3((state[0],state[3]),read_u64(b[seg(0):len(b)]),BFAST)
    state[1],state[4] = _frac_3((state[1],state[4]),read_u64(b[seg(1):len(b)]),BFAST)
    state[2],state[5] = _frac_3((state[2],state[5]),read_u64(b[seg(2):len(b)]),BFAST)
    return state

def _tower_layer_0(state,b,tot_len):
    i,j,k = 0,0,0
    leng = len(b)
    assert leng <= seg(3)
    if leng <= seg(2):
        (i, j) = read_short(b)
        k = 0
    else:
        i = read_u64(b[seg(0):leng])
        j = read_u64(b[seg(1):leng])
        k = read_u64(b[leng-seg(1):leng])
    if tot_len >= seg(3):
        state[0],state[2],state[4] = _chixx(state[0], state[2], state[4])
        state[1],state[3],state[5] = _chixx(state[1], state[3], state[5])
        i ^= wrapping_add(state[0],state[1])
        j ^= wrapping_add(state[2],state[3])
        k ^= wrapping_add(state[4],state[5])
    else:
        i ^= state[0]
        j ^= state[1]
        k ^= state[2]
    return i,j,k

def _tower_layer_x(a,tot_len,BFAST):
    i,j,k = a
    rot = tot_len & 0b111111
    i,j,k = _chixx(i,j,k)
    i = rotate_left(i,rot)
    j = rotate_right(j,rot)
    k ^= tot_len
    if not BFAST:
        lo0,hi0 = wmul(i ^ DEFAULT_SECRET[3], j)
        lo1,hi1 = wmul(j ^ DEFAULT_SECRET[4], k)
        lo2,hi2 = wmul(k ^ DEFAULT_SECRET[5], i)
        return i ^ lo0 ^ hi2, j ^ lo1 ^ hi0, k ^ lo2 ^ hi1
    else:
        lo0,hi0 = wmul(i, j)
        lo1,hi1 = wmul(j, k)
        lo2,hi2 = wmul(k, i)
        return lo0 ^ hi2, lo1 ^ hi0, lo2 ^ hi1

def tower_loong(b,seed,BFAST):
    tot_len = len(b)
    assert tot_len > 16
    off = 0
    rem = tot_len
    state = DEFAULT_SECRET
    state[0] = wrapping_add(state[0],seed)
    state[1] = wrapping_sub(state[1],seed)
    state[2] ^= seed
    if rem >= seg(12):
        state[3] = wrapping_add(state[3],seed)
        state[4] = wrapping_sub(state[4],seed)
        state[5] ^= seed
        ring_prev = INIT_RING_PREV
        while not rem < seg(12):
            state,ring_prev = _tower_layer_12(state,b[off:tot_len],ring_prev,BFAST)
            off += seg(12)
            rem -= seg(12)
        state[0] ^= ring_prev
    if rem >= seg(6):
        state = _tower_layer_6(state,b[off:tot_len],BFAST)
        off += seg(6)
        rem -= seg(6)
    if rem >= seg(3):
        state = _tower_layer_3(state,b[off:tot_len],BFAST)
        off += seg(3)
    return _tower_layer_x(_tower_layer_0(state,b[off:tot_len],tot_len),tot_len,BFAST)

def tower_short(b,seed):
    leng = len(b)
    i,j = read_short(b)
    lo,hi = wmul(seed ^ DEFAULT_SECRET[0], leng ^ DEFAULT_SECRET[1])
    return i ^ lo ^ leng, j ^ hi ^ seed

def epi_short(a):
    i,j = a
    i ^= DEFAULT_SECRET[2]
    j ^= DEFAULT_SECRET[3]
    lo,hi = wmul(i, j)
    i ^= lo ^ DEFAULT_SECRET[4]
    j ^= hi ^ DEFAULT_SECRET[5]
    lo,hi = wmul(i, j)
    return i ^ j ^ lo ^ hi

def epi_short_128(a,BFAST):
    i,j = a
    if not BFAST:
        lo0,hi0 = wmul(i ^ DEFAULT_SECRET[2], j)
        lo1,hi1 = wmul(i, j ^ DEFAULT_SECRET[3])
        i ^= lo0 ^ hi1
        j ^= lo1 ^ hi0
        lo0,hi0 = wmul(i ^ DEFAULT_SECRET[4], j)
        lo1,hi1 = wmul(i, j ^ DEFAULT_SECRET[5])
        return u64s_to_u128(i ^ lo0 ^ hi1, j ^ lo1 ^ hi0)
    else:
        lo0,hi0 = wmul(i, j)
        lo1,hi1 = wmul(i ^ DEFAULT_SECRET[2], j ^ DEFAULT_SECRET[3])
        i = lo0 ^ hi1
        j = lo1 ^ hi0
        lo0,hi0 = wmul(i,j)
        lo1,hi1 = wmul(i ^ DEFAULT_SECRET[4], j ^ DEFAULT_SECRET[5])
        return u64s_to_u128(lo0 ^ hi1, lo1 ^ hi0)

def epi_loong(a,BFAST):
    i,j,k = a
    if not BFAST:
        lo0,hi0 = wmul(i ^ DEFAULT_SECRET[0], j)
        lo1,hi1 = wmul(j ^ DEFAULT_SECRET[1], k)
        lo2,hi2 = wmul(k ^ DEFAULT_SECRET[2], i)
        i ^= lo0 ^ hi2
        j ^= lo1 ^ hi0
        k ^= lo2 ^ hi1
    else:
        lo0,hi0 = wmul(i, j)
        lo1,hi1 = wmul(j, k)
        lo2,hi2 = wmul(k, i)
        i = lo0 ^ hi2
        j = lo1 ^ hi0
        k = lo2 ^ hi1
    return wrapping_add(wrapping_add(i,j),k)

def epi_loong_128(a,BFAST):
    i,j,k = a
    if not BFAST:
        lo0,hi0 = wmul(i ^ DEFAULT_SECRET[0], j)
        lo1,hi1 = wmul(j ^ DEFAULT_SECRET[1], k)
        lo2,hi2 = wmul(k ^ DEFAULT_SECRET[2], i)
        i ^= lo0 ^ lo1 ^ hi2
        j ^= hi0 ^ hi1 ^ lo2
    else:
        lo0,hi0 = wmul(i, j)
        lo1,hi1 = wmul(j, k)
        lo2,hi2 = wmul(k, i)
        i ^= lo0 ^ lo1 ^ hi2
        j ^= hi0 ^ hi1 ^ lo2
    return u64s_to_u128(i, j)

def base_hash(b,seed,BFAST):
    if len(b) <= seg(2):
        return epi_short(tower_short(b, seed))
    else:
        return epi_loong(tower_loong(b,seed,BFAST),BFAST)

def base_hash_128(b,seed,BFAST):
    if len(b) <= seg(2):
        return int.from_bytes(epi_short_128(tower_short(b,seed),BFAST).to_bytes(16,'little'),'big')
    else:
        return int.from_bytes(epi_loong_128(tower_loong(b,seed,BFAST),BFAST).to_bytes(16,'little'),'big')

def hash(b,seed):
    return base_hash(b,seed,False)
# One-shot MuseAir hash with 128-bit output.
#
# Note that the 128-bit variant is designed to be **as fast as** the 64-bit variant,
# so you can use it if necessary without worrying about performance.
def hash_128(b,seed):
    return base_hash_128(b,seed,False)
# The `-BFast` variant is faster but *less* immune to blinding multiplication.
#
# ("less" here means when it actually happens, it will only result in the most recent state being lost, rather than all the past state of a stripe being catastrophically lost!)
def hash_BFAST(b,seed):
    return base_hash(b,seed,True)

def hash_128_BFAST(b,seed):
    return base_hash_128(b,seed,True)

def test():
    data = bytes(range(1,17))
    print('With BlindFast = false: 64-bit hash: '+hex(hash(data,0x12345678ABCDEF))[2:])
    print('With BlindFast = false: 128-bit hash: '+hex(hash_128(data,0x12345678ABCDEF))[2:])
    print('With BlindFast = true: 64-bit hash: '+hex(hash_BFAST(data,0x12345678ABCDEF))[2:])
    print('With BlindFast = true: 128-bit hash: '+hex(hash_128_BFAST(data,0x12345678ABCDEF))[2:])

if __name__ == '__main__':
    test()
