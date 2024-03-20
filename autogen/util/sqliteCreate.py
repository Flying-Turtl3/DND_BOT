import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('dnd_races.db')
c = conn.cursor()

# Create the table
c.execute('''
CREATE TABLE IF NOT EXISTS races (
    Race TEXT PRIMARY KEY,
    AbilityScoreIncrease TEXT,
    Traits TEXT,
    TraitDescriptions TEXT
)
''')

# Data to be inserted
races_data = [
    ("Dwarf", "Constitution +2", "Darkvision, Dwarven Resilience, Dwarven Combat Training, Stonecunning", "Night vision, resistance to poison, proficiency with certain weapons, expertise in stonework analysis"),
    ("Elf", "Dexterity +2", "Darkvision, Keen Senses, Fey Ancestry, Trance", "Night vision, proficiency in Perception, charm and sleep magic resistance, meditative rest"),
    ("Halfling", "Dexterity +2", "Lucky, Brave, Halfling Nimbleness", "Reroll 1s on d20s, resistance to fear, move through space of larger creatures"),
    ("Human", "+1 to all ability scores", "", "Versatile and adaptable nature"),
    ("Dragonborn", "Strength +2, Charisma +1", "Draconic Ancestry, Breath Weapon, Damage Resistance", "Choose a dragon type for damage type resistance, exhale destructive energy, resist same damage type"),
    ("Gnome", "Intelligence +2", "Darkvision, Gnome Cunning", "Night vision, advantage on all Intelligence, Wisdom, and Charisma saving throws against magic"),
    ("Half-Elf", "Charisma +2, two other ability scores +1", "Darkvision, Fey Ancestry, Skill Versatility", "Night vision, charm and sleep magic resistance, proficiency in two skills"),
    ("Half-Orc", "Strength +2, Constitution +1", "Darkvision, Savage Attacks, Relentless Endurance", "Night vision, extra critical hit damage, can drop to 1 HP instead of 0 once per long rest"),
    ("Tiefling", "Intelligence +1, Charisma +2", "Darkvision, Hellish Resistance, Infernal Legacy", "Night vision, resistance to fire damage, can cast Hellish Rebuke and Thaumaturgy")
]

# Insert the data
c.executemany('''
INSERT INTO races (Race, AbilityScoreIncrease, Traits, TraitDescriptions) VALUES (?, ?, ?, ?)
''', races_data)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully, and data inserted.")
