-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `Viajero_Frecuente` DEFAULT CHARACTER SET utf8 ;
USE `Viajero_Frecuente` ;

-- -----------------------------------------------------
-- Table `Viajero_Frecuente`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Viajero_Frecuente`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `apellido` VARCHAR(45) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Viajero_Frecuente`.`viajes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Viajero_Frecuente`.`viajes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(150) NOT NULL,
  `cupo` INT NOT NULL,
  `fecha` DATE NOT NULL,
  `fecha_fin` DATE NOT NULL,
  `descripcion` TEXT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `usuario_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_viajes_usuarios1_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_viajes_usuarios1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `Viajero_Frecuente`.`usuarios` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Viajero_Frecuente`.`inscripciones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Viajero_Frecuente`.`inscripciones` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `usuario_id` INT NOT NULL,
  `viaje_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `usuario_viaje_UNIQUE` (`usuario_id`, `viaje_id`) VISIBLE,
  INDEX `fk_usuarios_has_viajes_viajes1_idx` (`viaje_id` ASC) VISIBLE,
  INDEX `fk_usuarios_has_viajes_usuarios1_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_usuarios_has_viajes_usuarios1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `Viajero_Frecuente`.`usuarios` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_usuarios_has_viajes_viajes1`
    FOREIGN KEY (`viaje_id`)
    REFERENCES `Viajero_Frecuente`.`viajes` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
