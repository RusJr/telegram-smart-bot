import logging

from p_bot.bot import PBot


class PBotManager:

    bots = {}  # telegram user_id -> PBot object
    logger = logging.getLogger('PBotManager')

    @classmethod
    def get_or_create(cls, user_id: str, user_name=None) -> PBot:
        if user_id in cls.bots:
            return cls.bots[user_id]
        else:
            new_p_bot = PBot(user_name or 'Низнакомиц))0')
            cls.bots[user_id] = new_p_bot
            cls.logger.info('Created new PBot for user_id: %s', user_id)
            return new_p_bot


if __name__ == '__main__':
    p_bot = PBotManager.get_or_create('007', 'Vovchik228')
    p_bot = PBotManager.get_or_create('007', 'Vovchik228')
    p_bot = PBotManager.get_or_create('007', 'Vovchik228')
    p_bot = PBotManager.get_or_create('008', 'Vovchik228')
    p_bot = PBotManager.get_or_create('009', 'Vovchik228')
    p_bot = PBotManager.get_or_create('007', 'Vovchik228')
    p_bot = PBotManager.get_or_create('007', 'Vovchik228')
    print(p_bot.get_answer('Знаешь как меня зовут?'))
