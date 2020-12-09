-- Table: public.cst_postopki_jn_izvajalci

-- DROP TABLE public.cst_postopki_jn_izvajalci;

CREATE TABLE public.cst_postopki_jn_izvajalci
(
    idizpobrazca bigint,
    idizppriloge bigint,
    id_obrazecsubjekt bigint,
    zaporedna smallint,
    ponudniktipsubjekta character varying(16) COLLATE pg_catalog."default",
    ponudnikorganizacija character varying(256) COLLATE pg_catalog."default",
    ponudnikorganizacijakratko character varying(256) COLLATE pg_catalog."default",
    ponudnikmaticna character varying(64) COLLATE pg_catalog."default",
    ponudnikdavcna character varying(64) COLLATE pg_catalog."default",
    ponudniknaslov character varying(256) COLLATE pg_catalog."default",
    ponudnikpostnastevilka character varying(64) COLLATE pg_catalog."default",
    ponudnikkraj character varying(256) COLLATE pg_catalog."default",
    ponudnikdrzava character varying(128) COLLATE pg_catalog."default",
    ponudnikdrzava_oznaka character varying(32) COLLATE pg_catalog."default",
    ponudnik_obcina character varying(256) COLLATE pg_catalog."default",
    ponudnik_oblika character varying(256) COLLATE pg_catalog."default",
    ponudnik_glavna_dejavnost_skd character varying(64) COLLATE pg_catalog."default",
    ponudnik_vrsta_lastnine character varying(256) COLLATE pg_catalog."default",
    ponudnik_poreklo_kapitala character varying(256) COLLATE pg_catalog."default",
    ponudnik_velik_rs character varying(256) COLLATE pg_catalog."default",
    ponudnik_velik_eu character varying(256) COLLATE pg_catalog."default",
    ponudnik_regija character varying(256) COLLATE pg_catalog."default",
    ponudnik_prorup character varying(64) COLLATE pg_catalog."default",
    ponudnik_regija_narocnika character varying(256) COLLATE pg_catalog."default",
    ponudnik_url character varying(256) COLLATE pg_catalog."default",
    subjektjemsp character varying(8) COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.cst_postopki_jn_izvajalci
    OWNER to matej;

-- Index: id_obrazecsubjekt_index

-- DROP INDEX public.id_obrazecsubjekt_index;

CREATE INDEX id_obrazecsubjekt_index
    ON public.cst_postopki_jn_izvajalci USING btree
    (id_obrazecsubjekt)
    TABLESPACE pg_default;