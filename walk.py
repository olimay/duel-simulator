import random
from statistics import mode, variance

print("imported")

def randomwalk(step_big, step_small, x_0 = 0, a = -100, b = 100):
  x = x_0
  rounds = 0
  while x > a and x < b:
    step = random.rand(-2,0,2)
    direction = 0
    dist = 0
    if step < 0:
      direction = -1
    elif step > 0:
      direction = 1
    if abs(step) == 2:
      dist = step_big
    elif abs(step) == 1:
      dist = step_small
    # take the step
    x += direction*dist
    rounds += 1
  return rounds

def simulate(step_big, step_small, n = 10000):
  roundcounts = []
  for i in range(n):
    roundcounts.push(randomwalk(step_big, step_small))
  mean = sum(roundcounts)/n
  print("range = [{},{}]\nmean = {}\nmode = {}, variance = {}".format(
    min(roundcounts),
    max(roundcounts),
    mode(roundcounts),
    variance(roundcounts),
    ))
