# Analizator Opinii o Podręcznikach – Proof of Concept

## Cel projektu

Celem projektu jest sprawdzenie możliwości wykorzystania modeli AI do automatycznej analizy opinii dotyczących podręczników szkolnych.

System ma umożliwiać:

* dodawanie podręczników,
* dodawanie opinii do podręczników,
* automatyczne przetwarzanie opinii przez model AI,
* zapis uporządkowanych danych w bazie,
* generowanie raportów i podsumowań.

---

# Architektura

## Technologie

* Backend: FastAPI (Python)
* Baza danych: PostgreSQL
* Konteneryzacja: Docker + Docker Compose
* AI: OpenAI API (GPT-4o-mini)

---

# Model danych

## Tabela: ksiazki

Przechowuje informacje o podręcznikach.

| Pole        | Typ    |
| ----------- | ------ |
| id          | SERIAL |
| tytul       | TEXT   |
| wydawnictwo | TEXT   |
| przedmiot   | TEXT   |

---

## Tabela: opinie

Przechowuje surowe opinie użytkowników.

| Pole         | Typ       |
| ------------ | --------- |
| id           | SERIAL    |
| ksiazka_id   | INTEGER   |
| tresc        | TEXT      |
| autor_typ    | TEXT      |
| data_dodania | TIMESTAMP |

---

## Tabela: analizy_opinii

Przechowuje wynik analizy wykonanej przez AI.

| Pole      | Typ     |
| --------- | ------- |
| id        | SERIAL  |
| opinia_id | INTEGER |
| temat     | TEXT    |
| sentyment | TEXT    |
| plus      | TEXT    |
| minus     | TEXT    |

---

# Proces działania

## Krok 1 – Dodanie książki

Przykład:

Tytuł:
Matematyka 1

Wydawnictwo:
Nowa Era

Przedmiot:
Matematyka

---

## Krok 2 – Dodanie opinii

Przykład:

"Dramat, nic nie rozumiem z geometrii w tym podręczniku, ilustracje są nieczytelne. Za to algebra jest całkiem nieźle rozpisana."

Opinia zostaje zapisana w tabeli `opinie`.

---

## Krok 3 – Analiza przez AI

Prompt:

Przeanalizuj poniższą opinię.

Wyciągnij:

1. temat,
2. sentyment,
3. największy plus,
4. największy minus.

Zwróć wyłącznie JSON:

{
"temat": "",
"sentyment": "",
"plus": "",
"minus": ""
}

---

## Krok 4 – Zapis wyniku

Przykładowy wynik:

{
"temat": "Geometria",
"sentyment": "Negatywny",
"plus": "Algebra dobrze rozpisana",
"minus": "Nieczytelne ilustracje"
}

Wynik trafia do tabeli `analizy_opinii`.

---

# Raport zbiorczy

System pobiera wszystkie analizy dla wybranego podręcznika.

Następnie wysyła je do AI z prośbą o przygotowanie raportu.

Przykładowe pytanie:

Jesteś analitykiem produktu.

Na podstawie poniższych danych przygotuj raport dla wydawnictwa.

Wskaż:

* najczęściej chwalone elementy,
* najczęściej zgłaszane problemy,
* rekomendacje zmian.

---

# API

## POST /ksiazki

Dodanie książki.

## GET /ksiazki

Lista książek.

## POST /ksiazki/{id}/opinie

Dodanie opinii.

## GET /ksiazki/{id}/opinie

Pobranie opinii.

## POST /opinie/{id}/analizuj

Uruchomienie analizy AI.

## GET /ksiazki/{id}/raport

Generowanie raportu zbiorczego.

---

# Cel PoC

Zweryfikowanie, czy modele AI są w stanie skutecznie:

* analizować nieuporządkowane opinie,
* zamieniać je na dane strukturalne,
* tworzyć użyteczne raporty dla wydawnictw.

Po pozytywnej weryfikacji projekt może zostać rozwinięty do pełnego systemu analizy feedbacku dla wydawnictw edukacyjnych.
