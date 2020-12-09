-- Table: public.cst_companies_kg

-- DROP TABLE public.cst_companies_kg;

CREATE TABLE public.cst_companies_kg
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    country_name character varying(128) COLLATE pg_catalog."default",
    company_id character varying(64) COLLATE pg_catalog."default" NOT NULL,
    company_name character varying(256) COLLATE pg_catalog."default",
    CONSTRAINT cst_companies_kg_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.cst_companies_kg
    OWNER to matej;