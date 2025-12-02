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
-- Name: teams; Type: TABLE; Schema: public; Owner: gameserver
--

CREATE TABLE public.teams (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    vpn_connected boolean DEFAULT false NOT NULL,
    vpn_last_connect timestamp with time zone,
    vpn_last_disconnect timestamp with time zone,
    affiliation character varying(128) DEFAULT NULL::character varying,
    logo character varying(64) DEFAULT NULL::character varying,
    website character varying(128) DEFAULT NULL::character varying,
    vpn_connection_count integer DEFAULT 0 NOT NULL,
    vpn2_connected boolean DEFAULT false NOT NULL,
    wg_vulnbox_connected boolean DEFAULT false NOT NULL,
    wg_boxes_connected boolean DEFAULT false NOT NULL
);


ALTER TABLE public.teams OWNER TO gameserver;

--
-- Name: teams_id_seq; Type: SEQUENCE; Schema: public; Owner: gameserver
--

CREATE SEQUENCE public.teams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.teams_id_seq OWNER TO gameserver;

--
-- Name: teams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gameserver
--

ALTER SEQUENCE public.teams_id_seq OWNED BY public.teams.id;


--
-- Name: teams id; Type: DEFAULT; Schema: public; Owner: gameserver
--

ALTER TABLE ONLY public.teams ALTER COLUMN id SET DEFAULT nextval('public.teams_id_seq'::regclass);


--
-- Data for Name: teams; Type: TABLE DATA; Schema: public; Owner: gameserver
--

COPY public.teams (id, name, vpn_connected, vpn_last_connect, vpn_last_disconnect, affiliation, logo, website, vpn_connection_count, vpn2_connected, wg_vulnbox_connected, wg_boxes_connected) FROM stdin;
1	Team 1	t	\N	\N	\N	\N	\N	1	t	t	t
2	Team 2	t	\N	\N	\N	\N	\N	1	t	t	t
3	Team 3	t	\N	\N	\N	\N	\N	1	t	t	t
\.


--
-- Name: teams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gameserver
--

SELECT pg_catalog.setval('public.teams_id_seq', 5, true);


--
-- Name: teams teams_pkey; Type: CONSTRAINT; Schema: public; Owner: gameserver
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

