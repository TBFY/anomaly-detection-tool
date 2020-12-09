-- Table: public.mju_cpv

-- DROP TABLE public.mju_cpv;

CREATE TABLE public.mju_cpv
(
    code character varying(16) COLLATE pg_catalog."default" NOT NULL DEFAULT nextval('mju_cpv_code_seq'::regclass),
    bg text COLLATE pg_catalog."default",
    cs text COLLATE pg_catalog."default",
    da text COLLATE pg_catalog."default",
    de text COLLATE pg_catalog."default",
    el text COLLATE pg_catalog."default",
    en text COLLATE pg_catalog."default",
    es text COLLATE pg_catalog."default",
    et text COLLATE pg_catalog."default",
    fi text COLLATE pg_catalog."default",
    fr text COLLATE pg_catalog."default",
    ga text COLLATE pg_catalog."default",
    hr text COLLATE pg_catalog."default",
    hu text COLLATE pg_catalog."default",
    it text COLLATE pg_catalog."default",
    lt text COLLATE pg_catalog."default",
    lv text COLLATE pg_catalog."default",
    mt text COLLATE pg_catalog."default",
    nl text COLLATE pg_catalog."default",
    pl text COLLATE pg_catalog."default",
    pt text COLLATE pg_catalog."default",
    ro text COLLATE pg_catalog."default",
    sk text COLLATE pg_catalog."default",
    sl text COLLATE pg_catalog."default",
    sv text COLLATE pg_catalog."default",
    CONSTRAINT mju_cpv_pkey PRIMARY KEY (code)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.mju_cpv
    OWNER to matej;