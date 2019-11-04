--
-- PostgreSQL database dump
--

-- Dumped from database version 12.0
-- Dumped by pg_dump version 12.0

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

--
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: listdir; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.listdir (
    id integer NOT NULL,
    parentpath character varying,
    filename character varying,
    size character varying,
    md5 character varying,
    sha1 character varying
);


ALTER TABLE public.listdir OWNER TO postgres;

--
-- Name: listdir_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.listdir_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.listdir_id_seq OWNER TO postgres;

--
-- Name: listdir_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.listdir_id_seq OWNED BY public.listdir.id;


--
-- Name: listdir id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.listdir ALTER COLUMN id SET DEFAULT nextval('public.listdir_id_seq'::regclass);


--
-- Name: listdir listdir_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.listdir
    ADD CONSTRAINT listdir_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

