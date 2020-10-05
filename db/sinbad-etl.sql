-----------------------------
----------- VIEW -----------
-----------------------------

CREATE TYPE SF_COMPLIANT AS ENUM (
    'COMPLIANT',
    'NON-COMPLIANT',
    'YELLOW'
);

-----------------------------
----------- TABLE -----------
-----------------------------

CREATE EXTENSION IF NOT EXISTS citext WITH SCHEMA public;

COMMENT ON EXTENSION citext IS 'data type for case-insensitive character strings';

CREATE TABLE public.sf_companies (
  sf_company_id         SERIAL PRIMARY KEY,
  sf_act_symbol         citext NOT NULL UNIQUE,
  sf_company_name       citext NOT NULL,
  sf_security_name      TEXT,
  sf_exchange           TEXT,
  sf_cqs_symbol         TEXT,
  sf_etf                TEXT,
  sf_round_lot_size     DECIMAL,
  sf_test_issue         TEXT,
  sf_nasdaq_symbol      TEXT,
  sf_aaoifi_compliant   SF_COMPLIANT NOT NULL DEFAULT 'YELLOW',
  sf_nc_reason          TEXT,
  sf_last_screened      TIMESTAMP DEFAULT NOW(),
  sf_created            TIMESTAMP DEFAULT NOW(),
  sf_updated            TIMESTAMP DEFAULT NOW()
);

ALTER TABLE public.sf_companies OWNER TO sinbad;

CREATE OR REPLACE FUNCTION company_updated() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW.sf_updated := now();
  NEW.sf_last_screened := now();
  RAISE NOTICE 'Data changed for ''sf_companies'' ''%'' on %', OLD.sf_updated, NEW.sf_updated;
  RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_company_updated
  BEFORE UPDATE ON sf_companies
  FOR EACH ROW
  EXECUTE PROCEDURE company_updated();