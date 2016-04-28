from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import logging
from unittest import TestCase

from pcs.lib import error_codes
from pcs.lib.commands.constraint import ticket as ticket_command
from pcs.lib.env import LibraryEnvironment as Env
from pcs.lib.errors import ReportItemSeverity as severities
from pcs.test.tools.assertions import assert_xml_equal, assert_raise_library_error
from pcs.test.tools.misc import get_test_resource as rc
from pcs.test.tools.pcs_mock import mock
from pcs.test.tools.xml import get_xml_manipulation_creator_from_file


class CreateTest(TestCase):
    def setUp(self):
        self.mock_logger = mock.MagicMock(logging.Logger)
        self.create_cib = get_xml_manipulation_creator_from_file(
            rc("cib-empty.xml")
        )

    def test_sucess_create(self):
        resource_xml = '<primitive id="resourceA" class="service" type="exim"/>'
        cib = (
            self.create_cib()
                .append_to_first_tag_name('resources', resource_xml)
        )

        env = Env(self.mock_logger, cib_data=str(cib))
        ticket_command.create(
                env, "ticketA", "resourceA", "master", {"loss-policy": "fence"}
        )

        assert_xml_equal(
            env.get_cib_xml(),
            str(cib.append_to_first_tag_name(
                'constraints', """
                    <rsc_ticket
                        id="ticket-ticketA-resourceA-Master"
                        rsc="resourceA"
                        rsc-role="Master"
                        ticket="ticketA"
                        loss-policy="fence"
                    />
                """
            ))
        )

    def test_refuse_for_nonexisting_resource(self):
        env = Env(self.mock_logger, cib_data=str(self.create_cib()))
        assert_raise_library_error(
            lambda: ticket_command.create(
                env, "ticketA", "resourceA", "master", {"loss-policy": "fence"}
            ),
            (
                severities.ERROR,
                error_codes.RESOURCE_DOES_NOT_EXIST,
                {"resource_id": "resourceA"},
            ),
        )