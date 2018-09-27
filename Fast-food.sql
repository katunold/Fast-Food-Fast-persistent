--
-- PostgreSQL database dump
--

-- Dumped from database version 10.4
-- Dumped by pg_dump version 10.4

-- Started on 2018-09-26 21:18:25 EAT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2913 (class 1262 OID 29266)
-- Name: Fast-Food; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "Fast-Food" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';


ALTER DATABASE "Fast-Food" OWNER TO postgres;

\connect -reuse-previous=on "dbname='Fast-Food'"

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 7 (class 2615 OID 29267)
-- Name: production; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA production;


ALTER SCHEMA production OWNER TO postgres;

--
-- TOC entry 9 (class 2615 OID 29268)
-- Name: test; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA test;


ALTER SCHEMA test OWNER TO postgres;

--
-- TOC entry 1 (class 3079 OID 12964)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2915 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 203 (class 1259 OID 29385)
-- Name: menu_items; Type: TABLE; Schema: production; Owner: postgres
--

CREATE TABLE production.menu_items (
    item_id integer NOT NULL,
    item_name character varying(255) NOT NULL,
    user_id integer NOT NULL,
    item_status character varying(100) NOT NULL
);


ALTER TABLE production.menu_items OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 29383)
-- Name: menu_items_item_id_seq; Type: SEQUENCE; Schema: production; Owner: postgres
--

CREATE SEQUENCE production.menu_items_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE production.menu_items_item_id_seq OWNER TO postgres;

--
-- TOC entry 2916 (class 0 OID 0)
-- Dependencies: 202
-- Name: menu_items_item_id_seq; Type: SEQUENCE OWNED BY; Schema: production; Owner: postgres
--

ALTER SEQUENCE production.menu_items_item_id_seq OWNED BY production.menu_items.item_id;


--
-- TOC entry 207 (class 1259 OID 29416)
-- Name: orders; Type: TABLE; Schema: production; Owner: postgres
--

CREATE TABLE production.orders (
    order_id integer NOT NULL,
    user_id integer NOT NULL,
    order_item character varying(255) NOT NULL,
    order_date timestamp(6) without time zone NOT NULL,
    order_status character varying(100) NOT NULL,
    item_id integer NOT NULL
);


ALTER TABLE production.orders OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 29414)
-- Name: orders_order_id_seq; Type: SEQUENCE; Schema: production; Owner: postgres
--

CREATE SEQUENCE production.orders_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE production.orders_order_id_seq OWNER TO postgres;

--
-- TOC entry 2917 (class 0 OID 0)
-- Dependencies: 206
-- Name: orders_order_id_seq; Type: SEQUENCE OWNED BY; Schema: production; Owner: postgres
--

ALTER SEQUENCE production.orders_order_id_seq OWNED BY production.orders.order_id;


--
-- TOC entry 199 (class 1259 OID 29271)
-- Name: user; Type: TABLE; Schema: production; Owner: postgres
--

CREATE TABLE production."user" (
    user_id integer NOT NULL,
    user_name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    contact character varying(255) NOT NULL,
    user_type character varying(100) NOT NULL,
    password character varying(255) NOT NULL
);


ALTER TABLE production."user" OWNER TO postgres;

--
-- TOC entry 198 (class 1259 OID 29269)
-- Name: user_user_id_seq; Type: SEQUENCE; Schema: production; Owner: postgres
--

CREATE SEQUENCE production.user_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE production.user_user_id_seq OWNER TO postgres;

--
-- TOC entry 2918 (class 0 OID 0)
-- Dependencies: 198
-- Name: user_user_id_seq; Type: SEQUENCE OWNED BY; Schema: production; Owner: postgres
--

ALTER SEQUENCE production.user_user_id_seq OWNED BY production."user".user_id;


--
-- TOC entry 205 (class 1259 OID 29401)
-- Name: menu_items; Type: TABLE; Schema: test; Owner: postgres
--

CREATE TABLE test.menu_items (
    item_id integer NOT NULL,
    item_name character varying(255) NOT NULL,
    user_id integer NOT NULL,
    item_status character varying(100) NOT NULL
);


ALTER TABLE test.menu_items OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 29399)
-- Name: menu_items_item_id_seq; Type: SEQUENCE; Schema: test; Owner: postgres
--

CREATE SEQUENCE test.menu_items_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE test.menu_items_item_id_seq OWNER TO postgres;

--
-- TOC entry 2919 (class 0 OID 0)
-- Dependencies: 204
-- Name: menu_items_item_id_seq; Type: SEQUENCE OWNED BY; Schema: test; Owner: postgres
--

ALTER SEQUENCE test.menu_items_item_id_seq OWNED BY test.menu_items.item_id;


--
-- TOC entry 209 (class 1259 OID 29434)
-- Name: orders; Type: TABLE; Schema: test; Owner: postgres
--

CREATE TABLE test.orders (
    order_id integer NOT NULL,
    user_id integer NOT NULL,
    order_item character varying(255) NOT NULL,
    order_date timestamp(6) without time zone NOT NULL,
    order_status character varying(100) NOT NULL,
    item_id integer NOT NULL
);


ALTER TABLE test.orders OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 29432)
-- Name: orders_order_id_seq; Type: SEQUENCE; Schema: test; Owner: postgres
--

CREATE SEQUENCE test.orders_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE test.orders_order_id_seq OWNER TO postgres;

--
-- TOC entry 2920 (class 0 OID 0)
-- Dependencies: 208
-- Name: orders_order_id_seq; Type: SEQUENCE OWNED BY; Schema: test; Owner: postgres
--

ALTER SEQUENCE test.orders_order_id_seq OWNED BY test.orders.order_id;


--
-- TOC entry 201 (class 1259 OID 29284)
-- Name: user; Type: TABLE; Schema: test; Owner: postgres
--

CREATE TABLE test."user" (
    user_id integer NOT NULL,
    user_name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    contact character varying(255) NOT NULL,
    user_type character varying(100) NOT NULL,
    password character varying(255) NOT NULL
);


ALTER TABLE test."user" OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 29282)
-- Name: user_user_id_seq; Type: SEQUENCE; Schema: test; Owner: postgres
--

CREATE SEQUENCE test.user_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE test.user_user_id_seq OWNER TO postgres;

--
-- TOC entry 2921 (class 0 OID 0)
-- Dependencies: 200
-- Name: user_user_id_seq; Type: SEQUENCE OWNED BY; Schema: test; Owner: postgres
--

ALTER SEQUENCE test.user_user_id_seq OWNED BY test."user".user_id;


--
-- TOC entry 2745 (class 2604 OID 29388)
-- Name: menu_items item_id; Type: DEFAULT; Schema: production; Owner: postgres
--

ALTER TABLE ONLY production.menu_items ALTER COLUMN item_id SET DEFAULT nextval('production.menu_items_item_id_seq'::regclass);


--
-- TOC entry 2747 (class 2604 OID 29419)
-- Name: orders order_id; Type: DEFAULT; Schema: production; Owner: postgres
--

ALTER TABLE ONLY production.orders ALTER COLUMN order_id SET DEFAULT nextval('production.orders_order_id_seq'::regclass);


--
-- TOC entry 2743 (class 2604 OID 29274)
-- Name: user user_id; Type: DEFAULT; Schema: production; Owner: postgres
--

ALTER TABLE ONLY production."user" ALTER COLUMN user_id SET DEFAULT nextval('production.user_user_id_seq'::regclass);


--
-- TOC entry 2746 (class 2604 OID 29404)
-- Name: menu_items item_id; Type: DEFAULT; Schema: test; Owner: postgres
--

ALTER TABLE ONLY test.menu_items ALTER COLUMN item_id SET DEFAULT nextval('test.menu_items_item_id_seq'::regclass);


--
-- TOC entry 2748 (class 2604 OID 29437)
-- Name: orders order_id; Type: DEFAULT; Schema: test; Owner: postgres
--

ALTER TABLE ONLY test.orders ALTER COLUMN order_id SET DEFAULT nextval('test.orders_order_id_seq'::regclass);


--
-- TOC entry 2744 (class 2604 OID 29287)
-- Name: user user_id; Type: DEFAULT; Schema: test; Owner: postgres
--

ALTER TABLE ONLY test."user" ALTER COLUMN user_id SET DEFAULT nextval('test.user_user_id_seq'::regclass);


--
-- TOC entry 2901 (class 0 OID 29385)
-- Dependencies: 203
-- Data for Name: menu_items; Type: TABLE DATA; Schema: production; Owner: postgres
--

COPY production.menu_items (item_id, item_name, user_id, item_status) FROM stdin;
\.


--
-- TOC entry 2905 (class 0 OID 29416)
-- Dependencies: 207
-- Data for Name: orders; Type: TABLE DATA; Schema: production; Owner: postgres
--

COPY production.orders (order_id, user_id, order_item, order_date, order_status, item_id) FROM stdin;
\.


--
-- TOC entry 2897 (class 0 OID 29271)
-- Dependencies: 199
-- Data for Name: user; Type: TABLE DATA; Schema: production; Owner: postgres
--

COPY production."user" (user_id, user_name, email, contact, user_type, password) FROM stdin;
\.


--
-- TOC entry 2903 (class 0 OID 29401)
-- Dependencies: 205
-- Data for Name: menu_items; Type: TABLE DATA; Schema: test; Owner: postgres
--

COPY test.menu_items (item_id, item_name, user_id, item_status) FROM stdin;
\.


--
-- TOC entry 2907 (class 0 OID 29434)
-- Dependencies: 209
-- Data for Name: orders; Type: TABLE DATA; Schema: test; Owner: postgres
--

COPY test.orders (order_id, user_id, order_item, order_date, order_status, item_id) FROM stdin;
\.


--
-- TOC entry 2899 (class 0 OID 29284)
-- Dependencies: 201
-- Data for Name: user; Type: TABLE DATA; Schema: test; Owner: postgres
--

COPY test."user" (user_id, user_name, email, contact, user_type, password) FROM stdin;
\.


--
-- TOC entry 2922 (class 0 OID 0)
-- Dependencies: 202
-- Name: menu_items_item_id_seq; Type: SEQUENCE SET; Schema: production; Owner: postgres
--

SELECT pg_catalog.setval('production.menu_items_item_id_seq', 1, false);


--
-- TOC entry 2923 (class 0 OID 0)
-- Dependencies: 206
-- Name: orders_order_id_seq; Type: SEQUENCE SET; Schema: production; Owner: postgres
--

SELECT pg_catalog.setval('production.orders_order_id_seq', 1, false);


--
-- TOC entry 2924 (class 0 OID 0)
-- Dependencies: 198
-- Name: user_user_id_seq; Type: SEQUENCE SET; Schema: production; Owner: postgres
--

SELECT pg_catalog.setval('production.user_user_id_seq', 1, false);


--
-- TOC entry 2925 (class 0 OID 0)
-- Dependencies: 204
-- Name: menu_items_item_id_seq; Type: SEQUENCE SET; Schema: test; Owner: postgres
--

SELECT pg_catalog.setval('test.menu_items_item_id_seq', 1, false);


--
-- TOC entry 2926 (class 0 OID 0)
-- Dependencies: 208
-- Name: orders_order_id_seq; Type: SEQUENCE SET; Schema: test; Owner: postgres
--

SELECT pg_catalog.setval('test.orders_order_id_seq', 1, false);


--
-- TOC entry 2927 (class 0 OID 0)
-- Dependencies: 200
-- Name: user_user_id_seq; Type: SEQUENCE SET; Schema: test; Owner: postgres
--

SELECT pg_catalog.setval('test.user_user_id_seq', 1, false);


--
-- TOC entry 2758 (class 2606 OID 29392)
-- Name: menu_items menu_items_item_name_key; Type: CONSTRAINT; Schema: production; Owner: postgres
--

ALTER TABLE ONLY production.menu_items
    ADD CONSTRAINT menu_items_item_name_key UNIQUE (item_name);


--
-- TOC entry 2760 (class 2606 OID 29390)
-- Name: menu_items menu_items_pkey; Type: CONSTRAINT; Schema: production; Owner: postgres
--

ALTER TABLE ONLY production.menu_items
    ADD CONSTRAINT menu_items_pkey PRIMARY KEY (item_id);


--
-- TOC entry 2766 (class 2606 OID 29421)
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: production; Owner: postgres
--

ALTER TABLE ONLY production.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);


--
-- TOC entry 2750 (class 2606 OID 29279)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: production; Owner: postgres
--

ALTER TABLE ONLY production."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (user_id);


--
-- TOC entry 2752 (class 2606 OID 29281)
-- Name: user user_user_name_email_key; Type: CONSTRAINT; Schema: production; Owner: postgres
--

ALTER TABLE ONLY production."user"
    ADD CONSTRAINT user_user_name_email_key UNIQUE (user_name, email);


--
-- TOC entry 2762 (class 2606 OID 29408)
-- Name: menu_items menu_items_item_name_key; Type: CONSTRAINT; Schema: test; Owner: postgres
--

ALTER TABLE ONLY test.menu_items
    ADD CONSTRAINT menu_items_item_name_key UNIQUE (item_name);


--
-- TOC entry 2764 (class 2606 OID 29406)
-- Name: menu_items menu_items_pkey; Type: CONSTRAINT; Schema: test; Owner: postgres
--

ALTER TABLE ONLY test.menu_items
    ADD CONSTRAINT menu_items_pkey PRIMARY KEY (item_id);


--
-- TOC entry 2768 (class 2606 OID 29439)
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: test; Owner: postgres
--

ALTER TABLE ONLY test.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);


--
-- TOC entry 2754 (class 2606 OID 29292)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: test; Owner: postgres
--

ALTER TABLE ONLY test."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (user_id);


--
-- TOC entry 2756 (class 2606 OID 29294)
-- Name: user user_user_name_email_key; Type: CONSTRAINT; Schema: test; Owner: postgres
--

ALTER TABLE ONLY test."user"
    ADD CONSTRAINT user_user_name_email_key UNIQUE (user_name, email);


--
-- TOC entry 2769 (class 2606 OID 29393)
-- Name: menu_items menu_items_user_id_fkey; Type: FK CONSTRAINT; Schema: production; Owner: postgres
--

ALTER TABLE ONLY production.menu_items
    ADD CONSTRAINT menu_items_user_id_fkey FOREIGN KEY (user_id) REFERENCES production."user"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2772 (class 2606 OID 29427)
-- Name: orders orders_item_id_fkey; Type: FK CONSTRAINT; Schema: production; Owner: postgres
--

ALTER TABLE ONLY production.orders
    ADD CONSTRAINT orders_item_id_fkey FOREIGN KEY (item_id) REFERENCES production.menu_items(item_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2771 (class 2606 OID 29422)
-- Name: orders orders_user_id_fkey; Type: FK CONSTRAINT; Schema: production; Owner: postgres
--

ALTER TABLE ONLY production.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES production."user"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2770 (class 2606 OID 29409)
-- Name: menu_items menu_items_user_id_fkey; Type: FK CONSTRAINT; Schema: test; Owner: postgres
--

ALTER TABLE ONLY test.menu_items
    ADD CONSTRAINT menu_items_user_id_fkey FOREIGN KEY (user_id) REFERENCES test."user"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2774 (class 2606 OID 29445)
-- Name: orders orders_item_id_fkey; Type: FK CONSTRAINT; Schema: test; Owner: postgres
--

ALTER TABLE ONLY test.orders
    ADD CONSTRAINT orders_item_id_fkey FOREIGN KEY (item_id) REFERENCES test.menu_items(item_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2773 (class 2606 OID 29440)
-- Name: orders orders_user_id_fkey; Type: FK CONSTRAINT; Schema: test; Owner: postgres
--

ALTER TABLE ONLY test.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES test."user"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;


-- Completed on 2018-09-26 21:18:26 EAT

--
-- PostgreSQL database dump complete
--


