import datetime

"""Retrive Study Information"""
f = open("Exams And Topics.md","r")
inputFile = f.read()
f.close()
inputFile = inputFile.split("\n# ")[1:]
for i in range(len(inputFile)):
    inputFile[i] = inputFile[i].split("\n## ")
    for j in range(len(inputFile[i])):
        inputFile[i][j] = inputFile[i][j].split("\n- ")
        for k in range(len(inputFile[i][j])):
            inputFile[i][j][k] = inputFile[i][j][k].removesuffix("\n")
            if k == 0:
                inputFile[i][j][k] = inputFile[i][j][k].split(" - ")

"""Parse Study Information"""
allData = []
for i in range(len(inputFile)):
    tempSubjectDict = {
"Subject": inputFile[i][0][0][0],
 "Papers": [
 ]
}
    for j in range(1,len(inputFile[i])):
        halvesFound = False
        k = 0
        tempPaperDict = {
         "Name:": inputFile[i][j][0][0],
         "Date": inputFile[i][j][0][1].removesuffix(", 2023"),
         "Topics" : inputFile[i][j][1:],
         "Half Topics" : []
     }
        while not(halvesFound) and k < len(tempPaperDict["Topics"]) :
            if "\n\n---" in tempPaperDict["Topics"][k]:
                tempPaperDict["Topics"][k] = tempPaperDict["Topics"][k].removesuffix("\n\n---")
                halvesFound = True
                k = k + 1
                tempPaperDict["Half Topics"] = tempPaperDict["Topics"][k:]
                tempPaperDict["Topics"] = tempPaperDict["Topics"][:k]
            else:
                k = k + 1
        tempSubjectDict["Papers"].append(tempPaperDict)
    allData.append(tempSubjectDict)

"""Create Study Timetable"""
days = []
start_date = datetime.date(2023, 2, 27)
end_date = datetime.date(2023, 7, 9)
while start_date <= end_date:
  days.append(str(start_date.strftime('%B %dth '))[:-3])
  start_date += datetime.timedelta(days=1)
daysDict = {key: {"Learn":[], "Practice":[], "Consolidate":[]} for key in days}

"""Populate Study Timetable"""
for subject in allData:
    for paper in subject["Papers"]:
        ExamIndex = days.index(paper["Date"])
        spaces = int(ExamIndex / 10)
        # 1:2:3:4
        for topicIndex in range(len(paper["Topics"])-1,0,-1):
            currentDay = ExamIndex - 4
            for sessionIndex,sessionType in enumerate(("Consolidate", "Practice", "Learn")):
                placed = False
                while not(placed) and currentDay > -1:
                    if len(daysDict[days[currentDay]][sessionType]) != 3:
                        daysDict[days[currentDay]][sessionType].append(paper["Topics"][topicIndex])
                        placed = True
                    currentDay = currentDay - 1
                currentDay = currentDay - (spaces*(3-sessionIndex))

"""Return Study Timetable"""
plan = "\n"
for day in daysDict:
    if daysDict[day] != {"Learn":[], "Practice":[], "Consolidate":[]}:
        plan += ("# "+day+"\n\n")
        for sessionType in daysDict[day]:
            if daysDict[day][sessionType] != []:
                plan += ("## " + sessionType +"\n\n")
                for topic in daysDict[day][sessionType]:
                    plan += ("- " + topic + "\n")
                plan += ("\n")
f = open("Study Plan.md","w")
f.write(plan)
f.close()
print(plan)