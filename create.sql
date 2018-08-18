DROP TABLE IF EXISTS recipes;

CREATE TABLE IF NOT EXISTS recipes (
  id SERIAL PRIMARY KEY,
  -- name of recipe
  title varchar(100) NOT NULL,
  -- time required to cook/bake the recipe
  making_time varchar(100)NOT NULL,
  -- number of people the recipe will feed
  serves varchar(100)  NOT NULL,
  -- food items necessary to prepare the recipe
  ingredients varchar(300)  NOT NULL,
  -- price of recipe
  cost integer NOT NULL
);

INSERT INTO recipes (
  id,
  title,
  making_time,
  serves,
  ingredients,
  cost
)
VALUES (
  1,
  'チキンカレー',
  '45分',
  '4人',
  '玉ねぎ,肉,スパイス',
  1000
);

INSERT INTO recipes (
  id,
  title,
  making_time,
  serves,
  ingredients,
  cost
)
VALUES (
  2,
  'オムライス',
  '30分',
  '2人',
  '玉ねぎ,卵,スパイス,醤油',
  700
);
