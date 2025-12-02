--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2 (Debian 17.2-1.pgdg120+1)
-- Dumped by pg_dump version 17.2 (Debian 17.2-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: services; Type: TABLE; Schema: public; Owner: cte2025
--

CREATE TABLE public.services (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    checker_script character varying NOT NULL,
    checker_timeout integer DEFAULT 30 NOT NULL,
    package character varying(32),
    checker_script_dir character varying,
    checker_enabled boolean DEFAULT true NOT NULL,
    checker_subprocess boolean DEFAULT false NOT NULL,
    num_payloads integer DEFAULT 0 NOT NULL,
    flag_ids character varying(128) DEFAULT NULL::character varying,
    flags_per_tick double precision DEFAULT 1 NOT NULL,
    setup_package character varying(32) DEFAULT NULL::character varying,
    checker_route character varying(64) DEFAULT NULL::character varying,
    ports character varying DEFAULT ''::character varying NOT NULL,
    checker_runner character varying DEFAULT ''::character varying NOT NULL,
    runner_config jsonb
);


ALTER TABLE public.services OWNER TO cte2025;

--
-- Name: services_id_seq; Type: SEQUENCE; Schema: public; Owner: cte2025
--

CREATE SEQUENCE public.services_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.services_id_seq OWNER TO cte2025;

--
-- Name: services_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cte2025
--

ALTER SEQUENCE public.services_id_seq OWNED BY public.services.id;


--
-- Name: services id; Type: DEFAULT; Schema: public; Owner: cte2025
--

ALTER TABLE ONLY public.services ALTER COLUMN id SET DEFAULT nextval('public.services_id_seq'::regclass);


--
-- Data for Name: services; Type: TABLE DATA; Schema: public; Owner: cte2025
--

COPY public.services (id, name, checker_script, checker_timeout, package, checker_script_dir, checker_enabled, checker_subprocess, num_payloads, flag_ids, flags_per_tick, setup_package, checker_route, ports, checker_runner, runner_config) FROM stdin;
1	Firewall	 	60	\N	\N	t	f	2	custom,custom	2	\N	\N		eno:EnoCheckerRunner	{"url": "http://10.69.251.16:8100"}
2	Gitter	 	60	\N	\N	t	f	2	custom,custom	2	\N	\N		eno:EnoCheckerRunner	{"url": "http://10.69.251.17:8200"}
3	Pillarboxd	 	60	\N	\N	t	f	3	custom,custom,custom	3	\N	\N		eno:EnoCheckerRunner	{"url": "http://10.69.251.18:8300"}
5	Heavensent	 	60	\N	\N	t	f	2	custom,custom	2	\N	\N		eno:EnoCheckerRunner	{"url": "http://10.69.251.19:8500"}
4	Jitterish	 	60	\N	\N	t	f	3	custom,custom,custom	3	\N	\N		eno:EnoCheckerRunner	{"url": "http://10.69.251.20:8400"}
\.


--
-- Name: services_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cte2025
--

SELECT pg_catalog.setval('public.services_id_seq', 5, true);


--
-- Name: services services_pkey; Type: CONSTRAINT; Schema: public; Owner: cte2025
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

