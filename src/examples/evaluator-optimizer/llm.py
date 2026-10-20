import os
from dataclasses import dataclass
from enum import StrEnum

from anthropic import AsyncAnthropic
from pydantic import BaseModel


class Model(StrEnum):
    OPUS = "claude-opus-5-5"
    SONNET = "claude-sonnet-5-5"
    HAIKU = "claude-haiku-5-5"


class Effort(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    XHIGH = "xhigh"
    MAX = "max"


@dataclass(frozen=True)
class AgentConfig:
    model: Model
    effort: Effort
    system: str
    output: type[BaseModel]


client = AsyncAnthropic(auth_token=os.environ["ANTHROPIC_AUTH_TOKEN"], max_retries=5)


async def call(agent: AgentConfig, message: str) -> BaseModel:
    response = await client.messages.parse(
        model=agent.model,
        max_tokens=8192,
        system=agent.system,
        thinking={"type": "adaptive"},
        output_config={"effort": agent.effort},
        output_format=agent.output,
        messages=[{"role": "user", "content": message}],
    )
    return response.parsed_output
