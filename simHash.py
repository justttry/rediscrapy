	
#!/usr/bin/python
# coding=utf-8
class simhash:
    
    #���캯��
    def __init__(self, tokens='', hashbits=128):        
        self.hashbits = hashbits
        self.hash = self.simhash(tokens);
    
    #toString����    
    def __str__(self):
        return str(self.hash)
    
    #����simhashֵ    
    def simhash(self, tokens):
        v = [0] * self.hashbits
        for t in [self._string_hash(x) for x in tokens]: #tΪtoken����ͨhashֵ
            for i in range(self.hashbits):
                bitmask = 1 << i
                if t & bitmask :
                    v[i] += 1 #�鿴��ǰbitλ�Ƿ�Ϊ1,�ǵĻ�����λ+1
                else:
                    v[i] -= 1 #����Ļ�,��λ-1
        fingerprint = 0
        for i in range(self.hashbits):
            if v[i] >= 0:
                fingerprint += 1 << i
        return fingerprint #�����ĵ���fingerprintΪ���ո���λ>=0�ĺ�
    
    #��������
    def hamming_distance(self, other):
        x = (self.hash ^ other) & ((1 << self.hashbits) - 1)
        tot = 0;
        while x :
            tot += 1
            x &= x - 1
        return tot
    
    #�����ƶ�
    def similarity (self, other):
        a = float(self.hash)
        b = float(other)
        if a > b : return b / a
        else: return a / b
    
    #���source����hashֵ   (һ���ɱ䳤�Ȱ汾��Python������ɢ��)
    def _string_hash(self, source):        
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** self.hashbits - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            return x
             

if __name__ == '__main__':
    s = 'This is a test string for testing'
    hash1 = simhash(s.split())
    
    s = 'This is a test string for testing also'
    hash2 = simhash(s.split())
    
    s = 'nai nai ge xiong cao'
    hash3 = simhash(s.split())
    
    print(hash1.hamming_distance(hash2.hash) , "   " , hash1.similarity(hash2.hash))
    print(hash1.hamming_distance(hash3.hash) , "   " , hash1.similarity(hash3.hash))