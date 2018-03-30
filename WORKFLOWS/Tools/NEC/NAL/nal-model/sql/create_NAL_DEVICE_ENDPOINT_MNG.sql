-- DB Engine
SET storage_engine=INNODB;

-- create
DROP TABLE IF EXISTS NAL_DEVICE_ENDPOINT_MNG;

CREATE TABLE NAL_DEVICE_ENDPOINT_MNG (
  create_id                     VARCHAR(64),
  create_date                   DATETIME,
  update_id                     VARCHAR(64),
  update_date                   DATETIME,
  delete_flg                    DECIMAL(1) DEFAULT 0 NOT NULL,
  ID                            INT NOT NULL AUTO_INCREMENT,
  extension_info                TEXT,
  PRIMARY KEY(ID)
);
