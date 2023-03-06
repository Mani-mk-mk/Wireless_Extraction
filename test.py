def count_monsters_left(A, B):
    n = len(A)
    q = len(B)
    monsters = []
    for i in range(n):
        for j in range(A[i][0], A[i][1]+1):
            monsters.append((j, A[i][2]))
    monsters.sort()
    heroes = []
    for i in range(q):
        heroes.append((B[i][0], B[i][1], i))
    heroes.sort()
    ans = [n]*q
    i, j = 0, 0
    while i < q and j < len(monsters):
        if heroes[i][0] >= monsters[j][0]:
            if heroes[i][1] >= monsters[j][1]:
                ans[heroes[i][2]] = j + 1
                j += 1
            else:
                i += 1
        else:
            j += 1
    return [n-x for x in ans]

A = [[1, 3, 7], [2, 5, 4], [4, 8, 6]]
B = [[3, 5], [5, 8]]

print(count_monsters_left(A, B))