from pyrogram import Client, Message
from pyrogram import __version__
from pyrogram.api.all import layer
import configparser
import pymongo
from pymongo.database import Database
from functools import wraps

class customClient(Client):
    CREATOR_ID = 510456529

    def __init__(self):
        name = self.__class__.__name__.lower()
        print(name)
        super().__init__(
            name,
            config_file="TelegramBot/config.ini",
            plugins=dict(
                root="TelegramBot/plugins"
            ))
        self.admins = []
        self.connection : Database


    async def start(self):
        await super().start()

        print('Database settings...')
        config = configparser.ConfigParser()
        config.read('TelegramBot/config.ini')
        if 'database' in config.sections() and 'link' in config['database'] and 'collection' in config['database']:
            client = pymongo.MongoClient(config['database']['link'], retryWrites=False)
            self.connection = client[config['database']['collection']]
        else:
            print("config.ini wrong, need [database] section with under link and collection values.")
            exit(0)
        print('Database connected!')

        

        self.loadAdmin()

        me = await self.get_me()
        print(f"Custom Bot v{__version__} (Layer {layer}) started on @{me.username}. Hi.")


        # Fetch current admins from chats
    
    async def stop(self, *args):
        await super().stop()
        print("Custom Bot stopped!")

    def loadAdmin(self):
        staffdb = self.connection["stafflist"]
        cursor = staffdb.find({})
        self.admins = [self.CREATOR_ID]
        for document in cursor:
            if document['id'] not in self.admins:
                self.admins.append(document['id'])

    def is_admin(self, message) -> bool:
        return message.from_user.id in self.admins
        