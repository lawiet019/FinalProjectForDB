DROP DATABASE IF EXISTS itws6960_project;
CREATE DATABASE itws6960_project;

USE itws6960_project;
DROP TABLE IF EXISTS wifi;
DROP TABLE IF EXISTS restuarants;
DROP TABLE IF EXISTS violations;
DROP TABLE IF EXISTS landmarks;

CREATE TABLE wifi {
    longitude float(10),
    latitude float(10),
    wifiID varchar(50),
    address varchar(255),
    accessPointName varchar(255),
    wifiType varchar(255)
};

CREATE TABLE restuarants {
    CAMIS varchar(25),
    longitude float(10),
    latitude float(10),
    restuarantName varchar(255),
    street varchar(255),
    zipcode int,
    phone varchar(20) -- phone numebr char or int??

};

CREATE TABLE violations {
    CAMIS varchar(25),
    InspectionDate timestamp,
    violationCodes char(3),
    violationDescription varchar(255),
    grade char(1),
    score int
};

CREATE TABLE landmarks {
    objectID int,
    landmarkName varchar(255),
    centerLogitude float(10),
    centerLatitude float (10),
    address varchar(255),
    additionalInfoURL varchar(255) -- can be stored this way because database gives bit.ly that are all under 255 characters
};

CREATE TABLE subway {
    longitude float(10),
    latitude float(10),
    name varchar(255),
    lines varchar(25)
};
