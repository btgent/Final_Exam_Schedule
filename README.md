# Final_Exam_Schedule

Purpose: 
  Optimizing Spring 2020 final timetables for UW students in order to schedule final exams more efficiently (using Gurobi optimizer).

Program Type:
   Using integer programming on this project. Identifying this as a min-cost flow problem. Goal is to find a feasible solution.

 Constraints:
   1. Exams cannot have the same time slot with the same student’s other exam.
   2. Exams can only happen between 9:00 am to 8:30 pm. 
   3. Exams have either 150-min duration.
   4. There are no back-to-back exams for any student. 
   5. Exams can only start at every full and half clock.
   6. Exams happens between Aug 1st to Aug 20th
   7. There is one and only one final for each course.
   8. There are no exams during the weekends.
   9. Each student takes 1-6 courses for Term Spring 2020.
   10. All exams take place at PAC.
   11. PAC can hold a maximum of 11 different exams at the same time.
