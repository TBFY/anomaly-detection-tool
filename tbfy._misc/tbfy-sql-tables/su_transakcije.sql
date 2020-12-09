-- Table: public.su_transakcije

-- DROP TABLE public.su_transakcije;

CREATE TABLE public.su_transakcije
(
    podracun_v_breme text COLLATE pg_catalog."default",
    datum_transakcije date,
    znesek_transakcije numeric(16,4),
    oznaka_valute_transakcije text COLLATE pg_catalog."default",
    racun_v_dobro text COLLATE pg_catalog."default",
    naziv_prejemnika text COLLATE pg_catalog."default",
    maticna_stevilka text COLLATE pg_catalog."default",
    davcna_stevilka integer,
    sifra_pu integer,
    zr_sns_oe text COLLATE pg_catalog."default",
    namen text COLLATE pg_catalog."default",
    koda_namena text COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE public.su_transakcije
    OWNER to matej;
-- Index: idatum_transakcije_su_transakcije

-- DROP INDEX public.idatum_transakcije_su_transakcije;

CREATE INDEX idatum_transakcije_su_transakcije
    ON public.su_transakcije USING btree
    (datum_transakcije ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idavcna_stevilka_su_transakcije

-- DROP INDEX public.idavcna_stevilka_su_transakcije;

CREATE INDEX idavcna_stevilka_su_transakcije
    ON public.su_transakcije USING btree
    (davcna_stevilka ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: imaticna_stevilka_su_transakcije

-- DROP INDEX public.imaticna_stevilka_su_transakcije;

CREATE INDEX imaticna_stevilka_su_transakcije
    ON public.su_transakcije USING btree
    (maticna_stevilka COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: isifra_pu_su_transakcije

-- DROP INDEX public.isifra_pu_su_transakcije;

CREATE INDEX isifra_pu_su_transakcije
    ON public.su_transakcije USING btree
    (sifra_pu ASC NULLS LAST)
    TABLESPACE pg_default;