def f(n):
  if n == 1:
    return n
  if n == 0:
    return n
  return f(n-1) + f(n-2)

print(f(5))
