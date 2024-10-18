CREATE TABLE Netflix (
    show_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type  CHAR(10),
    title VARCHAR(50),
    director VARCHAR(20),
    country VARCHAR(20),
    score DECIMAL(3,1)
);


INSERT INTO Netflix (type, title, director, country)
VALUES
    ("Movie", "Chappie", "Neill Blomkamp", "South Africa, United States"),
    ("Movie", "Clear and Present Danger", "Phillip Noyce", "United States, Mexico"),
    ("Movie", "Cliffhanger", "Renny Harlin", "United States, Italy, France, Japan"),
    ("Movie", "Cold Mountain", "Anthony Minghella", "United States, Italy, Romania, United Kingdom"),
    ("Movie", "Crocodile Dundee in Los Angeles", "Simon Wincer", "Australia, United States");

CREATE TABLE NetflixCast (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    actors TEXT
);
INSERT INTO NetflixCast (title,actors)
VALUES
    ('Chappie', 'Sharlto Copley,Dev Patel,Hugh Jackman'),
    ('Clear and Present Danger','Harrison Ford,Willem Dafoe,Anne Archer'),
    ('Cliffhanger', 'Sylvester Stallone,John Lithgow,Michael Rooker'),
    ('Cold Mountain', 'Jude Law,Nicole Kidman,Renee Zellweger'),
    ('Crocodile Dundee in Los Angeles','Paul Hogan,Linda Kozlowski,Jere Burns'),
    ('Do the Right Thing', 'Danny Aiello,Ossie Davis,Ruby Dee'),
    ('El patrón, radiografía de un crimen', 'Joaquín Furriel,Luis Luque,Rafael Ferro');

CREATE TABLE Amazon (
    show_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type  CHAR(10),
    title VARCHAR(50),
    director VARCHAR(20),
    country VARCHAR(20),
    score DECIMAL(3,1)
);

INSERT INTO Amazon (title, director, country, type)
VALUES
    ("The Grand Seduction", "Don McKellar", "Canada", "Movie"),
    ("Take Care Good Night", "Girish Joshi", "India", "Movie"),
    ("Secrets of Deception", "Josh Webber", "United States", "Movie"),
    ("Pink: Staying True", "Sonia Anderson", "United States", "Movie"),
    ("Monster Maker", "Giles Foster", "United Kingdom", "Movie"),
    ("Living With Dinosaurs", "Paul Weiland", "United Kingdom", "Movie");

CREATE TABLE AmazonCast (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    actors TEXT
);

INSERT INTO AmazonCast (title, actors)
VALUES
    ("The Grand Seduction", "Brendan Gleeson, Taylor Kitsch, Liane Balaban"),
    ("Take Care Good Night", "Mahesh Manjrekar, Sachin Khedekar, Isha Keskar"),
    ("Secrets of Deception", "Tom Sizemore, Richard T. Jones, Jahnee Wallace"),
    ("Pink: Staying True", "Pink"),
    ("Monster Maker", "George Costigan, Ron Cook, Kelsey Grammer"),
    ("Living With Dinosaurs", "Mark Addy, Jemima Rooper, Craig Hall");

    
CREATE TABLE Disney (
    show_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type  CHAR(10),
    title VARCHAR(50),
    director VARCHAR(20),
    country VARCHAR(20),
    score DECIMAL(3,1)
);

INSERT INTO Disney (type, title, director, country)
VALUES
    ("Movie", "Duck the Halls: A Mickey Mouse Christmas Special", "Alonso Ramirez Ramos", "United States"),
    ("Movie", "Ice Age: A Mammoth Christmas", "Karen Disher", "United States"),
    ("Movie", "Becoming Cousteau", "Liz Garbus", "United States"),
    ("TV Show", "Port Protection Alaska", "Not Available", "United States"),
    ("TV Show", "Secrets of the Zoo: Tampa", "Not Available", "United States"),
    ("Movie", "Get a Horse!", "Lauren MacMullan", "United States"),
    ("Movie", "Home Sweet Home Alone", "Dan Mazer", "United States");

CREATE TABLE DisneyCast (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    actors TEXT
);

INSERT INTO DisneyCast (title, actors)
VALUES
    ("Duck the Halls: A Mickey Mouse Christmas Special", "Chris Diamantopoulos, Russi Taylor, Tony Anselmo"),
    ("Ice Age: A Mammoth Christmas", "Ray Romano, John Leguizamo, Denis Leary"),
    ("Becoming Cousteau", "Vincent Cassel"),
    ("Port Protection Alaska", "Sam Carlson,Timothy Leach,Matt Carlson"),
    ("Secrets of the Zoo: Tampa", "Lauren Smith,Jason Reiter,Devon Koop"),
    ("Get a Horse!", "Walt Disney, Marcellite Garner, Billy Bletcher"),
    ("Home Sweet Home Alone", "Archie Yates, Rob Delaney, Ellie Kemper");

DROP TABLE IF EXISTS users;

CREATE TABLE users
(
        user_id TEXT PRIMARY KEY,
        password TEXT NOT NULL
);

DROP TABLE IF EXISTS reviews;
CREATE TABLE reviews
(
        user_id TEXT,
        film VARCHAR(50),
        review TEXT NOT NULL,
        score DECIMAL(3,1)
);


DROP TABLE IF EXISTS Admin;

CREATE TABLE Admin
(
        admin_id TEXT PRIMARY KEY,
        password TEXT NOT NULL

);



DROP TABLE IF EXISTS Score;

CREATE TABLE Score
(
        title TEXT,
        score DECIMAL(3,1)
);

DROP TABLE IF EXISTS Favourites;

CREATE TABLE Favourites
(
        user_id TEXT
        film TEXT
);

