import json
class Nutritional:
  def __init__(self):
    self.value = None
    self.unit = None

  def __iter__(self):
    yield from {
          "value": self.value,
          "unit": self.unit
    }.items()
  def __str__(self):
        return json.dumps(self.to_json())

  def __repr__(self):
      return self.__str__()
        
  def to_json(self):
    to_return = {"value": self.value, "unit": self.unit}
    return to_return
  def __getitem__(self, key):
    return getattr(self, key)
  def __setitem__(self, key, value):
    setattr(self, key, value)

  
  

