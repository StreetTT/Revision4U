# Classful
import datetime

class ExamSeason:
    def __init__(self):
        self.Subjects = []
        self.File = ""
        self.Calander = []
        self.PopulateCalander()
        
    def AddSubject(self,subject):
        self.Subjects.append(subject)

    def GetFile(self):
        return self.File

    def FileToList(self):
        self.File = self.File.split("\n# ")[1:]
        for i in range(len(self.File)):
            self.File[i] = self.File[i].split("\n## ")
            for j in range(len(self.File[i])):
                self.File[i][j] = self.File[i][j].split("\n- ")
                for k in range(len(self.File[i][j])):
                    self.File[i][j][k] = self.File[i][j][k].removesuffix("\n")
                    if k == 0:
                        self.File[i][j][k] = self.File[i][j][k].split(" - ")
    
    def GetFileFromPC(self,filename):
        f = open(filename,"r")
        self.File = (f.read())
        f.close()
        self.FileToList()
        
    def ParseStudyData(self):
        for i in range(len(self.GetFile())):
            currentSubject = Subject()
            currentSubject.SetSubject(self.GetFile()[i][0][0][0])
            for j in range(1,len(self.GetFile()[i])):
                currentPaper = Paper()
                currentPaper.SetPaper(self.GetFile()[i][j][0][0])
                dateIndex = self.FindDate(datetime.datetime.strptime(self.GetFile()[i][j][0][1], '%H:%M %B %d %Y'))
                currentPaper.SetDate(dateIndex)
                currentPaper.SetDateTime(datetime.datetime.strptime(self.GetFile()[i][j][0][1], '%H:%M %B %d %Y'))
                fullTopics, halfTopics = currentPaper.SplitTopics(self.GetFile()[i][j][1:])
                currentPaper.SetFullTopics(fullTopics)
                currentPaper.SetHalfTopics(halfTopics)
                currentSubject.AddPaper(currentPaper)
                self.Calander[dateIndex].AddExam(currentPaper)
                currentPaper.SetSubject(currentSubject)
            self.AddSubject(currentSubject)
    
    def FindDate(self,date):
        for index,dateValue in enumerate(self.Calander):
            if dateValue.GetDate() == date.replace(hour=0, minute=0):
                return index
        self.Calander.append(Date(date))
        return len(self.Calander) - 1
    
    def PopulateCalander(self):
        now = datetime.datetime((datetime.datetime.now()).year, 3, 1)
        tomorrow = now
        self.Calander = [Date(now)]
        while tomorrow != now + datetime.timedelta(days=120):
            self.Calander.append(Date(tomorrow))
            tomorrow = tomorrow + datetime.timedelta(days=1)

    def PrintCalander(self):
        plan = "\n"
        for date in (self.Calander):
            if not (date.IsEmpty()) and date.GetDate() > (datetime.datetime.now() - datetime.timedelta(days=1)):
                plan += ("# "+str(date)+"\n")
                if date.GetExams() != []:
                    for exam in date.GetExams():
                        plan += ('### ' + exam.GetSubject().GetSubject() + " - " + exam.GetDateTime().strftime("%H:%M") + " - " + exam.GetPaper() + "\n")
                    plan += "\n"
                plan += "\n"
                for sessionType in ("Consolidate", "Practice", "Learn"):
                    if sessionType == "Consolidate" and date.GetConsolidateTopics() != []:
                        plan += ("## " + sessionType +"\n\n")
                        for topic in date.GetConsolidateTopics():
                            plan += ("- " + topic + "\n")
                    elif sessionType == "Practice" and date.GetPracticeTopics() != []:
                        plan += ("## " + sessionType +"\n\n")
                        for topic in date.GetPracticeTopics():
                            plan += ("- " + topic + "\n")
                    elif sessionType == "Learn" and date.GetLearnTopics() != []:
                        plan += ("## " + sessionType +"\n\n")
                        for topic in date.GetLearnTopics():
                            plan += ("- " + topic + "\n")
                plan += ("\n")
        f = open("Study Plan.md","w")
        f.write(plan)
        f.close()

    def PopulateStudyTimetable(self):
        for subject in self.Subjects:
            papers = subject.GetPapers()
            for paper in papers:
                spaces = int(paper.GetDate() / 10)
                for topicIndex in range(len(paper.GetFullTopics())-1,0,-1):
                    currentDay = paper.GetDate() - 10
                    for sessionIndex,sessionType in enumerate(("Consolidate", "Practice", "Learn")):
                        placed = False
                        while not(placed) and currentDay > -1:
                            if self.Calander[currentDay].GetTopicCount() != self.Calander[currentDay].GetDayMax():
                                if sessionType == "Consolidate":
                                    self.Calander[currentDay].AddConsolidateTopic(paper.GetFullTopics(topicIndex))
                                elif sessionType == "Practice":
                                    self.Calander[currentDay].AddPracticeTopic(paper.GetFullTopics(topicIndex))
                                else:
                                    self.Calander[currentDay].AddLearnTopic(paper.GetFullTopics(topicIndex))
                                placed = True
                            currentDay = currentDay - 1
                        currentDay = currentDay - (spaces*(3-sessionIndex))

class Subject:
    def __init__(self):
        self.Subject = None
        self.Papers = []
    
    def AddPaper(self,paper):
        self.Papers.append(paper)

    def GetPapers(self):
        return self.Papers
        
    def GetSubject(self):
        return self.Subject
        
    def SetSubject(self, subject):
        self.Subject = subject


class Paper:
    def __init__(self):
        self.Paper = ""
        self.Date = None
        self.Time = None
        self.Subject = None
        self.FullTopics = []
        self.HalfTopics = []

    def GetSubject(self):
        return self.Subject
        
    def SetSubject(self, subject):
        self.Subject = subject
    
    def SetFullTopics(self,topic):
        self.FullTopics = (topic)
    
    def SetHalfTopics(self,topic):
        self.HalfTopics = (topic)

    def GetFullTopics(self,index=-1):
        if index != -1:
            return self.FullTopics[index]
        return self.FullTopics
    
    def GetHalfTopics(self,index=-1):
        if index != -1:
            return self.HalfTopics[index]
        return self.HalfTopics
    
    def GetDate(self):
        return self.Date
        
    def SetDate(self, date):
        self.Date = date

    def GetDateTime(self):
        return self.DateTime
        
    def SetDateTime(self, dateTime):
        self.DateTime = dateTime    
        
    def GetPaper(self):
        return self.Paper
        
    def SetPaper(self, paper):
        self.Paper = paper
    def SplitTopics(self,topics):
        halvesFound = False
        k = 0
        FullTopics = []
        HalfTopics = []
        while not(halvesFound) and k < len(topics) :
            if "\n\n---" in topics[k]:
                topics[k] = topics[k].removesuffix("\n\n---")
                halvesFound = True
                k = k + 1
                HalfTopics = topics[k:]
                FullTopics = topics[:k]
            else:
                k = k + 1
                FullTopics = topics
        return FullTopics, HalfTopics
            
class StudyTimetable:
    def __init__(self):
        self.Dates = []

class Date:
    def __init__(self,date):
        self.Date = date
        self.Exams = []
        self.TopicCount = 0
        self.LearnTopics = []
        self.PracticeTopics = []
        self.ConsolidateTopics = []
        
    def AddExam(self,exam):
        self.Exams.append(exam)

    def GetDayMax(self):
        if len(self.Exams) == 0:
            return 3
        elif len(self.Exams) == 1:
            return 1
        return 0
    
    def AddLearnTopic(self,topic):
        self.LearnTopics.append(topic)
        self.TopicCount += 1
    
    def AddPracticeTopic(self,topic):
        self.PracticeTopics.append(topic)
        self.TopicCount += 1
    
    def AddConsolidateTopic(self,topic):
        self.ConsolidateTopics.append(topic)
        self.TopicCount += 1

    def GetExams(self):
        return self.Exams

    def GetLearnTopics(self):
        return self.LearnTopics
    
    def GetPracticeTopics(self):
        return self.PracticeTopics
    
    def GetConsolidateTopics(self):
        return self.ConsolidateTopics

    def GetTopicCount(self):
        return self.TopicCount
    
    def GetDate(self):
        return self.Date 
        
    def SetDate(self, date):
        self.Date = date

    def IsEmpty(self):
        return self.Exams == [] and self.TopicCount == 0

    def __str__(self):
        return self.Date.strftime("%B %d %Y")
    
    def PrintDate(self):
        print(str(self))
        print("-")
        print("Exams: " + str(self.Exams))
        print("ConsolidateTopics: "+ str(self.ConsolidateTopics))
        print("PracticeTopics: "+ str(self.PracticeTopics))
        print("LearnTopics: "+ str(self.LearnTopics))
        
def main():
    CurrentExamSeason = ExamSeason()
    CurrentExamSeason.GetFileFromPC("Exams And Topics.md")
    CurrentExamSeason.ParseStudyData()
    CurrentExamSeason.PopulateStudyTimetable()
    CurrentExamSeason.PrintCalander()
    print("Timetable Made!")
    
if "__main__" == __name__:
    main()
