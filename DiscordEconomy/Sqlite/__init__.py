import asyncio
from asyncio import tasks
from sqlite3 import connect
import typing
import random
import aiosqlite

from ..exceptions import (NoItemFound, ItemAlreadyExists)
from ..objects import UserObject, UserObjectLevel, UserObjectTurf, UserObjectRPG, UserObjectCrime

from ..__version__ import check_for_updates

__all__ = ["Economy"]


class Economy:
    def __init__(self, database_name: typing.Optional[str] = "database.db"):
        """
        Initialize default options, save database name
        """

        self.__database_name = database_name
        self.__loop = asyncio.get_event_loop()

        self.__loop.run_until_complete(self.__is_table_exists())
        self.__loop.run_until_complete(check_for_updates())


    async def __is_table_exists(self) -> None:
        """Checks if table exists, if not it creates economy table"""

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        await c.execute("CREATE TABLE IF NOT EXISTS economy(id integer, bank integer, wallet integer, items text, control integer)")
        await c.execute("CREATE TABLE IF NOT EXISTS level(id integer, level integer, points integer, xp integer, gamble integer, fish integer)")
        await c.execute("CREATE TABLE IF NOT EXISTS rpg(id integer , job integer, level integer, xp integer, stren integer, dex integer, cons integer, intel integer, wis integer , cha integer, bag text, bank integer, pouch integer, head text, chest text, legs text, foot text, weapon text, belt text, mana integer, points integer)")
        await c.execute("CREATE TABLE IF NOT EXISTS crime(id integer, plant integer, metal integer, wood integer, stone integer, water integer, electric integer, items text, rob integer, steal integer, arson integer, deal integer, worker integer, gatherer integer, thug integer, agent integer, control text)")
        await c.execute("CREATE TABLE IF NOT EXISTS turf(id integer, faction integer, region integer, esp integer, cesp integer , prot integer, att integer, work integer , total integer , control text)")
        await con.commit()
        await con.close()
    
    


    async def is_registered(self, user_id: typing.Union[str, int]) -> bool:
        """
        **Params**:
        \n
        user_id - user id to check if it is in the database

        **Returns**:
        \n
        bool
        """

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        query = await c.execute("SELECT * FROM economy WHERE id = ?", (user_id,))
        query = await query.fetchone()
       

        if not query:
            await c.execute(f"INSERT INTO economy VALUES(?, 0, 0, ?, 0)", (user_id, ""))
        
        await con.commit()
        
        await con.close()

        return True

    async def is_lvlregistered(self, user_id: typing.Union[str, int]) -> bool:
        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        query = await c.execute("SELECT * FROM level WHERE id = ?", (user_id,))
        query = await query.fetchone()
       

        if not query:
            await c.execute(f"INSERT INTO level VALUES({user_id}, 0, 0, 0, 0, 0)")
        
        await con.commit()
        
        await con.close()

        return True
    


    async def get_user(self, user_id: typing.Union[str, int]) -> UserObject:
        """
        Obtains user from a database

        **Code Example**:
        \n
        ```python
        import DiscordEconomy
        import asyncio

        economy = DiscordEconomy.Economy()


        async def main() -> None:
            await economy.is_registered(12345)
            user = await economy.get_user(12345)

            print(user.wallet)
            print(user.bank)
            print(user.items)

        asyncio.get_event_loop().run_until_complete(main())
        ```

        **Params**:
        \n
        user_id - user id to obtain it from this id

        **Returns**:
        \n
        UserObject

        """

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        r = await c.execute("SELECT * FROM economy WHERE id = ?", (user_id,))
        r = await r.fetchone()

        await con.close()

        bank = r[1]
        wallet = r[2]
        items = r[3].split(" | ")
        control = r[4]
       

        if items[0] == "":
            items.pop(0)

        return UserObject(bank, wallet, items, control)

    async def get_user_lvl(self, user_id: typing.Union[str, int]) -> UserObject:
        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        r = await c.execute("SELECT * FROM level WHERE id = ?", (user_id,))
        r = await r.fetchone()

        await con.close()

        level = r[1]
        points = r[2]
        xp = r[3]
        gamble = r[4]
        fish = r[5]
        
        return UserObjectLevel(level,points, xp, gamble, fish)


    async def delete_user_account(self, user_id: typing.Union[str, int]) -> None:
        """
        Deletes user account from a database

        **Params**:
        \n
        user_id - which user should be deleted

        **Returns**:
        \n
        bool
        """

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        await c.execute("DELETE FROM economy WHERE id = ?", (user_id,))

        await con.commit()
        await con.close()


    async def get_all_data(self) -> typing.AsyncGenerator[UserObject, None]:
        """
        Obtains all data from database

        **Code Example**:
        \n
        ```python
        import DiscordEconomy
        import asyncio

        economy = DiscordEconomy.Economy()


        async def main() -> None:
            r = economy.get_all_data()
            async for i in r:
                print(i.bank)

        asyncio.get_event_loop().run_until_complete(main())
        ```

        **Params**:
        \n
        Doesn't take any params

        **Returns**:
        \n
        async generator of UserObject

        """

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        r = await c.execute("SELECT * FROM economy")
        r = await r.fetchall()

        await con.close()

        for user in r:
            items = user[3].split(" | ")

            if items[0] == "":
                items.pop(0)

            yield UserObject(user[1], user[2], items)
    
   
        

   


    async def add_money(self, user_id: typing.Union[str, int], value: str, amount: int) -> None:
        """
        Adds money to user account

        **Code Example**:
        \n
        ```python
        import DiscordEconomy
        import asyncio

        economy = DiscordEconomy.Economy()


        async def main() -> None:
            await economy.is_registered(12345)
            await economy.add_money(12345, "wallet", 500)

        asyncio.get_event_loop().run_until_complete(main())
        ```

        **Params**:
        \n
        user_id - user id to add money to

        value - in what place money should be added, for example 'bank' or 'wallet'

        amount - how much should be added to user account

        **Returns**:
        \n
        None
        """

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        user_account = await c.execute(f"SELECT {value} FROM economy WHERE id = ?", (user_id,))
        user_account = await user_account.fetchone()
        user_account = user_account[0]

        money = user_account + amount

        await c.execute(f"UPDATE economy SET {value} = ? WHERE id = ?", (money, user_id,))

        await con.commit()
        await con.close()


    async def remove_money(self, user_id: typing.Union[str, int], value: str, amount: int) -> None:
        """
        Adds money to user account

        **Params**:
        \n
        user_id - user id to add money to

        value - in what place money should be removed, for example 'bank' or 'wallet'

        amount - how much should be removed from user account

        **Returns**:
        \n
        None
        """

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        user_account = await c.execute(f"SELECT {value} FROM economy WHERE id = ?", (user_id,))
        user_account = await user_account.fetchone()
        user_account = user_account[0]

        money = user_account - amount

        await c.execute(f"UPDATE economy SET {value} = ? WHERE id = ?", (money, user_id,))

        await con.commit()
        await con.close()


    async def set_money(self, user_id: typing.Union[str, int], value: str, amount: int) -> None:
        """
        Sets user money to certain amount

        **Params**:
        \n
        user_id - user id to set money

        value - in what place money should be set, for example 'bank' or 'wallet'

        amount - to what amount money should be set

        **Returns**:
        \n
        None
        """

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        await c.execute(f"UPDATE economy SET {value} = ? WHERE id = ?", (amount, user_id,))

        await con.commit()
        await con.close()

    
    async def add_item(self, user_id: typing.Union[str, int], item: str,) -> None:    
        """
        Adds item to user account

        **Code Example**:
        \n
        ```python
        import DiscordEconomy
        import asyncio

        economy = DiscordEconomy.Economy()


        async def main() -> None:
            await economy.is_registered(12345)
            await economy.add_item(12345, "sword")

        asyncio.get_event_loop().run_until_complete(main())
        ```

        **Params**:
        \n
        user_id - user id where the item should be added

        item - which item should be added to user

        **Returns**:
        \n
        None | if user already have this item raises ItemAlreadyExists
        """

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        query = await c.execute("SELECT items FROM economy WHERE id = ?", (user_id,))
        query = await query.fetchone()

        _user_items = query[0].split(" | ")


        #if item in _user_items:
         #   raise ItemAlreadyExists("User already have this item")

        _user_items.append(item)
        
        
        await c.execute("UPDATE economy SET items = ? WHERE id = ?", (" | ".join(_user_items), user_id))
    
        await con.commit()
        await con.close()


    async def remove_item(self, user_id: typing.Union[str, int], item: str) -> None:
        """
        Removes item to user account

        **Params**:
        \n
        user_id - user id where the item should be removed

        item - which item should be removed from user

        **Returns**:
        \n
        None
        """

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        query = await c.execute("SELECT items FROM economy WHERE id = ?", (user_id,))
        query = await query.fetchone()

        _user_items = query[0].split(" | ")

        if item in _user_items:
            _user_items.pop(_user_items.index(item))

            await c.execute("UPDATE economy SET items = ? WHERE id = ?", (" | ".join(_user_items), user_id))

            await con.commit()
            await con.close()


        else:
            raise NoItemFound("User doesn't have this item")

    async def set_xp(self, user_id: typing.Union[str, int], value: str, amount: int) -> None:
        """
        Sets user money to certain amount

        **Params**:
        \n
        user_id - user id to set money

        value - in what place money should be set, for example 'level' or 'xp'

        amount - to what amount money should be set

        **Returns**:
        \n
        None
        """

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        await c.execute(f"UPDATE level SET {value} = ? WHERE id = ?", (amount, user_id,))

        await con.commit()
        await con.close()

    async def add_xp(self, user_id: typing.Union[str, int], value: str, amount: int) -> None:
       

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        user_account = await c.execute(f"SELECT {value} FROM level WHERE id = ?", (user_id,))
        user_account = await user_account.fetchone()
        user_account = user_account[0]

        nxp = user_account + amount

        await c.execute(f"UPDATE level SET {value} = ? WHERE id = ?", (nxp, user_id,))

        await con.commit()
        await con.close()
    
    async def add_level(self, user_id: typing.Union[str, int], value: str, amount: int) -> None:
       

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        user_account = await c.execute(f"SELECT {value} FROM level WHERE id = ?", (user_id,))
        user_account = await user_account.fetchone()
        user_account = user_account[0]

        nlevel = user_account + amount

        await c.execute(f"UPDATE level SET {value} = ? WHERE id = ?", (nlevel, user_id,))

        await con.commit()
        await con.close()

##RPG

    async def is_rpgregistered(self, user_id: typing.Union[str, int]) -> bool:
        """
        **Params**:
        \n
        user_id - user id to check if it is in the database

        **Returns**:
        \n
        bool
        """

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        query = await c.execute("SELECT * FROM rpg WHERE id = ?", (user_id,))
        query = await query.fetchone()
       

        if not query:
            await c.execute(f"INSERT INTO rpg VALUES(?, 0, 0, 0, 0, 0, 0, 0, 0, 0, ?, 0, 0, ?, ?, ?, ?, ?, ?, 0, 0)",(user_id, "","","","","","",""))
        
        await con.commit()
        
        await con.close()

        return True

    async def get_user_rpg(self, user_id: typing.Union[str, int]) -> UserObject:
        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        r = await c.execute("SELECT * FROM rpg WHERE id = ?", (user_id,))
        r = await r.fetchone()

        await con.close()

        
        job = r[1]
        level = r[2]
        xp = r[3]
        str = r[4]
        dex = r[5]
        cons = r[6]
        int = r[7]
        wis = r[8]
        cha = r[9]
        bag = r[10].split(" | ")
        bank = r[11]
        pouch = r[12]
        head = r[13].split(" | ")
        chest = r[14].split(" | ")
        legs = r[15].split(" | ")
        foot = r[16].split(" | ")
        weapon = r[17].split(" | ")
        belt = r[18].split(" | ")
        mana = r[19]
        points = r[20]

        if bag[0] == "" :
            bag.pop(0)

        if head[0] == "":
            head.pop(0)

        if chest[0] == "":
            chest.pop(0)

        if legs[0] == "":
            legs.pop(0)

        if foot[0] == "":
            foot.pop(0)

        if weapon[0] == "":
            weapon.pop(0)

        if belt[0] == "":
            belt.pop(0)    
        
        return UserObjectRPG(job, level, xp , str, dex, cons, int, wis, cha, bag, bank, pouch, head, chest, legs, foot, weapon, belt, mana, points)    
   

    async def add_rpg_item(self, user_id: typing.Union[str, int], value: str, item: str,) -> None:    
        """
        Adds rpg item to user account. Value is where item will be added.

        **Code Example**:
        \n
        ```python
        import DiscordEconomy
        import asyncio

        economy = DiscordEconomy.Economy()


        async def main() -> None:
            await economy.is_registered(12345)
            await economy.add_item(12345, "sword")

        asyncio.get_event_loop().run_until_complete(main())
        ```

        **Params**:
        \n
        user_id - user id where the item should be added

        item - which item should be added to user

        **Returns**:
        \n
        None | if user already have this item raises ItemAlreadyExists
        """

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        query = await c.execute(f"SELECT {value} FROM rpg WHERE id = ?", (user_id,))
        query = await query.fetchone()

        _user_items = query[0].split(" | ")


        #if item in _user_items:
         #   raise ItemAlreadyExists("User already have this item")

        _user_items.append(item)
        
        
        await c.execute(f"UPDATE rpg SET {value} = ? WHERE id = ?", (" | ".join(_user_items), user_id))
    
        await con.commit()
        await con.close()


    async def remove_rpg_item(self, user_id: typing.Union[str, int], value:str, item: str) -> None:
        """
        Removes item from selected value stash.

        **Params**:
        \n
        user_id - user id where the item should be removed

        item - which item should be removed from user

        **Returns**:
        \n
        None
        """

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        query = await c.execute(f"SELECT {value} FROM rpg WHERE id = ?", (user_id,))
        query = await query.fetchone()

        _user_items = query[0].split(" | ")

        if item in _user_items:
            _user_items.pop(_user_items.index(item))

            await c.execute("UPDATE economy SET items = ? WHERE id = ?", (" | ".join(_user_items), user_id))

            await con.commit()
            await con.close()


        else:
            raise NoItemFound("User doesn't have this item")

    async def add_rpg_stat(self, user_id: typing.Union[str, int], value: str, amount: int) -> None:
        """
        Adds any amount to value where value is integer.

        """
        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        user_account = await c.execute(f"SELECT {value} FROM rpg WHERE id = ?", (user_id,))
        user_account = await user_account.fetchone()
        user_account = user_account[0]

        namount = user_account + amount

        await c.execute(f"UPDATE rpg SET {value} = ? WHERE id = ?", (namount, user_id,))

        await con.commit()
        await con.close()
    
    async def set_rpg_stat(self, user_id: typing.Union[str, int], value: str, amount: int) -> None:
        """
        Sets users stuff to amount, where value is whatever.

        **Params**:
        \n
        user_id - user id to set money

        value - in what place money should be set, for example 'level' or 'xp'

        amount - to what amount money should be set

        **Returns**:
        \n
        None
        """

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        await c.execute(f"UPDATE rpg SET {value} = ? WHERE id = ?", (amount, user_id,))

        await con.commit()
        await con.close()

    ##CRIME
    
    async def is_cregistered(self, user_id: typing.Union[str, int]) -> bool:
        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        query = await c.execute("SELECT * FROM crime WHERE id = ?", (user_id,))
        query = await query.fetchone()
       

        if not query:
            await c.execute(f"INSERT INTO crime VALUES(?, 0, 0, 0, 0, 0, 0, ?, 0, 0, 0 ,0 ,0 ,0 ,0 ,0, ?)",(user_id, "",""))
        
        await con.commit()
        
        await con.close()

        return True

    async def get_c_user(self, user_id: typing.Union[str, int]) -> UserObject:
        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        r = await c.execute("SELECT * FROM crime WHERE id = ?", (user_id,))
        r = await r.fetchone()

        await con.close()

        plant = r[1]
        metal = r[2]
        wood= r[3]
        stone = r[4]
        water = r[5]
        electric = r[6]
        item = r[7].split(" | ")
        rob = r[8]
        steal = r[9]
        arson = r[10]
        deal = r[11]
        worker = r[12]
        gatherer = r[13]
        thug = r[14]
        agent = r[15]
        control = r[16].split(" | ")

        if item[0] == "" :
            item.pop(0)

        if control[0] == "":
            control.pop(0)

        return UserObjectCrime(plant, metal, wood, stone, water, electric, item, rob , steal , arson , deal , worker, gatherer, thug, agent, control)

    
    async def add_crime_stat(self, user_id: typing.Union[str, int], value: str, amount: int) -> None:
        """
        Adds any amount to value where value is integer. Previous +1
        value - set for plant, wood, stone , workers, deal, rob... etc.

        """
        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        user_account = await c.execute(f"SELECT {value} FROM crime WHERE id = ?", (user_id,))
        user_account = await user_account.fetchone()
        user_account = user_account[0]

        namount = user_account + amount

        await c.execute(f"UPDATE crime SET {value} = ? WHERE id = ?", (namount, user_id,))

        await con.commit()
        await con.close()
    
    async def remove_crime_stat(self, user_id: typing.Union[str, int], value: str, amount: int) -> None:
        """
        Adds any amount to value where value is integer. Previous +1
        value - set for plant, wood, stone , workers, deal, rob... etc.

        """
        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        user_account = await c.execute(f"SELECT {value} FROM crime WHERE id = ?", (user_id,))
        user_account = await user_account.fetchone()
        user_account = user_account[0]

        namount = user_account - amount

        await c.execute(f"UPDATE crime SET {value} = ? WHERE id = ?", (namount, user_id,))

        await con.commit()
        await con.close()
    
    async def set_crime_stat(self, user_id: typing.Union[str, int], value: str, amount: int) -> None:
        """
        Sets users stuff to amount, where value is whatever.

        **Params**:
        \n
        user_id - user id to set money

        value - set for plant, wood, stone , workers, deal, rob... etc.

        amount - to what amount money should be set

        **Returns**:
        \n
        None
        """

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        await c.execute(f"UPDATE crime SET {value} = ? WHERE id = ?", (amount, user_id,))

        await con.commit()
        await con.close()

    async def add_crime_item(self, user_id: typing.Union[str, int],item: str,) -> None:    
        """
        Adds rpg item to user account. Value is where item will be added.

        **Code Example**:
        \n
        ```python
        import DiscordEconomy
        import asyncio

        economy = DiscordEconomy.Economy()


        async def main() -> None:
            await economy.is_registered(12345)
            await economy.add_item(12345, "sword")

        asyncio.get_event_loop().run_until_complete(main())
        ```

        **Params**:
        \n
        user_id - user id where the item should be added

        item - which item should be added to user

        **Returns**:
        \n
        None | if user already have this item raises ItemAlreadyExists
        """
        value = "items"
        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        query = await c.execute(f"SELECT {value} FROM crime WHERE id = ?", (user_id,))
        query = await query.fetchone()

        _user_items = query[0].split(" | ")


        #if item in _user_items:
         #   raise ItemAlreadyExists("User already have this item")

        _user_items.append(item)
        
        
        await c.execute(f"UPDATE crime SET {value} = ? WHERE id = ?", (" | ".join(_user_items), user_id))
    
        await con.commit()
        await con.close()


    async def remove_crime_item(self, user_id: typing.Union[str, int], item: str) -> None:
        """
        Removes item from selected value stash.

        **Params**:
        \n
        user_id - user id where the item should be removed

        item - which item should be removed from user

        **Returns**:
        \n
        None
        """
        value = "items"
        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        query = await c.execute(f"SELECT {value} FROM crime WHERE id = ?", (user_id,))
        query = await query.fetchone()

        _user_items = query[0].split(" | ")

        if item in _user_items:
            _user_items.pop(_user_items.index(item))

            await c.execute("UPDATE crime SET items = ? WHERE id = ?", (" | ".join(_user_items), user_id))

            await con.commit()
            await con.close()


        else:
            raise NoItemFound("User doesn't have this item")

    ##TURF
    async def is_tregistered(self, user_id: typing.Union[str, int]) -> bool:
    

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        query = await c.execute("SELECT * FROM turf WHERE id = ?", (user_id,))
        query = await query.fetchone()
        

        if not query:
            await c.execute(f"INSERT INTO turf VALUES(?, 0, 0, 0, 0, 0, 0, 0, 0, ?)", (user_id, ""))
        
        await con.commit()
        
        await con.close()

        return True


    async def get_t_user(self, user_id: typing.Union[str, int]) -> UserObject:
        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        r = await c.execute("SELECT * FROM turf WHERE id = ?", (user_id,))
        r = await r.fetchone()

        await con.close()

        faction = r[1]
        region = r[2]
        esp = r[3]
        cesp = r[4]
        prot = r[5]
        att = r[6]
        work = r[7]
        total = r[8]
        control = r[9].split(" | ")

        if control[0] == "":
            control.pop(0)

            
    
        return UserObjectTurf(faction,region, esp, cesp, prot, att, work, total ,control)

    async def add_turf_stat(self, user_id: typing.Union[str, int], value: str, amount: int) -> None:
        """
        

        """
        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        user_account = await c.execute(f"SELECT {value} FROM turf WHERE id = ?", (user_id,))
        user_account = await user_account.fetchone()
        user_account = user_account[0]

        namount = user_account + amount

        await c.execute(f"UPDATE turf SET {value} = ? WHERE id = ?", (namount, user_id,))

        await con.commit()
        await con.close()
    
    async def remove_turf_stat(self, user_id: typing.Union[str, int], value: str, amount: int) -> None:
        """
       

        """
        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        user_account = await c.execute(f"SELECT {value} FROM turf WHERE id = ?", (user_id,))
        user_account = await user_account.fetchone()
        user_account = user_account[0]

        namount = user_account - amount

        await c.execute(f"UPDATE turf SET {value} = ? WHERE id = ?", (namount, user_id,))

        await con.commit()
        await con.close()
    
    async def set_turf_stat(self, user_id: typing.Union[str, int], value: str, amount: int) -> None:
        """
        Sets users stuff to amount, where value is whatever.

        **Params**:
        \n
        user_id - user id to set money

        value - 

        amount - to what amount money should be set

        **Returns**:
        \n
        None
        """

        con = await aiosqlite.connect(self.__database_name)
        c = await con.cursor()

        await c.execute(f"UPDATE turf SET {value} = ? WHERE id = ?", (amount, user_id,))

        await con.commit()
        await con.close()