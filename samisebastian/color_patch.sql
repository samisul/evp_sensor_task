UPDATE data
SET color = CASE
    WHEN dust >= 91 OR co2 >= 1501 THEN 'red'
    WHEN dust >= 31 OR co2 >= 451 THEN 'yellow'
    WHEN dust >= 30 OR co2 >= 451 THEN 'green'
    ELSE 'invalid'  -- default value if conditions are not met
END;
