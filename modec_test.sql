--
-- PostgreSQL database dump
--

-- Dumped from database version 13.0
-- Dumped by pg_dump version 13.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: equipments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.equipments (
    id integer NOT NULL,
    name character varying NOT NULL,
    code character varying NOT NULL,
    location character varying NOT NULL,
    activation_status boolean NOT NULL,
    vessel_code character varying NOT NULL
);


ALTER TABLE public.equipments OWNER TO postgres;

--
-- Name: equipments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.equipments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.equipments_id_seq OWNER TO postgres;

--
-- Name: equipments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.equipments_id_seq OWNED BY public.equipments.id;


--
-- Name: vessels; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vessels (
    id integer NOT NULL,
    code text NOT NULL
);


ALTER TABLE public.vessels OWNER TO postgres;

--
-- Name: vessels_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.vessels_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.vessels_id_seq OWNER TO postgres;

--
-- Name: vessels_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.vessels_id_seq OWNED BY public.vessels.id;


--
-- Name: equipments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipments ALTER COLUMN id SET DEFAULT nextval('public.equipments_id_seq'::regclass);


--
-- Name: vessels id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vessels ALTER COLUMN id SET DEFAULT nextval('public.vessels_id_seq'::regclass);


--
-- Data for Name: equipments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.equipments (id, name, code, location, activation_status, vessel_code) FROM stdin;
3	compressor	5310B9D9	Brazil	t	MV102
4	compressor	5310B9D10	Brazil	t	MV102
5	compressor	5310B9D11	Brazil	t	MV102
1	compressor	5310B9D7	Brazil	t	MV102
2	compressor	5310B9D8	Brazil	t	MV102
\.


--
-- Data for Name: vessels; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vessels (id, code) FROM stdin;
1	MV102
4	MV103
7	MV104
10	MV105
11	MV106
12	MV107
\.


--
-- Name: equipments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.equipments_id_seq', 5, true);


--
-- Name: vessels_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.vessels_id_seq', 16, true);


--
-- Name: equipments equipments_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipments
    ADD CONSTRAINT equipments_code_key UNIQUE (code);


--
-- Name: equipments equipments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipments
    ADD CONSTRAINT equipments_pkey PRIMARY KEY (id);


--
-- Name: vessels vessels_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vessels
    ADD CONSTRAINT vessels_code_key UNIQUE (code);


--
-- Name: equipments equipments_vessel_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipments
    ADD CONSTRAINT equipments_vessel_code_fkey FOREIGN KEY (vessel_code) REFERENCES public.vessels(code);


--
-- PostgreSQL database dump complete
--

