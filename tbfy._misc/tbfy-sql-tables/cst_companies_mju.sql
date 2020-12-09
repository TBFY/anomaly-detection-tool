-- Table: public.cst_companies_mju

-- DROP TABLE public.cst_companies_mju;

CREATE TABLE public.cst_companies_mju
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    company_id character varying(12) COLLATE pg_catalog."default" NOT NULL,
    company_name character varying(256) COLLATE pg_catalog."default",
    CONSTRAINT cst_companies_mju_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.cst_companies_mju
    OWNER to matej;