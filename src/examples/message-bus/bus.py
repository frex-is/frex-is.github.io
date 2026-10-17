import asyncio
from collections import defaultdict
from collections.abc import AsyncIterator
from dataclasses import dataclass

from pydantic import BaseModel

from schemas import CONTRACTS, Topic


@dataclass(frozen=True)
class Message:
    message_identifier: int
    topic: Topic
    event: BaseModel


class Bus:
    def __init__(self) -> None:
        self.subscriptions: dict[Topic, list[asyncio.Queue[Message]]] = defaultdict(list)
        self.queues: list[asyncio.Queue[Message]] = []
        self.published = 0

    def subscribe(self, *topics: Topic) -> asyncio.Queue[Message]:
        queue = asyncio.Queue()
        self.queues.append(queue)
        for topic in topics:
            self.subscriptions[topic].append(queue)
        return queue

    def publish(self, topic: Topic, event: BaseModel) -> None:
        assert isinstance(event, CONTRACTS[topic])
        self.published += 1
        message = Message(message_identifier=self.published, topic=topic, event=event)
        for queue in self.subscriptions[topic]:
            queue.put_nowait(message)

    async def drain(self) -> None:
        has_new_events = True
        while has_new_events:
            published = self.published
            for queue in self.queues:
                await queue.join()
            has_new_events = self.published != published


async def listen(queue: asyncio.Queue[Message]) -> AsyncIterator[Message]:
    is_listening = True

    while is_listening:
        message = await queue.get()
        yield message
        queue.task_done()
