-- 1. Создание нового пользователя
INSERT INTO users (login, first_name, last_name, email, password_hash)
VALUES ('Asti_buldog', 'Асти', 'Бульдог', 'asti.buldog@mail.ru', 'kakoi_to_hash_test');

-- 2. Поиск пользователя по логину
SELECT *
FROM users
WHERE login = 'maria_lemeshchenko';


-- 3. Поиск пользователя по маске имени или фамилии
SELECT id, login, first_name, last_name
FROM users
WHERE LOWER(first_name) LIKE '%мар%'
   OR LOWER(last_name) LIKE '%мар%';


-- 4. Создание события
INSERT INTO events (title, description, event_date, location, organizer_id)
VALUES ('Test Event', 'Описание тестового события', '2026-06-01', 'Москва', 1);


-- 5. Получение списка событий
SELECT id, title, event_date, location
FROM events
ORDER BY event_date DESC;


-- 6. Поиск событий по дате
SELECT *
FROM events
WHERE event_date = '2026-04-20';


-- 7. Регистрация пользователя на событие
INSERT INTO event_participants (event_id, user_id, status)
VALUES (1, 6, 'registered');


-- 8. Получение участников события
SELECT u.id,
       u.login,
       u.first_name,
       u.last_name
FROM users u
JOIN event_participants ep ON u.id = ep.user_id
WHERE ep.event_id = 1
  AND ep.status = 'registered'
ORDER BY u.last_name;


-- 9. Получение событий пользователя
SELECT e.id,
       e.title,
       e.event_date,
       e.location
FROM events e
JOIN event_participants ep ON e.id = ep.event_id
WHERE ep.user_id = 1
  AND ep.status = 'registered'
ORDER BY e.event_date;


-- 10. Получение количества участников на каждом событии
SELECT e.id,
       e.title,
       COUNT(ep.user_id) AS participants_count
FROM events e
LEFT JOIN event_participants ep ON e.id = ep.event_id
GROUP BY e.id, e.title
ORDER BY participants_count DESC;

--10.1 Получение только активных участников на каждом событии
SELECT e.id,
       e.title,
       COUNT(ep.user_id) AS participants_count
FROM events e
LEFT JOIN event_participants ep
       ON e.id = ep.event_id
      AND ep.status = 'registered'
GROUP BY e.id, e.title
ORDER BY participants_count DESC;


-- 11. Получение пользователей без регистраций
SELECT u.id, u.login
FROM users u
LEFT JOIN event_participants ep ON u.id = ep.user_id
WHERE ep.user_id IS NULL;


-- 12. Отмена регистрации
UPDATE event_participants
SET status = 'cancelled'
WHERE event_id = 1
  AND user_id = 6;

-- 13. Самые популярные события по количеству регистраций
SELECT e.id,
       e.title,
       e.event_date,
       e.location,
       COUNT(ep.user_id) AS participants_count
FROM events e
LEFT JOIN event_participants ep
       ON e.id = ep.event_id
      AND ep.status = 'registered'
GROUP BY e.id, e.title, e.event_date, e.location
ORDER BY participants_count DESC, e.event_date;

-- 14. Количество событий у каждого организатора
SELECT u.id,
       u.login,
       u.first_name,
       u.last_name,
       COUNT(e.id) AS events_created
FROM users u
LEFT JOIN events e
       ON u.id = e.organizer_id
GROUP BY u.id, u.login, u.first_name, u.last_name
ORDER BY events_created DESC, u.id;

-- 15. Города с наибольшим количеством событий
SELECT location,
       COUNT(*) AS events_count
FROM events
GROUP BY location
ORDER BY events_count DESC, location;

-- Оптимизированные запросы

-- 1. Оптимизированный поиск пользователя по логину
-- Выбираю не все поля, а только нужные
SELECT id, login, first_name, last_name, email
FROM users
WHERE login = 'maria_lemeshchenko';

-- 2. Оптимизированный поиск событий по дате
-- Выбираю только нужные колонки, запрос работает с индексом по event_date
SELECT id, title, event_date, location
FROM events
WHERE event_date = '2026-04-20'
ORDER BY id;

-- 3. Оптимизированное получение участников события
-- Фильтрация по status сразу в JOIN и выбор только нужных полей
SELECT u.id,
u.login,
u.first_name,
u.last_name
FROM event_participants ep
JOIN users u ON u.id = ep.user_id
WHERE ep.event_id = 1
AND ep.status = 'registered'
ORDER BY u.last_name, u.first_name;

-- 4. Оптимизированное получение событий пользователя
-- Сначала фильтруем таблицу регистраций по user_id и status
SELECT e.id,
e.title,
e.event_date,
e.location
FROM event_participants ep
JOIN events e ON e.id = ep.event_id
WHERE ep.user_id = 1
AND ep.status = 'registered'
ORDER BY e.event_date, e.id;

-- 5. Оптимизированный запрос по количеству участников на каждом событии
-- Считаю только активные регистрации
SELECT e.id,
e.title,
COUNT(ep.user_id) AS participants_count
FROM events e
LEFT JOIN event_participants ep
ON ep.event_id = e.id
AND ep.status = 'registered'
GROUP BY e.id, e.title
ORDER BY participants_count DESC, e.id;

-- 6. Оптимизированный запрос по количеству событий у каждого организатора
SELECT u.id,
u.login,
COUNT(e.id) AS events_count
FROM users u
LEFT JOIN events e ON e.organizer_id = u.id
GROUP BY u.id, u.login
ORDER BY events_count DESC, u.id;

-- 7. Оптимизированный запрос по городам с наибольшим количеством событий
SELECT location,
COUNT(*) AS events_count
FROM events
GROUP BY location
ORDER BY events_count DESC, location;