#!/usr/bin/env python3
import unittest
from unittest.mock import patch

from openpilot.selfdrive.car import gen_empty_fingerprint
from openpilot.selfdrive.car.hyundai.interface import CarInterface
from openpilot.selfdrive.car.hyundai.values import CAR, CarControllerParams, HyundaiFlags


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
    CP = self.get_params(fingerprint, "Hyundai Ioniq 5 (with HDA II) 2022-23")
    self.assertTrue(CP.flags & HyundaiFlags.CANFD_HDA2)
    self.assertEqual(len(CP.safetyConfigs), 2)

  def test_selected_carrot_can_uses_carrot_default_layout(self):
    fingerprint = gen_empty_fingerprint()
    fingerprint[4][0x123] = 8
    CP = self.get_params(fingerprint, "Hyundai Ioniq 5 (Southeast Asia only) 2022-23")
    self.assertFalse(CP.flags & HyundaiFlags.CANFD_HDA2)
    self.assertFalse(CP.flags & HyundaiFlags.CANFD_CAMERA_SCC)
    self.assertEqual(len(CP.safetyConfigs), 2)

  def test_selected_hda1_overrides_ambiguous_hda2_frame(self):
    fingerprint = gen_empty_fingerprint()
    fingerprint[6][0x50] = 16
    CP = self.get_params(fingerprint, "Hyundai Ioniq 5 (without HDA II) 2022-23")
    self.assertFalse(CP.flags & HyundaiFlags.CANFD_HDA2)
    self.assertEqual(len(CP.safetyConfigs), 2)

  def test_ioniq5_carrot_tuning_and_safety_limits(self):
    fingerprint = gen_empty_fingerprint()
    fingerprint[2][0x50] = 16
    CP = self.get_params(fingerprint)
    controller_params = CarControllerParams(CP)

    # Ioniq 5 vehicle and base torque data already match Carrot.
    self.assertEqual(CP.mass, 1948.)
    self.assertEqual(CP.wheelbase, 2.97)
    self.assertEqual(CP.steerRatio, 14.26)
    self.assertEqual(controller_params.STEER_MAX, 270)
    self.assertEqual(controller_params.STEER_DELTA_UP, 2)
    self.assertEqual(controller_params.STEER_DELTA_DOWN, 3)

    # Apply Carrot's Ioniq 5 longitudinal response and command limits.
    self.assertEqual(list(CP.longitudinalTuning.kpV), [1.0])
    self.assertEqual(list(CP.longitudinalTuning.kiV), [0.0])
    self.assertEqual(CP.longitudinalTuning.kf, 1.0)
    self.assertEqual(CarControllerParams.ACCEL_MIN, -4.0)
    self.assertEqual(CarControllerParams.ACCEL_MAX, 2.5)


if __name__ == "__main__":
  unittest.main()
