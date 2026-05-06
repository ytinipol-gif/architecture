const database = db.getSiblingDB("events_db");

database.event_participants.deleteOne({ id: 100 });
database.events.deleteOne({ id: 100 });
database.users.deleteOne({ id: 100 });

print("=== Создание нового пользователя ===");
database.users.insertOne({
  id: 100,
  login: "asti_buldog",
  first_name: "Асти",
  last_name: "Бульдог",
  email: "asti.buldog@mail.ru",
  password_hash: "kakoi_to_hash_test",
  created_at: new Date()
});
printjson(database.users.findOne({ login: "asti_buldog" }));

print("\n=== Поиск пользователя по логину ===");
printjson(
  database.users.findOne(
    { login: "maria_lemeshchenko" },
    { login: 1, first_name: 1, last_name: 1, email: 1 }
  )
);

print("\n=== Поиск пользователя по маске имени или фамилии ===");
printjson(
  database.users.find(
    {
      $or: [
        { first_name: { $regex: "мар", $options: "i" } },
        { last_name: { $regex: "мар", $options: "i" } }
      ]
    },
    { login: 1, first_name: 1, last_name: 1 }
  ).sort({ last_name: 1, first_name: 1 }).toArray()
);

print("\n=== Создание события ===");
const organizer = database.users.findOne({ login: "maria_lemeshchenko" });
database.events.insertOne({
  id: 100,
  title: "Test Event",
  description: "Описание тестового события",
  event_date: ISODate("2026-06-01T00:00:00Z"),
  location: "Москва",
  organizer_id: organizer.id,
  created_at: new Date()
});
printjson(database.events.findOne({ title: "Test Event" }));

print("\n=== Получение списка событий ===");
printjson(
  database.events.find(
    {},
    { title: 1, event_date: 1, location: 1 }
  ).sort({ event_date: -1 }).toArray()
);

print("\n=== Поиск событий по дате ===");
printjson(
  database.events.find({
    event_date: ISODate("2026-04-20T00:00:00Z")
  }).toArray()
);

print("\n=== Регистрация пользователя на событие ===");
const eventForRegistration = database.events.findOne({ id: 1 });
const userForRegistration = database.users.findOne({ id: 6 });
database.event_participants.insertOne({
  id: 100,
  event_id: eventForRegistration.id,
  user_id: userForRegistration.id,
  registration_date: new Date(),
  status: "registered"
});
printjson(
  database.event_participants.findOne({
    event_id: eventForRegistration.id,
    user_id: userForRegistration.id
  })
);

print("\n=== Получение участников события ===");
const participants = database.event_participants.aggregate([
  {
    $match: {
      event_id: eventForRegistration.id,
      status: "registered"
    }
  },
  {
    $lookup: {
      from: "users",
      localField: "user_id",
      foreignField: "id",
      as: "user"
    }
  },
  { $unwind: "$user" },
  {
    $project: {
      _id: 0,
      id: "$user.id",
      login: "$user.login",
      first_name: "$user.first_name",
      last_name: "$user.last_name"
    }
  },
  {
    $sort: {
      last_name: 1,
      first_name: 1
    }
  }
]).toArray();
printjson(participants);

print("\n=== Получение событий пользователя ===");
const userEvents = database.event_participants.aggregate([
  {
    $match: {
      user_id: organizer.id,
      status: "registered"
    }
  },
  {
    $lookup: {
      from: "events",
      localField: "event_id",
      foreignField: "id",
      as: "event"
    }
  },
  { $unwind: "$event" },
  {
    $project: {
      _id: 0,
      id: "$event.id",
      title: "$event.title",
      event_date: "$event.event_date",
      location: "$event.location"
    }
  },
  { $sort: { event_date: 1 } }
]).toArray();
printjson(userEvents);

print("\n=== Количество участников на каждом событии ===");
printjson(
  database.event_participants.aggregate([
    {
      $group: {
        _id: "$event_id",
        participants_count: { $sum: 1 }
      }
    },
    {
      $lookup: {
        from: "events",
        localField: "_id",
        foreignField: "id",
        as: "event"
      }
    },
    { $unwind: "$event" },
    {
      $project: {
        _id: 0,
        event_id: "$event.id",
        title: "$event.title",
        participants_count: 1
      }
    },
    { $sort: { participants_count: -1 } }
  ]).toArray()
);

print("\n=== Только активные участники ===");
printjson(
  database.event_participants.aggregate([
    {
      $match: {
        status: "registered"
      }
    },
    {
      $group: {
        _id: "$event_id",
        participants_count: { $sum: 1 }
      }
    },
    {
      $lookup: {
        from: "events",
        localField: "_id",
        foreignField: "id",
        as: "event"
      }
    },
    { $unwind: "$event" },
    {
      $project: {
        _id: 0,
        title: "$event.title",
        participants_count: 1
      }
    },
    { $sort: { participants_count: -1 } }
  ]).toArray()
);

print("\n=== Пользователи без регистраций ===");
printjson(
  database.users.aggregate([
    {
      $lookup: {
        from: "event_participants",
        localField: "id",
        foreignField: "user_id",
        as: "registrations"
      }
    },
    {
      $match: {
        registrations: { $size: 0 }
      }
    },
    {
      $project: {
        _id: 0,
        login: 1,
        first_name: 1,
        last_name: 1
      }
    }
  ]).toArray()
);

print("\n=== Отмена регистрации ===");
printjson(
  database.event_participants.updateOne(
    {
      event_id: eventForRegistration.id,
      user_id: userForRegistration.id,
      status: "registered"
    },
    {
      $set: {
        status: "cancelled"
      }
    }
  )
);

print("\n=== Самые популярные события ===");
printjson(
  database.event_participants.aggregate([
    {
      $match: {
        status: "registered"
      }
    },
    {
      $group: {
        _id: "$event_id",
        participants_count: { $sum: 1 }
      }
    },
    {
      $lookup: {
        from: "events",
        localField: "_id",
        foreignField: "id",
        as: "event"
      }
    },
    { $unwind: "$event" },
    {
      $project: {
        _id: 0,
        title: "$event.title",
        event_date: "$event.event_date",
        location: "$event.location",
        participants_count: 1
      }
    },
    {
      $sort: {
        participants_count: -1,
        event_date: 1
      }
    }
  ]).toArray()
);

print("\n=== Количество событий у каждого организатора ===");
printjson(
  database.events.aggregate([
    {
      $group: {
        _id: "$organizer_id",
        events_created: { $sum: 1 }
      }
    },
    {
      $lookup: {
        from: "users",
        localField: "_id",
        foreignField: "id",
        as: "organizer"
      }
    },
    { $unwind: "$organizer" },
    {
      $project: {
        _id: 0,
        login: "$organizer.login",
        first_name: "$organizer.first_name",
        last_name: "$organizer.last_name",
        events_created: 1
      }
    },
    { $sort: { events_created: -1, login: 1 } }
  ]).toArray()
);

print("\n=== 15. Города с наибольшим количеством событий ===");
printjson(
  database.events.aggregate([
    {
      $group: {
        _id: "$location",
        events_count: { $sum: 1 }
      }
    },
    {
      $project: {
        _id: 0,
        location: "$_id",
        events_count: 1
      }
    },
    { $sort: { events_count: -1, location: 1 } }
  ]).toArray()
);
