CREATE TABLE IF NOT EXISTS "businesses" (
  "business_id" varchar PRIMARY KEY,
  "name" varchar,
  "url" varchar,
  "address" varchar,
  "city" varchar,
  "state" varchar,
  "postal_code" integer,
  "review_count" integer,
  "rating" float,
  "price" varchar
);

CREATE TABLE IF NOT EXISTS "category" (
  "category_id" integer PRIMARY KEY,
  "alias" varchar,
  "title" varchar
);

CREATE TABLE IF NOT EXISTS "business_categories" (
  "business_id" varchar,
  "category_id" integer
);

CREATE TABLE IF NOT EXISTS "mobile_friendly" (
  "business_id" varchar PRIMARY KEY,
  "mobile_friendliness" boolean,
  "screenshot" varchar,
  "last_updated" timestamp
);

CREATE TABLE IF NOT EXISTS "google_my_business" (
  "business_id" varchar PRIMARY KEY,
  "verified_status" boolean
);

CREATE TABLE IF NOT EXISTS "zip_codes" (
  "id" int PRIMARY KEY,
  "zip_code" int,
  "state" varchar
);

ALTER TABLE "business_categories" ADD FOREIGN KEY ("business_id") REFERENCES "businesses" ("business_id");

ALTER TABLE "business_categories" ADD FOREIGN KEY ("category_id") REFERENCES "category" ("category_id");

ALTER TABLE "mobile_friendly" ADD FOREIGN KEY ("business_id") REFERENCES "businesses" ("business_id");

ALTER TABLE "google_my_business" ADD FOREIGN KEY ("business_id") REFERENCES "businesses" ("business_id");
