INSERT INTO races (name, skill, base_HP, base_speed, description) VALUES
    ('Man', 'Hardy', 100, 10, 'Humanity has had to struggle to hold their place in this world.  Humans are strong, fast, and highly adaptable.'),
    ('Elf', 'Uncanny Sense', 70, 13, 'Elves'),
    ('Dwarf', 'Strength of Stone', 130, 8, 'Dwarves'),
    ('Goblin', 'Blind Rage', 60, 15, 'Goblins are small, muscular, but frail-boned.  They are not the brightest of beings, and rely on instinct more than thought.');

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
    ('Light', 2, 5, 'Basic protection, high mobility'),
    ('Medium', 5, 15, 'Balanced protection and mobility'),
    ('Heavy', 8, 30, 'Maximum protection, reduced mobility');

INSERT INTO weapons (name, damage, damage_type, range, description) VALUES
    ('None', 10, 'impact', 0, 'No weapon equipped, he is fighting with his fists.'),
    ('Infantry Sword', 40, 'slashing', 1, 'A short, one-handed and double-edged blade.  Ideal for fighting in close quarters.'),
    ('Bow', 50, 'piercing', 60, 'Long-range projectile weapon.'),
    ('Longbow', 60, 'piercing', 100, 'A larger, more powerful bow.');
