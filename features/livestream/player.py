import asyncio
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import (
    InputAudioStream,
    InputVideoStream,
)
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
)
from pytgcalls.types.stream import StreamAudioEnded

from core.session_reuse import get_active_client
from .state import next_item, set_playing, clear

_CALLS = {}  # user_id: PyTgCalls


async def _get_player(user_id: int) -> PyTgCalls:
    if user_id in _CALLS:
        return _CALLS[user_id]

    client = await get_active_client(user_id)
    player = PyTgCalls(client)
    await player.start()
    _CALLS[user_id] = player

    @player.on_stream_end()
    async def on_end(_, chat_id):
        item = next_item(chat_id)
        if not item:
            await player.leave_group_call(chat_id)
            clear(chat_id)
            return
        await _play(player, chat_id, item)

    return player


async def _play(player, chat_id: int, item: dict):
    if item["type"] == "audio":
        stream = InputAudioStream(
            item["source"],
            HighQualityAudio(),
        )
    else:
        stream = InputVideoStream(
            item["source"],
            HighQualityVideo(),
        )

    await player.join_group_call(chat_id, stream)
    set_playing(chat_id, True)


async def play_item(user_id: int, chat_id: int, item: dict):
    player = await _get_player(user_id)
    await _play(player, chat_id, item)


async def pause(user_id: int, chat_id: int):
    player = await _get_player(user_id)
    await player.pause_stream(chat_id)


async def resume(user_id: int, chat_id: int):
    player = await _get_player(user_id)
    await player.resume_stream(chat_id)


async def stop(user_id: int, chat_id: int):
    player = await _get_player(user_id)
    await player.leave_group_call(chat_id)
    clear(chat_id)