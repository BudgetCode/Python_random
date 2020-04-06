distance , most , excep = list(map(int,input().split()))
excep_days = dict()

for x in range(excep):
    inp = list(map(int,input().split()))
    excep_days[inp[0]] = inp[1]

days_passed = -1

while distance > 0:
    days_passed +=1
    if days_passed in excep_days:
        distance -= excep_days[days_passed]
    else:
        distance -= most

print(days_passed)
