CREATE TABLE `Newzealand_data` (
  `Id` int(11) DEFAULT NULL,
  `system_id` varchar(150) DEFAULT NULL,
  `system_name` varchar(45) DEFAULT NULL,
  `website` varchar(150) DEFAULT NULL,
  `company_name` varchar(150) DEFAULT NULL,
  `country` varchar(150) DEFAULT NULL,
  `city` varchar(150) DEFAULT NULL,
  `state_province` varchar(150) DEFAULT NULL,
  `postal_code` varchar(45) DEFAULT NULL,
  `address_line_1` varchar(150) DEFAULT NULL,
  `telephone` varchar(150) DEFAULT NULL,
  `parentCompanyName` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Newzealand_api` (
  `Id` int(11) DEFAULT NULL,
  `CompanyName` varchar(150) DEFAULT NULL,
  `StreetAddress1` varchar(150) DEFAULT NULL,
  `City` varchar(150) DEFAULT NULL,
  `State` varchar(150) DEFAULT NULL,
  `PostalCode` varchar(150) DEFAULT NULL,
  `Country` varchar(150) DEFAULT NULL,
  `Srch_CompanyName` varchar(150) DEFAULT NULL,
  `Srch_RawAddress` text,
  `Srch_APIURL` text,
  `Srch_Source` varchar(45) DEFAULT NULL,
  `Created_dt` date DEFAULT NULL,
  `Srch_StreetAddress` text,
  `Srch_City` varchar(150) DEFAULT NULL,
  `Srch_State` varchar(150) DEFAULT NULL,
  `Srch_Country` varchar(150) DEFAULT NULL,
  `Srch_PostalCode` varchar(150) DEFAULT NULL,
  `PhoneNumber` varchar(45) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

