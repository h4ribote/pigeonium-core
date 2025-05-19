-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;

CREATE TABLE `balance` (
  `address` binary(16) NOT NULL,
  `currencyId` binary(16) NOT NULL,
  `amount` bigint UNSIGNED NOT NULL
);

CREATE TABLE `contract` (
  `address` binary(16) NOT NULL,
  `script` text COLLATE utf8mb4_0900_as_cs NOT NULL
);

CREATE TABLE `currency` (
  `currencyId` binary(16) NOT NULL,
  `name` varchar(32) COLLATE utf8mb4_0900_as_cs NOT NULL,
  `symbol` varchar(8) COLLATE utf8mb4_0900_as_cs NOT NULL,
  `issuer` binary(16) NOT NULL,
  `supply` bigint UNSIGNED NOT NULL
);

CREATE TABLE `transaction` (
  `indexId` bigint UNSIGNED NOT NULL,
  `source` binary(16) NOT NULL,
  `dest` binary(16) NOT NULL,
  `currencyId` binary(16) NOT NULL,
  `amount` bigint UNSIGNED NOT NULL,
  `feeAmount` bigint UNSIGNED NOT NULL,
  `inputData` varbinary(64) NOT NULL,
  `publicKey` binary(64) NOT NULL,
  `isContract` tinyint(1) NOT NULL,
  `signature` binary(64) NOT NULL,
  `timestamp` bigint NOT NULL,
  `adminSignature` binary(64) NOT NULL
);

CREATE TABLE `variable` (
  `address` binary(16) NOT NULL,
  `varKey` binary(16) NOT NULL,
  `varValue` binary(16) NOT NULL
);

ALTER TABLE `balance`
  ADD UNIQUE KEY `balance` (`address`,`currencyId`);

ALTER TABLE `currency`
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `symbol` (`symbol`),
  ADD UNIQUE KEY `currencyId` (`currencyId`),
  ADD UNIQUE KEY `issuer` (`issuer`);

ALTER TABLE `transaction`
  ADD UNIQUE KEY `indexId` (`indexId`),
  ADD UNIQUE KEY `signature` (`signature`);

ALTER TABLE `variable`
  ADD UNIQUE KEY `var` (`address`,`varKey`);

COMMIT;
