#!/usr/bin/env python3
import unittest
from unittest.mock import patch

from openpilot.selfdrive.car import gen_empty_fingerprint
from openpilot.selfdrive.car.hyundai.interface import CarInterface
from openpilot.selfdrive.car.hyundai.values import CAR, HyundaiFlags


class TestIoniq5CanfdDetection(unittest.TestCase):
  @staticmethod
  def get_params(fingerprint, selected_car=""):
    with patch("openpilot.selfdrive.car.hyundai.interface.Params") as params:
      params.return_value.get.return_value = selected_car
      params.return_value.get_bool.return_value = False
      return CarInterface.get_params(CAR.IONIQ_5, fingerprint, [], False, False)

  def test_hda2_on_internal_panda(self):
    fingerprint = gen_empty_fingerprint()
    fingerprint[2][0x50] = 16

    CP = self.get_params(fingerprint)

    self.assertTrue(CP.flags & HyundaiFlags.CANFD_HDA2)
    self.assertFalse(CP.flags & HyundaiFlags.CANFD_HDA2_ALT_STEERING)

  def test_hda2_alt_steering_on_external_red_panda(self):
    fingerprint = gen_empty_fingerprint()
    fingerprint[6][0x110] = 32

    CP = self.get_params(fingerprint)

    self.assertTrue(CP.flags & HyundaiFlags.CANFD_HDA2)
    self.assertTrue(CP.flags & HyundaiFlags.CANFD_HDA2_ALT_STEERING)
    self.assertEqual(len(CP.safetyConfigs), 2)

  def test_non_hda2_on_external_red_panda(self):
    fingerprint = gen_empty_fingerprint()
    fingerprint[6][0x123] = 8

    CP = self.get_params(fingerprint)

    self.assertFalse(CP.flags & HyundaiFlags.CANFD_HDA2)
    self.assertEqual(len(CP.safetyConfigs), 2)

  def test_selected_hda2_uses_hda2_layout_without_initial_camera_frames(self):
    fingerprint = gen_empty_fingerprint()
    fingerprint[4][0x123] = 8
    CP = self.get_params(fingerprint, "현대 아이오닉 5 (HDA2) 2022-23")
    self.assertTrue(CP.flags & HyundaiFlags.CANFD_HDA2)
    self.assertEqual(len(CP.safetyConfigs), 2)

  def test_selected_southeast_asia_uses_hda2_harness_layout(self):
    fingerprint = gen_empty_fingerprint()
    fingerprint[4][0x123] = 8
    CP = self.get_params(fingerprint, "현대 아이오닉 5 (HDA2 대체 조향) 2022-23")
    self.assertTrue(CP.flags & HyundaiFlags.CANFD_HDA2)
    self.assertEqual(len(CP.safetyConfigs), 2)

  def test_selected_hda1_overrides_ambiguous_hda2_frame(self):
    fingerprint = gen_empty_fingerprint()
    fingerprint[6][0x50] = 16
    CP = self.get_params(fingerprint, "현대 아이오닉 5 (HDA1) 2022-23")
    self.assertFalse(CP.flags & HyundaiFlags.CANFD_HDA2)
    self.assertEqual(len(CP.safetyConfigs), 2)


if __name__ == "__main__":
  unittest.main()
