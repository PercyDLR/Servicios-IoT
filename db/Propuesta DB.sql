-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema IoT_DB
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `IoT_DB` ;

-- -----------------------------------------------------
-- Schema IoT_DB
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `IoT_DB` ;
USE `IoT_DB` ;

-- -----------------------------------------------------
-- Table `IoT_DB`.`lugar`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `IoT_DB`.`lugar` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NULL,
  `latitud` FLOAT NULL,
  `longitud` FLOAT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `IoT_DB`.`medicion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `IoT_DB`.`medicion` (
  `id` INT(11) GENERATED ALWAYS AS (),
  `id_lugar` INT(11) NOT NULL,
  `temp_avg` FLOAT NOT NULL,
  `humedad_avg` FLOAT NOT NULL,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_medicion_lugar1_idx` (`id_lugar` ASC) VISIBLE,
  CONSTRAINT `fk_medicion_lugar1`
    FOREIGN KEY (`id_lugar`)
    REFERENCES `IoT_DB`.`lugar` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `IoT_DB`.`sensor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `IoT_DB`.`sensor` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `id_lugar` INT(11) NOT NULL,
  `nombre` VARCHAR(255) NULL DEFAULT NULL,
  `estado` TINYINT(1) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_sensor_lugar1_idx` (`id_lugar` ASC) VISIBLE,
  CONSTRAINT `fk_sensor_lugar1`
    FOREIGN KEY (`id_lugar`)
    REFERENCES `IoT_DB`.`lugar` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `IoT_DB`.`bateria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `IoT_DB`.`bateria` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_sensor` INT(11) NOT NULL,
  `valor` FLOAT NOT NULL,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_bateria_sensor1_idx` (`id_sensor` ASC) VISIBLE,
  CONSTRAINT `fk_bateria_sensor1`
    FOREIGN KEY (`id_sensor`)
    REFERENCES `IoT_DB`.`sensor` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
