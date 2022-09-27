class UserObject(object):
    """
    User object, returned from a database.
    """

    def __init__(self, bank, wallet, items, control):
        self.bank = bank
        self.wallet = wallet
        self.items = items
        self.control = control

    def __repr__(self):
        return f"User(bank={self.bank}, wallet={self.wallet}, items={self.items}, control = {self.control})"


class UserObjectLevel(object):
    """
    User object, returned from a database.
    """

    def __init__(self, level, points, xp, gamble, fish):
        
        self.level = level
        self.points = points
        self.xp = xp
        self.gamble = gamble
        self.fish = fish

    def __repr__(self):
        return f"User(level = {self.level}, points = {self.points}, xp = {self.xp}, gamble = {self.gamble}, fish = {self.fish})"

class UserObjectTurf(object):
    """
    User object, returned from a database.
    """

    def __init__(self, faction, region, esp, cesp , prot, att, work, total, control):
        
        self.faction = faction
        self.region = region
        self.esp = esp
        self.cesp = cesp
        self.prot = prot
        self.att = att
        self.work = work
        self.total = total
        self.control = control
    def __repr__(self):
        return f"User(faction = {self.faction}, region = {self.region}, esp = {self.esp}, cesp = {self.cesp}, prot = {self.prot}, att= {self.att}, work = {self.work}, total = {self.total}, control = {self.control})"

class UserObjectRPG(object):
    """
    User object, returned from a database.
    """

    def __init__(self, job, level, xp , stren, dex, cons, intel, wis, cha, bag, bank, pouch, head, chest, legs, foot, weapon, belt, mana, points):
        
        self.job = job
        self.level = level
        self.xp = xp
        self.stren= stren
        self.dex = dex
        self.cons = cons
        self.intel = intel
        self.wis = wis
        self.cha = cha
        self.bag = bag
        self.bank = bank
        self.pouch = pouch
        self.head = head
        self.chest = chest
        self.legs = legs
        self.foot = foot
        self.weapon = weapon
        self.belt = belt
        self.mana = mana
        self.points = points

    def __repr__(self):
        return f"User(job = {self.job}, level = {self.level}, xp = {self.xp}, stren= {self.stren}, dex = {self.dex}, cons = {self.cons}, intel = {self.intel}, wis = {self.wis}, cha = {self.cha}, bag = {self.bag}, bank = {self.bank}, pouch = {self.pouch}, head = {self.head}, chest = {self.chest}, legs = {self.legs}, foot = {self.foot}, weapon = {self.weapon}, belt = {self.belt}, mana = {self.mana}, points = {self.points})"


class UserObjectCrime(object):
    """
    User object, returned from crime database.
    """

    def __init__(self, plant, metal, wood, stone, water, electric, item, rob , steal , arson , deal , worker, gatherer, thug, agent, control):
        
        self.plant = plant
        self.metal = metal
        self.wood = wood
        self.stone = stone
        self.water = water
        self.electric = electric
        self.item = item
        self.rob = rob
        self.steal = steal
        self.arson = arson
        self.deal = deal
        self.worker = worker
        self.gatherer = gatherer
        self.thug = thug
        self.agent = agent
        self.control = control

    def __repr__(self):
        return f"User(plant = {self.plant}, metal = {self.metal}, wood = {self.wood}, stone = {self.stone}, water = {self.water}, electric = {self.electric}, items = {self.item},rob = {self.rob}, steal = {self.steal}, arson = {self.arson}, deal = {self.deal}, worker ={self.worker}, gatherer = {self.gatherer}, thug = {self.thug}, agent = {self.agent}, control = {self.control})"

