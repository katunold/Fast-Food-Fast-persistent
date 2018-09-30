DROP DATABASE IF EXISTS "Fast-Food";
CREATE DATABASE "Fast-Food";
\connect "Fast-Food"

DROP SCHEMA IF EXISTS production CASCADE;

CREATE SCHEMA production;

CREATE TABLE production."user" (
    user_id SERIAL NOT NULL PRIMARY KEY,
    user_name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    contact character varying(255) NOT NULL,
    user_type character varying(100) NOT NULL,
    password character varying(255) NOT NULL
);


CREATE TABLE production."menu_items" (
    item_id SERIAL NOT NULL,
    item_name character varying(255) NOT NULL,
    user_id integer NOT NULL REFERENCES production."user"(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
    item_status character varying(100) NOT NULL
);

CREATE TABLE production."orders" (
    order_id SERIAL NOT NULL PRIMARY KEY,
    user_id integer NOT NULL NOT NULL REFERENCES production."user"(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
    order_item character varying(255) NOT NULL,
    special_notes text NOT NULL,
    order_date timestamp(6) without time zone NOT NULL,
    item_id integer NOT NULL REFERENCES production."menu_items"(item_id) ON UPDATE CASCADE ON DELETE CASCADE,
    order_status character varying(100) NOT NULL
);

CREATE TABLE production."blacklist_token" (
    token_id SERIAL NOT NULL PRIMARY KEY,
    token character varying(500) NOT NULL,
    blacklisted_on timestamp(6) without time zone NOT NULL
);

DROP SCHEMA IF EXISTS test CASCADE;

CREATE SCHEMA test;

CREATE TABLE test."user" (
    user_id SERIAL NOT NULL PRIMARY KEY,
    user_name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    contact character varying(255) NOT NULL,
    user_type character varying(100) NOT NULL,
    password character varying(255) NOT NULL
);

CREATE TABLE test."menu_items" (
    item_id SERIAL NOT NULL,
    item_name character varying(255) NOT NULL,
    user_id integer NOT NULL REFERENCES test."user"(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
    item_status character varying(100) NOT NULL
);

CREATE TABLE test."orders" (
    order_id SERIAL NOT NULL PRIMARY KEY,
    user_id integer NOT NULL REFERENCES test."user"(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
    order_item character varying(255) NOT NULL,
    special_notes text NOT NULL,
    order_date timestamp(6) without time zone NOT NULL,
    item_id integer NOT NULL REFERENCES test."menu_items"(item_id) ON UPDATE CASCADE ON DELETE CASCADE,
    order_status character varying(100) NOT NULL
);

CREATE TABLE test."blacklist_token" (
    token_id SERIAL NOT NULL PRIMARY KEY,
    token character varying(500) NOT NULL,
    blacklisted_on timestamp(6) without time zone NOT NULL
);


