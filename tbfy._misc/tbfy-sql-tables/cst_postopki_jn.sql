-- Table: public.cst_postopki_jn

-- DROP TABLE public.cst_postopki_jn;

CREATE TABLE public.cst_postopki_jn
(
    vir character varying(64) COLLATE pg_catalog."default",
    letoobdelave smallint,
    izvajanjeos character varying(8) COLLATE pg_catalog."default",
    idizpobrazca bigint NOT NULL,
    jnstevilka character varying(256) COLLATE pg_catalog."default",
    cpv_naslovobjave text COLLATE pg_catalog."default",
    datumposiljanjaobvestila timestamp without time zone,
    datumobjaveobvestila timestamp without time zone,
    oznakaobrazca character varying(64) COLLATE pg_catalog."default",
    zakon character varying(64) COLLATE pg_catalog."default",
    kategorijanarocnika integer,
    kategorijanarocnika_naziv character varying(256) COLLATE pg_catalog."default",
    narocnikorganizacija character varying(256) COLLATE pg_catalog."default",
    narocnikorganizacijakratko character varying(256) COLLATE pg_catalog."default",
    narocnikmaticna character varying(32) COLLATE pg_catalog."default",
    narocnikdavcna character varying(32) COLLATE pg_catalog."default",
    narocniknaslov character varying(256) COLLATE pg_catalog."default",
    narocnikpostnastevilka character varying(16) COLLATE pg_catalog."default",
    narocnikkraj character varying(256) COLLATE pg_catalog."default",
    narocnik_id_sifnuts_koda character varying(64) COLLATE pg_catalog."default",
    narocnik_obcina character varying(256) COLLATE pg_catalog."default",
    narocnik_oblika character varying(256) COLLATE pg_catalog."default",
    narocnik_glavna_dejavnost_skd character varying(64) COLLATE pg_catalog."default",
    narocnik_glavna_dejavnost_skd_opis character varying(256) COLLATE pg_catalog."default",
    narocnik_vrsta_lastnine character varying(256) COLLATE pg_catalog."default",
    narocnik_poreklo_kapitala character varying(256) COLLATE pg_catalog."default",
    narocnik_velik_rs character varying(256) COLLATE pg_catalog."default",
    narocnik_velik_eu character varying(256) COLLATE pg_catalog."default",
    narocnik_regija character varying(256) COLLATE pg_catalog."default",
    narocnik_prorup character varying(32) COLLATE pg_catalog."default",
    narocnik_zavezanec_po_zakonu character varying(32) COLLATE pg_catalog."default",
    narocnik_dejavnost character varying(256) COLLATE pg_catalog."default",
    vimenudrugih character varying(256) COLLATE pg_catalog."default",
    vrstanarocila character varying(256) COLLATE pg_catalog."default",
    kategorijastoritve character varying(256) COLLATE pg_catalog."default",
    naslovnarocilanarocnik text COLLATE pg_catalog."default",
    opisnarocilanarocnik text COLLATE pg_catalog."default",
    vrstapostopka character varying(256) COLLATE pg_catalog."default",
    vrstapostopka_eu character varying(256) COLLATE pg_catalog."default",
    merila character varying(256) COLLATE pg_catalog."default",
    okvirnisporazum character varying(16) COLLATE pg_catalog."default",
    skolikoos character varying(256) COLLATE pg_catalog."default",
    skupnonarocanje character varying(16) COLLATE pg_catalog."default",
    skupnonarocanjenosilecmaticna character varying(64) COLLATE pg_catalog."default",
    skupnonarocanjenosilecorganizacija character varying(256) COLLATE pg_catalog."default",
    subvstanprogram text COLLATE pg_catalog."default",
    eusredstva character varying(32) COLLATE pg_catalog."default",
    euprojekt text COLLATE pg_catalog."default",
    objavaveu character varying(32) COLLATE pg_catalog."default",
    idizppriloge character varying(128) COLLATE pg_catalog."default" NOT NULL,
    naslovsklopa text COLLATE pg_catalog."default",
    datumoddajesklopa date,
    stprejetihponudb smallint,
    stprejetiheponudb smallint,
    skupnaponudba character varying(32) COLLATE pg_catalog."default",
    ocenjenavrednost double precision,
    ocenjenavrednostvaluta character varying(16) COLLATE pg_catalog."default",
    ocenjenavrednostzddv character varying(64) COLLATE pg_catalog."default",
    ocenjenavrednoststopnjaddv character varying(128) COLLATE pg_catalog."default",
    koncnavrednost double precision,
    koncnavrednostvaluta character varying(16) COLLATE pg_catalog."default",
    koncnavrednostzddv character varying(64) COLLATE pg_catalog."default",
    koncnavrednoststopnjaddv character varying(128) COLLATE pg_catalog."default",
    trajanje_meseci character varying(256) COLLATE pg_catalog."default",
    rokveljavnostipogodbe character varying(256) COLLATE pg_catalog."default",
    oddanopodizvajalcem character varying(32) COLLATE pg_catalog."default",
    oddanopodizvajalcemvrednostbrezddv character varying(128) COLLATE pg_catalog."default",
    oddanopodizvajalcemvrednostvaluta character varying(16) COLLATE pg_catalog."default",
    oddanopodizvajalcemdelez character varying(256) COLLATE pg_catalog."default",
    oddanopodizvajalcemvrednostneznana character varying(32) COLLATE pg_catalog."default",
    oddanopodizvajalcemopis text COLLATE pg_catalog."default",
    okoljskividik character varying(32) COLLATE pg_catalog."default",
    okoljskividikzelenojavnonarocanje character varying(32) COLLATE pg_catalog."default",
    okoljski_mehanizem_drugo text COLLATE pg_catalog."default",
    okoljski_mehanizem_vsota character varying(128) COLLATE pg_catalog."default",
    socialnividik character varying(16) COLLATE pg_catalog."default",
    socialni_vidik_drugo text COLLATE pg_catalog."default",
    socialni_vidik_vsota character varying(64) COLLATE pg_catalog."default",
    cpv_glavni character varying(32) COLLATE pg_catalog."default",
    cpv_glavni_2mesti character varying(4) COLLATE pg_catalog."default",
    brezodpiranja_konkurenceos text COLLATE pg_catalog."default",
    izlocitev_neobicajno_nizke_ponudbe text COLLATE pg_catalog."default",
    variantna_ponudba text COLLATE pg_catalog."default",
    drzava_porekla_blaga_storitve text COLLATE pg_catalog."default",
    pravila_za_izbiro_podizvajalcev text COLLATE pg_catalog."default",
    obvezna_vkljucitev_podizvajalcev text COLLATE pg_catalog."default",
    obvezno_podizvajalci_delez_max text COLLATE pg_catalog."default",
    podrocja_zjnvetps_vsota text COLLATE pg_catalog."default",
    pd_utemeljitev_pogajanj text COLLATE pg_catalog."default",
    gpp_toolkit text COLLATE pg_catalog."default",
    priloga_uredbe_zejn character varying(128) COLLATE pg_catalog."default",
    priloga_uredbe_zejn_cpv character varying(64) COLLATE pg_catalog."default",
    prejsnje_objave_pjn character varying(256) COLLATE pg_catalog."default",
    prejsnje_objave_pjn_datum timestamp without time zone,
    prejsnje_objave_uleu character varying(256) COLLATE pg_catalog."default",
    prejsnje_objave_uleu_datum timestamp without time zone,
    obveznost_objave_uleu character varying(16) COLLATE pg_catalog."default",
    wwwobjave character varying(256) COLLATE pg_catalog."default",
    characterization text COLLATE pg_catalog."default",
    d_drugeutemeljitve text COLLATE pg_catalog."default",
    dodatnekodecpv text COLLATE pg_catalog."default",
    elektronskadrazba character varying(16) COLLATE pg_catalog."default",
    narocilojeoddano character varying(16) COLLATE pg_catalog."default",
    natecajzakljucenbrezpodelitvenagrad character varying(256) COLLATE pg_catalog."default",
    nmvseoddajanasplosnempodrocju character varying(16) COLLATE pg_catalog."default",
    objavilenapjn character varying(16) COLLATE pg_catalog."default",
    obrazecpredmetsklop_naslov text COLLATE pg_catalog."default",
    obrazecpredmetsklop_opis text COLLATE pg_catalog."default",
    obvezno_podizvajalci_delez_min text COLLATE pg_catalog."default",
    podrocje character varying(256) COLLATE pg_catalog."default",
    pd_utemeljitev_pogajanj_eu text COLLATE pg_catalog."default",
    podrocja_zjnvetps_eu text COLLATE pg_catalog."default",
    pospesenipostopekutemeljitev text COLLATE pg_catalog."default",
    sifrapd text COLLATE pg_catalog."default",
    sklopi character varying(16) COLLATE pg_catalog."default",
    skupnojavnonarocanjecentralniorganzanabavo character varying(16) COLLATE pg_catalog."default",
    sporazumovladnihnarocilih character varying(16) COLLATE pg_catalog."default",
    stevilkasklopa text COLLATE pg_catalog."default",
    steviloponudnikovizlocenihzaradipravnomocneobsodbe character varying(16) COLLATE pg_catalog."default",
    steviloprejetihponudbdrugihclaniceu character varying(16) COLLATE pg_catalog."default",
    steviloprejetihponudbmsp character varying(16) COLLATE pg_catalog."default",
    steviloprejetihponudbneclaniceu character varying(16) COLLATE pg_catalog."default",
    stevilkaobjaveeu character varying(256) COLLATE pg_catalog."default",
    prejsnje_objave_rokzasprejemanjeponudnikovihvprasanj timestamp without time zone,
    prejsnje_objave_rokzaprejemponudb timestamp without time zone,
    prejsnje_objave_odpiranjeponudbdatum timestamp with time zone,
    prejsnje_objave_sys_spremembaizracunanihdatum timestamp with time zone,
    vrstapostopkaizracunan text COLLATE pg_catalog."default",
    sys_spremembaizracunanihdatum timestamp without time zone,
    dinamicninabavnisistemvzpostavitev character varying(32) COLLATE pg_catalog."default",
    popravekobrazca text COLLATE pg_catalog."default",
    popravljenspopravkom text COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE public.cst_postopki_jn
    OWNER to matej;
-- Index: idizppriloge_index

-- DROP INDEX public.idizppriloge_index;

CREATE INDEX idizppriloge_index
    ON public.cst_postopki_jn USING btree
    (idizppriloge COLLATE pg_catalog."default" varchar_ops ASC NULLS LAST)
    TABLESPACE pg_default;