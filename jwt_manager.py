# -*- coding: utf-8 -*-
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

from jwt import encode, decode
from dotenv import load_dotenv
import os

load_dotenv()


def create_token(data: dict) -> str:
    token: str = encode(payload=data,
                        key=os.getenv('SECRET_KEY'),
                        algorithm="HS256"
                        )
    return token

def validate_token(token: str) -> dict:
    data: dict = decode(
        token,
        key=os.getenv('SECRET_KEY'),
        algorithms=["HS256"]
    )
    return data
