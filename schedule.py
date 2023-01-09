import requests
courseURL = 'http://sis.rutgers.edu/soc/api/courses.json?year=2022&term=9&campus=NB'
day = {
    'M' : 0,
    'T' : 1,
    'W' : 2,
    'H' : 3,
    'F' : 4
}
# Connects to SOC API
res = requests.get(courseURL)
res = res.json()
schedule = []
# Iterates through only SCI Undergrad classes, should add grad classes, and depending on input adds the select classroom
for course in res:
    if course['school']['code'] != '04':
        continue
    sections = course['sections']
    for s in sections:
        meetingTimes = s['meetingTimes']
        for meet in meetingTimes:
            if meet['buildingCode'] == 'CI'and meet['roomNumber'] == '203':
                schedule.append((course['title'], s['index'] + ", " + s['instructorsText'], day[meet['meetingDay']], meet['startTimeMilitary'] +" - "+ meet['endTimeMilitary']))

schedule = sorted(schedule, key = lambda x:x[3])
prevDay = schedule[0][3]
prevInd = 0
newSchedule = []
amtClasses = 0
for ind in range(len(schedule)):
    if ind == len(schedule)-1:
        temp = sorted(schedule[prevInd:], key = lambda x:x[3])
        amtClasses = max(amtClasses, ind-prevInd)
        prevDay = currDay
        prevInd = ind
        newSchedule.append(temp)
        continue
    currDay = schedule[ind][3]
    if prevDay != currDay:
        temp = sorted(schedule[prevInd:ind], key = lambda x:x[3])
        amtClasses = max(amtClasses, ind-prevInd)
        prevDay = currDay
        prevInd = ind
        newSchedule.append(temp)
for row in newSchedule:
    while len(row) < amtClasses:
        row.append((0,0))
finalSchedule = []
for y in range(len(newSchedule[0])):
    temp = []
    for x in range(len(newSchedule)):
        if newSchedule[x][y] != (0,0):
            print('\n'.join(map(lambda x: str(x or ''), (newSchedule[x][y]))))
            break
            # temp.append(" ".join(newSchedule[x][y]))
    finalSchedule.append(temp)
for row in finalSchedule:
    for col in row:
        # temp = col[0] + '\n' + col[1]
        print(col, end = "\t")
    print()
