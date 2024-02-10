#!/usr/bin/env python3

"""Unit tests for the base model."""


from models.base_model import BaseModel
from models import storage
import unittest
from datetime import datetime
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.review import Review
from uuid import uuid4


class TestBaseModel(unittest.TestCase):
    """Define unit tests for the base model class."""

    def setUp(self):
        """Set up for the subsequent tests."""
        self.model = BaseModel()
        self.model.name = "My First Model"
        self.model.my_number = 89

    def test_id_type(self):
        """Test for ID type."""
        self.assertEqual(type(self.model.id), str)

    def test_created_at_type(self):
        """Test for 'created_at' type."""
        self.assertEqual(type(self.model.created_at), datetime)

    def test_updated_at_type(self):
        """Test for 'updated_at' type."""
        self.assertEqual(type(self.model.updated_at), datetime)

    def test_name_type(self):
        """Test for 'name' type."""
        self.assertEqual(type(self.model.name), str)

    def test_my_number_type(self):
        """Test for 'my_number' type."""
        self.assertEqual(type(self.model.my_number), int)

    def test_save_updates_updated_at(self):
        """Test for saving 'updated_at'."""
        old_updated_at = self.model.updated_at
        self.model.save()
        self.assertNotEqual(old_updated_at, self.model.updated_at)

    def test_to_dict_returns_dict(self):
        """Test for the return type of 'to_dict'."""
        self.assertEqual(type(self.model.to_dict()), dict)

    def test_to_dict_contains_correct_keys(self):
        """Test for the dictionary containing the correct keys."""
        model_dict = self.model.to_dict()
        self.assertIn('id', model_dict)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)
        self.assertIn('name', model_dict)
        self.assertIn('my_number', model_dict)
        self.assertIn('__class__', model_dict)

    def test_to_dict_created_at_format(self):
        """Test for the format of 'created_at'."""
        model_dict = self.model.to_dict()
        created_at = model_dict['created_at']
        self.assertEqual(created_at, self.model.created_at.isoformat())

    def test_to_dict_updated_at_format(self):
        """Test for the format of 'updated_at'."""
        model_dict = self.model.to_dict()
        updated_at = model_dict['updated_at']
        self.assertEqual(updated_at, self.model.updated_at.isoformat())


class TestBaseModelTwo(unittest.TestCase):
    """Define additional unit tests for the base model."""

    def setUp(self):
        """Set up for the subsequent tests (part two)."""
        self.my_model = BaseModel()

    def test_to_dict_method(self):
        """Test for the 'to_dict' method."""
        my_model_dict = self.my_model.to_dict()
        self.assertIsInstance(my_model_dict['created_at'], str)
        self.assertIsInstance(my_model_dict['updated_at'], str)
        self.assertEqual(my_model_dict['__class__'], 'BaseModel')

    def test_id_generation(self):
        """Test for ID generation type."""
        self.assertIsInstance(self.my_model.id, str)

    def test_created_at_and_updated_at_types(self):
        """Test for the types of 'created_at' and 'updated_at'."""
        self.assertIsInstance(self.my_model.created_at, datetime)
        self.assertIsInstance(self.my_model.updated_at, datetime)

    def test_str_representation(self):
        """Test for string representation."""
        expected = "[BaseModel] ({}) {}".format(
            self.my_model.id, self.my_model.__dict__)
        self.assertEqual(str(self.my_model), expected)

    def test_from_dict_method(self):
        """Test for the 'from_dict' method."""
        my_model_dict = self.my_model.to_dict()
        my_new_model = BaseModel(**my_model_dict)
        self.assertIsInstance(my_new_model, BaseModel)
        self.assertEqual(my_new_model.id, self.my_model.id)
        self.assertEqual(my_new_model.created_at, self.my_model.created_at)
        self.assertEqual(my_new_model.updated_at, self.my_model.updated_at)


class TestBaseModelThree(unittest.TestCase):
    """Define additional unit tests for the base model (part three)."""

    def test_review(self):
        """Test for the review."""
        place_id = uuid4()
        user_id = uuid4()
        review = Review()
        review.place_id = place_id
        review.user_id = user_id
        review.text = "Good"
        self.assertEqual(review.place_id, place_id)
        self.assertEqual(review.user_id, user_id)
        self.assertEqual(review.text, "Good")

    def test_city(self):
        """Test for the city."""
        state_id = uuid4()
        city = City()
        city.name = "Nairobi"
        city.state_id = state_id
        self.assertEqual(city.name, "Nairobi")
        self.assertEqual(city.state_id, state_id)

    def test_state(self):
        """Test for the state."""
        state = State()
        state.name = "Kenya"
        self.assertEqual(state.name, "Kenya")

    def test_amenity(self):
        """Test for the amenity."""
        amenity = Amenity()
        amenity.name = "Free Wifi"
        self.assertEqual(amenity.name, "Free Wifi")


if __name__ == "__main__":
    unittest.main()
