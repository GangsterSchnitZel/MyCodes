-- Keep a log of any SQL queries you execute as you solve the mystery.
--All you know is that the theft took place on July 28, 2021 and that it took place on Humphrey Street.


--Run .tables to get an overview.
.tables
--Run .schema to see wich structure is inside of the tables.
.schema
--Look through crime_scene_reports
SELECT * FROM crime_scene_reports;
-- | 295 | 2021 | 7     | 28  | Humphrey Street      |
--Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
--Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.
--Look through the interviews for the three witnesses.
SELECT * FROM interviews;
-- Interview1:  Ruth| 2021 | 7     | 28  | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
--If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
--Interview2: Eugene      | 2021 | 7     | 28  | I don't know the thief's name, but it was someone I recognized.
--Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
--Interview3: Raymond     | 2021 | 7     | 28  | As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
--In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
--The thief then asked the person on the other end of the phone to purchase the flight ticket.

--Look ath the ATM transactions to see if the thief was withdrawing some money the morning on Leggett Street
SELECT * FROM atm_transactions WHERE atm_location = 'Leggett Street';
246  | 28500762       | 2021 | 7     | 28  | Leggett Street | withdraw         | 48     |
| 264  | 28296815       | 2021 | 7     | 28  | Leggett Street | withdraw         | 20     |
| 266  | 76054385       | 2021 | 7     | 28  | Leggett Street | withdraw         | 60     |
| 267  | 49610011       | 2021 | 7     | 28  | Leggett Street | withdraw         | 50     |
| 269  | 16153065       | 2021 | 7     | 28  | Leggett Street | withdraw         | 80     |
| 275  | 86363979       | 2021 | 7     | 28  | Leggett Street | deposit          | 10     |
| 288  | 25506511       | 2021 | 7     | 28  | Leggett Street | withdraw         | 20     |
| 313  | 81061156       | 2021 | 7     | 28  | Leggett Street | withdraw         | 30     |
| 336  | 26013199       | 2021 | 7     | 28  | Leggett Street | withdraw         | 35     |
--Check for license plates that left the area in a range from 10 minutes after the theft from 10:15
SELECT * FROM bakery_security_logs WHERE year = '2021' AND month = '7' AND day = '28';
| id  | year | month | day | hour | minute | activity | license_plate
| 254 | 2021 | 7     | 28  | 9    | 14     | entrance | 4328GD8       |
| 255 | 2021 | 7     | 28  | 9    | 15     | entrance | 5P2BI95       |
| 256 | 2021 | 7     | 28  | 9    | 20     | entrance | 6P58WS2       |
| 257 | 2021 | 7     | 28  | 9    | 28     | entrance | G412CB7
-- Check the license plates in the people register
SELECT * FROM people WHERE license_plate = '4328GD8';
SELECT * FROM people WHERE license_plate = '5P2BI95';
SELECT * FROM people WHERE license_plate = '6P58WS2';
SELECT * FROM people WHERE license_plate = 'G412CB7';
|   id   | name |  phone_number  | passport_number | license_plate |
+--------+------+----------------+-----------------+---------------+
| 467400 | Luca | (389) 555-5198 | 8496433585      | 4328GD8       |
221103 | Vanessa | (725) 555-4692 | 2963008352      | 5P2BI95
 243696 | Barry | (301) 555-4174 | 7526138472      | 6P58WS2
 398010 | Sofia | (130) 555-0289 | 1695452385      | G412CB7

 --Check with bank account number who withdrawal money this morning and was in the parking lot
SELECT * FROM bank_accounts WHERE account_number = 28500762;
SELECT * FROM bank_accounts WHERE account_number = 28296815 ;
SELECT * FROM bank_accounts WHERE account_number = 76054385 ;
SELECT * FROM bank_accounts WHERE account_number = 49610011 ;
SELECT * FROM bank_accounts WHERE account_number = 16153065;
SELECT * FROM bank_accounts WHERE account_number = 86363979;
SELECT * FROM bank_accounts WHERE account_number = 25506511;
SELECT * FROM bank_accounts WHERE account_number = 81061156;
SELECT * FROM bank_accounts WHERE account_number = 26013199;
| account_number | person_id | creation_year |
+----------------+-----------+---------------+
| 28500762       | 467400    | 2014          |
| 28296815       | 395717    | 2014          |
| 76054385       | 449774    | 2015          |
| 49610011       | 686048    | 2010          |
| 16153065       | 458378    | 2012          |
| 86363979       | 948985    | 2010          |
| 25506511       | 396669    | 2014          |
| 81061156       | 438727    | 2018          |
| 26013199       | 514354    | 2012          |
--check full names with person_id
SELECT * FROM people WHERE id = 467400;
SELECT * FROM people WHERE id = 395717;
SELECT * FROM people WHERE id = 449774;
SELECT * FROM people WHERE id = 686048;
SELECT * FROM people WHERE id = 458378;
SELECT * FROM people WHERE id = 948985;
SELECT * FROM people WHERE id = 396669;
SELECT * FROM people WHERE id = 438727;
SELECT * FROM people WHERE id = 514354;
--ALL which withdraw money in the morning
|   id   | name |  phone_number  | passport_number | license_plate |
+--------+------+----------------+-----------------+---------------+
| 467400 | Luca | (389) 555-5198 | 8496433585      | 4328GD8       |
| 395717 | Kenny | (826) 555-1652 | 9878712108      | 30G67EN       |
| 449774 | Taylor | (286) 555-6063 | 1988161715      | 1106N58       |
| 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
| 458378 | Brooke | (122) 555-4581 | 4408372428      | QX4YZN3       |
| 948985 | Kaelyn | (098) 555-1164 | 8304650265      | I449449       |
| 396669 | Iman | (829) 555-5269 | 7049073643      | L93JTIZ       |
| 438727 | Benista | (338) 555-6650 | 9586786673      | 8X428L0       |
| 514354 | Diana | (770) 555-1861 | 3592750733      | 322W7JE       |
--Luca and Diana and Iman and Bruce was in the parking lot and was withdrawing money in the morning at the ATM
--Check for phone calls
SELECT * FROM phone_calls WHERE year = '2021' and month = '7' and day = '28';
| 285 | (367) 555-5533 | (704) 555-5790 | 2021 | 7     | 28  | 75       |
| 236 | (367) 555-5533 | (344) 555-9601 | 2021 | 7     | 28  | 120      |
--Bruce is the only one who called this day.
-- Look for people bruce called.
SELECT * FROM phone_calls WHERE caller  = '(367) 555-5533' AND year = 2021 AND month = 7 AND day = 28;
+-----+----------------+----------------+------+-------+-----+----------+
| id  |     caller     |    receiver    | year | month | day | duration |
+-----+----------------+----------------+------+-------+-----+----------+
| 233 | (367) 555-5533 | (375) 555-8161 | 2021 | 7     | 28  | 45       |
| 236 | (367) 555-5533 | (344) 555-9601 | 2021 | 7     | 28  | 120      |
| 245 | (367) 555-5533 | (022) 555-4052 | 2021 | 7     | 28  | 241      |
| 285 | (367) 555-5533 | (704) 555-5790 | 2021 | 7     | 28  | 75       |
+-----+----------------+----------------+------+-------+-----+----------+
-- Look for their names
SELECT * FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE phone_calls.caller  = '(367) 555-5533' AND year = 2021 AND month = 7 AND day = 28;
|   id   |  name   |  phone_number  | passport_number | license_plate | id  |     caller     |    receiver    | year | month | day | duration |
+--------+---------+----------------+-----------------+---------------+-----+----------------+----------------+------+-------+-----+----------+
| 864400 | Robin   | (375) 555-8161 |                 | 4V16VO0       | 233 | (367) 555-5533 | (375) 555-8161 | 2021 | 7     | 28  | 45       |
| 985497 | Deborah | (344) 555-9601 | 8714200946      | 10I5658       | 236 | (367) 555-5533 | (344) 555-9601 | 2021 | 7     | 28  | 120      |
| 315221 | Gregory | (022) 555-4052 | 3355598951      | V4C670D       | 245 | (367) 555-5533 | (022) 555-4052 | 2021 | 7     | 28  | 241      |
| 652398 | Carl    | (704) 555-5790 | 7771405611      | 81MZ921       | 285 | (367) 555-5533 | (704) 555-5790 | 2021 | 7     | 28  | 75       |
--Look for airports
SELECT * FROM airports;
 8  | CSF          | Fiftyville Regional Airport             | Fiftyville    |
 --Look for flights at the fiftyville airport
 SELECT * FROM flights WHERE origin_airport_id = 8 AND year = 2021 AND month = 7 AND day = 29;
+----+-------------------+------------------------+------+-------+-----+------+--------+
| id | origin_airport_id | destination_airport_id | year | month | day | hour | minute |
+----+-------------------+------------------------+------+-------+-----+------+--------+
| 36 | 8                 | 4                      | 2021 | 7     | 29  | 8    | 20     |
--Found earliest flight at 29th.
-- They want to go to | 4  | LGA          | LaGuardia Airport                       | New York City |
--Look for the compliance in passenger list
SELECT * FROM passengers WHERE flight_id = 36;
+-----------+-----------------+------+
| flight_id | passport_number | seat |
+-----------+-----------------+------+
| 36        | 7214083635      | 2A   |
| 36        | 1695452385      | 3B   |
| 36        | 5773159633      | 4A   |
| 36        | 1540955065      | 5C   |
| 36        | 8294398571      | 6C   |
| 36        | 1988161715      | 6D   |
| 36        | 9878712108      | 7A   |
| 36        | 8496433585      | 7B   |
+-----------+-----------------+------+
--Robin must be the compliance. He did not got a password_number. But Bruce is registered in that plane.
