const database = db.getSiblingDB("events_db");

database.users.deleteMany({});
database.events.deleteMany({});
database.event_participants.deleteMany({});
database.counters.deleteMany({});

const userIds = Array.from({ length: 16 }, () => new ObjectId());
const eventIds = Array.from({ length: 16 }, () => new ObjectId());

database.users.insertMany([
  {
    _id: userIds[0],
    id: 1,
    login: "maria_lemeshchenko",
    first_name: "Мария",
    last_name: "Лемещенко",
    email: "marialemeshchenko@mail.ru",
    password_hash: "hash_privet_mir1",
    roles: ["participant", "organizer"],
    profile: {
      city: "Москва",
      phone: "+79990000001"
    },
    created_at: ISODate("2026-04-01T09:00:00Z")
  },
  {
    _id: userIds[1],
    id: 2,
    login: "ivan_petrov",
    first_name: "Иван",
    last_name: "Петров",
    email: "ivan.petrov@mail.ru",
    password_hash: "hash_privet_mir2",
    created_at: ISODate("2026-04-01T09:05:00Z")
  },
  {
    _id: userIds[2],
    id: 3,
    login: "anna_smirnova",
    first_name: "Анна",
    last_name: "Смирнова",
    email: "anna.smirnova@mail.ru",
    password_hash: "hash_privet_mir3",
    created_at: ISODate("2026-04-01T09:10:00Z")
  },
  {
    _id: userIds[3],
    id: 4,
    login: "alex_ivanov",
    first_name: "Алексей",
    last_name: "Иванов",
    email: "alex.ivanov@mail.ru",
    password_hash: "hash_privet_mir4",
    created_at: ISODate("2026-04-01T09:15:00Z")
  },
  {
    _id: userIds[4],
    id: 5,
    login: "olga_sokolova",
    first_name: "Ольга",
    last_name: "Соколова",
    email: "olga.sokolova@mail.ru",
    password_hash: "hash_privet_mir5",
    created_at: ISODate("2026-04-01T09:20:00Z")
  },
  {
    _id: userIds[5],
    id: 6,
    login: "dmitry_kuznetsov",
    first_name: "Дмитрий",
    last_name: "Кузнецов",
    email: "dmitry.kuznetsov@mail.ru",
    password_hash: "hash_privet_mir6",
    created_at: ISODate("2026-04-01T09:25:00Z")
  },
  {
    _id: userIds[6],
    id: 7,
    login: "elena_popova",
    first_name: "Елена",
    last_name: "Попова",
    email: "elena.popova@mail.ru",
    password_hash: "hash_privet_mir7",
    created_at: ISODate("2026-04-01T09:30:00Z")
  },
  {
    _id: userIds[7],
    id: 8,
    login: "sergey_vasiliev",
    first_name: "Сергей",
    last_name: "Васильев",
    email: "sergey.vasiliev@mail.ru",
    password_hash: "hash_privet_mir8",
    created_at: ISODate("2026-04-01T09:35:00Z")
  },
  {
    _id: userIds[8],
    id: 9,
    login: "nina_morozova",
    first_name: "Нина",
    last_name: "Морозова",
    email: "nina.morozova@mail.ru",
    password_hash: "hash_privet_mir9",
    created_at: ISODate("2026-04-01T09:40:00Z")
  },
  {
    _id: userIds[9],
    id: 10,
    login: "marina_livenets",
    first_name: "Марина",
    last_name: "Ливенец",
    email: "marina.livenets@mail.ru",
    password_hash: "hash_privet_mir10",
    created_at: ISODate("2026-04-01T09:45:00Z")
  },
  {
    _id: userIds[10],
    id: 11,
    login: "boris_derevyashko",
    first_name: "Борис",
    last_name: "Деревяшко",
    email: "boris.derevyashko@mail.ru",
    password_hash: "hash_privet_mir11",
    created_at: ISODate("2026-04-01T09:50:00Z")
  },
  {
    _id: userIds[11],
    id: 12,
    login: "yulia_komorov",
    first_name: "Юлия",
    last_name: "Коморов",
    email: "yulia.komorov@mail.ru",
    password_hash: "hash_privet_mir12",
    created_at: ISODate("2026-04-01T09:55:00Z")
  },
  {
    _id: userIds[12],
    id: 13,
    login: "mikhail_shmid",
    first_name: "Михаил",
    last_name: "Шмид",
    email: "mikhail.shmid@mail.ru",
    password_hash: "hash_privet_mir13",
    created_at: ISODate("2026-04-01T10:00:00Z")
  },
  {
    _id: userIds[13],
    id: 14,
    login: "stanislav_orlov",
    first_name: "Станислав",
    last_name: "Орлов",
    email: "stanislav.orlov@mail.ru",
    password_hash: "hash_privet_mir14",
    created_at: ISODate("2026-04-01T10:05:00Z")
  },
  {
    _id: userIds[14],
    id: 15,
    login: "kuzma_pronsky",
    first_name: "Кузьма",
    last_name: "Пронский",
    email: "kuzma.pronsky@mail.ru",
    password_hash: "hash_privet_mir15",
    created_at: ISODate("2026-04-01T10:10:00Z")
  },
  {
    _id: userIds[15],
    id: 16,
    login: "kirill_savichev",
    first_name: "Кирилл",
    last_name: "Савичев",
    email: "kirill.savichev@mail.ru",
    password_hash: "hash_privet_mir16",
    created_at: ISODate("2026-04-01T10:15:00Z")
  }
]);

database.events.insertMany([
  {
    _id: eventIds[0],
    id: 1,
    title: "Архитектурный митап",
    description: "Встреча по архитектуре приложений",
    event_date: ISODate("2026-04-01T00:00:00Z"),
    location: "Москва",
    organizer_id: 1,
    tags: ["architecture", "meetup"],
    venue: {
      hall: "Аудитория 305",
      format: "offline"
    },
    created_at: ISODate("2026-04-01T11:00:00Z")
  },
  {
    _id: eventIds[1],
    id: 2,
    title: "Python Meetup",
    description: "Обсуждение Python и FastAPI",
    event_date: ISODate("2026-04-05T00:00:00Z"),
    location: "Санкт-Петербург",
    organizer_id: 2,
    created_at: ISODate("2026-04-01T11:05:00Z")
  },
  {
    _id: eventIds[2],
    id: 3,
    title: "SQL Day",
    description: "Практика по SQL и PostgreSQL",
    event_date: ISODate("2026-04-10T00:00:00Z"),
    location: "Казань",
    organizer_id: 3,
    created_at: ISODate("2026-04-01T11:10:00Z")
  },
  {
    _id: eventIds[3],
    id: 4,
    title: "DevOps Base",
    description: "Основы DevOps и CI/CD",
    event_date: ISODate("2026-04-12T00:00:00Z"),
    location: "Москва",
    organizer_id: 4,
    created_at: ISODate("2026-04-01T11:15:00Z")
  },
  {
    _id: eventIds[4],
    id: 5,
    title: "AI Forum",
    description: "Современные подходы в AI",
    event_date: ISODate("2026-04-15T00:00:00Z"),
    location: "Новосибирск",
    organizer_id: 5,
    created_at: ISODate("2026-04-01T11:20:00Z")
  },
  {
    _id: eventIds[5],
    id: 6,
    title: "Backend School",
    description: "Бэкенд разработка для начинающих",
    event_date: ISODate("2026-04-18T00:00:00Z"),
    location: "Екатеринбург",
    organizer_id: 6,
    created_at: ISODate("2026-04-01T11:25:00Z")
  },
  {
    _id: eventIds[6],
    id: 7,
    title: "Docker Hands-on Kazan",
    description: "Практика по Docker",
    event_date: ISODate("2026-04-20T00:00:00Z"),
    location: "Казань",
    organizer_id: 7,
    created_at: ISODate("2026-04-01T11:30:00Z")
  },
  {
    _id: eventIds[7],
    id: 8,
    title: "Testing Workshop Samara",
    description: "Тестирование API сервисов",
    event_date: ISODate("2026-04-22T00:00:00Z"),
    location: "Самара",
    organizer_id: 8,
    created_at: ISODate("2026-04-01T11:35:00Z")
  },
  {
    _id: eventIds[8],
    id: 9,
    title: "Clean Code Talk",
    description: "Чистый код и рефакторинг",
    event_date: ISODate("2026-04-25T00:00:00Z"),
    location: "Уфа",
    organizer_id: 9,
    created_at: ISODate("2026-04-01T11:40:00Z")
  },
  {
    _id: eventIds[9],
    id: 10,
    title: "Docker Hands-on Moscow",
    description: "Практика по Docker",
    event_date: ISODate("2026-04-20T00:00:00Z"),
    location: "Москва",
    organizer_id: 10,
    created_at: ISODate("2026-04-01T11:45:00Z")
  },
  {
    _id: eventIds[10],
    id: 11,
    title: "Testing Workshop Sochi",
    description: "Тестирование API сервисов",
    event_date: ISODate("2026-04-28T00:00:00Z"),
    location: "Сочи",
    organizer_id: 11,
    created_at: ISODate("2026-04-01T11:50:00Z")
  },
  {
    _id: eventIds[11],
    id: 12,
    title: "Clean Code Talk",
    description: "Чистый код и рефакторинг",
    event_date: ISODate("2026-05-25T00:00:00Z"),
    location: "Москва",
    organizer_id: 12,
    created_at: ISODate("2026-04-01T11:55:00Z")
  },
  {
    _id: eventIds[12],
    id: 13,
    title: "Database Meetup",
    description: "Проектирование и индексы в БД",
    event_date: ISODate("2026-04-28T00:00:00Z"),
    location: "Москва",
    organizer_id: 13,
    created_at: ISODate("2026-04-01T12:00:00Z")
  },
  {
    _id: eventIds[13],
    id: 14,
    title: "Cloud Computing",
    description: "Облачные технологии и сервисы",
    event_date: ISODate("2026-04-30T00:00:00Z"),
    location: "Санкт-Петербург",
    organizer_id: 14,
    created_at: ISODate("2026-04-01T12:05:00Z")
  },
  {
    _id: eventIds[14],
    id: 15,
    title: "Microservices Architecture",
    description: "Микросервисная архитектура",
    event_date: ISODate("2026-05-05T00:00:00Z"),
    location: "Казань",
    organizer_id: 15,
    created_at: ISODate("2026-04-01T12:10:00Z")
  },
  {
    _id: eventIds[15],
    id: 16,
    title: "Kubernetes Workshop",
    description: "Практика по Kubernetes",
    event_date: ISODate("2026-05-10T00:00:00Z"),
    location: "Екатеринбург",
    organizer_id: 16,
    created_at: ISODate("2026-04-01T12:15:00Z")
  }
]);

database.event_participants.insertMany([
  { id: 1, event_id: 1, user_id: 2, registration_date: ISODate("2026-04-02T09:00:00Z"), status: "registered" },
  { id: 2, event_id: 1, user_id: 3, registration_date: ISODate("2026-04-02T09:05:00Z"), status: "registered" },
  { id: 3, event_id: 2, user_id: 1, registration_date: ISODate("2026-04-02T09:10:00Z"), status: "registered" },
  { id: 4, event_id: 2, user_id: 4, registration_date: ISODate("2026-04-02T09:15:00Z"), status: "registered" },
  { id: 5, event_id: 3, user_id: 5, registration_date: ISODate("2026-04-02T09:20:00Z"), status: "registered" },
  { id: 6, event_id: 3, user_id: 6, registration_date: ISODate("2026-04-02T09:25:00Z"), status: "registered" },
  { id: 7, event_id: 4, user_id: 7, registration_date: ISODate("2026-04-02T09:30:00Z"), status: "registered" },
  { id: 8, event_id: 5, user_id: 8, registration_date: ISODate("2026-04-02T09:35:00Z"), status: "registered" },
  { id: 9, event_id: 6, user_id: 9, registration_date: ISODate("2026-04-02T09:40:00Z"), status: "registered" },
  { id: 10, event_id: 7, user_id: 10, registration_date: ISODate("2026-04-02T09:45:00Z"), status: "registered" },
  { id: 11, event_id: 8, user_id: 1, registration_date: ISODate("2026-04-02T09:50:00Z"), status: "registered" },
  { id: 12, event_id: 8, user_id: 2, registration_date: ISODate("2026-04-02T09:55:00Z"), status: "registered" },
  { id: 13, event_id: 9, user_id: 3, registration_date: ISODate("2026-04-02T10:00:00Z"), status: "registered" },
  { id: 14, event_id: 9, user_id: 4, registration_date: ISODate("2026-04-02T10:05:00Z"), status: "registered" },
  { id: 15, event_id: 11, user_id: 9, registration_date: ISODate("2026-04-02T10:10:00Z"), status: "registered" },
  { id: 16, event_id: 16, user_id: 14, registration_date: ISODate("2026-04-02T10:15:00Z"), status: "registered" },
  { id: 17, event_id: 12, user_id: 13, registration_date: ISODate("2026-04-02T10:20:00Z"), status: "registered" },
  { id: 18, event_id: 10, user_id: 2, registration_date: ISODate("2026-04-02T10:25:00Z"), status: "registered" },
  { id: 19, event_id: 16, user_id: 1, registration_date: ISODate("2026-04-02T10:30:00Z"), status: "registered" },
  { id: 20, event_id: 10, user_id: 5, registration_date: ISODate("2026-04-02T10:35:00Z"), status: "registered" }
]);

database.counters.insertMany([
  { _id: "users", value: 16 },
  { _id: "events", value: 16 },
  { _id: "event_participants", value: 20 }
]);

print("Тестовые данные для MongoDB успешно добавлены");
print("users: " + database.users.countDocuments({}));
print("events: " + database.events.countDocuments({}));
print("event_participants: " + database.event_participants.countDocuments({}));
