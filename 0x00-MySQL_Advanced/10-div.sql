-- a function SafeDiv that divides (and returns) the first by the second number or returns 0 if the second number is equal to 0.
DELIMITER $$

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
	DECLARE output FLOAT DEFAULT 0;
	IF b != 0 THEN
		SET output = a / b;
	END IF;
	RETURN output;
END$$

DELIMITER ;
