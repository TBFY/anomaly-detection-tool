-- Table: public.mju_skd

-- DROP TABLE public.mju_skd;

CREATE TABLE public.mju_skd
(
    level smallint,
    code character varying(16) COLLATE pg_catalog."default",
    descriptor character varying(256) COLLATE pg_catalog."default",
    descriptor_en character varying(256) COLLATE pg_catalog."default",
    code_parent character varying(16) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE public.mju_skd
    OWNER to matej;