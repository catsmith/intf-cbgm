-- CREATE USER ntg CREATEDB PASSWORD 'topsecret';
-- CREATE ROLE ntg_readonly;
-- CREATE DATABASE ntg_user OWNER ntg;
-- CREATE DATABASE mark_ph31 OWNER ntg;
-- \c mark_ph31
-- CREATE SCHEMA ntg AUTHORIZATION ntg;
-- ALTER DATABASE mark_ph31 SET search_path = ntg, public;
--CREATE EXTENSION mysql_fdw;
--GRANT USAGE ON FOREIGN DATA WRAPPER mysql_fdw TO ntg;


CREATE USER ntg CREATEDB PASSWORD 'topsecret';
CREATE ROLE ntg_readonly;
CREATE DATABASE ntg_user OWNER ntg;
CREATE DATABASE gal_ph1 OWNER ntg;
\c gal_ph1
CREATE SCHEMA ntg AUTHORIZATION ntg;
ALTER DATABASE gal_ph1 SET search_path = ntg, public;
--CREATE EXTENSION mysql_fdw;
--GRANT USAGE ON FOREIGN DATA WRAPPER mysql_fdw TO ntg;
