INSERT INTO races (name, skill, base_HP, base_speed, base_agility, base_damage, description) VALUES
    ('Man', 'Hardy', 100, 10, 100, 10, 'Humanity has had to struggle to hold their place in this world.  Humans are strong, fast, and highly adaptable.'),
    ('Elf', 'Uncanny Sense', 70, 13, 120, 8, 'Elves'),
    ('Dwarf', 'Strength of Stone', 130, 8, 80, 12, 'Dwarves'),
    ('Goblin', 'Blind Rage', 60, 15, 110, 9, 'Goblins are small, muscular, but frail-boned.  They are not the brightest of beings, and rely on instinct more than thought.');

INSERT INTO classes (name, skill) VALUES
    ('Basic', NULL),
    ('Knight', 'Vows of Honor'),
    ('Marksman', 'Keen Aim'),
    ('Berzerker', 'Berzerk'),
    ('Rogue', 'Stealth'),
    ('Battlemage', 'Magic Attacks'),
    ('Auramancer', 'Aura Boost'),
    ('Healing Mage', 'Healing'),
    ('Commander', 'Leadership'),
    ('Hero', 'Heroic Feat');

INSERT INTO armors (name, defense_bonus, weight, description) VALUES
    ('Literally Nothing', 0, 0, 'No armor'),
    ('Ornamental Robes', 1, 0, 'Look fancy, but offer about as much protection as you would expect.'),
    ('Enchanted Wizard Robes', 10, 0, 'Robes that have been enchanted to provide some protection.'),
    ('Leather Armor', 2, 1, 'A light, flexible armor made from treated animal hide.'),
    ('Gambison', 5, 1, 'A thick, padded armor made from animal hide and wool.'),
    ('Studded Leather', 7, 2, 'A leather armor with metal studs for added protection.'),
    ('Chainmail', 10, 3, 'A series of interlocking metal rings that provide good protection and mobility.'),
    ('Dwarf Mail', 12, 4, 'A heavier version of chainmail, made from thick, square metal rings.'),
    ('Elf Weave', 15, 2, 'A lightweight mail armor made from interwoven strips of metal.'),
    ('Bone Armor', 18, 3, 'A heavy armor made from a patchwork of bones.'),
    ('Plate Armor', 20, 4, 'A strong protection, plate armor is made from interlocking metal plates.'),
    ('Heavy Plate Mail', 25, 5, 'The heaviest of all armor, plate mail is made from interlocking metal plates and chainmail.');

INSERT INTO weapons (name, damage, damage_type, range, description) VALUES
    ('None', 10, 'mundane', 0, 'No weapon equipped, he is fighting with his fists.'),
    ('Infantry Sword', 40, 'mundane', 1, 'A short, one-handed and double-edged blade.  Ideal for fighting in close quarters.'),
    ('Greatsword', 50, 'mundane', 1, 'A large, heavy sword.'),
    ('Longsword', 45, 'mundane', 1, 'A long, double-edged blade.'),
    ('Battleaxe', 45, 'mundane', 1, 'A heavy axe with a long handle.'),
    ('Dwarven Battleaxe', 50, 'mundane', 1, 'A heavy axe with a long handle.'),
    ('Dwarven Greatsword', 60, 'mundane', 1, 'A strong, heavy sword forged by dwarves.'),
    ('Elf Blade', 40, 'mundane', 1, 'A sleek, one-edged blade ideal for slashing.'),
    ('Goblin Spear', 30, 'mundane', 1, 'A spear made of wood and bone, poorly made but effective.'),
    ('Goblin Dagger', 20, 'mundane', 1, 'A small, sharp dagger, mishapen but deadly.'),
    ('Bone Club', 30, 'mundane', 1, 'A club made of bone, powerful but heavy.'),
    ('Bow', 50, 'mundane', 80, 'Long-range projectile weapon.'),
    ('Longbow', 60, 'mundane', 100, 'A larger, more powerful bow.'),
    ('Crossbow', 80, 'mundane', 60, 'A ranged weapon that fires bolts.'),
    ('Dwarven Crossbow', 100, 'mundane', 60, 'A ranged weapon that fires bolts.'),
    ('Elf Bow', 60, 'mundane', 110, 'The ultimate ranged weapon, made by elves.');

INSERT INTO squads (name, commander, description) VALUES
    ('Lion Knights', 'default', 'A squad of Lion Knights'),
    ('Dwarves of Underhall', 'default', 'The powerful and wealthy kingdom of Dwarves.'),
    ('Horde of the Western Wastes', 'default', 'A nomadic tribe of goblins, who roam the deserts and wastelands.'),
    ('Goldenleaf Elves', 'default', 'A kingdom of elves who live in the Western Woods, known for their combination of magic, horticulture, and mining.'),
    ('Falcon Knights', 'default', 'A squad of Falcon Knights.'),
    ('Moonblessed Elves', 'default', 'A kingdom of elves living high in the mountains who worship the moon..');

INSERT INTO units (squad_id, name, race, class, armor, weapon, description) VALUES
    (1, 'George', 'Man', 'Basic', 'Gambison', 'Infantry Sword', 'An infantry soldier of the Lion Knights.'),
    (1, 'Henrik', 'Man', 'Basic', 'Gambison', 'Infantry Sword', 'An infantry soldier of the Lion Knights.'),
    (1, 'Melvedar', 'Man', 'Battlemage', 'Enchanted Wizard Robes', 'None', 'A battlemage of the Lion Knights.'),
    (1, 'Will', 'Man', 'Knight', 'Plate Armor', 'Infantry Sword', 'A knight of the Lion Knights.'),
    (2, 'Durrennal', 'Dwarf', 'Basic', 'Dwarf Mail', 'Dwarven Greatsword', 'A dwarf soldier.'),
    (2, 'Goreggel', 'Dwarf', 'Basic', 'Dwarf Mail', 'Dwarven Battleaxe', 'A dwarf soldier.'),
    (2, 'Nurhallen', 'Dwarf', 'Marksman', 'Dwarf Mail', 'Dwarven Crossbow', 'A dwarf crossbowman.'),
    (2, 'Ahlarromen', 'Dwarf', 'Berzerker', 'Literally Nothing', 'Bone Club', 'A dwarf berzerker.'),
    (3, 'Nug', 'Goblin', 'Basic', 'Literally Nothing', 'Goblin Spear', 'A goblin soldier.'),
    (3, 'Haj', 'Goblin', 'Basic', 'Literally Nothing', 'Goblin Spear', 'A goblin soldier.'),
    (3, 'Nek', 'Goblin', 'Basic', 'Literally Nothing', 'Goblin Spear', 'A goblin soldier.'),
    (3, 'Org', 'Goblin', 'Rogue', 'Leather Armor', 'Goblin Dagger', 'A goblin assasin.'),
    (4, 'Kelawill', 'Elf', 'Basic', 'Elf Weave', 'Elf Blade', 'An elf soldier.'),
    (4, 'Forlandin', 'Elf', 'Basic', 'Elf Weave', 'Elf Blade', 'An elf soldier.'),
    (4, 'Grasbell', 'Elf', 'Battlemage', 'Plate Armor', 'Longsword', 'An elf battlemage.'),
    (4, 'Urthalen', 'Elf', 'Auramancer', 'Enchanted Wizard Robes', 'None', 'An elf auramancer.'),
    (5, 'Friedman', 'Man', 'Knight', 'Chainmail', 'Longsword', 'A falcon knight.'),
    (5, 'Ned', 'Man', 'Knight', 'Chainmail', 'Longsword', 'A falcon knight.'),
    (5, 'Edvard', 'Man', 'Knight', 'Chainmail', 'Battleaxe', 'A falcon knight.'),
    (5, 'Jamieson', 'Man', 'Knight', 'Plate Armor', 'Longbow', 'A falcon knight.'),
    (6, 'Moonstone', 'Elf', 'Battlemage', 'Elf Weave', 'Elf Bow', 'An elf soldier.'),
    (6, 'Moonbeam', 'Elf', 'Battlemage', 'Elf Weave', 'Elf Blade', 'An elf soldier.'),
    (6, 'Mooncrest', 'Elf', 'Battlemage', 'Elf Weave', 'Elf Blade', 'An elf soldier.'),
    (6, 'Moonlight', 'Elf', 'Battlemage', 'Elf Weave', 'Greatsword', 'An elf captain.');

