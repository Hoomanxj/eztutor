-- Keep a log of any SQL queries you execute as you solve the mystery.

/*
    key info:
    city: Fiftyville
    theft date: 28 July 2023
    time: based on crime report 10:15
    witnesses: 3
    witness 1: saw the theif exit bakery parking within 10 minutes of theft (10:15 - 10:25)
    witness 2: saw the theif withdraw some money from the ATM in Leggett Street earlier the
        day of theft
    witness 3: the theif talked with accomplice for less than a minute right after the theft;
        they were going to take the earliest flight the day after (29 July);
        accomplice was suppose to have bought the tickets (the tickes should be in their name
            or have been bought using their bank account)
*/

-- query the reports where duck was mentioned
SELECT description FROM crime_scene_reports
WHERE description LIKE '%duck%';

-- query the interviews where bakery was mentioned
SELECT transcript FROM interviews
WHERE transcript LIKE '%bakery%';

/*
    based on the second interview, check the ATM withdrawals before the theft
    in Leggett Street
*/
SELECT * FROM atm_transactions
WHERE year = 2023
AND month = 7
AND day = 28
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw';

-- use the atm info to find the name of the account owners from "bank" and "people" tables
SELECT people.name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE bank_accounts.account_number IN (
    SELECT account_number FROM atm_transactions
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND atm_location = 'Leggett Street'
    AND transaction_type = 'withdraw'
);

/*
    get the licence plate numbers of people who exited from bakery
    within 10 minutes of theft (10:15 - 10:25), based on the first
    interview
*/
SELECT license_plate FROM bakery_security_logs
WHERE year = 2023
AND month = 7
AND day = 28
AND hour = 10
AND minute BETWEEN 15 AND 25
AND activity = 'exit';


-- get the phone number of people making a call for less than a minute, after the theft
SELECT phone_calls.caller, phone_calls.receiver FROM phone_calls
WHERE phone_calls.year = 2023
AND phone_calls.month = 7
AND phone_calls.day = 28
AND phone_calls.duration < 60;

-- get the passport number of people flying from Fiftyville on 28 July
SELECT passport_number FROM passengers
    JOIN flights ON flights.id = passengers.flight_id
    WHERE flights.id IN (
        SELECT flights.id FROM flights
        JOIN airports ON airports.id = flights.origin_airport_id
        WHERE airports.city = 'Fiftyville'
        AND flights.year = 2023
        AND flights.month = 7
        AND flights.day = 29
    );

-- use the name, phone number, license plate and passport number to find the thief
SELECT * FROM people
WHERE people.name IN (
    SELECT DISTINCT people.name FROM people
    JOIN bank_accounts ON bank_accounts.person_id = people.id
    WHERE bank_accounts.account_number IN (
        SELECT DISTINCT account_number FROM atm_transactions
        WHERE year = 2023
        AND month = 7
        AND day = 28
        AND atm_location = 'Leggett Street'
        AND transaction_type = 'withdraw'
    )
)
AND people.license_plate IN (
    SELECT DISTINCT license_plate FROM bakery_security_logs
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND hour = 10
    AND minute BETWEEN 15 AND 25
    AND activity = 'exit'
)
AND people.phone_number IN (
    SELECT phone_calls.caller FROM phone_calls
    WHERE phone_calls.year = 2023
    AND phone_calls.month = 7
    AND phone_calls.day = 28
    AND phone_calls.duration < 60
)
AND people.passport_number IN (
    SELECT passport_number FROM passengers
        JOIN flights ON flights.id = passengers.flight_id
        WHERE flights.id IN (
            SELECT flights.id FROM flights
            JOIN airports ON airports.id = flights.origin_airport_id
            WHERE airports.city = 'Fiftyville'
            AND flights.year = 2023
            AND flights.month = 7
            AND flights.day = 29
            AND flights.hour = 8
        )
);

-- since "Bruce" is the only matching entery, he is the theif

-- use Bruces phone calls to find the accomplice
SELECT * FROM people
WHERE people.phone_number IN (
    SELECT receiver FROM phone_calls
    WHERE phone_calls.year = 2023
    AND phone_calls.month = 7
    AND phone_calls.day = 28
    AND phone_calls.caller = '(367) 555-5533'
    AND phone_calls.duration < 60
)
;
-- Bruce only called Robin at that period so accomplice is Robin

-- Now use the flight id to find the destination
SELECT city FROM airports
JOIN flights ON flights.destination_airport_id = airports.id
WHERE flights.id IN (
    SELECT flights.id FROM flights
    JOIN airports ON airports.id = flights.origin_airport_id
    WHERE airports.city = 'Fiftyville'
    AND flights.year = 2023
    AND flights.month = 7
    AND flights.day = 29
    AND flights.hour = 8
);

-- this shows that Bruce escaped to New York City
