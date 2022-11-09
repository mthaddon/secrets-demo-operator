#!/usr/bin/env python3
# Copyright 2022 Tom Haddon
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

import logging
import random
import string

from ops.charm import CharmBase
from ops.main import main


class SecretsCharmCharm(CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.leader_elected, self._on_leader_elected)
        self.framework.observe(self.on.config_changed, self._on_config_changed)

    def _on_config_changed(self, _) -> None:
        peer_relation = self.model.get_relation("secrets-charm-peers")
        secret_id = peer_relation.data[self.app]["secret-id"]
        if secret_id:
            secret = self.model.get_secret(id=secret_id)
            secret_key = secret.get("secret-key")
            logging.warning("secret-key set to %s", secret_key)
        else:
            logging.error("Unable to get secret-key")

    def _on_leader_elected(self, _) -> None:
        peer_relation = self.model.get_relation("secrets-charm-peers")
        if not peer_relation.data[self.app].get("secret-id"):
            secret_value = "".join(
                random.choice(string.ascii_letters + string.digits) for _ in range(32)
            )
            logging.warning("Secret value %s", secret_value)
            secret = self.app.add_secret({"secret-key": secret_value})
            peer_relation.data[self.app]["secret-id"] = secret.id


if __name__ == "__main__":  # pragma: nocover
    main(SecretsCharmCharm)
