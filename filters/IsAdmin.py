from aiogram import types
from aiogram.filters import BaseFilter

from loader import database


class IsAdmin(BaseFilter):
    async def __call__(self, message: types.Message):
        admins_ids = database.fetchall(
            """
            SELECT user_id FROM admins;
            """
        )
        if len(admins_ids) != 0:
            self.admins_ids = [admin_id[0] for admin_id in admins_ids]

        return message.from_user.id in self.admins_ids
