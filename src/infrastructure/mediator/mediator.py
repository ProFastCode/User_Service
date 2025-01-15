from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field

from src.application.common.command import CR, CT, Command, CommandHandler
from src.application.common.event import ER, ET, Event, EventHandler
from src.application.common.query import QR, QT, Query, QueryHandler


@dataclass(eq=False)
class Mediator:
    events_map: dict[type[Event], list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    commands_map: dict[type[Command], CommandHandler] = field(
        default_factory=dict,
        kw_only=True,
    )
    queries_map: dict[type[Query], QueryHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    def register_event_handler(
        self, event: type[Event], event_handlers: Iterable[EventHandler[ET, ER]]
    ):
        self.events_map[event].extend(event_handlers)

    def register_command_handler(
        self, command: type[Command], command_handler: CommandHandler[CT, CR]
    ):
        self.commands_map[command] = command_handler

    def register_query_handler(
        self, query: type[Query], query_handler: QueryHandler[QT, QR]
    ):
        self.queries_map[query] = query_handler

    async def publish(self, events: Iterable[Event]) -> None:
        for event in events:
            for handler in self.events_map.get(event.__class__, []):
                await handler(event)

    async def send(self, command: Command[CR]) -> CR:
        handler = self.commands_map.get(command.__class__, None)
        if not handler:
            raise ValueError  # TODO: Exc
        return await handler(command)

    async def query(self, query: Query[QR]) -> QR:
        handler = self.queries_map.get(query.__class__, None)
        if not handler:
            raise ValueError  # TODO: Exc
        return await handler(query=query)
