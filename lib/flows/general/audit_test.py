#!/usr/bin/env python
"""The auditing system."""


import os

from grr.lib import aff4
from grr.lib import rdfvalue
from grr.lib import test_lib


class TestAuditSystem(test_lib.FlowTestsBaseclass):

  def testFlowExecution(self):
    client_mock = test_lib.ActionMock("ListDirectory", "StatFile")

    for _ in test_lib.TestFlowHelper(
        "ListDirectory", client_mock, client_id=self.client_id,
        pathspec=rdfvalue.PathSpec(
            path=os.path.join(self.base_path, "test_img.dd/test directory"),
            pathtype=rdfvalue.PathSpec.PathType.OS),
        token=self.token):
      pass

    fd = aff4.FACTORY.Open("aff4:/audit/log", token=self.token)

    event = fd[0]

    self.assertEqual(event.action, rdfvalue.AuditEvent.Action.RUN_FLOW)
    self.assertEqual(event.flow, "ListDirectory")
    self.assertEqual(event.user, self.token.username)
