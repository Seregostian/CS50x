-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT description FROM crime_scene_reports
WHERE year = 2001
AND month = 7
AND day = 28;

SELECT *
  FROM interviews
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND transcript LIKE "%thief%";

SELECT *
  FROM interviews
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND transcript LIKE "%bakery%";

SELECT *
  FROM interviews
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND transcript LIKE "%flight%";

-- Seems like wether i start with flight, bakery or thief, they all give the same output text. I will have to
-- Change my approach, maybe the street? money transfer?

SELECT name
  FROM people, bank_accounts
 WHERE people.id = bank_accounts.person_id
   AND account_number IN
       (SELECT account_number
          FROM atm_transactions
         WHERE year = 2021
           AND month = 7
           AND day = 28
           AND atm_location = "Leggett Street"
           AND transaction_type = "withdraw")
 ORDER BY name;

-- Still not enough information to go on, maybe instead of the money transfer and the steet, the phone call that lasted
-- less than one minute?
-- As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
-- In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
-- The thief then asked the person on the other end of the phone to purchase the flight ticket.

SELECT *
FROM airports;

-- Ok, some progress

SELECT *
FROM flights
WHERE origin_airport_id = 8
AND day = 29
ORDER BY hour ASC;

-- Got a list of flights, thief mentioned they would be getting into the EARLIEST flight, so it has to be this one
--  36 | 8                 | 4                      | 2021 | 7     | 29  | 8    | 20

SELECT *
FROM passengers
WHERE flight_id = 36;

-- Still not precise enough, i need to know which one of those is the one who called

SELECT * FROM people
WHERE passport_number
IN (SELECT passport_number FROM passengers WHERE flight_id = 36)
AND phone_number
IN (SELECT caller FROM phone_calls WHERE day = 28 AND month = 7 AND duration < 60);

-- Wow! license plates! now at least i got names and dates related to this ID 36, not sue what to do with these plates tho
-- Absolutely forgot to check the walkthrough, this bakery_security_logs would've been very useful a while ago lol

SELECT * FROM bakery_security_logs
WHERE day = 28 AND month = 7 AND hour = 10 AND minute <= 25 AND activity = "exit"
AND license_plate
IN (SELECT license_plate FROM people
WHERE passport_number
IN (SELECT passport_number FROM passengers WHERE flight_id = 36)
AND phone_number
IN (SELECT caller FROM phone_calls WHERE day = 28 AND month = 7 AND duration < 60));

-- i get these as a result!
-- +-----+------+-------+-----+------+--------+----------+---------------+
-- | id  | year | month | day | hour | minute | activity | license_plate |
-- +-----+------+-------+-----+------+--------+----------+---------------+
-- | 261 | 2021 | 7     | 28  | 10   | 18     | exit     | 94KL13X       |
-- | 264 | 2021 | 7     | 28  | 10   | 20     | exit     | G412CB7       |
-- | 267 | 2021 | 7     | 28  | 10   | 23     | exit     | 0NTHK55       |
-- +-----+------+-------+-----+------+--------+----------+---------------+
-- from which they all coincide with the license places of Bruce (94KL13X), Sofia (G412CB7) and Kelsey (0NTHK55)

-- Now, i can just select from their plates and ID, and if they match, then we get the list from three to one!
-- Thus giving me the name of the thief!

SELECT * FROM people
WHERE license_plate IN ("94KL13X", "G412CB7", "0NTHK55")
AND id IN ("686048", "395717", "449774");

-- Solved, the thief was Bruce!
--Still need to know who was the receiver from that phone call, to get the accomplice!
--Also, the destination of its Fiftyville escape flight, so:

SELECT caller, receiver
FROM phone_calls
WHERE year = 2021
AND month = 7
AND day = 28
AND duration < 60;

-- |     caller     |    receiver    |
-- +----------------+----------------+
-- | (130) 555-0289 | (996) 555-8899 |
-- | (499) 555-9472 | (892) 555-8872 |
-- | (367) 555-5533 | (375) 555-8161 |

-- Now, i know Buce's phone is (367) 555-5533, so now i know he was calling to (375) 555-8161!

SELECT *
FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60
AND caller IN ("(367) 555-5533")
AND receiver IN ("(375) 555-8161");

-- So Bruce called Robin! there's the accomplice!
-- Bruce said he wants to leave as soon as possible, so better check the flights

SELECT full_name, city
FROM airports
WHERE id IN (1, 4, 11);

-- After checking, there's only three possibilities:
-- New York at 8:20 AM
-- Chicago at 9:30 AM
-- San Francisco at 12:15 PM

SELECT *
FROM flights
JOIN airports
ON airports.id = flights.origin_airport_id
WHERE flights.year = 2021
AND flights.month = 7
AND flights.day = 29
AND flights.hour
BETWEEN 00 AND 12 AND airports.city = "Fiftyville"
ORDER BY flights.hour, flights.minute;

-- Need a more specific list, let's try this :

SELECT name, passport_number
FROM people
WHERE people.name IN ("Bruce")
AND passport_number IN (
    SELECT passport_number
    FROM passengers
    JOIN flights
    ON flights.id = passengers.flight_id
    JOIN airports
    ON airports.id = flights.origin_airport_id
    WHERE flights.year = 2021 AND flights.month = 7 AND flights.day = 29 AND flights.hour BETWEEN 00 AND 12
    AND flights.origin_airport_id IN (
        SELECT airports.id
        FROM airports
        WHERE airports.city = "Fiftyville"
    )
    AND flights.destination_airport_id IN (
        SELECT airports.id
        FROM airports
        WHERE airports.city IN ("New York City", "Chicago", "San Francisco")
    )
)
