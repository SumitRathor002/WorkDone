import json
from typing import Any, Dict, List
import os


script_dir = os.path.dirname(os.path.abspath(__file__))

json_definition = json.load(open(os.path.join(script_dir, "definition.json"), "r"))

testcase_output = json.load(open(os.path.join(script_dir,'output.json'), "r"))


def check_type(value: Any, definition: Dict[str, Any]) -> bool:
        """
        A helper function for validate_output()
        Returns True if the given input value matches the definition
        """

        if definition['type'] == 'string' and isinstance(value, str):
            return True
        
        elif definition['type'] == 'integer' and isinstance(value, int):
            return True
        
        elif definition['type'] == 'array' and isinstance(value, list):
            item_type = definition['items']['type']
            return all(check_type(item, {'type': item_type}) for item in value)
        
        elif definition['type'] == 'object' and isinstance(value, dict):

            for key, prop_def in definition['properties'].items():
                if key not in value:
                    return False
                if not check_type(value[key], prop_def):
                    return False
                
            # Check for extra fields not defined in the schema
            if len(value) > len(definition['properties']):
                return False
            return True
        
        return False
        
        # elif definition['type'] == 'object' and isinstance(value, dict):

        #     for key, prop_def in definition['properties'].items():
        #         if key in value or not check_type(value[key], prop_def):
        #             return False
        #     return True
        
        # return False



def validate_output(output: Dict[str, Any], definition: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Returns list of matched values with json definition"""

    output_def = definition[0]["parameters"]["properties"]["OUTPUT"]
    item_def = output_def["items"]
    
    valid_items = [item for item in output["OUTPUT"] if check_type(item, item_def)]
    return valid_items

valid_output = validate_output(testcase_output, json_definition)
print(valid_output)
