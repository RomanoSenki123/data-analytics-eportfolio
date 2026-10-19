PRAGMA foreign_keys = ON;

CREATE TABLE Student (
    StudentNumber INTEGER PRIMARY KEY,
    StudentName TEXT NOT NULL,
    ExamScore INTEGER NOT NULL CHECK (ExamScore BETWEEN 0 AND 100),
    Support TEXT NOT NULL CHECK (Support IN ('Yes', 'No')),
    DateOfBirth TEXT NOT NULL
);

CREATE TABLE Teacher (
    TeacherID TEXT PRIMARY KEY,
    TeacherName TEXT NOT NULL UNIQUE
);

CREATE TABLE ExamBoard (
    ExamBoardID TEXT PRIMARY KEY,
    ExamBoardName TEXT NOT NULL UNIQUE
);

CREATE TABLE Course (
    CourseID TEXT PRIMARY KEY,
    CourseName TEXT NOT NULL UNIQUE,
    TeacherID TEXT NOT NULL,
    FOREIGN KEY (TeacherID) REFERENCES Teacher (TeacherID)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE Enrolment (
    StudentNumber INTEGER NOT NULL,
    CourseID TEXT NOT NULL,
    ExamBoardID TEXT NOT NULL,
    PRIMARY KEY (StudentNumber, CourseID),
    FOREIGN KEY (StudentNumber) REFERENCES Student (StudentNumber)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (CourseID) REFERENCES Course (CourseID)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (ExamBoardID) REFERENCES ExamBoard (ExamBoardID)
        ON UPDATE CASCADE ON DELETE RESTRICT
);
