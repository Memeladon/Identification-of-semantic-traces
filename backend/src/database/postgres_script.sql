CREATE TABLE "site_user" (
  "id" SERIAL PRIMARY KEY,
  "username" VARCHAR(32) NOT NULL,
  "full_name" TEXT NOT NULL,
  "password" TEXT NOT NULL,
  "created_at" TIMESTAMP,
  "modified_at" TIMESTAMP
);

CREATE TABLE "chat_of_interest" (
  "id" SERIAL PRIMARY KEY,
  "site_user" INTEGER NOT NULL,
  "name" BYTEA
);

CREATE INDEX "idx_chat_of_interest__site_user" ON "chat_of_interest" ("site_user");

ALTER TABLE "chat_of_interest" ADD CONSTRAINT "fk_chat_of_interest__site_user" FOREIGN KEY ("site_user") REFERENCES "site_user" ("id") ON DELETE CASCADE;

CREATE TABLE "chat" (
  "id" SERIAL PRIMARY KEY,
  "chat_of_interest" INTEGER,
  "title" TEXT NOT NULL,
  "type" TEXT NOT NULL,
  "last_message" TEXT NOT NULL,
  "chatphoto" TEXT NOT NULL,
  "interest_status" INTEGER
);

CREATE INDEX "idx_chat__chat_of_interest" ON "chat" ("chat_of_interest");

ALTER TABLE "chat" ADD CONSTRAINT "fk_chat__chat_of_interest" FOREIGN KEY ("chat_of_interest") REFERENCES "chat_of_interest" ("id") ON DELETE SET NULL;

CREATE TABLE "user_of_interest" (
  "id" INTEGER PRIMARY KEY,
  "site_user" INTEGER NOT NULL,
  "name" TEXT NOT NULL
);

CREATE INDEX "idx_user_of_interest__site_user" ON "user_of_interest" ("site_user");

ALTER TABLE "user_of_interest" ADD CONSTRAINT "fk_user_of_interest__site_user" FOREIGN KEY ("site_user") REFERENCES "site_user" ("id") ON DELETE CASCADE;

CREATE TABLE "user" (
  "id" SERIAL PRIMARY KEY,
  "user_of_interest" INTEGER,
  "first_name" TEXT NOT NULL,
  "last_name" TEXT NOT NULL,
  "username" TEXT NOT NULL,
  "phone_number" TEXT NOT NULL,
  "profilephoto" TEXT NOT NULL,
  "interest_status" INTEGER
);

CREATE INDEX "idx_user__user_of_interest" ON "user" ("user_of_interest");

ALTER TABLE "user" ADD CONSTRAINT "fk_user__user_of_interest" FOREIGN KEY ("user_of_interest") REFERENCES "user_of_interest" ("id") ON DELETE SET NULL