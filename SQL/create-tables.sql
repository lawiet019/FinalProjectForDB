DROP TABLE IF EXISTS inspections;
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS landmarks;
DROP TABLE IF EXISTS restuarants;
DROP TABLE IF EXISTS subway;
DROP TABLE IF EXISTS violations;
DROP TABLE IF EXISTS wifi;

CREATE TABLE inspections (
    CAMIS varchar(25),
    InspectionDate timestamp,
    ViolationCode VARCHAR(10),
    score int
);

CREATE TABLE grades (
    CAMIS VARCHAR(25),
    GradeDate TIMESTAMP,
    Grade CHAR(1)
);

CREATE TABLE landmarks (
    objectID int,
    landmarkName varchar(255),
    centerLogitude float(10),
    centerLatitude float (10),
    neighborhood varchar(255),
    address varchar(255),
    additionalInfoURL varchar(255) -- can be stored this way because database gives bit.ly that are all under 255 characters
);

CREATE TABLE restuarants (
    CAMIS varchar(25),
    longitude float(10),
    latitude float(10),
    restuarantName varchar(255),
    cuisineType VARCHAR(255),
    street varchar(255),
    zipcode varchar(6),
    neighborhood varchar(255),
    phone varchar(10) -- phone numebr char or int??
);

CREATE TABLE violations (
    violationID varchar(25),
    violationDescription varchar(500)
);