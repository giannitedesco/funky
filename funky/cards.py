from collections import namedtuple
from enum import Enum

class PlantType(Enum):
	stufe3 = -1
	green = 0
	coal = 1
	oil = 2
	hybrid = coal | oil
	trash = 4
	nuclear = 8

FunkCard = namedtuple('FunkCard', (
				'idx',
				'price',
				'type',
				'resources',
				'capacity',
			))

cards = (
	FunkCard(0,  3,  PlantType.oil,     1, 2),
	FunkCard(1,  4,  PlantType.coal,    2, 1),
	FunkCard(2,  5,  PlantType.hybrid,  2, 1),
	FunkCard(3,  6,  PlantType.trash,   1, 1),
	FunkCard(4,  7,  PlantType.oil,     3, 2),

	FunkCard(5,  8,  PlantType.coal,    3, 2),
	FunkCard(6,  9,  PlantType.oil,     1, 1),
	FunkCard(7,  10, PlantType.coal,    2, 2),
	FunkCard(8,  11, PlantType.nuclear, 1, 2),
	FunkCard(9,  12, PlantType.hybrid,  2, 2),

	FunkCard(10, 13, PlantType.green,   0, 1),
	FunkCard(11, 14, PlantType.trash,   2, 2),
	FunkCard(12, 15, PlantType.coal,    2, 3),
	FunkCard(13, 16, PlantType.oil,     2, 3),
	FunkCard(14, 17, PlantType.nuclear, 1, 2),

	FunkCard(15, 18, PlantType.green,   0, 2),
	FunkCard(16, 19, PlantType.trash,   2, 3),
	FunkCard(17, 20, PlantType.coal,    3, 5),
	FunkCard(18, 21, PlantType.hybrid,  2, 4),
	FunkCard(19, 22, PlantType.green,   0, 2),

	FunkCard(20, 23, PlantType.nuclear, 1, 3),
	FunkCard(21, 24, PlantType.trash,   2, 4),
	FunkCard(22, 25, PlantType.coal,    2, 5),
	FunkCard(23, 26, PlantType.oil,     2, 5),
	FunkCard(24, 27, PlantType.green,   0, 3),

	FunkCard(25, 28, PlantType.nuclear, 1, 4),
	FunkCard(26, 29, PlantType.hybrid,  1, 4),
	FunkCard(27, 30, PlantType.trash,   3, 6),
	FunkCard(28, 31, PlantType.coal,    3, 6),
	FunkCard(29, 32, PlantType.oil,     3, 6),

	FunkCard(30, 33, PlantType.green,   0, 4),
	FunkCard(31, 34, PlantType.nuclear, 1, 5),
	FunkCard(32, 35, PlantType.oil,     1, 5),
	FunkCard(33, 36, PlantType.coal,    3, 7),
	FunkCard(34, 37, PlantType.green,   0, 4),

	FunkCard(35, 38, PlantType.trash,   3, 7),
	FunkCard(36, 39, PlantType.nuclear, 1, 6),
	FunkCard(37, 40, PlantType.oil,     2, 6),
	FunkCard(38, 42, PlantType.coal,    2, 6),
	FunkCard(39, 44, PlantType.green,   0, 5),

	FunkCard(40, 46, PlantType.hybrid,  3, 7),
	FunkCard(41, 50, PlantType.green,   0, 6),
	FunkCard(42, -1, PlantType.stufe3,  0, 0), # phase 3
)
