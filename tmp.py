df = [['a', 'b'], [2, 4]]
zf = list(zip(*df))

rf = {}
for name, value in zf:
  rf[name] = value
print(rf)

rf = {key: value for key, value in zip(df[0], df[1])}
print(rf)
