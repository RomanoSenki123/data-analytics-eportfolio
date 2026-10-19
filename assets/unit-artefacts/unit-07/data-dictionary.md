# Unit 7 data dictionary

| Table | Column | Key or constraint | Meaning |
|---|---|---|---|
| Student | StudentNumber | Primary key | Source student identifier |
| Student | StudentName | Required | Student's full name |
| Student | ExamScore | 0–100 | Student-level score supplied in the source |
| Student | Support | Yes/No | Whether support is recorded |
| Student | DateOfBirth | Required | ISO-formatted date of birth |
| Teacher | TeacherID | Primary key | Generated teacher identifier |
| Teacher | TeacherName | Unique | Teacher's display name |
| Course | CourseID | Primary key | Generated course identifier |
| Course | CourseName | Unique | Course name |
| Course | TeacherID | Foreign key | Teacher responsible for the course |
| ExamBoard | ExamBoardID | Primary key | Generated board identifier |
| ExamBoard | ExamBoardName | Unique | Exam board name |
| Enrolment | StudentNumber | Composite primary and foreign key | Enrolled student |
| Enrolment | CourseID | Composite primary and foreign key | Enrolled course |
| Enrolment | ExamBoardID | Foreign key | Board used for that student-course enrolment |
