SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `DBProject` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `DBProject` ;

-- -----------------------------------------------------
-- Table `DBProject`.`Users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DBProject`.`Users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(100) NULL,
  `email` VARCHAR(100) NOT NULL,
  `name` VARCHAR(100) NULL,
  `about` VARCHAR(200) NULL,
  `isAnonymous` TINYINT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC));


-- -----------------------------------------------------
-- Table `DBProject`.`Forums`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DBProject`.`Forums` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(150) NULL,
  `short_name` VARCHAR(150) NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Forums_Users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_Forums_Users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `DBProject`.`Users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DBProject`.`Threads`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DBProject`.`Threads` (
  `id` INT NOT NULL,
  `title` VARCHAR(150) NOT NULL,
  `date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `message` TEXT NULL,
  `slug` VARCHAR(150) NULL,
  `isClosed` TINYINT NULL DEFAULT 0,
  `isDeleted` TINYINT NULL DEFAULT 0,
  `user_id` INT NOT NULL,
  `forum_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Thread_Users_idx` (`user_id` ASC),
  INDEX `fk_Thread_Forums1_idx` (`forum_id` ASC),
  CONSTRAINT `fk_Thread_Users`
    FOREIGN KEY (`user_id`)
    REFERENCES `DBProject`.`Users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Thread_Forums1`
    FOREIGN KEY (`forum_id`)
    REFERENCES `DBProject`.`Forums` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DBProject`.`Posts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DBProject`.`Posts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `message` TEXT NULL,
  `isApproved` TINYINT NULL DEFAULT 0,
  `isHighlighted` TINYINT NULL DEFAULT 0,
  `isEdited` TINYINT NULL DEFAULT 0,
  `isSpam` TINYINT NULL DEFAULT 0,
  `isDeleted` TINYINT NULL DEFAULT 0,
  `post_id` INT NULL DEFAULT NULL,
  `user_id` INT NOT NULL,
  `forum_id` INT NOT NULL,
  `thread_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Post_Post1_idx` (`post_id` ASC),
  INDEX `fk_Post_Users1_idx` (`user_id` ASC),
  INDEX `fk_Post_Forums1_idx` (`forum_id` ASC),
  INDEX `fk_Post_Thread1_idx` (`thread_id` ASC),
  CONSTRAINT `fk_Post_Post1`
    FOREIGN KEY (`post_id`)
    REFERENCES `DBProject`.`Posts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Post_Users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `DBProject`.`Users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Post_Forums1`
    FOREIGN KEY (`forum_id`)
    REFERENCES `DBProject`.`Forums` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Post_Thread1`
    FOREIGN KEY (`thread_id`)
    REFERENCES `DBProject`.`Threads` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
