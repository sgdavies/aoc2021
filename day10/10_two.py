dat = """12332 4 3 4 4 2 4
4346 3 1 1 4
10606 3 3 2 2 2 3 2 3 3
12433 4 4 4 1 1 1 4
4332 1 3 2 3 2 1 1
13987 4 1 1 4
9168 3 1 1 4 1 3 2
12041 1 2 4 2 4 4 2 3 4
4942 1 4 2 3 1 2 1 1 2
7324 4 3 4 2 3 2 1 3 4
4912 4 3 2 4 1 2
15588 4 2 3 4 1 3 1 2
4739 1 2 2 4 4
8673 2 1 3 1 1 1 3 2
8294 4 3 2 3 3 1 4 4
12196 1 3 2 4 4 4 4 1
7234 1 4 3 4 1 4 1
8983 4 4 4 3 4 2 3
4371 3 3 2 4 3 1 2 3 4
9171 3 4 2 4
11709 2 3 3
7906 1 2 4 3 2 1
5422 2 3 3 3 4 2 4 1 4
6222 1 1 1 3 4
14924 2 2 4 2
14737 3 2 3 4 2 1 1
4191 4 2 4 2 4 1 3 3 1
8062 3 1 3 3 1 1
13538 3 3 4 3 1 1 2 2 2
13364 3 2 1 2 1
7433 2 4 2 3 3
15442 4 3 3 3 3 4 3 4
7319 4 2 1 3 1 2 1 3 2
11216 3 1 4 4 3 3 1 2 1
4191 1 3 2 2 4 1
4572 1 2 4 1 4 4 3
14058 3 4 1 3 2 3
10593 4 2 3 3 3 3 2 1 2
7247 2 2 2 4 3 2 4 2
7071 2 4 2 1 4 2 4 2
11419 2 1 3 4 3 3 1 1 3
15322 2 4 4 2 3 1 1 2
9194 3 4 2 4 3 3 2 2
5317 1 4 1 2 3 3 3 2
7741 1 2 2 2 4 2 3 1 1
14713 1 2 1 3 1 1 4 2 4
14191 1 1 3 4 4 1 1 3 3"""

vals = []
for row in dat.split('\n'):
    nums = [int(x) for x in row.split(" ")]
    ans = nums.pop(0)
    while nums:
        ans*= 5
        ans += nums.pop(0)
    vals.append(ans)

vals.sort()
print(vals[len(vals)//2])
print(vals[-1])