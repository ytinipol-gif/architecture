workspace "Система управления событиями" "Целевая микросервисная архитектура платформы управления событиями" {

    model {

        user = person "Пользователь" "Пользователь системы, который просматривает события, создает события, регистрируется на них и управляет своими регистрациями."

        emailService = softwareSystem "Email-сервис" "Внешняя система для отправки email-уведомлений пользователям."

        eventSystem = softwareSystem "Система управления событиями" "Платформа для управления пользователями, событиями и регистрациями на события." {

            webApp = container "Веб-приложение" "Пользовательский интерфейс системы." "React, Web Browser"

            apiGateway = container "API Gateway" "Единая точка входа в backend-систему. Выполняет маршрутизацию запросов в нужные микросервисы." "HTTP Gateway"

            userService = container "Сервис пользователей" "Отвечает за создание пользователей, поиск по логину и поиск по имени/фамилии." "REST API service"
            eventService = container "Сервис событий" "Отвечает за создание событий, получение списка событий и поиск событий по дате." "REST API service"
            registrationService = container "Сервис регистраций" "Отвечает за регистрацию пользователя на событие, получение участников события, получение событий пользователя и отмену регистрации." "REST API service"
            notificationService = container "Сервис уведомлений" "Отвечает за отправку уведомлений пользователям." "REST API service"

            userDb = container "База пользователей" "Хранит данные пользователей." "PostgreSQL"
            eventDb = container "База событий" "Хранит данные событий." "PostgreSQL"
            registrationDb = container "База регистраций" "Хранит данные о регистрациях пользователей на события." "PostgreSQL"

            noSqlStore = container "NoSQL-хранилище" "Используется для быстрых операций чтения и поисковых представлений событий." "MongoDB"
            cache = container "Кеш" "Используется для хранения часто запрашиваемых данных." "Redis"
            broker = container "Брокер сообщений" "Используется для асинхронного взаимодействия между сервисами." "RabbitMQ"

            user -> webApp "Использует пользовательский интерфейс" "HTTPS"
            webApp -> apiGateway "Отправляет запросы" "HTTPS/REST"

            apiGateway -> userService "Маршрутизирует запросы пользователей" "HTTPS/REST"
            apiGateway -> eventService "Маршрутизирует запросы событий" "HTTPS/REST"
            apiGateway -> registrationService "Маршрутизирует запросы регистраций" "HTTPS/REST"

            userService -> userDb "Читает и записывает данные пользователей" "JDBC"
            eventService -> eventDb "Читает и записывает данные событий" "JDBC"
            registrationService -> registrationDb "Читает и записывает данные регистраций" "JDBC"

            eventService -> noSqlStore "Обновляет поисковые представления событий" "HTTPS/REST"
            eventService -> cache "Кеширует часто запрашиваемые события" "TCP/Redis"

            registrationService -> userService "Проверяет существование пользователя" "HTTPS/REST"
            registrationService -> eventService "Проверяет существование события и доступность регистрации" "HTTPS/REST"

            registrationService -> broker "Публикует событие о регистрации" "AMQP"
            broker -> notificationService "Передает событие о регистрации" "AMQP"
            notificationService -> emailService "Отправляет email-уведомления" "HTTPS/REST"
        }
    }

    views {

        systemContext eventSystem system_context {
            include user
            include eventSystem
            include emailService
            autolayout lr
        }

        container eventSystem container_view {
            include *
            autolayout lr
        }

        dynamic eventSystem user_registers_for_event {
            title "Регистрация пользователя на событие"

            user -> webApp "Открывает страницу события и нажимает кнопку регистрации"
            webApp -> apiGateway "POST /events/{eventId}/registrations" "HTTPS/REST"
            apiGateway -> registrationService "Передает запрос на регистрацию" "HTTPS/REST"
            registrationService -> userService "Проверяет существование пользователя" "HTTPS/REST"
            userService -> userDb "Читает данные пользователя" "JDBC"
            registrationService -> eventService "Проверяет существование события и доступность регистрации" "HTTPS/REST"
            eventService -> eventDb "Читает данные события" "JDBC"
            registrationService -> registrationDb "Проверяет отсутствие существующей регистрации" "JDBC"
            registrationService -> registrationDb "Создает запись о регистрации" "JDBC"
            registrationService -> broker "Публикует событие о регистрации" "AMQP"
            broker -> notificationService "Передает событие о регистрации" "AMQP"
            notificationService -> emailService "Отправляет подтверждение регистрации" "HTTPS/REST"
            registrationService -> apiGateway "Возвращает успешный результат" "HTTPS/REST"
            apiGateway -> webApp "Возвращает успешный результат" "HTTPS/REST"

            autolayout lr
        }

        theme default
    }

}