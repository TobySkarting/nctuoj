use nctuoj;
DROP PROCEDURE add_submissions;
DELIMITER //
CREATE PROCEDURE add_submissions(number INT)
    BEGIN
        label1: LOOP
        SET number=number-1;
        INSERT INTO `submissions` (`user_id`, `problem_id`, `execute_type_id`, `time_usage`, `memory_usage`, `score`) VALUES(FLOOR(RAND()*99+1), FLOOR(RAND()*99+1), FLOOR(RAND()*7+1), FLOOR(RAND()*65535), FLOOR(RAND()*65535), FLOOR(RAND()*100));
        IF number <> 0 THEN ITERATE label1; END IF;
        LEAVE label1;
    END LOOP label1;
END;//
DELIMITER ;
CALL add_submissions(700000);
