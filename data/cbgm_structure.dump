--
-- PostgreSQL database dump
--

-- Dumped from database version 12.7 (Debian 12.7-1.pgdg100+1)
-- Dumped by pg_dump version 12.7 (Debian 12.7-1.pgdg100+1)

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
-- Name: ntg; Type: SCHEMA; Schema: -; Owner: ntg
--

CREATE SCHEMA ntg;


ALTER SCHEMA ntg OWNER TO ntg;

--
-- Name: adr2bk_id(integer); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.adr2bk_id(adr integer) RETURNS integer
    LANGUAGE sql IMMUTABLE
    AS $$ SELECT (adr / 10000000) $$;


ALTER FUNCTION ntg.adr2bk_id(adr integer) OWNER TO ntg;

--
-- Name: adr2chapter(integer); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.adr2chapter(adr integer) RETURNS integer
    LANGUAGE sql IMMUTABLE
    AS $$ SELECT ((adr / 100000) % 100) $$;


ALTER FUNCTION ntg.adr2chapter(adr integer) OWNER TO ntg;

--
-- Name: adr2verse(integer); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.adr2verse(adr integer) RETURNS integer
    LANGUAGE sql IMMUTABLE
    AS $$ SELECT ((adr / 1000) % 100) $$;


ALTER FUNCTION ntg.adr2verse(adr integer) OWNER TO ntg;

--
-- Name: adr2word(integer); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.adr2word(adr integer) RETURNS integer
    LANGUAGE sql IMMUTABLE
    AS $$ SELECT (adr % 1000) $$;


ALTER FUNCTION ntg.adr2word(adr integer) OWNER TO ntg;

--
-- Name: apparatus_cliques_view_trigger_f(); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.apparatus_cliques_view_trigger_f() RETURNS trigger
    LANGUAGE plpgsql
    AS $$ BEGIN
      IF TG_OP = 'INSERT' THEN
        INSERT INTO apparatus  (pass_id, ms_id, labez, lesart, cbgm, origin)
               VALUES (NEW.pass_id, NEW.ms_id, NEW.labez, NEW.lesart, NEW.cbgm, NEW.origin);
        INSERT INTO ms_cliques (pass_id, ms_id, labez, clique)
               VALUES (NEW.pass_id, NEW.ms_id, NEW.labez, NEW.clique);
      ELSIF TG_OP = 'UPDATE' THEN
        SET CONSTRAINTS ALL DEFERRED;
        UPDATE apparatus
        SET pass_id = NEW.pass_id, ms_id = NEW.ms_id, labez = NEW.labez, lesart = NEW.lesart, cbgm = NEW.cbgm, origin = NEW.origin
        WHERE (pass_id, ms_id) = (OLD.pass_id, OLD.ms_id);
        UPDATE ms_cliques
        SET pass_id = NEW.pass_id, ms_id = NEW.ms_id, labez = NEW.labez, clique = NEW.clique
        WHERE (pass_id, ms_id) = (OLD.pass_id, OLD.ms_id);
      ELSIF TG_OP = 'DELETE' THEN
        DELETE FROM ms_cliques
        WHERE (pass_id, ms_id) = (OLD.pass_id, OLD.ms_id);
        DELETE FROM apparatus
        WHERE (pass_id, ms_id) = (OLD.pass_id, OLD.ms_id);
      END IF;
      RETURN NEW;
    END; $$;


ALTER FUNCTION ntg.apparatus_cliques_view_trigger_f() OWNER TO ntg;

--
-- Name: char_labez(integer); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.char_labez(l integer) RETURNS character
    LANGUAGE sql IMMUTABLE
    AS $$ SELECT CASE WHEN l > 0 THEN chr (l + 96) ELSE 'z' END $$;


ALTER FUNCTION ntg.char_labez(l integer) OWNER TO ntg;

--
-- Name: cliques_trigger_f(); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.cliques_trigger_f() RETURNS trigger
    LANGUAGE plpgsql
    AS $$ BEGIN
      IF TG_OP IN ('UPDATE', 'DELETE') THEN
        -- transfer data to tts table
        INSERT INTO cliques_tts (pass_id, labez, clique,
                                 sys_period, user_id_start, user_id_stop)
        VALUES (OLD.pass_id, OLD.labez, OLD.clique,
                close_period (OLD.sys_period), OLD.user_id_start, user_id ());
      END IF;
      IF TG_OP IN ('UPDATE', 'INSERT') THEN
        NEW.sys_period = tstzrange (now (), NULL);
        NEW.user_id_start = user_id ();
        RETURN NEW;
      END IF;
      RETURN OLD;
   END; $$;


ALTER FUNCTION ntg.cliques_trigger_f() OWNER TO ntg;

--
-- Name: close_period(tstzrange); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.close_period(period tstzrange) RETURNS tstzrange
    LANGUAGE sql IMMUTABLE
    AS $$ SELECT TSTZRANGE (LOWER (period), NOW ()) $$;


ALTER FUNCTION ntg.close_period(period tstzrange) OWNER TO ntg;

--
-- Name: is_older(integer, character, character, character, character); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.is_older(passage_id integer, labez2 character, clique2 character, labez1 character, clique1 character) RETURNS boolean
    LANGUAGE sql STABLE
    AS $$ WITH RECURSIVE locstem_rec (pass_id, labez, clique, source_labez, source_clique) AS (
  SELECT pass_id, labez, clique, source_labez, source_clique
  FROM locstem i
  WHERE i.pass_id = passage_id AND i.labez = labez1 AND i.clique = clique1
  UNION
  SELECT l.pass_id, l.labez, l.clique, l.source_labez, l.source_clique
  FROM locstem l, locstem_rec r
  WHERE l.pass_id = r.pass_id AND l.labez = r.source_labez AND l.clique = r.source_clique
  )

SELECT EXISTS (SELECT * FROM locstem_rec WHERE source_labez = labez2 AND source_clique = clique2); $$;


ALTER FUNCTION ntg.is_older(passage_id integer, labez2 character, clique2 character, labez1 character, clique1 character) OWNER TO ntg;

--
-- Name: is_p_older(integer, character, character, character, character); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.is_p_older(passage_id integer, labez2 character, clique2 character, labez1 character, clique1 character) RETURNS boolean
    LANGUAGE sql STABLE
    AS $$ SELECT EXISTS (SELECT * FROM locstem
               WHERE pass_id = passage_id AND
                     labez = labez1 AND clique = clique1 AND
                     source_labez = labez2 AND source_clique = clique2); $$;


ALTER FUNCTION ntg.is_p_older(passage_id integer, labez2 character, clique2 character, labez1 character, clique1 character) OWNER TO ntg;

--
-- Name: is_p_unclear(integer, character, character); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.is_p_unclear(passage_id integer, labez1 character, clique1 character) RETURNS boolean
    LANGUAGE sql STABLE
    AS $$ SELECT EXISTS (SELECT * FROM locstem
               WHERE pass_id = passage_id AND
                     labez = labez1 AND clique = clique1 AND
                     source_labez = '?'); $$;


ALTER FUNCTION ntg.is_p_unclear(passage_id integer, labez1 character, clique1 character) OWNER TO ntg;

--
-- Name: is_unclear(integer, character, character); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.is_unclear(passage_id integer, labez1 character, clique1 character) RETURNS boolean
    LANGUAGE sql STABLE
    AS $$ WITH RECURSIVE locstem_rec (pass_id, labez, clique, source_labez, source_clique) AS (
  SELECT pass_id, labez, clique, source_labez, source_clique
  FROM locstem i
  WHERE i.pass_id = passage_id AND i.labez = labez1 AND i.clique = clique1
  UNION
  SELECT l.pass_id, l.labez, l.clique, l.source_labez, l.source_clique
  FROM locstem l, locstem_rec r
  WHERE l.pass_id = r.pass_id AND l.labez = r.source_labez AND l.clique = r.source_clique
  )

SELECT EXISTS (SELECT * FROM locstem_rec WHERE source_labez = '?'); $$;


ALTER FUNCTION ntg.is_unclear(passage_id integer, labez1 character, clique1 character) OWNER TO ntg;

--
-- Name: labez_array_to_string(character[]); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.labez_array_to_string(a character[]) RETURNS character
    LANGUAGE sql IMMUTABLE
    AS $$ SELECT array_to_string (a, '/', '') $$;


ALTER FUNCTION ntg.labez_array_to_string(a character[]) OWNER TO ntg;

--
-- Name: labez_clique(character, character); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.labez_clique(labez character, clique character) RETURNS character
    LANGUAGE sql IMMUTABLE
    AS $$ SELECT labez || COALESCE (NULLIF (clique, '1'), '') $$;


ALTER FUNCTION ntg.labez_clique(labez character, clique character) OWNER TO ntg;

--
-- Name: locstem_trigger_f(); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.locstem_trigger_f() RETURNS trigger
    LANGUAGE plpgsql
    AS $$ BEGIN
      IF TG_OP IN ('UPDATE', 'DELETE') THEN
        -- transfer data to tts table
        INSERT INTO locstem_tts (pass_id, labez, clique, source_labez, source_clique,
                                 sys_period, user_id_start, user_id_stop)
        VALUES (OLD.pass_id, OLD.labez, OLD.clique, OLD.source_labez, OLD.source_clique,
                close_period (OLD.sys_period), OLD.user_id_start, user_id ());
      END IF;
      IF TG_OP IN ('UPDATE', 'INSERT') THEN
        NEW.sys_period = tstzrange (now (), NULL);
        NEW.user_id_start = user_id ();
        RETURN NEW;
      END IF;
      RETURN OLD;
   END; $$;


ALTER FUNCTION ntg.locstem_trigger_f() OWNER TO ntg;

--
-- Name: ms_cliques_trigger_f(); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.ms_cliques_trigger_f() RETURNS trigger
    LANGUAGE plpgsql
    AS $$ BEGIN
      IF TG_OP IN ('UPDATE', 'DELETE') THEN
        -- transfer data to tts table
        INSERT INTO ms_cliques_tts (pass_id, ms_id, labez, clique,
                                    sys_period, user_id_start, user_id_stop)
        VALUES (OLD.pass_id, OLD.ms_id, OLD.labez, OLD.clique,
                close_period (OLD.sys_period), OLD.user_id_start, user_id ());
      END IF;
      IF TG_OP IN ('UPDATE', 'INSERT') THEN
        NEW.sys_period = tstzrange (now (), NULL);
        NEW.user_id_start = user_id ();
        RETURN NEW;
      END IF;
      RETURN OLD;
   END; $$;


ALTER FUNCTION ntg.ms_cliques_trigger_f() OWNER TO ntg;

--
-- Name: notes_trigger_f(); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.notes_trigger_f() RETURNS trigger
    LANGUAGE plpgsql
    AS $$ BEGIN
      IF TG_OP IN ('UPDATE', 'DELETE') THEN
        -- transfer data to tts table
        INSERT INTO notes_tts (pass_id, note,
                               sys_period, user_id_start, user_id_stop)
        VALUES (OLD.pass_id, OLD.note,
                close_period (OLD.sys_period), OLD.user_id_start, user_id ());
      END IF;
      IF TG_OP IN ('UPDATE', 'INSERT') THEN
        NEW.sys_period = tstzrange (now (), NULL);
        NEW.user_id_start = user_id ();
        RETURN NEW;
      END IF;
      RETURN OLD;
   END; $$;


ALTER FUNCTION ntg.notes_trigger_f() OWNER TO ntg;

--
-- Name: ord_labez(character); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.ord_labez(l character) RETURNS integer
    LANGUAGE sql IMMUTABLE
    AS $$ SELECT CASE WHEN ascii (l) >= 122 THEN 0 ELSE ascii (l) - 96 END $$;


ALTER FUNCTION ntg.ord_labez(l character) OWNER TO ntg;

--
-- Name: reading(character, character varying); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.reading(labez character, lesart character varying) RETURNS character varying
    LANGUAGE sql IMMUTABLE
    AS $$ SELECT CASE WHEN labez = 'zz' THEN '' WHEN labez = 'zu' THEN 'overlap' ELSE COALESCE (NULLIF (lesart, ''), 'om') END $$;


ALTER FUNCTION ntg.reading(labez character, lesart character varying) OWNER TO ntg;

--
-- Name: user_id(); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.user_id() RETURNS integer
    LANGUAGE sql STABLE
    AS $$ SELECT current_setting ('ntg.user_id')::int; $$;


ALTER FUNCTION ntg.user_id() OWNER TO ntg;

--
-- Name: varnew2clique(character); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.varnew2clique(varnew character) RETURNS character
    LANGUAGE sql IMMUTABLE
    AS $$ SELECT COALESCE (NULLIF (REGEXP_REPLACE (varnew, '^[^0-9]+', ''), ''), '1') $$;


ALTER FUNCTION ntg.varnew2clique(varnew character) OWNER TO ntg;

--
-- Name: varnew2labez(character); Type: FUNCTION; Schema: ntg; Owner: ntg
--

CREATE FUNCTION ntg.varnew2labez(varnew character) RETURNS character
    LANGUAGE sql IMMUTABLE
    AS $_$ SELECT REGEXP_REPLACE (varnew, '[0-9]+$', '') $_$;


ALTER FUNCTION ntg.varnew2labez(varnew character) OWNER TO ntg;

--
-- Name: labez_agg(character); Type: AGGREGATE; Schema: ntg; Owner: ntg
--

CREATE AGGREGATE ntg.labez_agg(character) (
    SFUNC = array_append,
    STYPE = character[],
    INITCOND = '{}',
    FINALFUNC = ntg.labez_array_to_string
);


ALTER AGGREGATE ntg.labez_agg(character) OWNER TO ntg;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: affinity; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.affinity (
    rg_id integer NOT NULL,
    ms_id1 integer NOT NULL,
    ms_id2 integer NOT NULL,
    affinity double precision DEFAULT '0'::double precision NOT NULL,
    common integer NOT NULL,
    equal integer NOT NULL,
    older integer NOT NULL,
    newer integer NOT NULL,
    unclear integer NOT NULL,
    p_older integer NOT NULL,
    p_newer integer NOT NULL,
    p_unclear integer NOT NULL
);


ALTER TABLE ntg.affinity OWNER TO ntg;

--
-- Name: books; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.books (
    bk_id integer NOT NULL,
    siglum character varying NOT NULL,
    book character varying NOT NULL,
    passage int4range NOT NULL
);


ALTER TABLE ntg.books OWNER TO ntg;

--
-- Name: ms_ranges; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.ms_ranges (
    rg_id integer NOT NULL,
    ms_id integer NOT NULL,
    length integer
);


ALTER TABLE ntg.ms_ranges OWNER TO ntg;

--
-- Name: ranges; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.ranges (
    rg_id integer NOT NULL,
    bk_id integer NOT NULL,
    range character varying NOT NULL,
    passage int4range NOT NULL
);


ALTER TABLE ntg.ranges OWNER TO ntg;

--
-- Name: ranges_view; Type: VIEW; Schema: ntg; Owner: ntg
--

CREATE VIEW ntg.ranges_view AS
 SELECT bk.bk_id,
    bk.siglum,
    bk.book,
    ch.rg_id,
    ch.range,
    ch.passage
   FROM (ntg.books bk
     JOIN ntg.ranges ch USING (bk_id));


ALTER TABLE ntg.ranges_view OWNER TO ntg;

--
-- Name: affinity_p_view; Type: VIEW; Schema: ntg; Owner: ntg
--

CREATE VIEW ntg.affinity_p_view AS
 SELECT ch.bk_id,
    ch.rg_id,
    ch.range,
    aff.ms_id1,
    aff.ms_id2,
    aff.common,
    aff.equal,
    aff.p_older AS older,
    aff.p_newer AS newer,
    aff.p_unclear AS unclear,
    aff.affinity,
    ch1.length AS ms1_length,
    ch2.length AS ms2_length
   FROM (((ntg.affinity aff
     JOIN ntg.ranges_view ch USING (rg_id))
     JOIN ntg.ms_ranges ch1 ON (((aff.ms_id1 = ch1.ms_id) AND (aff.rg_id = ch1.rg_id))))
     JOIN ntg.ms_ranges ch2 ON (((aff.ms_id2 = ch2.ms_id) AND (aff.rg_id = ch2.rg_id))));


ALTER TABLE ntg.affinity_p_view OWNER TO ntg;

--
-- Name: affinity_view; Type: VIEW; Schema: ntg; Owner: ntg
--

CREATE VIEW ntg.affinity_view AS
 SELECT ch.bk_id,
    ch.rg_id,
    ch.range,
    aff.ms_id1,
    aff.ms_id2,
    aff.common,
    aff.equal,
    aff.older,
    aff.newer,
    aff.unclear,
    aff.affinity,
    ch1.length AS ms1_length,
    ch2.length AS ms2_length
   FROM (((ntg.affinity aff
     JOIN ntg.ranges_view ch USING (rg_id))
     JOIN ntg.ms_ranges ch1 ON (((aff.ms_id1 = ch1.ms_id) AND (aff.rg_id = ch1.rg_id))))
     JOIN ntg.ms_ranges ch2 ON (((aff.ms_id2 = ch2.ms_id) AND (aff.rg_id = ch2.rg_id))));


ALTER TABLE ntg.affinity_view OWNER TO ntg;

--
-- Name: apparatus; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.apparatus (
    ms_id integer NOT NULL,
    pass_id integer NOT NULL,
    labez character varying(64) NOT NULL,
    cbgm boolean NOT NULL,
    labezsuf character varying(64) DEFAULT ''::character varying NOT NULL,
    certainty real DEFAULT '1'::real NOT NULL,
    lesart character varying(1024),
    origin character varying(64) NOT NULL,
    CONSTRAINT apparatus_certainty_check CHECK (((certainty > (0.0)::double precision) AND (certainty <= (1.0)::double precision))),
    CONSTRAINT apparatus_check CHECK (((certainty = (1.0)::double precision) >= cbgm))
);


ALTER TABLE ntg.apparatus OWNER TO ntg;

--
-- Name: manuscripts; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.manuscripts (
    ms_id integer NOT NULL,
    hsnr integer NOT NULL,
    hs character varying(32) NOT NULL
);


ALTER TABLE ntg.manuscripts OWNER TO ntg;

--
-- Name: passages; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.passages (
    pass_id integer NOT NULL,
    bk_id integer NOT NULL,
    begadr integer NOT NULL,
    endadr integer NOT NULL,
    passage int4range NOT NULL,
    variant boolean DEFAULT false NOT NULL,
    spanning boolean DEFAULT false NOT NULL,
    spanned boolean DEFAULT false NOT NULL,
    fehlvers boolean DEFAULT false NOT NULL
);


ALTER TABLE ntg.passages OWNER TO ntg;

--
-- Name: readings; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.readings (
    pass_id integer NOT NULL,
    labez character varying(64) NOT NULL,
    lesart character varying(1024)
);


ALTER TABLE ntg.readings OWNER TO ntg;

--
-- Name: apparatus_view; Type: VIEW; Schema: ntg; Owner: ntg
--

CREATE VIEW ntg.apparatus_view AS
 SELECT p.pass_id,
    p.begadr,
    p.endadr,
    p.passage,
    p.spanning,
    p.spanned,
    p.fehlvers,
    ms.ms_id,
    ms.hs,
    ms.hsnr,
    a.labez,
    a.cbgm,
    a.labezsuf,
    a.certainty,
    a.origin,
    COALESCE(a.lesart, r.lesart) AS lesart
   FROM (((ntg.apparatus a
     JOIN ntg.readings r USING (pass_id, labez))
     JOIN ntg.passages p USING (pass_id))
     JOIN ntg.manuscripts ms USING (ms_id));


ALTER TABLE ntg.apparatus_view OWNER TO ntg;

--
-- Name: ms_cliques; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.ms_cliques (
    ms_id integer NOT NULL,
    pass_id integer NOT NULL,
    labez character varying(64) NOT NULL,
    clique character varying(2) DEFAULT '1'::character varying NOT NULL,
    sys_period tstzrange DEFAULT tstzrange(now(), NULL::timestamp with time zone) NOT NULL,
    user_id_start integer NOT NULL,
    user_id_stop integer
);


ALTER TABLE ntg.ms_cliques OWNER TO ntg;

--
-- Name: apparatus_cliques_view; Type: VIEW; Schema: ntg; Owner: ntg
--

CREATE VIEW ntg.apparatus_cliques_view AS
 SELECT a.pass_id,
    a.begadr,
    a.endadr,
    a.passage,
    a.spanning,
    a.spanned,
    a.fehlvers,
    a.ms_id,
    a.hs,
    a.hsnr,
    a.labez,
    a.cbgm,
    a.labezsuf,
    a.certainty,
    a.origin,
    a.lesart,
    q.clique,
    ntg.labez_clique((q.labez)::bpchar, (q.clique)::bpchar) AS labez_clique
   FROM (ntg.apparatus_view a
     LEFT JOIN ntg.ms_cliques q USING (ms_id, pass_id, labez));


ALTER TABLE ntg.apparatus_cliques_view OWNER TO ntg;

--
-- Name: apparatus_view_agg; Type: VIEW; Schema: ntg; Owner: ntg
--

CREATE VIEW ntg.apparatus_view_agg AS
 SELECT apparatus_cliques_view.pass_id,
    apparatus_cliques_view.ms_id,
    apparatus_cliques_view.hs,
    apparatus_cliques_view.hsnr,
    mode() WITHIN GROUP (ORDER BY apparatus_cliques_view.lesart) AS lesart,
    ntg.labez_agg((apparatus_cliques_view.labez)::bpchar ORDER BY (apparatus_cliques_view.labez)::bpchar) AS labez,
    ntg.labez_agg((apparatus_cliques_view.clique)::bpchar ORDER BY (apparatus_cliques_view.clique)::bpchar) AS clique,
    ntg.labez_agg((apparatus_cliques_view.labezsuf)::bpchar ORDER BY (apparatus_cliques_view.labezsuf)::bpchar) AS labezsuf,
    ntg.labez_agg(apparatus_cliques_view.labez_clique ORDER BY apparatus_cliques_view.labez_clique) AS labez_clique,
    ntg.labez_agg((((apparatus_cliques_view.labez)::text || (apparatus_cliques_view.labezsuf)::text))::bpchar ORDER BY apparatus_cliques_view.labez, apparatus_cliques_view.labezsuf) AS labez_labezsuf,
    ntg.labez_agg(((((apparatus_cliques_view.labez)::text || (apparatus_cliques_view.labezsuf)::text) || (apparatus_cliques_view.clique)::text))::bpchar ORDER BY apparatus_cliques_view.labez, apparatus_cliques_view.labezsuf, apparatus_cliques_view.clique) AS labez_labezsuf_clique,
    max(apparatus_cliques_view.certainty) AS certainty
   FROM ntg.apparatus_cliques_view
  GROUP BY apparatus_cliques_view.pass_id, apparatus_cliques_view.ms_id, apparatus_cliques_view.hs, apparatus_cliques_view.hsnr;


ALTER TABLE ntg.apparatus_view_agg OWNER TO ntg;

--
-- Name: att; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.att (
    id integer NOT NULL,
    hsnr integer NOT NULL,
    hs character varying(32) NOT NULL,
    begadr integer NOT NULL,
    endadr integer NOT NULL,
    labez character varying(64) DEFAULT ''::character varying NOT NULL,
    labezsuf character varying(64) DEFAULT ''::character varying,
    certainty real DEFAULT '1'::real NOT NULL,
    lemma character varying(1024) DEFAULT ''::character varying,
    lesart character varying(1024) DEFAULT ''::character varying,
    labezorig character varying(32) DEFAULT ''::character varying NOT NULL,
    labezsuforig character varying(64) DEFAULT ''::character varying,
    suffix2 character varying(32) DEFAULT ''::character varying,
    kontrolle character varying(1) DEFAULT ''::character varying,
    fehler character varying(2) DEFAULT ''::character varying,
    suff character varying(32) DEFAULT ''::character varying,
    vid character varying(32) DEFAULT ''::character varying,
    vl character varying(32) DEFAULT ''::character varying,
    korr character varying(32) DEFAULT ''::character varying,
    lekt character varying(32) DEFAULT ''::character varying,
    komm character varying(32) DEFAULT ''::character varying,
    anfalt integer,
    endalt integer,
    labezalt character varying(32) DEFAULT ''::character varying,
    lasufalt character varying(32) DEFAULT ''::character varying,
    base character varying(8) DEFAULT ''::character varying,
    over character varying(1) DEFAULT ''::character varying,
    comp character varying(1) DEFAULT ''::character varying,
    over1 character varying(1) DEFAULT ''::character varying,
    comp1 character varying(1) DEFAULT ''::character varying,
    printout character varying(32) DEFAULT ''::character varying,
    category character varying(1) DEFAULT ''::character varying,
    passage int4range NOT NULL
);


ALTER TABLE ntg.att OWNER TO ntg;

--
-- Name: att_id_seq; Type: SEQUENCE; Schema: ntg; Owner: ntg
--

CREATE SEQUENCE ntg.att_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ntg.att_id_seq OWNER TO ntg;

--
-- Name: att_id_seq; Type: SEQUENCE OWNED BY; Schema: ntg; Owner: ntg
--

ALTER SEQUENCE ntg.att_id_seq OWNED BY ntg.att.id;


--
-- Name: books_bk_id_seq; Type: SEQUENCE; Schema: ntg; Owner: ntg
--

CREATE SEQUENCE ntg.books_bk_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ntg.books_bk_id_seq OWNER TO ntg;

--
-- Name: books_bk_id_seq; Type: SEQUENCE OWNED BY; Schema: ntg; Owner: ntg
--

ALTER SEQUENCE ntg.books_bk_id_seq OWNED BY ntg.books.bk_id;


--
-- Name: cliques; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.cliques (
    pass_id integer NOT NULL,
    labez character varying(64) NOT NULL,
    clique character varying(2) DEFAULT '1'::character varying NOT NULL,
    sys_period tstzrange DEFAULT tstzrange(now(), NULL::timestamp with time zone) NOT NULL,
    user_id_start integer NOT NULL,
    user_id_stop integer
);


ALTER TABLE ntg.cliques OWNER TO ntg;

--
-- Name: cliques_tts; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.cliques_tts (
    pass_id integer NOT NULL,
    labez character varying(64) NOT NULL,
    clique character varying(2) DEFAULT '1'::character varying NOT NULL,
    sys_period tstzrange DEFAULT tstzrange(now(), NULL::timestamp with time zone) NOT NULL,
    user_id_start integer NOT NULL,
    user_id_stop integer
);


ALTER TABLE ntg.cliques_tts OWNER TO ntg;

--
-- Name: readings_view; Type: VIEW; Schema: ntg; Owner: ntg
--

CREATE VIEW ntg.readings_view AS
 SELECT p.begadr,
    p.endadr,
    p.passage,
    r.pass_id,
    r.labez,
    r.lesart
   FROM (ntg.readings r
     JOIN ntg.passages p USING (pass_id));


ALTER TABLE ntg.readings_view OWNER TO ntg;

--
-- Name: cliques_view; Type: VIEW; Schema: ntg; Owner: ntg
--

CREATE VIEW ntg.cliques_view AS
 SELECT r.begadr,
    r.endadr,
    r.passage,
    r.lesart,
    q.pass_id,
    q.labez,
    q.clique,
    q.sys_period,
    q.user_id_start,
    q.user_id_stop
   FROM (ntg.cliques q
     JOIN ntg.readings_view r USING (pass_id, labez));


ALTER TABLE ntg.cliques_view OWNER TO ntg;

--
-- Name: export_cliques; Type: VIEW; Schema: ntg; Owner: ntg
--

CREATE VIEW ntg.export_cliques AS
 SELECT cliques_view.passage,
    cliques_view.labez,
    cliques_view.clique,
    cliques_view.sys_period,
    cliques_view.user_id_start,
    cliques_view.user_id_stop
   FROM ntg.cliques_view
  WHERE (cliques_view.user_id_start <> 0)
UNION
 SELECT p.passage,
    cq.labez,
    cq.clique,
    cq.sys_period,
    cq.user_id_start,
    cq.user_id_stop
   FROM (ntg.cliques_tts cq
     JOIN ntg.passages p USING (pass_id))
  ORDER BY 1, 4, 2, 3;


ALTER TABLE ntg.export_cliques OWNER TO ntg;

--
-- Name: locstem; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.locstem (
    pass_id integer NOT NULL,
    labez character varying(64) NOT NULL,
    clique character varying(2) DEFAULT '1'::character varying NOT NULL,
    source_labez character varying(64) NOT NULL,
    source_clique character varying(2) DEFAULT '1'::character varying NOT NULL,
    sys_period tstzrange DEFAULT tstzrange(now(), NULL::timestamp with time zone) NOT NULL,
    user_id_start integer NOT NULL,
    user_id_stop integer,
    CONSTRAINT check_same_source CHECK (((labez)::text <> (source_labez)::text))
);


ALTER TABLE ntg.locstem OWNER TO ntg;

--
-- Name: locstem_tts; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.locstem_tts (
    pass_id integer NOT NULL,
    labez character varying(64) NOT NULL,
    clique character varying(2) DEFAULT '1'::character varying NOT NULL,
    source_labez character varying(64) NOT NULL,
    source_clique character varying(2) DEFAULT '1'::character varying NOT NULL,
    sys_period tstzrange DEFAULT tstzrange(now(), NULL::timestamp with time zone) NOT NULL,
    user_id_start integer NOT NULL,
    user_id_stop integer
);


ALTER TABLE ntg.locstem_tts OWNER TO ntg;

--
-- Name: locstem_view; Type: VIEW; Schema: ntg; Owner: ntg
--

CREATE VIEW ntg.locstem_view AS
 SELECT p.begadr,
    p.endadr,
    p.passage,
    p.fehlvers,
    locstem.pass_id,
    locstem.labez,
    locstem.clique,
    locstem.source_labez,
    locstem.source_clique,
    locstem.sys_period,
    locstem.user_id_start,
    locstem.user_id_stop
   FROM (ntg.locstem
     JOIN ntg.passages p USING (pass_id));


ALTER TABLE ntg.locstem_view OWNER TO ntg;

--
-- Name: export_locstem; Type: VIEW; Schema: ntg; Owner: ntg
--

CREATE VIEW ntg.export_locstem AS
 SELECT locstem_view.passage,
    locstem_view.labez,
    locstem_view.clique,
    locstem_view.source_labez,
    locstem_view.source_clique,
    locstem_view.sys_period,
    locstem_view.user_id_start,
    locstem_view.user_id_stop
   FROM ntg.locstem_view
UNION
 SELECT p.passage,
    lt.labez,
    lt.clique,
    lt.source_labez,
    lt.source_clique,
    lt.sys_period,
    lt.user_id_start,
    lt.user_id_stop
   FROM (ntg.locstem_tts lt
     JOIN ntg.passages p USING (pass_id))
  ORDER BY 1, 6, 2, 3;


ALTER TABLE ntg.export_locstem OWNER TO ntg;

--
-- Name: ms_cliques_tts; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.ms_cliques_tts (
    ms_id integer NOT NULL,
    pass_id integer NOT NULL,
    labez character varying(64) NOT NULL,
    clique character varying(2) DEFAULT '1'::character varying NOT NULL,
    sys_period tstzrange DEFAULT tstzrange(now(), NULL::timestamp with time zone) NOT NULL,
    user_id_start integer NOT NULL,
    user_id_stop integer
);


ALTER TABLE ntg.ms_cliques_tts OWNER TO ntg;

--
-- Name: ms_cliques_view; Type: VIEW; Schema: ntg; Owner: ntg
--

CREATE VIEW ntg.ms_cliques_view AS
 SELECT q.begadr,
    q.endadr,
    q.passage,
    q.lesart,
    ms.hs,
    ms.hsnr,
    mq.ms_id,
    mq.pass_id,
    mq.labez,
    mq.clique,
    mq.sys_period,
    mq.user_id_start,
    mq.user_id_stop
   FROM ((ntg.ms_cliques mq
     JOIN ntg.cliques_view q USING (pass_id, labez, clique))
     JOIN ntg.manuscripts ms USING (ms_id));


ALTER TABLE ntg.ms_cliques_view OWNER TO ntg;

--
-- Name: export_ms_cliques; Type: VIEW; Schema: ntg; Owner: ntg
--

CREATE VIEW ntg.export_ms_cliques AS
 SELECT ms_cliques_view.passage,
    ms_cliques_view.hsnr,
    ms_cliques_view.labez,
    ms_cliques_view.clique,
    ms_cliques_view.sys_period,
    ms_cliques_view.user_id_start,
    ms_cliques_view.user_id_stop
   FROM ntg.ms_cliques_view
  WHERE (ms_cliques_view.user_id_start <> 0)
UNION
 SELECT p.passage,
    m.hsnr,
    mcq.labez,
    mcq.clique,
    mcq.sys_period,
    mcq.user_id_start,
    mcq.user_id_stop
   FROM ((ntg.ms_cliques_tts mcq
     JOIN ntg.passages p USING (pass_id))
     JOIN ntg.manuscripts m USING (ms_id))
  ORDER BY 1, 5, 2, 3, 4;


ALTER TABLE ntg.export_ms_cliques OWNER TO ntg;

--
-- Name: notes; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.notes (
    pass_id integer NOT NULL,
    note character varying NOT NULL,
    sys_period tstzrange DEFAULT tstzrange(now(), NULL::timestamp with time zone) NOT NULL,
    user_id_start integer NOT NULL,
    user_id_stop integer
);


ALTER TABLE ntg.notes OWNER TO ntg;

--
-- Name: notes_tts; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.notes_tts (
    pass_id integer NOT NULL,
    note character varying NOT NULL,
    sys_period tstzrange DEFAULT tstzrange(now(), NULL::timestamp with time zone) NOT NULL,
    user_id_start integer NOT NULL,
    user_id_stop integer
);


ALTER TABLE ntg.notes_tts OWNER TO ntg;

--
-- Name: notes_view; Type: VIEW; Schema: ntg; Owner: ntg
--

CREATE VIEW ntg.notes_view AS
 SELECT p.begadr,
    p.endadr,
    p.passage,
    p.fehlvers,
    n.pass_id,
    n.note,
    n.sys_period,
    n.user_id_start,
    n.user_id_stop
   FROM (ntg.notes n
     JOIN ntg.passages p USING (pass_id));


ALTER TABLE ntg.notes_view OWNER TO ntg;

--
-- Name: export_notes; Type: VIEW; Schema: ntg; Owner: ntg
--

CREATE VIEW ntg.export_notes AS
 SELECT notes_view.passage,
    notes_view.note,
    notes_view.sys_period,
    notes_view.user_id_start,
    notes_view.user_id_stop
   FROM ntg.notes_view
UNION
 SELECT p.passage,
    notes_tts.note,
    notes_tts.sys_period,
    notes_tts.user_id_start,
    notes_tts.user_id_stop
   FROM (ntg.notes_tts
     JOIN ntg.passages p USING (pass_id))
  ORDER BY 1, 3;


ALTER TABLE ntg.export_notes OWNER TO ntg;

--
-- Name: import_cliques; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.import_cliques (
    labez character varying(64) NOT NULL,
    clique character varying(2) DEFAULT '1'::character varying NOT NULL,
    pass_id integer,
    passage int4range NOT NULL,
    sys_period tstzrange DEFAULT tstzrange(now(), NULL::timestamp with time zone) NOT NULL,
    user_id_start integer NOT NULL,
    user_id_stop integer
);


ALTER TABLE ntg.import_cliques OWNER TO ntg;

--
-- Name: import_locstem; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.import_locstem (
    labez character varying(64) NOT NULL,
    clique character varying(2) DEFAULT '1'::character varying NOT NULL,
    source_labez character varying(64) NOT NULL,
    source_clique character varying(2) DEFAULT '1'::character varying NOT NULL,
    pass_id integer,
    passage int4range NOT NULL,
    sys_period tstzrange DEFAULT tstzrange(now(), NULL::timestamp with time zone) NOT NULL,
    user_id_start integer NOT NULL,
    user_id_stop integer
);


ALTER TABLE ntg.import_locstem OWNER TO ntg;

--
-- Name: import_ms_cliques; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.import_ms_cliques (
    labez character varying(64) NOT NULL,
    clique character varying(2) DEFAULT '1'::character varying NOT NULL,
    pass_id integer,
    ms_id integer,
    passage int4range NOT NULL,
    hsnr integer NOT NULL,
    sys_period tstzrange DEFAULT tstzrange(now(), NULL::timestamp with time zone) NOT NULL,
    user_id_start integer NOT NULL,
    user_id_stop integer
);


ALTER TABLE ntg.import_ms_cliques OWNER TO ntg;

--
-- Name: import_notes; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.import_notes (
    note character varying NOT NULL,
    pass_id integer,
    passage int4range NOT NULL,
    sys_period tstzrange DEFAULT tstzrange(now(), NULL::timestamp with time zone) NOT NULL,
    user_id_start integer NOT NULL,
    user_id_stop integer
);


ALTER TABLE ntg.import_notes OWNER TO ntg;

--
-- Name: lac; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.lac (
    id integer NOT NULL,
    hsnr integer NOT NULL,
    hs character varying(32) NOT NULL,
    begadr integer NOT NULL,
    endadr integer NOT NULL,
    labez character varying(64) DEFAULT ''::character varying,
    labezsuf character varying(64) DEFAULT ''::character varying,
    lemma character varying(1024) DEFAULT ''::character varying,
    lesart character varying(1024) DEFAULT ''::character varying,
    suffix2 character varying(32) DEFAULT ''::character varying,
    kontrolle character varying(1) DEFAULT ''::character varying,
    fehler character varying(2) DEFAULT ''::character varying,
    suff character varying(32) DEFAULT ''::character varying,
    vid character varying(32) DEFAULT ''::character varying,
    vl character varying(32) DEFAULT ''::character varying,
    korr character varying(32) DEFAULT ''::character varying,
    lekt character varying(32) DEFAULT ''::character varying,
    komm character varying(32) DEFAULT ''::character varying,
    anfalt integer,
    endalt integer,
    labezalt character varying(32) DEFAULT ''::character varying,
    lasufalt character varying(32) DEFAULT ''::character varying,
    base character varying(8) DEFAULT ''::character varying,
    over character varying(1) DEFAULT ''::character varying,
    comp character varying(1) DEFAULT ''::character varying,
    over1 character varying(1) DEFAULT ''::character varying,
    comp1 character varying(1) DEFAULT ''::character varying,
    printout character varying(32) DEFAULT ''::character varying,
    category character varying(1) DEFAULT ''::character varying,
    passage int4range NOT NULL
);


ALTER TABLE ntg.lac OWNER TO ntg;

--
-- Name: lac_id_seq; Type: SEQUENCE; Schema: ntg; Owner: ntg
--

CREATE SEQUENCE ntg.lac_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ntg.lac_id_seq OWNER TO ntg;

--
-- Name: lac_id_seq; Type: SEQUENCE OWNED BY; Schema: ntg; Owner: ntg
--

ALTER SEQUENCE ntg.lac_id_seq OWNED BY ntg.lac.id;


--
-- Name: manuscripts_ms_id_seq; Type: SEQUENCE; Schema: ntg; Owner: ntg
--

CREATE SEQUENCE ntg.manuscripts_ms_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ntg.manuscripts_ms_id_seq OWNER TO ntg;

--
-- Name: manuscripts_ms_id_seq; Type: SEQUENCE OWNED BY; Schema: ntg; Owner: ntg
--

ALTER SEQUENCE ntg.manuscripts_ms_id_seq OWNED BY ntg.manuscripts.ms_id;


--
-- Name: ms_ranges_view; Type: VIEW; Schema: ntg; Owner: ntg
--

CREATE VIEW ntg.ms_ranges_view AS
 SELECT ch.bk_id,
    ch.siglum,
    ch.book,
    ch.rg_id,
    ch.range,
    ch.passage,
    mc.ms_id,
    mc.length
   FROM (ntg.ms_ranges mc
     JOIN ntg.ranges_view ch USING (rg_id));


ALTER TABLE ntg.ms_ranges_view OWNER TO ntg;

--
-- Name: nestle; Type: TABLE; Schema: ntg; Owner: ntg
--

CREATE TABLE ntg.nestle (
    id integer NOT NULL,
    begadr integer NOT NULL,
    endadr integer NOT NULL,
    passage int4range NOT NULL,
    lemma character varying(1024) DEFAULT ''::character varying
);


ALTER TABLE ntg.nestle OWNER TO ntg;

--
-- Name: nestle_id_seq; Type: SEQUENCE; Schema: ntg; Owner: ntg
--

CREATE SEQUENCE ntg.nestle_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ntg.nestle_id_seq OWNER TO ntg;

--
-- Name: nestle_id_seq; Type: SEQUENCE OWNED BY; Schema: ntg; Owner: ntg
--

ALTER SEQUENCE ntg.nestle_id_seq OWNED BY ntg.nestle.id;


--
-- Name: passages_pass_id_seq; Type: SEQUENCE; Schema: ntg; Owner: ntg
--

CREATE SEQUENCE ntg.passages_pass_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ntg.passages_pass_id_seq OWNER TO ntg;

--
-- Name: passages_pass_id_seq; Type: SEQUENCE OWNED BY; Schema: ntg; Owner: ntg
--

ALTER SEQUENCE ntg.passages_pass_id_seq OWNED BY ntg.passages.pass_id;


--
-- Name: passages_view; Type: VIEW; Schema: ntg; Owner: ntg
--

CREATE VIEW ntg.passages_view AS
 SELECT b.bk_id,
    b.siglum,
    b.book,
    ntg.adr2chapter(p.begadr) AS chapter,
    ntg.adr2verse(p.begadr) AS verse,
    ntg.adr2word(p.begadr) AS word,
    p.pass_id,
    p.begadr,
    p.endadr,
    p.passage,
    p.variant,
    p.spanning,
    p.spanned,
    p.fehlvers
   FROM (ntg.passages p
     JOIN ntg.books b USING (bk_id));


ALTER TABLE ntg.passages_view OWNER TO ntg;

--
-- Name: passages_view_lemma; Type: VIEW; Schema: ntg; Owner: ntg
--

CREATE VIEW ntg.passages_view_lemma AS
 SELECT p.bk_id,
    p.siglum,
    p.book,
    p.chapter,
    p.verse,
    p.word,
    p.pass_id,
    p.begadr,
    p.endadr,
    p.passage,
    p.variant,
    p.spanning,
    p.spanned,
    p.fehlvers,
    COALESCE(rl.lesart, 'undef'::character varying) AS lemma
   FROM (ntg.passages_view p
     LEFT JOIN ( SELECT r.pass_id,
            r.lesart
           FROM (ntg.readings r
             JOIN ntg.locstem l ON (((l.pass_id = r.pass_id) AND ((l.labez)::text = (r.labez)::text) AND ((l.source_labez)::text = '*'::text))))) rl ON ((p.pass_id = rl.pass_id)))
  ORDER BY p.pass_id;


ALTER TABLE ntg.passages_view_lemma OWNER TO ntg;

--
-- Name: ranges_rg_id_seq; Type: SEQUENCE; Schema: ntg; Owner: ntg
--

CREATE SEQUENCE ntg.ranges_rg_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ntg.ranges_rg_id_seq OWNER TO ntg;

--
-- Name: ranges_rg_id_seq; Type: SEQUENCE OWNED BY; Schema: ntg; Owner: ntg
--

ALTER SEQUENCE ntg.ranges_rg_id_seq OWNED BY ntg.ranges.rg_id;


--
-- Name: att id; Type: DEFAULT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.att ALTER COLUMN id SET DEFAULT nextval('ntg.att_id_seq'::regclass);


--
-- Name: books bk_id; Type: DEFAULT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.books ALTER COLUMN bk_id SET DEFAULT nextval('ntg.books_bk_id_seq'::regclass);


--
-- Name: lac id; Type: DEFAULT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.lac ALTER COLUMN id SET DEFAULT nextval('ntg.lac_id_seq'::regclass);


--
-- Name: manuscripts ms_id; Type: DEFAULT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.manuscripts ALTER COLUMN ms_id SET DEFAULT nextval('ntg.manuscripts_ms_id_seq'::regclass);


--
-- Name: nestle id; Type: DEFAULT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.nestle ALTER COLUMN id SET DEFAULT nextval('ntg.nestle_id_seq'::regclass);


--
-- Name: passages pass_id; Type: DEFAULT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.passages ALTER COLUMN pass_id SET DEFAULT nextval('ntg.passages_pass_id_seq'::regclass);


--
-- Name: ranges rg_id; Type: DEFAULT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.ranges ALTER COLUMN rg_id SET DEFAULT nextval('ntg.ranges_rg_id_seq'::regclass);


--
-- Name: affinity affinity_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.affinity
    ADD CONSTRAINT affinity_pkey PRIMARY KEY (rg_id, ms_id1, ms_id2);


--
-- Name: apparatus apparatus_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.apparatus
    ADD CONSTRAINT apparatus_pkey PRIMARY KEY (pass_id, ms_id, labez);


--
-- Name: att att_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.att
    ADD CONSTRAINT att_pkey PRIMARY KEY (id);


--
-- Name: books books_book_key; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.books
    ADD CONSTRAINT books_book_key UNIQUE (book);


--
-- Name: books books_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.books
    ADD CONSTRAINT books_pkey PRIMARY KEY (bk_id);


--
-- Name: books books_siglum_key; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.books
    ADD CONSTRAINT books_siglum_key UNIQUE (siglum);


--
-- Name: cliques cliques_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.cliques
    ADD CONSTRAINT cliques_pkey PRIMARY KEY (pass_id, labez, clique);


--
-- Name: cliques_tts cliques_tts_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.cliques_tts
    ADD CONSTRAINT cliques_tts_pkey PRIMARY KEY (pass_id, labez, clique, sys_period);


--
-- Name: import_cliques import_cliques_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.import_cliques
    ADD CONSTRAINT import_cliques_pkey PRIMARY KEY (passage, labez, clique, sys_period);


--
-- Name: import_locstem import_locstem_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.import_locstem
    ADD CONSTRAINT import_locstem_pkey PRIMARY KEY (passage, labez, clique, source_labez, source_clique, sys_period);


--
-- Name: import_ms_cliques import_ms_cliques_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.import_ms_cliques
    ADD CONSTRAINT import_ms_cliques_pkey PRIMARY KEY (hsnr, passage, labez, sys_period);


--
-- Name: import_notes import_notes_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.import_notes
    ADD CONSTRAINT import_notes_pkey PRIMARY KEY (passage, sys_period);


--
-- Name: lac lac_hs_passage_key; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.lac
    ADD CONSTRAINT lac_hs_passage_key UNIQUE (hs, passage);


--
-- Name: lac lac_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.lac
    ADD CONSTRAINT lac_pkey PRIMARY KEY (id);


--
-- Name: locstem locstem_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.locstem
    ADD CONSTRAINT locstem_pkey PRIMARY KEY (pass_id, labez, clique, source_labez, source_clique);


--
-- Name: locstem_tts locstem_tts_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.locstem_tts
    ADD CONSTRAINT locstem_tts_pkey PRIMARY KEY (pass_id, labez, clique, source_labez, source_clique, sys_period);


--
-- Name: manuscripts manuscripts_hs_key; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.manuscripts
    ADD CONSTRAINT manuscripts_hs_key UNIQUE (hs);


--
-- Name: manuscripts manuscripts_hsnr_key; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.manuscripts
    ADD CONSTRAINT manuscripts_hsnr_key UNIQUE (hsnr);


--
-- Name: manuscripts manuscripts_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.manuscripts
    ADD CONSTRAINT manuscripts_pkey PRIMARY KEY (ms_id);


--
-- Name: ms_cliques ms_cliques_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.ms_cliques
    ADD CONSTRAINT ms_cliques_pkey PRIMARY KEY (ms_id, pass_id, labez);


--
-- Name: ms_cliques_tts ms_cliques_tts_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.ms_cliques_tts
    ADD CONSTRAINT ms_cliques_tts_pkey PRIMARY KEY (ms_id, pass_id, labez, sys_period);


--
-- Name: ms_ranges ms_ranges_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.ms_ranges
    ADD CONSTRAINT ms_ranges_pkey PRIMARY KEY (rg_id, ms_id);


--
-- Name: nestle nestle_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.nestle
    ADD CONSTRAINT nestle_pkey PRIMARY KEY (id);


--
-- Name: notes notes_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.notes
    ADD CONSTRAINT notes_pkey PRIMARY KEY (pass_id);


--
-- Name: notes_tts notes_tts_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.notes_tts
    ADD CONSTRAINT notes_tts_pkey PRIMARY KEY (pass_id, sys_period);


--
-- Name: passages passages_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.passages
    ADD CONSTRAINT passages_pkey PRIMARY KEY (pass_id);


--
-- Name: ranges ranges_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.ranges
    ADD CONSTRAINT ranges_pkey PRIMARY KEY (rg_id);


--
-- Name: readings readings_pkey; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.readings
    ADD CONSTRAINT readings_pkey PRIMARY KEY (pass_id, labez);


--
-- Name: nestle unique_nestle_passage; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.nestle
    ADD CONSTRAINT unique_nestle_passage UNIQUE (passage);


--
-- Name: passages unique_passages_passage; Type: CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.passages
    ADD CONSTRAINT unique_passages_passage UNIQUE (passage);


--
-- Name: ix_affinity_rg_id_ms_id2; Type: INDEX; Schema: ntg; Owner: ntg
--

CREATE INDEX ix_affinity_rg_id_ms_id2 ON ntg.affinity USING btree (rg_id, ms_id2);


--
-- Name: ix_apparatus_pass_id_ms_id; Type: INDEX; Schema: ntg; Owner: ntg
--

CREATE UNIQUE INDEX ix_apparatus_pass_id_ms_id ON ntg.apparatus USING btree (pass_id, ms_id) WHERE (cbgm = true);


--
-- Name: ix_att_begadr_endadr_hs; Type: INDEX; Schema: ntg; Owner: ntg
--

CREATE INDEX ix_att_begadr_endadr_hs ON ntg.att USING btree (begadr, endadr, hs);


--
-- Name: ix_att_hs_passage; Type: INDEX; Schema: ntg; Owner: ntg
--

CREATE UNIQUE INDEX ix_att_hs_passage ON ntg.att USING btree (hs, passage) WHERE (certainty = (1.0)::double precision);


--
-- Name: ix_books_passage_gist; Type: INDEX; Schema: ntg; Owner: ntg
--

CREATE INDEX ix_books_passage_gist ON ntg.books USING gist (passage);


--
-- Name: ix_lac_passage_gist; Type: INDEX; Schema: ntg; Owner: ntg
--

CREATE INDEX ix_lac_passage_gist ON ntg.lac USING gist (passage);


--
-- Name: ix_locstem_unique_original; Type: INDEX; Schema: ntg; Owner: ntg
--

CREATE UNIQUE INDEX ix_locstem_unique_original ON ntg.locstem USING btree (pass_id) WHERE ((source_labez)::text = '*'::text);


--
-- Name: ix_nestle_passage_gist; Type: INDEX; Schema: ntg; Owner: ntg
--

CREATE INDEX ix_nestle_passage_gist ON ntg.nestle USING gist (passage);


--
-- Name: ix_ntg_apparatus_ms_id; Type: INDEX; Schema: ntg; Owner: ntg
--

CREATE INDEX ix_ntg_apparatus_ms_id ON ntg.apparatus USING btree (ms_id);


--
-- Name: ix_ntg_att_begadr; Type: INDEX; Schema: ntg; Owner: ntg
--

CREATE INDEX ix_ntg_att_begadr ON ntg.att USING btree (begadr);


--
-- Name: ix_ntg_att_endadr; Type: INDEX; Schema: ntg; Owner: ntg
--

CREATE INDEX ix_ntg_att_endadr ON ntg.att USING btree (endadr);


--
-- Name: ix_ntg_att_hs; Type: INDEX; Schema: ntg; Owner: ntg
--

CREATE INDEX ix_ntg_att_hs ON ntg.att USING btree (hs);


--
-- Name: ix_ntg_att_hsnr; Type: INDEX; Schema: ntg; Owner: ntg
--

CREATE INDEX ix_ntg_att_hsnr ON ntg.att USING btree (hsnr);


--
-- Name: ix_ntg_ms_cliques_ms_id; Type: INDEX; Schema: ntg; Owner: ntg
--

CREATE INDEX ix_ntg_ms_cliques_ms_id ON ntg.ms_cliques USING btree (ms_id);


--
-- Name: ix_ntg_ms_cliques_tts_ms_id; Type: INDEX; Schema: ntg; Owner: ntg
--

CREATE INDEX ix_ntg_ms_cliques_tts_ms_id ON ntg.ms_cliques_tts USING btree (ms_id);


--
-- Name: ix_passages_passage_gist; Type: INDEX; Schema: ntg; Owner: ntg
--

CREATE INDEX ix_passages_passage_gist ON ntg.passages USING gist (passage);


--
-- Name: ix_ranges_passage_gist; Type: INDEX; Schema: ntg; Owner: ntg
--

CREATE INDEX ix_ranges_passage_gist ON ntg.ranges USING gist (passage);


--
-- Name: readings_unique_pass_id_lesart; Type: INDEX; Schema: ntg; Owner: ntg
--

CREATE UNIQUE INDEX readings_unique_pass_id_lesart ON ntg.readings USING btree (pass_id, lesart) WHERE ((labez)::text !~ '^z'::text);


--
-- Name: apparatus_cliques_view apparatus_cliques_view_trigger; Type: TRIGGER; Schema: ntg; Owner: ntg
--

CREATE TRIGGER apparatus_cliques_view_trigger INSTEAD OF INSERT OR DELETE OR UPDATE ON ntg.apparatus_cliques_view FOR EACH ROW EXECUTE FUNCTION ntg.apparatus_cliques_view_trigger_f();


--
-- Name: cliques cliques_trigger; Type: TRIGGER; Schema: ntg; Owner: ntg
--

CREATE TRIGGER cliques_trigger BEFORE INSERT OR DELETE OR UPDATE ON ntg.cliques FOR EACH ROW EXECUTE FUNCTION ntg.cliques_trigger_f();


--
-- Name: locstem locstem_trigger; Type: TRIGGER; Schema: ntg; Owner: ntg
--

CREATE TRIGGER locstem_trigger BEFORE INSERT OR DELETE OR UPDATE ON ntg.locstem FOR EACH ROW EXECUTE FUNCTION ntg.locstem_trigger_f();


--
-- Name: ms_cliques ms_cliques_trigger; Type: TRIGGER; Schema: ntg; Owner: ntg
--

CREATE TRIGGER ms_cliques_trigger BEFORE INSERT OR DELETE OR UPDATE ON ntg.ms_cliques FOR EACH ROW EXECUTE FUNCTION ntg.ms_cliques_trigger_f();


--
-- Name: notes notes_trigger; Type: TRIGGER; Schema: ntg; Owner: ntg
--

CREATE TRIGGER notes_trigger BEFORE INSERT OR DELETE OR UPDATE ON ntg.notes FOR EACH ROW EXECUTE FUNCTION ntg.notes_trigger_f();


--
-- Name: affinity affinity_rg_id_fkey; Type: FK CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.affinity
    ADD CONSTRAINT affinity_rg_id_fkey FOREIGN KEY (rg_id, ms_id1) REFERENCES ntg.ms_ranges(rg_id, ms_id) ON DELETE CASCADE;


--
-- Name: affinity affinity_rg_id_fkey1; Type: FK CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.affinity
    ADD CONSTRAINT affinity_rg_id_fkey1 FOREIGN KEY (rg_id, ms_id2) REFERENCES ntg.ms_ranges(rg_id, ms_id) ON DELETE CASCADE;


--
-- Name: apparatus apparatus_ms_id_fkey; Type: FK CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.apparatus
    ADD CONSTRAINT apparatus_ms_id_fkey FOREIGN KEY (ms_id) REFERENCES ntg.manuscripts(ms_id) ON DELETE CASCADE;


--
-- Name: apparatus apparatus_pass_id_fkey; Type: FK CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.apparatus
    ADD CONSTRAINT apparatus_pass_id_fkey FOREIGN KEY (pass_id, labez) REFERENCES ntg.readings(pass_id, labez) ON DELETE CASCADE;


--
-- Name: cliques cliques_pass_id_fkey; Type: FK CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.cliques
    ADD CONSTRAINT cliques_pass_id_fkey FOREIGN KEY (pass_id, labez) REFERENCES ntg.readings(pass_id, labez) ON DELETE CASCADE;


--
-- Name: locstem locstem_pass_id_fkey; Type: FK CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.locstem
    ADD CONSTRAINT locstem_pass_id_fkey FOREIGN KEY (pass_id, labez, clique) REFERENCES ntg.cliques(pass_id, labez, clique) ON DELETE CASCADE;


--
-- Name: ms_cliques ms_cliques_ms_id_fkey; Type: FK CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.ms_cliques
    ADD CONSTRAINT ms_cliques_ms_id_fkey FOREIGN KEY (ms_id, pass_id, labez) REFERENCES ntg.apparatus(ms_id, pass_id, labez) ON DELETE CASCADE DEFERRABLE;


--
-- Name: ms_cliques ms_cliques_pass_id_fkey; Type: FK CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.ms_cliques
    ADD CONSTRAINT ms_cliques_pass_id_fkey FOREIGN KEY (pass_id, labez, clique) REFERENCES ntg.cliques(pass_id, labez, clique) ON DELETE CASCADE;


--
-- Name: ms_ranges ms_ranges_ms_id_fkey; Type: FK CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.ms_ranges
    ADD CONSTRAINT ms_ranges_ms_id_fkey FOREIGN KEY (ms_id) REFERENCES ntg.manuscripts(ms_id) ON DELETE CASCADE;


--
-- Name: ms_ranges ms_ranges_rg_id_fkey; Type: FK CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.ms_ranges
    ADD CONSTRAINT ms_ranges_rg_id_fkey FOREIGN KEY (rg_id) REFERENCES ntg.ranges(rg_id) ON DELETE CASCADE;


--
-- Name: notes notes_pass_id_fkey; Type: FK CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.notes
    ADD CONSTRAINT notes_pass_id_fkey FOREIGN KEY (pass_id) REFERENCES ntg.passages(pass_id) ON DELETE CASCADE;


--
-- Name: passages passages_bk_id_fkey; Type: FK CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.passages
    ADD CONSTRAINT passages_bk_id_fkey FOREIGN KEY (bk_id) REFERENCES ntg.books(bk_id) ON DELETE CASCADE;


--
-- Name: ranges ranges_bk_id_fkey; Type: FK CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.ranges
    ADD CONSTRAINT ranges_bk_id_fkey FOREIGN KEY (bk_id) REFERENCES ntg.books(bk_id) ON DELETE CASCADE;


--
-- Name: readings readings_pass_id_fkey; Type: FK CONSTRAINT; Schema: ntg; Owner: ntg
--

ALTER TABLE ONLY ntg.readings
    ADD CONSTRAINT readings_pass_id_fkey FOREIGN KEY (pass_id) REFERENCES ntg.passages(pass_id) ON DELETE CASCADE;


--
-- Name: FUNCTION adr2bk_id(adr integer); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.adr2bk_id(adr integer) TO ntg_readonly;


--
-- Name: FUNCTION adr2chapter(adr integer); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.adr2chapter(adr integer) TO ntg_readonly;


--
-- Name: FUNCTION adr2verse(adr integer); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.adr2verse(adr integer) TO ntg_readonly;


--
-- Name: FUNCTION adr2word(adr integer); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.adr2word(adr integer) TO ntg_readonly;


--
-- Name: FUNCTION apparatus_cliques_view_trigger_f(); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.apparatus_cliques_view_trigger_f() TO ntg_readonly;


--
-- Name: FUNCTION char_labez(l integer); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.char_labez(l integer) TO ntg_readonly;


--
-- Name: FUNCTION cliques_trigger_f(); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.cliques_trigger_f() TO ntg_readonly;


--
-- Name: FUNCTION close_period(period tstzrange); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.close_period(period tstzrange) TO ntg_readonly;


--
-- Name: FUNCTION is_older(passage_id integer, labez2 character, clique2 character, labez1 character, clique1 character); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.is_older(passage_id integer, labez2 character, clique2 character, labez1 character, clique1 character) TO ntg_readonly;


--
-- Name: FUNCTION is_p_older(passage_id integer, labez2 character, clique2 character, labez1 character, clique1 character); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.is_p_older(passage_id integer, labez2 character, clique2 character, labez1 character, clique1 character) TO ntg_readonly;


--
-- Name: FUNCTION is_p_unclear(passage_id integer, labez1 character, clique1 character); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.is_p_unclear(passage_id integer, labez1 character, clique1 character) TO ntg_readonly;


--
-- Name: FUNCTION is_unclear(passage_id integer, labez1 character, clique1 character); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.is_unclear(passage_id integer, labez1 character, clique1 character) TO ntg_readonly;


--
-- Name: FUNCTION labez_array_to_string(a character[]); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.labez_array_to_string(a character[]) TO ntg_readonly;


--
-- Name: FUNCTION labez_clique(labez character, clique character); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.labez_clique(labez character, clique character) TO ntg_readonly;


--
-- Name: FUNCTION locstem_trigger_f(); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.locstem_trigger_f() TO ntg_readonly;


--
-- Name: FUNCTION ms_cliques_trigger_f(); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.ms_cliques_trigger_f() TO ntg_readonly;


--
-- Name: FUNCTION notes_trigger_f(); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.notes_trigger_f() TO ntg_readonly;


--
-- Name: FUNCTION ord_labez(l character); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.ord_labez(l character) TO ntg_readonly;


--
-- Name: FUNCTION reading(labez character, lesart character varying); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.reading(labez character, lesart character varying) TO ntg_readonly;


--
-- Name: FUNCTION user_id(); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.user_id() TO ntg_readonly;


--
-- Name: FUNCTION varnew2clique(varnew character); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.varnew2clique(varnew character) TO ntg_readonly;


--
-- Name: FUNCTION varnew2labez(varnew character); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.varnew2labez(varnew character) TO ntg_readonly;


--
-- Name: FUNCTION labez_agg(character); Type: ACL; Schema: ntg; Owner: ntg
--

GRANT ALL ON FUNCTION ntg.labez_agg(character) TO ntg_readonly;


--
-- Name: TABLE affinity; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.affinity TO ntg_readonly;


--
-- Name: TABLE books; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.books TO ntg_readonly;


--
-- Name: TABLE ms_ranges; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.ms_ranges TO ntg_readonly;


--
-- Name: TABLE ranges; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.ranges TO ntg_readonly;


--
-- Name: TABLE ranges_view; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.ranges_view TO ntg_readonly;


--
-- Name: TABLE affinity_p_view; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.affinity_p_view TO ntg_readonly;


--
-- Name: TABLE affinity_view; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.affinity_view TO ntg_readonly;


--
-- Name: TABLE apparatus; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.apparatus TO ntg_readonly;


--
-- Name: TABLE manuscripts; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.manuscripts TO ntg_readonly;


--
-- Name: TABLE passages; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.passages TO ntg_readonly;


--
-- Name: TABLE readings; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.readings TO ntg_readonly;


--
-- Name: TABLE apparatus_view; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.apparatus_view TO ntg_readonly;


--
-- Name: TABLE ms_cliques; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.ms_cliques TO ntg_readonly;


--
-- Name: TABLE apparatus_cliques_view; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.apparatus_cliques_view TO ntg_readonly;


--
-- Name: TABLE apparatus_view_agg; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.apparatus_view_agg TO ntg_readonly;


--
-- Name: TABLE att; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.att TO ntg_readonly;


--
-- Name: TABLE cliques; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.cliques TO ntg_readonly;


--
-- Name: TABLE cliques_tts; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.cliques_tts TO ntg_readonly;


--
-- Name: TABLE readings_view; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.readings_view TO ntg_readonly;


--
-- Name: TABLE cliques_view; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.cliques_view TO ntg_readonly;


--
-- Name: TABLE export_cliques; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.export_cliques TO ntg_readonly;


--
-- Name: TABLE locstem; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.locstem TO ntg_readonly;


--
-- Name: TABLE locstem_tts; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.locstem_tts TO ntg_readonly;


--
-- Name: TABLE locstem_view; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.locstem_view TO ntg_readonly;


--
-- Name: TABLE export_locstem; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.export_locstem TO ntg_readonly;


--
-- Name: TABLE ms_cliques_tts; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.ms_cliques_tts TO ntg_readonly;


--
-- Name: TABLE ms_cliques_view; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.ms_cliques_view TO ntg_readonly;


--
-- Name: TABLE export_ms_cliques; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.export_ms_cliques TO ntg_readonly;


--
-- Name: TABLE notes; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.notes TO ntg_readonly;


--
-- Name: TABLE notes_tts; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.notes_tts TO ntg_readonly;


--
-- Name: TABLE notes_view; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.notes_view TO ntg_readonly;


--
-- Name: TABLE export_notes; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.export_notes TO ntg_readonly;


--
-- Name: TABLE import_cliques; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.import_cliques TO ntg_readonly;


--
-- Name: TABLE import_locstem; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.import_locstem TO ntg_readonly;


--
-- Name: TABLE import_ms_cliques; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.import_ms_cliques TO ntg_readonly;


--
-- Name: TABLE import_notes; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.import_notes TO ntg_readonly;


--
-- Name: TABLE lac; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.lac TO ntg_readonly;


--
-- Name: TABLE ms_ranges_view; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.ms_ranges_view TO ntg_readonly;


--
-- Name: TABLE nestle; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.nestle TO ntg_readonly;


--
-- Name: TABLE passages_view; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.passages_view TO ntg_readonly;


--
-- Name: TABLE passages_view_lemma; Type: ACL; Schema: ntg; Owner: ntg
--

GRANT SELECT ON TABLE ntg.passages_view_lemma TO ntg_readonly;


--
-- PostgreSQL database dump complete
--

