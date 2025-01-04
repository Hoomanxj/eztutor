CREATE TABLE teacher (
    id INTEGER AUTO_INCREMENT NOT NULL,
    name VARCHAR(50) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM("male", "female", "none-binary"),
    email VARCHAR(50) NOT NULL,
    cell VARCHAR(20),
    country VARCHAR (30),
    address TEXT,
    education_level ENUM("college", "bachelor's", "master's", "doctoral") NOT NULL,
    field_of_study VARCHAR(150) NOT NULL,
    native_language VARCHAR(50) NOT NULL,
    teaching_language VARCHAR(50) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE student (
    id INTEGER AUTO_INCREMENT NOT NULL,
    teacher_id INTEGER NOT NULL,
    name VARCHAR(50) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM("male", "female", "none-binary"),
    email VARCHAR(50) NOT NULL,
    cell VARCHAR(20),
    country VARCHAR(30),
    address TEXT,
    education_level ENUM("college", "bachelor's", "masters's", "doctroal") NOT NULL,
    field_of_study VARCHAR(150) NOT NULL,
    native_language VARCHAR(50) NOT NULL,
    learning_language VARCHAR(50) NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(teacher_id) REFERENCES teacher(id)
);

CREATE TABLE course (
    id INTEGER AUTO_INCREMENT NOT NULL,
    teacher_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    start_date DATETIME NOT NULL,
    end_date DATETIME,
    number_of_session INTEGER,
    session_duration SMALLINT NOT NULL,
    session_per_week SMALLINT NOT NULL,
    number_of_student SMALLINT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(teacher_id) REFERENCES teacher(id)
);

CREATE TABLE session (
    id INTEGER AUTO_INCREMENT NOT NULL,
    teacher_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    date DATETIME NOT NULL,
    duration SMALLINT NOT NULL,
    note TEXT NOT NULL,
    attendance BOOL NOT NULL,
    completed BOOL NOT NULL ,
    PRIMARY KEY(id),
    FOREIGN KEY(teacher_id) REFERENCES teacher(id),
    FOREIGN KEY(student_id) REFERENCES student(id),
    FOREIGN KEY(course_id) REFERENCES course(id)
);

CREATE TABLE assignment (
    id INTEGER AUTO_INCREMENT NOT NULL,
    teacher_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    start_date DATETIME NOT NULL,
    submission_date DATETIME,
    end_date DATETIME,
    PRIMARY KEY(id),
    FOREIGN KEY(teacher_id) REFERENCES teacher(id),
    FOREIGN KEY(student_id) REFERENCES student(id)
);

CREATE TABLE feedback (
    id INTEGER AUTO_INCREMENT NOT NULL,
    teacher_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    session_id INTEGER NOT NULL,
    assignment_id INTEGER NOT NULL,
    note TEXT NOT NULL,
    date DATETIME NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(teacher_id) REFERENCES teacher(id),
    FOREIGN KEY(student_id) REFERENCES student(id),
    FOREIGN KEY(session_id) REFERENCES session(id),
    FOREIGN KEY(assignment_id) REFERENCES assignment(id)
);

CREATE TABLE progress (
    id INTEGER AUTO_INCREMENT NOT NULL,
    teacher_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    note TEXT NOT NULL,
    date DATETIME,
    PRIMARY KEY(id),
    FOREIGN KEY(teacher_id) REFERENCES teacher(id),
    FOREIGN KEY(student_id) REFERENCES student(id),
    FOREIGN KEY(course_id) REFERENCES course(id)
);

CREATE TABLE tag (
    id INTEGER AUTO_INCREMENT NOT NULL,
    tag_category_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(tag_category_id) REFERENCES tag_category(id)
);

CREATE TABLE tag_category (
    id INTEGER AUTO_INCREMENT NOT NULL,
    name ENUM("speaking", "listening", "writing", "reading") NOT NULL,
    description TEXT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE assignment_category (
    id INTEGER AUTO_INCREMENT NOT NULL,
    name ENUM("speaking", "listening", "writing", "reading") NOT NULL,
    description TEXT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE assignment_tag_score (
    id INTEGER AUTO_INCREMENT NOT NULL,
    assignment_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    score SMALLINT NOT NULL,
    note TEXT,
    date DATETIME,
    PRIMARY KEY(id),
    FOREIGN KEY(assignment_id) REFERENCES assignment(id),
    FOREIGN KEY(tag_id) REFERENCES tag(id)
);

CREATE TABLE enrollment (
    id INTEGER AUTO_INCREMENT NOT NULL,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(student_id) REFERENCES student(id),
    FOREIGN KEY(course_id) REFERENCES course(id)
);