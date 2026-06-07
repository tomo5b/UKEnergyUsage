CREATE TABLE IF NOT EXISTS grid_national (
    ts                  TIMESTAMPTZ PRIMARY KEY,
    intensity_forecast  INTEGER,
    intensity_actual    INTEGER,
    intensity_index     TEXT,
    generation_mix      JSONB
);

CREATE TABLE IF NOT EXISTS grid_regional (
    ts                  TIMESTAMPTZ NOT NULL,
    region_shortname    TEXT        NOT NULL,
    intensity_forecast  INTEGER,
    intensity_actual    INTEGER,
    intensity_index     TEXT,
    PRIMARY KEY (ts, region_shortname)
);
