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

    def _on_leader_elected(self, _) -> None:
        peer_relation = self.model.get_relation("secrets-charm-peers")
        if not peer_relation.data[self.app].get("secret-id"):
            secret_value = "".join(
                random.choice(string.ascii_letters + string.digits) for _ in range(32)
            )
            logging.warning("Secret value %s", secret_value)
            secret = self.app.add_secret({"secret-key": secret_value})
            peer_relation.data[self.app]["secret-id"] = secret.id
            # XXX: Not currently working, we're not allowed to change permissions here.
            secret.grant(peer_relation.app, relation=peer_relation)


if __name__ == "__main__":  # pragma: nocover
    main(SecretsCharmCharm)
