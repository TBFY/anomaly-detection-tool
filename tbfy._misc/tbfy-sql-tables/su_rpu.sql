-- Table: public.su_rpu

-- DROP TABLE public.su_rpu;

CREATE TABLE public.su_rpu
(
    tip text COLLATE pg_catalog."default",
    skupina text COLLATE pg_catalog."default",
    podskupina text COLLATE pg_catalog."default",
    sifra_pu integer,
    maticna text COLLATE pg_catalog."default",
    davcna integer,
    ustanovitelj text COLLATE pg_catalog."default",
    naziv text COLLATE pg_catalog."default",
    kraj text COLLATE pg_catalog."default",
    obcina text COLLATE pg_catalog."default",
    skd text COLLATE pg_catalog."default",
    a text COLLATE pg_catalog."default",
    b text COLLATE pg_catalog."default",
    c text COLLATE pg_catalog."default",
    d text COLLATE pg_catalog."default",
    e text COLLATE pg_catalog."default",
    f text COLLATE pg_catalog."default",
    g text COLLATE pg_catalog."default",
    h text COLLATE pg_catalog."default",
    i text COLLATE pg_catalog."default",
    j text COLLATE pg_catalog."default",
    naslov text COLLATE pg_catalog."default",
    postna_stevilka text COLLATE pg_catalog."default",
    posta text COLLATE pg_catalog."default",
    ezr text COLLATE pg_catalog."default",
    sifra_proracuna text COLLATE pg_catalog."default",
    izbrisan boolean,
    kategorija text COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE public.su_rpu
    OWNER to matej;