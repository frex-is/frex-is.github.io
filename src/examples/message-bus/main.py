import asyncio
import time

from bus import Bus, Message, listen
from llm import AgentConfig, Effort, Model, call
from prompts import DIAGNOSTIC_ADVISOR_PROMPT, INCIDENT_DETECTOR_PROMPT, PUBLIC_COMMUNICATOR_PROMPT
from schemas import (
    AgentName,
    AlertFired,
    Correlation,
    Incident,
    IncidentOpened,
    Runbook,
    RunbookSuggested,
    Severity,
    StatusMessage,
    StatusPublished,
    Topic,
)

ALERT_INTERVAL = 0.5

AGENTS = {
    AgentName.DIAGNOSTIC_ADVISOR: AgentConfig(Model.HAIKU, Effort.LOW, DIAGNOSTIC_ADVISOR_PROMPT, Runbook),
    AgentName.INCIDENT_DETECTOR: AgentConfig(Model.SONNET, Effort.MEDIUM, INCIDENT_DETECTOR_PROMPT, Correlation),
    AgentName.PUBLIC_COMMUNICATOR: AgentConfig(Model.HAIKU, Effort.LOW, PUBLIC_COMMUNICATOR_PROMPT, StatusMessage),
}

ALERTS = [
    AlertFired(alert_identifier=1, source="api", severity=Severity.WARNING, message="Latence p95 de POST /payments/webhook à 2,4 s (seuil : 800 ms)"),
    AlertFired(alert_identifier=2, source="api", severity=Severity.CRITICAL, message="12 % d'erreurs 5xx sur POST /payments/webhook depuis 5 minutes"),
    AlertFired(alert_identifier=3, source="batch-03", severity=Severity.WARNING, message="Disque rempli à 85 %"),
    AlertFired(alert_identifier=4, source="payment-worker", severity=Severity.CRITICAL, message="3 400 messages en attente dans la file des webhooks Stripe"),
]

STARTED_AT = time.monotonic()


def elapsed() -> float:
    return time.monotonic() - STARTED_AT


def format_alerts_for_detection(seen: list[AlertFired]) -> str:
    alerts = "\n".join(alert.model_dump_json() for alert in seen)
    return f"Alertes reçues :\n{alerts}"


async def detect_incident(seen: list[AlertFired]) -> Incident | None:
    correlation = await call(AGENTS[AgentName.INCIDENT_DETECTOR], format_alerts_for_detection(seen))
    return correlation.incident


async def monitoring(bus: Bus) -> None:
    for alert in ALERTS:
        bus.publish(Topic.ALERT_FIRED, alert)
        await asyncio.sleep(ALERT_INTERVAL)


async def diagnostic_advisor(bus: Bus, queue: asyncio.Queue[Message]) -> None:
    async for message in listen(queue):
        alert = message.event
        suggestion = await call(AGENTS[AgentName.DIAGNOSTIC_ADVISOR], alert.model_dump_json())
        bus.publish(Topic.RUNBOOK_SUGGESTED, RunbookSuggested(alert_identifier=alert.alert_identifier, check=suggestion.check))


async def incident_detector(bus: Bus, queue: asyncio.Queue[Message]) -> None:
    seen: list[AlertFired] = []
    is_incident_opened = False

    async for message in listen(queue):
        seen.append(message.event)

        if is_incident_opened:
            continue

        incident = await detect_incident(seen)

        if incident is None:
            continue

        bus.publish(Topic.INCIDENT_OPENED, IncidentOpened(**incident.model_dump()))
        is_incident_opened = True


async def public_communicator(bus: Bus, queue: asyncio.Queue[Message]) -> None:
    async for message in listen(queue):
        incident = message.event
        status_message = await call(AGENTS[AgentName.PUBLIC_COMMUNICATOR], incident.model_dump_json())
        bus.publish(Topic.STATUS_PUBLISHED, StatusPublished(message=status_message.message))


async def event_logger(queue: asyncio.Queue[Message]) -> None:
    async for message in listen(queue):
        print(f"{elapsed():4.1f}s  #{message.message_identifier} [{message.topic}] {message.event.model_dump_json()}\n")


async def main() -> None:
    bus = Bus()
    subscribers = [
        asyncio.create_task(event_logger(bus.subscribe(*Topic))),
        asyncio.create_task(diagnostic_advisor(bus, bus.subscribe(Topic.ALERT_FIRED))),
        asyncio.create_task(incident_detector(bus, bus.subscribe(Topic.ALERT_FIRED))),
        asyncio.create_task(public_communicator(bus, bus.subscribe(Topic.INCIDENT_OPENED))),
    ]

    await monitoring(bus)
    await bus.drain()

    for subscriber in subscribers:
        subscriber.cancel()

    print(f"Flux traité : {bus.published} événements publiés")


if __name__ == "__main__":
    asyncio.run(main())
