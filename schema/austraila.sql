CREATE TABLE `austraila_data` (
  `id` int(11) DEFAULT NULL,
  `website` varchar(255) DEFAULT NULL,
  `company_name` varchar(150) DEFAULT NULL,
  `country` varchar(150) DEFAULT NULL,
  `City` varchar(60) DEFAULT NULL,
  `State` varchar(60) DEFAULT NULL,
  `Postalcode` varchar(50) DEFAULT NULL,
  `Street` varchar(150) DEFAULT NULL,
  `telephone` varchar(50) DEFAULT NULL,
  `ParentCompanyname` varchar(50) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `austraila_api_New` (
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
  `score` varchar(10) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



