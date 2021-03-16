from damage import *
from weaponsarmor import *

def bar(x, symbol = 'X'):
  print("".join([symbol for x in range(int(x))]))

bar(100,'=')

print("rapier S5 -> leather B5")
d = damage('S','B',5,5,rapier['type'],rapier['strength'],leather['type'],leather['strength'])
print(d)
bar(d)
print(100/d)

print("\nrapier S9 -> leather B1")
d = damage('S','B',9,1,rapier['type'],rapier['strength'],leather['type'],leather['strength'])
print(d)
bar(d)
print(100/d)

print("\nrapier T5 -> leather B5")
d = damage('T','B',5,5,rapier['type'],rapier['strength'],leather['type'],leather['strength'])
print(d)
bar(d)
print(100/d)

print("\nrapier T9 -> leather B1")
d = damage('T','B',9,1,rapier['type'],rapier['strength'],leather['type'],leather['strength'])
print(d)
bar(d)
print(100/d)

print("\nrapier S5 -> leather P5")
d = damage('S','P',5,5,rapier['type'],rapier['strength'],leather['type'],leather['strength'])
print(d)
bar(d)
print(100/d)

print("\nrapier S9 -> leather P1")
d = damage('S','P',9,1,rapier['type'],rapier['strength'],leather['type'],leather['strength'])
print(d)
bar(d)
print(100/d)

