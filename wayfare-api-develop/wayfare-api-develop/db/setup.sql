-- Creation script for the rideshare database tables.
-- I am looking into SQLAlchemy to see if we even need this, but for now this
-- is an example of a MySQL setup script.

CREATE DATABASE IF NOT EXISTS rideshare_dev;
USE rideshare_dev

CREATE TABLE user (
  id INT PRIMARY KEY AUTO_INCREMENT,
  first_name NVARCHAR(255),
  last_name NVARCHAR(255),
  email VARCHAR(40) NOT NULL,
  salt CHAR(16),
  token CHAR(64),
  time_registered DATETIME,
  admin BOOLEAN,
  UNIQUE KEY(email)
);

CREATE TABLE passenger (
  ride_id INT,
  user_id INT,
  status INT,
  -- updated TIMESTAMP,
  updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  -- Commented out because the ride table doesn't exist yet.
  -- FOREIGN KEY (ride_id)
  --   REFERENCES ride(id)
  --   ON DELETE CASCADE,
  FOREIGN KEY (user_id)
    REFERENCES user(id)
    ON DELETE CASCADE
  -- Similar foreign key for status.    
);

-- Some test data to play around with.
INSERT INTO user (first_name, last_name, email, salt, token, time_registered, admin)
VALUES
  ('Oliver', 'Wang', 'owang02@calpoly.edu', '$5$bfC6nhD1.Iq9z', '60c50c9cabbec7f007a3ce4eaa1c53e9abf776dbfbbf29378a67901886a11691', NOW(), TRUE),
  ('Karissa', 'Bennett', 'kbenne09@calpoly.edu', '$5$X7O4bDSSMmsli', 'd720fd8b2fb28dda1e9f2831a8464d9f39f13f82e85fdc8b7c5cd481505a5871', NOW(), TRUE),
  ('Barack', 'Obama', 'test@example.com', '$5$HCbxpstxuaw9c', 'faa8322bb46b0473f0c03369759569509c89d0b37b6eef8e063ae11c81434427', NOW(), FALSE);

INSERT INTO passenger (ride_id, user_id, status)
VALUES
  (0, 1, 0),
  (0, 2, 0);