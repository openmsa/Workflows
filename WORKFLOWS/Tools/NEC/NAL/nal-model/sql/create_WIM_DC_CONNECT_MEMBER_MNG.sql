-- DB Engine	
SET storage_engine=INNODB;	
	
-- create	
DROP TABLE IF EXISTS WIM_DC_CONNECT_MEMBER_MNG;	
	
CREATE TABLE WIM_DC_CONNECT_MEMBER_MNG (	
  create_id                     VARCHAR(64),	
  create_date                   DATETIME,	
  update_id                     VARCHAR(64),	
  update_date                   DATETIME,	
  delete_flg                    DECIMAL(1) DEFAULT 0 NOT NULL,	
  ID                            INT NOT NULL AUTO_INCREMENT,	
  extension_info                TEXT,	
  PRIMARY KEY(ID)	
);	
