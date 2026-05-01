import unittest
import yaml
from slac_devices.area import Area
from slac_devices.bpm import BPMCollection
from slac_devices.magnet import MagnetCollection
from pathlib import Path


class TestArea(unittest.TestCase):
    def setUp(self) -> None:
        self.config_location = (
            Path(__file__).parent / "test_data" / "config"
        )
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_area_with_no_magnets(self):
        mock_screen_data = {"screens": {}}
        with open(
            self.config_location / "screen" / "typical_screen.yaml", "r"
        ) as file:
            mock_screen_data["screens"] = yaml.safe_load(file)
        area = Area(name="mock_area", **mock_screen_data)
        self.assertIsNone(area.magnet_collection)
        self.assertIsNone(area.magnets)

    def test_area_repr_includes_counts_and_populated_types(self):
        area = Area.model_construct(
            name="L3",
            magnet_collection=MagnetCollection.model_construct(
                magnets={"M1": object(), "M2": object()}
            ),
            bpm_collection=BPMCollection.model_construct(
                bpms={"BPM1": object()}
            ),
            screen_collection=None,
            wire_collection=None,
            lblm_collection=None,
            pmt_collection=None,
            tcav_collection=None,
        )

        representation = repr(area)
        self.assertIn("Area(name='L3'", representation)
        self.assertIn("total_devices=3", representation)
        self.assertIn("'magnets': 2", representation)
        self.assertIn("'bpms': 1", representation)
        self.assertIn("'tcavs': 0", representation)
        self.assertIn("populated_types=['magnets', 'bpms']", representation)
