import random
from statistics import mode, variance

def randomwalk(step_big, step_small, x_0 = 0, a = -100, b = 100):
  x = x_0
  rounds = 0
  while x > a and x < b:
    step = random.randint(-2,2)
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
    roundcounts += [randomwalk(step_big, step_small)]
  mean = sum(roundcounts)/n
  gt10 = sum([(x > 10) for x in roundcounts])
  print("range = [{},{}]\ngreater than 10: {}\nmean = {}\nmode = {}, variance = {}".format(
    min(roundcounts),
    max(roundcounts),
    gt10/n,
    mean,
    mode(roundcounts),
    variance(roundcounts),
    ))
