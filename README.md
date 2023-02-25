# Revision4U

## How to use

1. Download the repository
2. Open the "Exams And Topics[TEMPLATE].md" file and fill in the details of your exams
3. Run the main.py file
4. Open the "Study Plan.md" file and see your study plan

## How it works

The code reads the "Exams And Topics.md" file and splits it into a list of subjects, each subject is a list of papers, each paper is a list of topics.

The code then creates a list of days between the start and end of the exam period.

The code then creates a dictionary of days, each day is a dictionary of session types, each session type is a list of topics.

The code then loops through each subject, each paper and each topic.

The code then finds the index of the exam date in the list of days.

The code then finds the number of spaces between the exam date and the start of the exam period.

The code then loops through each topic in reverse order.

The code then loops through each session type in reverse order.

The code then loops through each day in reverse order.

The code then adds the topic to the session type on the day if there are less than 3 topics in the session type.

The code then adds the number of spaces to the day if the session type is not "Learn".

The code then loops through each day in the dictionary of days.

The code then loops through each session type in the dictionary of session types.

The code then loops through each topic in the list of topics.

The code then adds the day, session type and topic to the plan if the list of topics is not empty.

The code then writes the plan to the "Study Plan.md" file.