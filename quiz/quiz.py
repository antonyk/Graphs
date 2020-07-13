
def sum(d):

  result = 0
  for item in d:
    if type(d[item]) is int:
      result += d[item]

  return result


d1 = {
  "cat": "bob",
  "dog": 23,
  19: 18,
  90: "fish"
}

print(sum(d1))

