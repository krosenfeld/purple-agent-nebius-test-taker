from a2a.server.tasks import TaskUpdater
from a2a.types import Message, TaskState, Part, TextPart
from a2a.utils import get_message_text, new_agent_text_message

from messenger import Messenger

import nebius

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test_taker")

class Agent:
    def __init__(self):
        logger.info("Test Taker initializing")

        self.messenger = Messenger()
        self.client = nebius.NeBiusClient(model="nemotron-3-nano-30b-a3b")

    async def run(self, message: Message, updater: TaskUpdater) -> None:
        """Implement your agent logic here.

        Args:
            message: The incoming message
            updater: Report progress (update_status) and results (add_artifact)

        Use self.messenger.talk_to_agent(message, url) to call other agents.
        """

        prompt = get_message_text(message)

        await updater.update_status(
            TaskState.working, new_agent_text_message("Thinking...")
        )

        response = self.client.generate_response(prompt)
        text = response or ""

        await updater.add_artifact(
            parts=[Part(root=TextPart(text=text))],
            name="Response",
        )
