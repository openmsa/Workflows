-- DB Engine
SET storage_engine=INNODB;

-- create
DROP TABLE IF EXISTS NAL_VIRTUAL_LAN_MNG;

CREATE TABLE NAL_VIRTUAL_LAN_MNG (
  create_id                     VARCHAR(64),
  create_date                   DATETIME,
  update_id                     VARCHAR(64),
  update_date                   DATETIME,
  delete_flg                    DECIMAL(1) DEFAULT 0 NOT NULL,
  ID                            INT NOT NULL AUTO_INCREMENT,
  network_id                    VARCHAR(64) NOT NULL,
  extension_info                TEXT,
  PRIMARY KEY(ID)
);
