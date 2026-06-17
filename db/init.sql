CREATE TABLE ksiazki (
  id SERIAL PRIMARY KEY,
  tytul TEXT NOT NULL,
  wydawnictwo TEXT NOT NULL,
  przedmiot TEXT
);

CREATE TABLE opinie (
  id SERIAL PRIMARY KEY,
  ksiazka_id INTEGER NOT NULL REFERENCES ksiazki(id) ON DELETE CASCADE,
  tresc TEXT NOT NULL,
  autor_typ TEXT,
  data_dodania TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE analizy_opinii (
  id SERIAL PRIMARY KEY,
  opinia_id INTEGER NOT NULL REFERENCES opinie(id) ON DELETE CASCADE,
  temat TEXT,
  sentyment TEXT,
  plus TEXT,
  minus TEXT
);

INSERT INTO ksiazki (tytul, wydawnictwo, przedmiot)
VALUES ('Matematyka 1', 'Nowa Era', 'matematyka');

INSERT INTO opinie (ksiazka_id, tresc, autor_typ)
VALUES
(1, 'Ogólnie ta książka do matmy z Nowej Ery jest spoko, rozdział o ułamkach super, ale na stronie 45 jest błąd w zadaniu 3. Nauczyciele na to narzekają.', 'nauczyciel'),
(1, 'Dramat, nic nie rozumiem z geometrii w tym podręczniku, ilustracje są nieczytelne. Za to algebra jest całkiem nieźle rozpisana.', 'uczeń'),
(1, 'Używam tego od miesiąca. Plus za fajne zadania maturalne na końcu rozdziału 2. Moje klasy bardzo to polubiły!', 'nauczyciel');
