# -*- coding: utf-8 -*-
#
# Copyright 2012-2015 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from helpers import unittest
try:
    from unittest import mock
except ImportError:
    import mock

import luigi.rpc
from luigi.scheduler import CentralPlannerScheduler
import central_planner_test
import luigi.server
from server_test import ServerTestBase


class RemoteSchedulerTest(unittest.TestCase):
    def testUrlArgumentVariations(self):
        for url in ['http://zorg.com', 'http://zorg.com/']:
            for suffix in ['api/123', '/api/123']:
                s = luigi.rpc.RemoteScheduler(url, 42)
                with mock.patch.object(s, '_fetcher') as fetcher:
                    s._fetch(suffix, '{}')
                    fetcher.fetch.assert_called_once_with('http://zorg.com/api/123', '{}', 42)


class RPCTest(central_planner_test.CentralPlannerTest, ServerTestBase):

    def get_app(self):
        conf = self.get_scheduler_config()
        sch = CentralPlannerScheduler(**conf)
        return luigi.server.app(sch)

    def setUp(self):
        super(RPCTest, self).setUp()
        self.sch = luigi.rpc.RemoteScheduler(self.get_url(''))
        self.sch._wait = lambda: None

    # disable test that doesn't work with remote scheduler

    def test_task_first_failure_time(self):
        pass

    def test_task_first_failure_time_remains_constant(self):
        pass

    def test_task_has_excessive_failures(self):
        pass

    def test_quadratic_behavior(self):
        """ This would be too slow to run through network """
        pass

    def test_get_work_speed(self):
        """ This would be too slow to run through network """
        pass
