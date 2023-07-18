import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        print("create")
        response = await session.post(
            "http://127.0.0.1:8080/users/", json={"name": "user_1", "password": "1234"}
        )
        print(response.status)
        json_data = await response.json()
        print(json_data)

        print("get")
        response = await session.get(
            "http://127.0.0.1:8080/users/1",
        )
        print(response.status)
        json_data = await response.json()
        print(json_data)

        print("patch")
        response = await session.patch(
            "http://127.0.0.1:8080/users/1", json={"name": "user_2"}
        )
        print(response.status)
        json_data = await response.json()
        print(json_data)

        print("get")
        response = await session.get(
            "http://127.0.0.1:8080/users/1",
        )
        print(response.status)
        json_data = await response.json()
        print(json_data)

        print("delete")
        response = await session.delete(
            "http://127.0.0.1:8080/users/1",
        )
        print(response.status)
        json_data = await response.json()
        print(json_data)

        print("get")
        response = await session.get(
            "http://127.0.0.1:8080/users/1",
        )
        print(response.status)
        json_data = await response.json()
        print(json_data)

        print("create")
        response = await session.post(
            "http://127.0.0.1:8080/ads/",
            json={"title": "ad_1", "description": "something else", "user_id": 1},
        )
        print(response.status)
        json_data = await response.json()
        print(json_data)

        print("get")
        response = await session.get(
            "http://127.0.0.1:8080/ads/1",
        )
        print(response.status)
        json_data = await response.json()
        print(json_data)

        print("patch")
        response = await session.patch(
            "http://127.0.0.1:8080/ads/1", json={"title": "ad_2"}
        )
        print(response.status)
        json_data = await response.json()
        print(json_data)

        print("get")
        response = await session.get(
            "http://127.0.0.1:8080/ads/1",
        )
        print(response.status)
        json_data = await response.json()
        print(json_data)

        print("delete")
        response = await session.delete(
            "http://127.0.0.1:8080/ads/1",
        )
        print(response.status)
        json_data = await response.json()
        print(json_data)

        print("get")
        response = await session.get(
            "http://127.0.0.1:8080/ads/1",
        )
        print(response.status)
        json_data = await response.json()
        print(json_data)


asyncio.run(main())
