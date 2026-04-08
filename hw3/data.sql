-- Тестовые данные для системы управления событиями

-- Пользователи
INSERT INTO users (login, first_name, last_name, email, password_hash) VALUES
('maria_lemeshchenko', 'Мария', 'Лемещенко', 'marialemeshchenko@mail.ru', 'hash_privet_mir1'),
('ivan_petrov', 'Иван', 'Петров', 'ivan.petrov@mail.ru', 'hash_privet_mir2'),
('anna_smirnova', 'Анна', 'Смирнова', 'anna.smirnova@mail.ru', 'hash_privet_mir3'),
('alex_ivanov', 'Алексей', 'Иванов', 'alex.ivanov@mail.ru', 'hash_privet_mir4'),
('olga_sokolova', 'Ольга', 'Соколова', 'olga.sokolova@mail.ru', 'hash_privet_mir5'),
('dmitry_kuznetsov', 'Дмитрий', 'Кузнецов', 'dmitry.kuznetsov@mail.ru', 'hash_privet_mir6'),
('elena_popova', 'Елена', 'Попова', 'elena.popova@mail.ru', 'hash_privet_mir7'),
('sergey_vasiliev', 'Сергей', 'Васильев', 'sergey.vasiliev@mail.ru', 'hash_privet_mir8'),
('nina_morozova', 'Нина', 'Морозова', 'nina.morozova@mail.ru', 'hash_privet_mir9'),
('marina_livenets', 'Марина', 'Ливенец', 'marina.livenets@mail.ru', 'hash_privet_mir10'),
('boris_derevyashko', 'Борис', 'Деревяшко', 'boris.derevyashko@mail.ru', 'hash_privet_mir11'),
('yulia_komorov', 'Юлия', 'Коморов', 'yulia.komorov@mail.ru', 'hash_privet_mir12'),
('mikhail_shmid', 'Михаил', 'Шмид', 'mikhail.shmid@mail.ru', 'hash_privet_mir13'),
('stanislav_orlov', 'Станислав', 'Орлов', 'stanislav.orlov@mail.ru', 'hash_privet_mir14'),
('kuzma_pronsky', 'Кузьма', 'Пронский', 'kuzma.pronsky@mail.ru', 'hash_privet_mir15'),
('kirill_savichev', 'Кирилл', 'Савичев', 'kirill.savichev@mail.ru', 'hash_privet_mir16');


-- События
INSERT INTO events (title, description, event_date, location, organizer_id) VALUES
('Архитектурный митап', 'Встреча по архитектуре приложений', '2026-04-01', 'Москва', 1),
('Python Meetup', 'Обсуждение Python и FastAPI', '2026-04-05', 'Санкт-Петербург', 2),
('SQL Day', 'Практика по SQL и PostgreSQL', '2026-04-10', 'Казань', 3),
('DevOps Base', 'Основы DevOps и CI/CD', '2026-04-12', 'Москва', 4),
('AI Forum', 'Современные подходы в AI', '2026-04-15', 'Новосибирск', 5),
('Backend School', 'Бэкенд разработка для начинающих', '2026-04-18', 'Екатеринбург', 6),
('Docker Hands-on Kazan', 'Практика по Docker', '2026-04-20', 'Казань', 7),
('Testing Workshop Samara', 'Тестирование API сервисов', '2026-04-22', 'Самара', 8),
('Clean Code Talk', 'Чистый код и рефакторинг', '2026-04-25', 'Уфа', 9),
('Docker Hands-on Moscow', 'Практика по Docker', '2026-04-20', 'Москва', 10),
('Testing Workshop Sochi', 'Тестирование API сервисов', '2026-04-28', 'Сочи', 11),
('Clean Code Talk', 'Чистый код и рефакторинг', '2026-05-25', 'Москва', 12),
('Database Meetup', 'Проектирование и индексы в БД', '2026-04-28', 'Москва', 13),
('Cloud Computing', 'Облачные технологии и сервисы', '2026-04-30', 'Санкт-Петербург', 14),
('Microservices Architecture', 'Микросервисная архитектура', '2026-05-05', 'Казань', 15),
('Kubernetes Workshop', 'Практика по Kubernetes', '2026-05-10', 'Екатеринбург', 16);


-- Регистрации на события
INSERT INTO event_participants (event_id, user_id, status) VALUES -- user_id соответствует порядку вставки пользователей (1..16)
(1, 2, 'registered'),
(1, 3, 'registered'),
(2, 1, 'registered'),
(2, 4, 'registered'),
(3, 5, 'registered'),
(3, 6, 'registered'),
(4, 7, 'registered'),
(5, 8, 'registered'),
(6, 9, 'registered'),
(7, 10, 'registered'),
(8, 1, 'registered'),
(8, 2, 'registered'),
(9, 3, 'registered'),
(9, 4, 'registered'),
(11, 9, 'registered'),
(16, 14, 'registered'),
(12, 13, 'registered'),
(10, 2, 'registered'),
(16, 1, 'registered'),
(10, 5, 'registered');