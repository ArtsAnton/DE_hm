select wealth.COUNTRY, wealth.GDP, education.LITERACY from wealth JOIN education ON wealth.COUNTRY = education.COUNTRY ORDER BY 2;

select wealth.COUNTRY, wealth.GDP, area.AGRICULTURE from wealth JOIN area ON wealth.COUNTRY = area.COUNTRY ORDER BY 2;


SELECT code.COUNTRY, capital.CAPITAL, code.ISO3, capital.ISO2, code.CURRENCY, code.PHONE
FROM code
    JOIN capital on code.COUNTRY = capital.COUNTRY;

SELECT a.COUNTRY, w.GDP, a.INDUSTRY, a.SERVICE, a.AGRICULTURE, l.ARABLE, l.COUNTRY, l.OTHER
FROM area a
    JOIN land l on a.COUNTRY = l.COUNTRY
    JOIN wealth w ON a.COUNTRY = w.COUNTRY;