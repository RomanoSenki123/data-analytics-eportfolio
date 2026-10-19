# Unit 7 normalisation notes

## Source assumption

The source supplies one exam score per student while each student has several courses. The score is therefore treated as a student-level attribute. If it instead represents a course assessment, `ExamScore` should move to `Enrolment` and be stored once for each student-course pair.

## Functional dependencies used

- `StudentNumber -> StudentName, ExamScore, Support, DateOfBirth`
- `CourseName -> TeacherName` in the supplied data
- `(StudentNumber, CourseName) -> ExamBoard`

## Normalisation decisions

1. **First normal form:** the repeating course, board and teacher groups were expanded to one row per student-course combination. Values are atomic and the candidate key is `(StudentNumber, CourseName)`.
2. **Second normal form:** attributes depending only on `StudentNumber` moved to `Student`; teacher assignment moved to `Course`; and the student-course relationship retained the board selected for that student.
3. **Third normal form:** the 2NF relations contained no remaining evidenced transitive dependencies. The physical 3NF database uses identifiers for `Teacher`, `Course` and `ExamBoard`, with `Enrolment` linking those entities and enforcing referential integrity.

`Maths` is associated with both AQA and EdExcel in the source. For that reason, exam board is stored on `Enrolment` rather than assumed to depend on course name alone.
