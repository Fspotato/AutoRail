from enum import Enum

# 路徑文檔

# 凝滯虛影(路徑)
class StagnantShadow(Enum):
    QUANTA = "quanta.png"
    GUST = "gust.png"
    FULMINATION = "fulmination.png"
    BLAZE = "blaze.png"
    SPIKE = "spike.png"
    RIME = "rime.png"
    MIRAGE = "mirage.png"
    ICICLE = "icicle.png"
    DOOM = "doom.png"
    PUPPERTRY = "puppertry.png"
    ABOMINATION = "abomination.png"
    CELESTITAL = "celestital.png"
    PERDITION = "perdition.png"
    SCORCH = "scorch.png"
    ROAST = "roast.png"
    NECTAR = "nectar.png"
    IRE = "ire.png"

# 地點(路徑)
class Place(Enum):
    BELOBOG = "belobog.png"
    LUOFU = "luofu.png"
    PENACONY = "penacony.png"

# 行跡素材(路徑)
class CrimsonFlower(Enum):
    ARROW_OF_THE_STARCHASER = "arrow_of_the_starchaser.png"
    FLOWER_OF_ETERNITY = "flower_of_eternity.png"
    HEAVEN_INCINERATOR = "heaven_incinerator.png"
    HEAVENLY_MELODY = "heavenly_melody.png"
    KEY_OF_WISDOM = "key_of_wisdom.png"
    MOON_MADNESS_FANG = "moon_madness_fang.png"
    MYRIAD_FRUIT = "myriad_fruit.png"
    OBSIDIAN_OF_OBSSESSIN = "obsidian_of_obsessin.png"
    SAFEGUARD_OF_AMBER = "safeguard_of_amber.png"
    STELLARIS_SYMPHONY = "stellaris_symphony.png"
    WORLDBREAKER_BLADE = "worldbreaker_blade.png"

# 遺器(路徑)
class Cavern(Enum):
    CONFLAGRATION = "conflagration.png"
    DARKNESS = "darkness.png"
    DREAMDIVE = "dreamdive.png"
    DRIFTING = "drifting.png"
    ELIXIR_SEEKERS = "elixir_seekers.png"
    GELID_WIND = "gelid_wind.png"
    HOLY_HYMN = "holy_hymn.png"
    JABBING_PUNCH = "jabbing_punch.png"
    PROVIDENCE = "providence.png"

# 歷戰餘響(路徑)
class Echo(Enum):
    DESTRUCTION = "destruction.png"
    ETERNAL_FREEZE = "eternal_freeze.png"
    DIVINE_SEED = "devine_seed.png"

# 強化素材(路徑)
class GoldenFlower(Enum):
    CREDIT = "credit.png"
    CHARACTER_EXP = 'character_exp.png'
    LIGHT_CONE_EXP = "light_cone_exp.png"

# 戰鬥相關(路徑)
AGAIN = "again.png"
BATTLE_START = "battle_start.png"
BATLLE_REAL_START = "battle_real_start.png"
EXIT_BATTLE = "exit_battle.png"
FUEL = "fuel.png"
POWER_REPLENISH = "power_replenish.png"

# 指南相關(路徑)
CAVERN_OF_CORROSION = "cavern.png"
CLAIM_DAILY_REWARD = "claim_daily_reward.png"
CLAIM_ALL_DAILY_REWARD = "claim_all_daily_reward.png"
CRIMSON_FLOWER = "crimson_flower.png"
DAILY_REWARD = "daily_reward.png"
ECHO_OF_WAR = "echo.png"
GOLDEN_FLOWER = "golden_flower.png"
GUIDE = "guide.png"
STAGNANT_SHADOW = "stagnant_shadow.png"
SURVIVAL = "survival.png"

# 日常任務相關(路徑)
ASSIGNMENT = "assignment.png"
ASSIGNMENT_AGAIN = "assignment_again.png"
NAMELESS_HONOR = "nameless_honor.png"
MISSIONS = "missions.png"
REWARDS = "rewards.png"

# 通用(路徑)
BACK_TO_LOGIN = "back_to_login.png"
CHARACTER_EXP = "character_exp.png"
CLOSE = "close.png"
CONFIRM = "confirm.png"
CONFIRM_YELLOW = 'confirm_yellow.png'
CREDIT = "credit.png"
EXIT_GAME = "exit_game.png"
FAST_CLAIM = "fast_claim.png"
LIGHT_CONE_EXP = "light_cone_exp.png"
PHONE = "phone.png"
SPACE_CLOSE = "space_close.png"
TRAILBLAZE_EXP = "trailblaze_exp.png"

# 繁體中文文檔

# 凝滯虛影
class StagnantShadowText(Enum):
    QUANTA_TEXT = "空海之形．量子"
    GUST_TEXT = "巽風之形．風"
    FULMINATION_TEXT = "鳴雷之形．雷"
    BLAZE_TEXT = "炎華之形．火"
    SPIKE_TEXT = "鋒芒之形．物理"
    RIME_TEXT = "霜晶之形．冰"
    MIRAGE_TEXT = "幻光之形．虛數"
    ICICLE_TEXT = "冰稜之形．冰"
    DOOM_TEXT = "震厄之形．雷"
    PUPPERTRY_TEXT = "偃偶之形．虛數"
    ABOMINATION_TEXT = "孽獸之形．量子"
    CELESTITAL_TEXT = "天人之形．風"
    PERDITION_TEXT = "幽府之形．物理"
    SCORCH_TEXT = "燔灼之形．火"
    ROAST_TEXT = "焦灼之形．量子"
    NECTAR_TEXT = "冰釀之形．冰"
    IRE_TEXT = "嗔怒之形．火"

# 行跡素材
class CrimsonFlowerText(Enum):
    ARROW_OF_THE_STARCHASER = "逐星之矢．巡獵"
    FLOWER_OF_ETERNITY = "永恆之花．豐饒"
    HEAVEN_INCINERATOR = "焚天之魔．虛無"
    HEAVENLY_MELODY = "天外樂章．同諧"
    KEY_OF_WISDOM = "智識之鑰．智識"
    MOON_MADNESS_FANG = "月狂獠牙．毀滅"
    MYRIAD_FRUIT = "萬相果實．豐饒"
    OBSIDIAN_OF_OBSSESSIN = "沉淪黑曜．虛無"
    SAFEGUARD_OF_AMBER = "琥珀堅守．存護"
    STELLARIS_SYMPHONY = "群星樂章．同諧"
    WORLDBREAKER_BLADE = "淨世殘刃．毀滅"

# 遺器
class CavernText(Enum):
    CONFLAGRATION = "野焰之徑 (火套、虛數)"
    DARKNESS = "幽冥之徑 (大公、持傷)"
    DREAMDIVE = "夢潛之徑 (死水、鐘錶)"
    DRIFTING = "漂泊之徑 (治癒、快槍)"
    ELIXIR_SEEKERS = "藥使之徑 (蒔者、信使)"
    GELID_WIND = "霜風之徑 (冰套、風套)"
    HOLY_HYMN = "聖頌之徑 (雷套、護盾)"
    JABBING_PUNCH = "迅拳之徑 (物理、擊破)"
    PROVIDENCE = "睿治之徑 (鐵衛、量子)"

# 地點
class PlaceText(Enum):
    BELOBOG_TEXT = "貝洛柏格"
    LUOFU_TEXT = "仙舟(羅浮)"
    PENACONY_TEXT = "匹諾康尼"

# 強化素材
class GoldenFlowerText(Enum):
    CHARACTER_EXP_TEXT = "角色經驗"
    CREDIT_TEXT = "信用點"
    LIGHT_CONE_EXP_TEXT = "光錐經驗"

# 歷戰餘響
class EchoText(Enum):
    DESTRUCTION = "毀滅的開端．末日獸"
    ETERNAL_FREEZE = "寒潮的落幕．可可莉亞"
    DIVINE_SEED = "不死的神實．幻朧"

# 指南相關
CAVERN_OF_CORROSION_TEXT = "侵蝕隧洞"
CRIMSON_FLOWER_TEXT = "擬造花萼(赤)"
ECHO_OF_WAR_TEXT = "歷戰餘響"
GOLDEN_FLOWER_TEXT = "擬造花萼(金)"
STAGNANT_SHADOW_TEXT = "凝滯虛影"

# 日常相關
NAMELESS_HONOR_TEXT = "無名勳禮"
DAILY_REWARD_TEXT = "每日任務"
ASSIGNMENT_TEXT = "委託任務"

# 通用
CHARACTER_EXP_TEXT = "角色經驗"
CREDIT_TEXT = "信用點"
LIGHT_CONE_EXP_TEXT = "光錐經驗"


action_thread_stop = [False]

Log_print = []