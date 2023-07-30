from typing import Optional, Union

import aiohttp
from pydantic import BaseModel

from exapy import models

BASE_URL = "https://api.exaroton.com/v1/"


class Response(BaseModel):
    success: bool
    error: Optional[str]
    data: Optional[Union[dict, list, str, None]]


class ExaError(Exception):
    pass


# TODO: create Server object i.e. server.files()


class Client:
    def __init__(self, token: str) -> None:
        self._token = token

    async def _get_data(self, route: str) -> dict | list | str | None:
        headers = {"Authorization": f"Bearer {self._token}"}

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(BASE_URL + route) as response:
                response.raise_for_status()

                raw_response_data = await response.json()
                response_data = Response(**raw_response_data)

                if response_data.success:
                    return response_data.data
                else:
                    raise ExaError(response_data.error)

    async def _post_object(self, route: str, object: dict) -> dict | list | str | None:
        headers = {"Authorization": f"Bearer {self._token}"}

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(BASE_URL + route, json=object) as response:
                response.raise_for_status()

                raw_response_data = await response.json()
                response_data = Response(**raw_response_data)

                if response_data.success:
                    assert response_data.data is not None
                    return response_data.data
                else:
                    raise ExaError(response_data.error)

    async def _put_object(self, route: str, object: dict) -> dict | list | str | None:
        headers = {"Authorization": f"Bearer {self._token}"}

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.put(BASE_URL + route, json=object) as response:
                response.raise_for_status()

                raw_response_data = await response.json()
                response_data = Response(**raw_response_data)

                if response_data.success:
                    assert response_data.data is not None
                    return response_data.data
                else:
                    raise ExaError(response_data.error)

    async def _delete_object(
        self, route: str, object: dict
    ) -> dict | list | str | None:
        headers = {"Authorization": f"Bearer {self._token}"}

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.delete(BASE_URL + route, json=object) as response:
                response.raise_for_status()

                raw_response_data = await response.json()
                response_data = Response(**raw_response_data)

                if response_data.success:
                    assert response_data.data is not None
                    return response_data.data
                else:
                    raise ExaError(response_data.error)

    async def account(self) -> models.Account:
        """Get information about the connected account

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            models.Account: The account information
        """
        data = await self._get_data("account")
        assert isinstance(data, dict)
        return models.Account(**data)

    async def servers(self) -> list[models.Server]:
        """Get a list of connected servers

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            list[models.Server]: list of connected server's information
        """
        data = await self._get_data("servers")
        assert isinstance(data, list)
        servers: list[models.Server] = []

        for server in data:
            servers.append(models.Server(**server))

        return servers

    async def server(self, server_id: str) -> models.Server:
        """Get information about a particular server

        Args:
            server_id (str): The server's .id

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            models.Server: The server information
        """
        data = await self._get_data(f"servers/{server_id}")
        assert isinstance(data, dict)
        return models.Server(**data)

    async def log(self, server_id: str) -> str | None:
        """Get a server's log

        Args:
            server_id (str): The server's .id

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            str | None: The server's log
        """
        data = await self._get_data(f"servers/{server_id}/logs")
        assert isinstance(data, dict)
        return data["content"]

    async def share_log(self, server_id: str) -> models.LogUpload:
        """Upload a server's log to mclo.gs

        Args:
            server_id (str): The server's .id

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            models.LogUpload: Information about the uploaded log
        """
        data = await self._get_data(f"servers/{server_id}/logs/share")
        assert isinstance(data, dict)
        return models.LogUpload(**data)

    async def ram(self, server_id: str) -> int:
        """Get a server's ram amount in GB

        Args:
            server_id (str): The server's .id

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            int: Amount of ram in GB
        """
        data = await self._get_data(f"servers/{server_id}/options/ram")
        assert isinstance(data, dict)
        return data["ram"]

    async def set_ram(self, server_id, ram: int) -> int:
        """Set a server's ram amount in GB

        Args:
            server_id (_type_): The server's .id
            ram (int): The amount of ram in GB

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            int: The new ram amount in GB
        """
        new_ram = {
            "ram": ram,
        }

        data = await self._post_object(f"servers/{server_id}/options/ram", new_ram)
        assert isinstance(data, dict)
        return data["ram"]

    async def motd(self, server_id: str) -> str:
        """Get a server's message of the day

        Args:
            server_id (str): The server's .id

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            str: The server's message of the day
        """
        data = await self._get_data(f"servers/{server_id}/options/motd")
        assert isinstance(data, dict)
        return data["motd"]

    async def set_motd(self, server_id: str, motd: str) -> str:
        """Set a server's message of the day

        Args:
            server_id (str): The server's .id
            motd (str): The new message of the day

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            str: The changed message of the day
        """
        new_motd = {
            "motd": motd,
        }

        data = await self._post_object(f"servers/{server_id}/options/motd", new_motd)
        assert isinstance(data, dict)
        return data["motd"]

    async def start(self, server_id: str, use_own_credits: bool = False) -> str | None:
        """Start a server

        Args:
            server_id (str): The server's .id
            use_own_credits (bool, optional): If shared servers should use your credits. Defaults to False.

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            str | None: Unknown
        """
        if use_own_credits:
            use_credits = {
                "useOwnCredits": True,
            }

            data = await self._post_object(f"servers/{server_id}/start", use_credits)
        else:
            data = await self._get_data(f"servers/{server_id}/start")

        # what is this string?
        assert isinstance(data, str) or data is None
        return data

    async def stop(self, server_id: str) -> str | None:
        """Stop a server

        Args:
            server_id (str): The server's .id

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            str | None: unknown
        """
        data = await self._get_data(f"servers/{server_id}/stop")
        assert isinstance(data, str) or data is None
        return data

    async def restart(self, server_id: str) -> str | None:
        """Restart a server

        Args:
            server_id (str): The server's .id

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            str | None: unknown
        """
        data = await self._get_data(f"servers/{server_id}/restart")
        assert isinstance(data, str) or data is None
        return data

    async def execute_command(self, server_id: str, command: str) -> str | None:
        """Execute a command on a server

        Args:
            server_id (str): The server's .id
            command (str): The command to execute

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            str | None: unknown
        """
        command_object = {
            "command": command,
        }
        data = await self._post_object(f"servers/{server_id}/command", command_object)
        assert isinstance(data, str) or data is None
        return data

    async def enabled_playerlists(self, server_id: str) -> list[str]:
        """Get a server's enabled playerlists; this is usually
        whitelist, ops, banned-players, and banned-ips

        Args:
            server_id (str): The server's .id

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            list[str]: The enabled playerlists
        """
        data = await self._get_data(f"servers/{server_id}/playerlists")
        assert isinstance(data, list)
        return data

    async def playerlist_content(self, server_id: str, list_name: str) -> list[str]:
        """Get the content of a playerlist

        Args:
            server_id (str): The server's .id
            list_name (str): The name of the playerlist to get the content of

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            list[str]: The playerlist's content
        """
        data = await self._get_data(f"servers/{server_id}/playerlists/{list_name}")
        assert isinstance(data, list)
        return data

    async def add_to_playerlist(
        self, server_id: str, list_name: str, content: list[str]
    ) -> list[str]:
        """Add content to a playerlist (player names, uuids, or ips)

        Args:
            server_id (str): The server's .id
            list_name (str): Name of the playerlist to add content to
            content (list[str]): The content to add

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            list[str]: The new playerlist content
        """
        create_object = {
            "entries": content,
        }
        data = await self._put_object(
            f"servers/{server_id}/playerlists/{list_name}", create_object
        )
        assert isinstance(data, list)
        return data

    async def remove_from_playerlist(
        self, server_id: str, list_name: str, content: list[str]
    ) -> list[str]:
        """Remove content from a playerlist (player names, uuids, or ips)

        Args:
            server_id (str): The server's .id
            list_name (str): Name of the playerlist to remove content from
            content (list[str]): The content to remove

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            list[str]: The new playerlist content
        """
        delete_object = {
            "entries": content,
        }
        data = await self._delete_object(
            f"servers/{server_id}/playerlists/{list_name}", delete_object
        )
        assert isinstance(data, list)
        return data

    async def path_info(self, server_id: str, path: str) -> models.PathInfo:
        """Get information about a file or directory

        Args:
            server_id (str): The server's .id
            path (str): The path

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            models.PathInfo: Information about the path
        """
        data = await self._get_data(f"servers/{server_id}/files/info/{path}")
        assert isinstance(data, dict)
        return models.PathInfo(**data)

    async def read_file_data(self, server_id: str, path: str) -> bytes:
        """Get a file's data

        Args:
            server_id (str): The server's .id
            path (str): The file path

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            bytes: The file's data
        """
        headers = {"Authorization": f"Bearer {self._token}"}

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(
                BASE_URL + f"servers/{server_id}/files/data/{path}"
            ) as response:
                response.raise_for_status()
                return await response.read()

    async def write_file_data(
        self, server_id: str, path: str, data: bytes
    ) -> str | None:
        """Write a file's data creating it if it doesn't exist

        Args:
            server_id (str): The server's .id
            path (str): The file path
            data (bytes): The data to write

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            str | None: unknown
        """
        headers = {"Authorization": f"Bearer {self._token}"}

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.put(
                BASE_URL + f"servers/{server_id}/files/data/{path}", data=data
            ) as response:
                response.raise_for_status()

                raw_response_data = await response.json()
                response_data = Response(**raw_response_data)

                if response_data.success:
                    assert (
                        isinstance(response_data.data, str)
                        or response_data.data is None
                    )
                    return response_data.data
                else:
                    raise ExaError(response_data.error)

    async def create_directory(self, server_id: str, path: str) -> str | None:
        """Create a directory

        Args:
            server_id (str): The server's .id
            path (str): Directory path

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            str | None: unknown
        """
        headers = {
            "Authorization": f"Bearer {self._token}",
            "content-type": "inode/directory",
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.put(
                BASE_URL + f"servers/{server_id}/files/data/{path}"
            ) as response:
                response.raise_for_status()

                raw_response_data = await response.json()
                response_data = Response(**raw_response_data)

                if response_data.success:
                    assert (
                        isinstance(response_data.data, str)
                        or response_data.data is None
                    )
                    return response_data.data
                else:
                    raise ExaError(response_data.error)

    async def delete_file_data(
        self,
        server_id: str,
        path: str,
    ) -> str | None:
        """Delete a file or directory

        Args:
            server_id (str): The server's .id
            path (str): The file/directory path

        Raises:
            ExaError: If the request is unsuccessful

        Returns:
            str | None: unknown
        """
        headers = {"Authorization": f"Bearer {self._token}"}

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.delete(
                BASE_URL + f"servers/{server_id}/files/data/{path}"
            ) as response:
                response.raise_for_status()

                raw_response_data = await response.json()
                response_data = Response(**raw_response_data)

                if response_data.success:
                    assert (
                        isinstance(response_data.data, str)
                        or response_data.data is None
                    )
                    return response_data.data
                else:
                    raise ExaError(response_data.error)

    async def get_config_options(
        self, server_id: str, path: str = "server.properties"
    ) -> list[models.ConfigOption]:
        """Get the config options set in a file; most commonly server.properties

        these are files with .is_config_file as True in their file info

        Args:
            server_id (str): The server's .id
            path (str, optional): File path to the config file. Defaults to "server.properties".

        Returns:
            list[models.ConfigOption]: The config options
        """
        data = await self._get_data(f"servers/{server_id}/files/config/{path}")
        assert isinstance(data, list)

        config_options: list[models.ConfigOption] = []

        for config_option in data:
            config_options.append(models.ConfigOption(**config_option))

        return config_options

    async def set_config_options(
        self, server_id: str, options: dict, path: str = "server.properties"
    ) -> list[models.ConfigOption]:
        """Set config options to different values these should be in the form of {key: value}

        Args:
            server_id (str): The server's .id
            options (dict): The config options to set
            path (str, optional): Path to the config file to set options in. Defaults to "server.properties".

        Returns:
            list[models.ConfigOption]: The file's new config options
        """
        data = await self._post_object(
            f"servers/{server_id}/files/config/{path}", options
        )
        assert isinstance(data, list)

        config_options: list[models.ConfigOption] = []

        for config_option in data:
            config_options.append(models.ConfigOption(**config_option))

        return config_options
