from aiohttp import web
from models import Base, engine, Session, User, Ad
import json
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.exc import IntegrityError

app = web.Application()


def hash_password(password: str):
    password = password.encode()
    password = hashpw(password, gensalt())
    password = password.decode()
    return password


def check_password(password: str, db_password_hash: str):
    password = password.encode()
    db_password_hash = db_password_hash.encode()
    return checkpw(password, db_password_hash)


@web.middleware
async def session_midleware(request: web.Request, handler):
    async with Session() as session:
        request["session"] = session
        response = await handler(request)
        return response


async def get_user(user_id: int, session: Session):
    user = await session.get(User, user_id)
    if user is None:
        raise web.HTTPNotFound(
            text=json.dumps({"error": "user not found"}),
            content_type="application/json",
        )
    return user


async def get_ad(ad_id: int, session: Session):
    ad = await session.get(Ad, ad_id)
    if ad is None:
        raise web.HTTPNotFound(
            text=json.dumps({"error": "ad not found"}),
            content_type="application/json",
        )
    return ad


class UserView(web.View):
    @property
    def session(self):
        return self.request["session"]

    @property
    def user_id(self):
        return int(self.request.match_info["user_id"])

    async def get(self):
        user = await get_user(self.user_id, self.session)

        return web.json_response(
            {
                "id": user.id,
                "name": user.name,
                "creation_time": int(user.creation_time.timestamp()),
            }
        )

    async def post(self):
        json_data = await self.request.json()
        json_data["password"] = hash_password(json_data["password"])
        user = User(**json_data)
        try:
            self.session.add(user)
            await self.session.commit()
        except IntegrityError as er:
            raise web.HTTPConflict(
                text=json.dumps({"error": "user already exists"}),
                content_type="application/json",
            )
        return web.json_response({"id": user.id})

    async def patch(self):
        json_data = await self.request.json()
        if "password" in json_data:
            json_data["password"] = hash_password(json_data["password"])
        user = await get_user(self.user_id, self.session)
        for field, value in json_data.items():
            setattr(user, field, value)
        try:
            self.session.add(user)
            await self.session.commit()
        except IntegrityError as er:
            raise web.HTTPConflict(
                text=json.dumps({"error": "user already exists"}),
                content_type="application/json",
            )
        return web.json_response({"id": user.id})

    async def delete(self):
        user = await get_user(self.user_id, self.session)
        await self.session.delete(user)
        await self.session.commit()
        return web.json_response({"id": user.id})


class AdView(web.View):
    @property
    def session(self):
        return self.request["session"]

    @property
    def ad_id(self):
        return int(self.request.match_info["ad_id"])

    async def get(self):
        ad = await get_ad(self.ad_id, self.session)

        return web.json_response(
            {
                "title": ad.title,
                "description": ad.description,
                "creation_time": int(ad.creation_time.timestamp()),
                "user_id": ad.user_id,
            }
        )

    async def post(self):
        json_data = await self.request.json()
        ad = Ad(**json_data)
        try:
            self.session.add(ad)
            await self.session.commit()
        except IntegrityError as er:
            raise web.HTTPConflict(
                text=json.dumps({"error": "ad already exists"}),
                content_type="application/json",
            )
        return web.json_response({"ad": ad.id})

    async def patch(self):
        json_data = await self.request.json()
        ad = await get_ad(self.ad_id, self.session)
        for field, value in json_data.items():
            setattr(ad, field, value)
        try:
            self.session.add(ad)
            await self.session.commit()
        except IntegrityError as er:
            raise web.HTTPConflict(
                text=json.dumps({"error": "ad already exists"}),
                content_type="application/json",
            )
        return web.json_response({"id": ad.id})

    async def delete(self):
        ad = await get_ad(self.ad_id, self.session)
        await self.session.delete(ad)
        await self.session.commit()
        return web.json_response({"id": ad.id})


async def orm_context(app: web.Application):
    print("Start")
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)
    yield
    print("Shut down")
    await engine.dispose()


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_midleware)
app.add_routes(
    [
        web.post("/users/", UserView),
        web.get("/users/{user_id:\d+}", UserView),
        web.patch("/users/{user_id:\d+}", UserView),
        web.delete("/users/{user_id:\d+}", UserView),
        web.post("/ads/", AdView),
        web.get("/ads/{ad_id:\d+}", AdView),
        web.patch("/ads/{ad_id:\d+}", AdView),
        web.delete("/ads/{ad_id:\d+}", AdView),
    ]
)

if __name__ == "__main__":
    web.run_app(app)
