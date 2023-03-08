# coding=utf-8
# 在创建一个类的对象时，如果之前使用同样参数创建过这个对象， 你想返回它的缓存引用。
import weakref

class Spam:
    _spam_cache = weakref.WeakValueDictionary()

    # __new__()先于__init__()调用
    def __new__(cls, name, age):
        key = hash(name + str(age))
        if key in cls._spam_cache:
            return cls._spam_cache[key]
        else:
            self = super().__new__(cls)
            setattr(self, "l", list())
            setattr(self, "hash", key)
            cls._spam_cache[key] = self
            return self
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.l.append(name)
        print(self.l)

s1 = Spam("hello", 1)
s2 = Spam("world", 2)
print(s1 is s2)
print(id(s1)==id(s2))

s3 = Spam("hello", 1)
print(s1 is s3)
print(id(s1)==id(s3))

t = s1.hash
m = {
    s1.hash: s1,
    s2.hash: s2,
    s3.hash: s3,
}
for k, v in m.items():
    print(k, v.name, v.age, v.l)

s = m[t] # 赋值都是引用
s.l.pop()
for k, v in m.items():
    print("xxx", k, v.name, v.age, v.l)