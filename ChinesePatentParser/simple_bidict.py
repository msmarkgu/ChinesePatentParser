from typing import TypeVar, Generic, Dict, Optional, List

K = TypeVar('K')  # Key type
V = TypeVar('V')  # Value type

class SimpleBiDict(Generic[K, V]):
    def __init__(self):
        self.forward: Dict[K, V] = {}
        self.backward: Dict[V, K] = {}
    
    def add(self, key: K, value: V) -> None:
        # Remove any existing mappings
        if key in self.forward:
            del self.backward[self.forward[key]]
        if value in self.backward:
            del self.forward[self.backward[value]]
            
        self.forward[key] = value
        self.backward[value] = key
    
    def get_by_key(self, key: K) -> Optional[V]:
        return self.forward.get(key)
    
    def get_by_value(self, value: V) -> Optional[K]:
        return self.backward.get(value)
    
    def del_by_key(self, key: K) -> None:
        if key in self.forward:
            value = self.forward[key]
            del self.forward[key]
            del self.backward[value]
    
    def del_by_value(self, value: V) -> None:
        if value in self.backward:
            key = self.backward[value]
            del self.backward[value]
            del self.forward[key]
    
    # Python 3.7+ maintains insertion order by default.
    def keys(self) -> List[K]:
        return list(self.forward.keys())
    
    def values(self) -> List[V]:
        return list(self.forward.values())
    
    def __str__(self) -> str:
        return str(self.forward)
