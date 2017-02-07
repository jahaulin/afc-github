CREATE TABLE user (
    uid INTEGER NOT NULL,
    default_password TEXT,
    password TEXT,
    student_grade INTEGER,
    student_class INTEGER,
    student_number INTEGER,
    student_name TEXT,
    student_tag TEXT,
    parent_name TEXT,
    parent_phone TEXT,
    PRIMARY KEY (uid),
    CONSTRAINT unique_index_student UNIQUE (student_grade, student_class, student_number)
);
CREATE TABLE course (
    cid INTEGER NOT NULL,
    name TEXT,
    description TEXT,
    classroom TEXT,
    price INTEGER,
    teacher TEXT,
    teacher_tag TEXT,
    teacher_phone TEXT,
    grades VARCHAR(10),
    upbound INTEGER,
    datetime TEXT,
    state INTEGER, count INTEGER, lowbound INTEGER,
    PRIMARY KEY (cid)
);
CREATE TABLE history (
    hid INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    timestamp DATETIME,
    message VARCHAR(1024),
    ip VARCHAR(40),
    PRIMARY KEY (hid),
    FOREIGN KEY(user_id) REFERENCES user (uid)
);
CREATE TABLE selection (
    sid INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    priority INTEGER,
    timestamp TIMESTAMP,
    PRIMARY KEY (sid),
    FOREIGN KEY(user_id) REFERENCES user (uid),
    FOREIGN KEY(course_id) REFERENCES course (cid)
);
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL
);
