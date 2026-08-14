#!/usr/bin/env python3
import unittest
from unittest.mock import patch

from cereal import car
from openpilot.selfdrive.car.car_helpers import get_startup_event


EventName = car.CarEvent.EventName


class TestStartupEvent(unittest.TestCase):
  @patch("openpilot.selfdrive.car.car_helpers.get_normalized_origin", return_value="github.com/master-kr/openpilot")
  @patch("openpilot.selfdrive.car.car_helpers.get_short_branch", return_value="release-c3-BDv2")
  @patch("openpilot.selfdrive.car.car_helpers.is_tested_branch", return_value=False)
  @patch("openpilot.selfdrive.car.car_helpers.is_comma_remote", return_value=False)
  def test_bdv2_release_has_normal_startup(self, _comma_remote, _tested, _branch, _origin):
    self.assertEqual(get_startup_event(True, True, True), EventName.startup)

  @patch("openpilot.selfdrive.car.car_helpers.get_normalized_origin", return_value="github.com/master-kr/openpilot")
  @patch("openpilot.selfdrive.car.car_helpers.get_short_branch", return_value="release-c3-BDv2-source")
  @patch("openpilot.selfdrive.car.car_helpers.is_tested_branch", return_value=False)
  @patch("openpilot.selfdrive.car.car_helpers.is_comma_remote", return_value=False)
  def test_bdv2_source_release_has_normal_startup(self, _comma_remote, _tested, _branch, _origin):
    self.assertEqual(get_startup_event(True, True, True), EventName.startup)

  @patch("openpilot.selfdrive.car.car_helpers.get_normalized_origin", return_value="github.com/another/openpilot")
  @patch("openpilot.selfdrive.car.car_helpers.get_short_branch", return_value="release-c3-BDv2")
  @patch("openpilot.selfdrive.car.car_helpers.is_tested_branch", return_value=False)
  @patch("openpilot.selfdrive.car.car_helpers.is_comma_remote", return_value=False)
  def test_other_fork_keeps_untested_warning(self, _comma_remote, _tested, _branch, _origin):
    self.assertEqual(get_startup_event(True, True, True), EventName.startupMaster)


if __name__ == "__main__":
  unittest.main()
