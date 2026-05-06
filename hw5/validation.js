const database = db.getSiblingDB("events_db");

const eventValidator = {
  $jsonSchema: {
    bsonType: "object",
    required: ["title", "description", "event_date", "location", "organizer_id", "created_at"],
    properties: {
      title: {
        bsonType: "string",
        minLength: 3,
        maxLength: 200,
        description: "Название события должно быть строкой длиной от 3 до 200 символов"
      },
      description: {
        bsonType: "string",
        minLength: 5,
        description: "Описание события должно быть строкой"
      },
      event_date: {
        bsonType: "date",
        description: "Дата события должна храниться в формате BSON Date"
      },
      location: {
        bsonType: "string",
        minLength: 2,
        maxLength: 255,
        description: "Место проведения должно быть строкой"
      },
      tags: {
        bsonType: "array",
        description: "Теги события могут храниться в виде массива строк",
        items: {
          bsonType: "string"
        }
      },
      venue: {
        bsonType: "object",
        description: "Дополнительная информация о месте проведения",
        properties: {
          hall: {
            bsonType: "string"
          },
          format: {
            bsonType: "string"
          }
        }
      },
      organizer_id: {
        bsonType: ["int", "long"],
        minimum: 1,
        description: "Организатор должен храниться как числовой идентификатор пользователя"
      },
      created_at: {
        bsonType: "date",
        description: "Дата создания документа должна быть типа Date"
      }
    }
  }
};

try {
  database.runCommand({
    collMod: "events",
    validator: eventValidator,
    validationLevel: "strict",
    validationAction: "error"
  });
  print("Валидация для коллекции events успешно обновлена");
} catch (error) {
  print("Команда collMod не выполнилась, пробую создать коллекцию с валидатором");
  try {
    database.createCollection("events", {
      validator: eventValidator,
      validationLevel: "strict",
      validationAction: "error"
    });
    print("Коллекция events создана с валидацией");
  } catch (createError) {
    print("Создать коллекцию не удалось:");
    print(createError.message);
  }
}

print("\nПробую вставить невалидный документ в коллекцию events");

try {
  database.events.insertOne({
    title: "A",
    description: 12345,
    event_date: "2026-06-01",
    location: "",
    organizer_id: "wrong_id",
    created_at: new Date()
  });
  print("Ошибка: невалидный документ был вставлен");
} catch (error) {
  print("Ожидаемая ошибка валидации:");
  print(error.message);
}
