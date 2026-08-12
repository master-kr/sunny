#!/usr/bin/env python3
import unittest

from openpilot.selfdrive.car import gen_empty_fingerprint
from openpilot.selfdrive.car.hyundai.interface import CarInterface
from openpilot.selfdrive.car.hyundai.values import CAR, HyundaiFlags


class TestIoniq5CanfdDetection(unittest.TestCase):
  @staticmethod
  def get_params(fingerprint):
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


if __name__ == "__main__":
  unittest.main()
