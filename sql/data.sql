INSERT INTO races (name, skill, base_HP, base_speed, base_agility, base_damage, description) VALUES
    ('Man', 'Hardy', 100, 10, 100, 10, 'Humanity has had to struggle to hold their place in this world.  Humans are strong, fast, and highly adaptable.'),
    ('Elf', 'Uncanny Sense', 70, 13, 120, 8, 'Elves'),
    ('Dwarf', 'Strength of Stone', 130, 8, 80, 12, 'Dwarves'),
    ('Goblin', 'Blind Rage', 60, 15, 110, 9, 'Goblins are small, muscular, but frail-boned.  They are not the brightest of beings, and rely on instinct more than thought.');

INSERT INTO classes (name, skill) VALUES
    ('Basic', NULL),
    ('Berzerker', 'Berzerk'),
    ('Rogue', 'Stealth'),
    ('Battlemage', 'Magic Attacks'),
    ('Auramancer', 'Aura Boost'),
    ('Healing Mage', 'Healing'),
    ('Commander', 'Leadership'),
    ('Hero', 'Heroic Feat');

INSERT INTO armors (name, defense_bonus, weight, description) VALUES
    ('None', 0, 0, 'No armor'),
    ('Leather Armor', 2, 5, 'A light, flexible armor made from treated animal hide.'),
    ('Gambison', 5, 15, 'A thick, padded armor made from animal hide and wool.'),
    ('Studded Leather', 7, 10, 'A leather armor with metal studs for added protection.'),
    ('Chainmail', 10, 20, 'A series of interlocking metal rings that provide good protection and mobility.'),
    ('Dwarf Mail', 12, 25, 'A heavier version of chainmail, made from thick, square metal rings.'),
    ('Elf Weave', 15, 30, 'A lightweight mail armor made from interwoven strips of metal.'),
    ('Bone Armor', 18, 35, 'A heavy armor made from a patchwork of bones.'),
    ('Plate Armor', 20, 40, 'The ultimate in protection, plate armor is made from interlocking metal plates.'),
    ('Heavy Plate Mail', 25, 45, 'The heaviest of all armor, plate mail is made from interlocking metal plates and chainmail.');

INSERT INTO weapons (name, damage, damage_type, range, description) VALUES
    ('None', 10, 'mundane', 0, 'No weapon equipped, he is fighting with his fists.'),
    ('Infantry Sword', 40, 'mundane', 1, 'A short, one-handed and double-edged blade.  Ideal for fighting in close quarters.'),
    ('Bow', 50, 'mundane', 60, 'Long-range projectile weapon.'),
    ('Longbow', 60, 'mundane', 100, 'A larger, more powerful bow.');

INSERT INTO squads (name, commander, description) VALUES
    ('Lion Knights', 'default', 'A squad of Lion Knights'),
    ('Dragon Knights', 'default', 'A squad of Dragon Knights');

INSERT INTO units (squad_id, name, race, class, level, armor, weapon, description) VALUES
    (1, 'George the Lion', 'Man', 'Basic', 1, 'None', 'Infantry Sword', 'George serves the Lion Knights with honor.'),
    (2, 'Halvar the Dragon', 'Man', 'Basic', 1, 'Leather Armor', 'Infantry Sword', 'Halvar is a Dragon Knights reknowned for his courage and daring.');