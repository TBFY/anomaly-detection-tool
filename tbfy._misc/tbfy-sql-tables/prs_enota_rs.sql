-- Table: public.prs_enota_rs

-- DROP TABLE public.prs_enota_rs;

CREATE TABLE public.prs_enota_rs
(
    enota numeric(9,0),
    maticna character varying(10) COLLATE pg_catalog."default",
    popolno_ime character varying(250) COLLATE pg_catalog."default",
    kratko_ime character varying(140) COLLATE pg_catalog."default",
    regija_sif character varying(2) COLLATE pg_catalog."default",
    regija character varying(40) COLLATE pg_catalog."default",
    upr_enota_sif character varying(4) COLLATE pg_catalog."default",
    upr_enota character varying(40) COLLATE pg_catalog."default",
    obcina_sif character varying(3) COLLATE pg_catalog."default",
    obcina character varying(40) COLLATE pg_catalog."default",
    naselje_sif character varying(3) COLLATE pg_catalog."default",
    naselje character varying(40) COLLATE pg_catalog."default",
    ulica_sif character varying(4) COLLATE pg_catalog."default",
    ulica character varying(40) COLLATE pg_catalog."default",
    ulica_hs character varying(4) COLLATE pg_catalog."default",
    ulica_hs_d character varying(1) COLLATE pg_catalog."default",
    postna_stevilka character varying(4) COLLATE pg_catalog."default",
    postni_kraj character varying(40) COLLATE pg_catalog."default",
    hs_mid numeric(10,0),
    reg_organ_sif character varying(4) COLLATE pg_catalog."default",
    reg_organ character varying(80) COLLATE pg_catalog."default",
    datum_vpisa timestamp with time zone,
    stevilka_vpisa character varying(30) COLLATE pg_catalog."default",
    zap_vpisa numeric(5,0),
    oblika_sif character varying(3) COLLATE pg_catalog."default",
    oblika character varying(80) COLLATE pg_catalog."default",
    podoblika_sif character varying(3) COLLATE pg_catalog."default",
    podoblika character varying(80) COLLATE pg_catalog."default",
    glavna_dejavnost_skd character varying(6) COLLATE pg_catalog."default",
    skis character varying(5) COLLATE pg_catalog."default",
    poreklo_kapitala_sif character varying(1) COLLATE pg_catalog."default",
    poreklo_kapitala character varying(60) COLLATE pg_catalog."default",
    vrsta_lastnine_sif character varying(1) COLLATE pg_catalog."default",
    vrsta_lastnine character varying(80) COLLATE pg_catalog."default",
    id_ddv character varying(2) COLLATE pg_catalog."default",
    st_davcna numeric(10,0),
    prorup character varying(5) COLLATE pg_catalog."default",
    zav_zdijz character varying(1) COLLATE pg_catalog."default",
    velik_eu_sif character varying(2) COLLATE pg_catalog."default",
    velik_eu character varying(60) COLLATE pg_catalog."default",
    velik_rs_sif character varying(1) COLLATE pg_catalog."default",
    velik_rs character varying(60) COLLATE pg_catalog."default",
    aktivnost_sif character varying(1) COLLATE pg_catalog."default",
    aktivnost character varying(40) COLLATE pg_catalog."default",
    vrsta_spremembe_sif character varying(3) COLLATE pg_catalog."default",
    vrsta_spremembe character varying(100) COLLATE pg_catalog."default",
    datum_spremembe timestamp with time zone,
    datum_vnosa timestamp with time zone,
    ajpes_izp_sif character varying(2) COLLATE pg_catalog."default",
    ajpes_izp character varying(100) COLLATE pg_catalog."default",
    drustvo_sif character varying(4) COLLATE pg_catalog."default",
    drustvo character varying(100) COLLATE pg_catalog."default",
    osnovni_kapital numeric(20,2),
    sifra_valute character varying(3) COLLATE pg_catalog."default",
    tip_kapitala_sif character varying(2) COLLATE pg_catalog."default",
    tip_kapitala character varying(100) COLLATE pg_catalog."default",
    vrsta_organa_sif character varying(2) COLLATE pg_catalog."default",
    vrsta_organa character varying(50) COLLATE pg_catalog."default",
    zbrisano character varying(1) COLLATE pg_catalog."default",
    sedez character varying(40) COLLATE pg_catalog."default",
    poseben_status_sif character varying(2) COLLATE pg_catalog."default",
    poseben_status character varying(80) COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.prs_enota_rs
    OWNER to matej;

-- Index: maticna_index

-- DROP INDEX public.maticna_index;

CREATE INDEX maticna_index
    ON public.prs_enota_rs USING btree
    (maticna COLLATE pg_catalog."default")
    TABLESPACE pg_default;