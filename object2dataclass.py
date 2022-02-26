from __future__ import annotations
from dataclasses import dataclass, Field, fields, is_dataclass, make_dataclass
from typing import Optional


@dataclass
class DataclassFieldInfo:
    field: Field
    wanted_value: any = None
    has_same_characteristics: bool = False
    fields: list[DataclassFieldInfo] = None

    def fields_are_similar(self) -> bool:
        are_similar = self.has_same_characteristics
        if are_similar and self.fields:
            for field in self.fields:
                are_similar = field.fields_are_similar()
        return are_similar


class Object2Dataclass:
    @staticmethod
    def __extract_dataclass_fields(dc: any, dc_fields: list[DataclassFieldInfo]):
        if dc is None:
            return

        for dc_field in fields(dc):
            dc_fields.append(DataclassFieldInfo(field=dc_field))
            if getattr(dc_field.type, '__dataclass_fields__', None):
                dc_fields[-1].fields = []
                Object2Dataclass.__extract_dataclass_fields(
                    getattr(dc, dc_field.name, None), dc_fields[-1].fields)

    @staticmethod
    def __find_dataclass_fields_in_object(obj: any, dc_fields: list[DataclassFieldInfo], parent_dc: DataclassFieldInfo = None):
        for item in obj:
            item_find_in_dc = [
                dc_field for dc_field in dc_fields if dc_field.field.name == item]
            if item_find_in_dc and len(item_find_in_dc) == 1:
                dc_find = item_find_in_dc[0]
                current_item = obj[item]

                if not isinstance(current_item, dict):
                    similar = type(current_item) == dc_find.field.type
                    dc_find.has_same_characteristics = similar
                    dc_find.wanted_value = current_item
                    if parent_dc:
                        parent_dc.has_same_characteristics = parent_dc.has_same_characteristics or similar
                else:
                    if dc_find.fields:
                        Object2Dataclass.__find_dataclass_fields_in_object(
                            current_item, dc_find.fields, dc_find)

    @staticmethod
    def __can_be_convert_to_dataclass(obj: any, dc: any):
        # Check if dc is a dataclass
        if (not is_dataclass(dc)):
            return (False, None)

        dc_fields: list[DataclassFieldInfo] = []

        # Retrieve dataclass fields
        Object2Dataclass.__extract_dataclass_fields(dc, dc_fields)

        # Find dataclass fields in the object
        Object2Dataclass.__find_dataclass_fields_in_object(obj, dc_fields)

        # Check if all fields have the same characteristics
        all_fields_are_similar = True
        for dc_field in dc_fields:
            all_fields_are_similar = dc_field.fields_are_similar()
            if not all_fields_are_similar:
                break

        return (all_fields_are_similar, dc_fields)

    @staticmethod
    def __fill_dataclass_with_object_values(created_dc: any, dc_fields: list[DataclassFieldInfo]):
        for field in dc_fields:
            if not field.fields:
                setattr(created_dc, field.field.name, field.wanted_value)
            else:
                Object2Dataclass.__fill_dataclass_with_object_values(
                    getattr(created_dc, field.field.name), field.fields)

    @staticmethod
    def can_be_convert_to_dataclass(obj: any, dc: any) -> bool:
        can_be_converted, _ = Object2Dataclass.__can_be_convert_to_dataclass(
            obj, dc)

        return can_be_converted

    @staticmethod
    def convert_object_to_dataclass(obj: any, dc: any) -> Optional[any]:
        can_be_converted, dc_fields = Object2Dataclass.__can_be_convert_to_dataclass(
            obj, dc)

        # If all data are available, convert object to dataclass
        if can_be_converted:
            created_dc: dc = dc()
            Object2Dataclass.__fill_dataclass_with_object_values(
                created_dc, dc_fields)
            return created_dc
        else:

            return None
