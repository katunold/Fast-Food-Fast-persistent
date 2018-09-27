DROP DATABASE IF EXISTS "Fast-Food";
CREATE DATABASE "Fast-Food";

CREATE SCHEMA production;

CREATE TABLE production."user" (
    user_id SERIAL NOT NULL PRIMARY KEY,
    user_name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    contact character varying(255) NOT NULL,
    user_type character varying(100) NOT NULL,
    password character varying(255) NOT NULL
);

CREATE SCHEMA test;

CREATE TABLE test."user" (
    user_id SERIAL NOT NULL PRIMARY KEY,
    user_name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    contact character varying(255) NOT NULL,
    user_type character varying(100) NOT NULL,
    password character varying(255) NOT NULL
);


