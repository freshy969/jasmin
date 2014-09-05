from Routes import Route
from Routables import Routable

class InvalidRoutingTableParameterError(Exception):
    """Raised when a parameter is not an instance of a desired class (used for
    validating inputs
    """

"""Generick Routing table
"""
class RoutingTable:
    type = 'generick'
    
    def __init__(self):
        self.table = []
        
    def add(self, route, order):
        if not isinstance(route, Route):
            raise InvalidRoutingTableParameterError("route is not an instance of Route")
        if not isinstance(order, int):
            raise InvalidRoutingTableParameterError("order is not an integer")
        if self.type == 'mo':
            if type(route.connector) is not list:
                if route.connector.type not in ['http', 'smpps']:
                    raise InvalidRoutingTableParameterError("connector '%s' type '%s' is not valid for MO Route" % (route.connector.cid, route.connector.type))
            else:
                for connector in route.connector:
                    if connector.type not in ['http', 'smpps']:
                        raise InvalidRoutingTableParameterError("connector '%s' type '%s' is not valid for MO Route" % (connector.cid, connector.type))
        if self.type == 'mt':
            if type(route.connector) is not list:
                if route.connector.type not in ['smppc']:
                    raise InvalidRoutingTableParameterError("connector '%s' type '%s' is not valid for MT Route" % (route.connector.cid, route.connector.type))
            else:
                for connector in route.connector:
                    if connector.type not in ['smppc']:
                        raise InvalidRoutingTableParameterError("connector '%s' type '%s' is not valid for MT Route" % (connector.cid, connector.type))
        if order < 0:
            raise InvalidRoutingTableParameterError("order must be 0 (default route) or greater")
        if order != 0 and route.type != self.type:
            raise InvalidRoutingTableParameterError("route must be of type '%s', '%s' was given" % (self.type, route.type))
        if order == 0 and route.type != 'default':
            raise InvalidRoutingTableParameterError("Route with order=0 must be a DefaultRoute")
        
        # Replace older routes with the same given order
        self.remove(order)

        self.table.append({order: route})
        self.table.sort(reverse=True)
        
    def remove(self, order):
        for r in self.table:
            if r.keys()[0] == order:
                self.table.remove(r)
                return True
            
        return False
        
    def getAll(self):
        return self.table
    
    def flush(self):
        self.table = []
        
    def getConnectorFor(self, routable):
        """This will return the right connector to send the routable to, if no routes were found it will
        return None
        """
        
        if not isinstance(routable, Routable):
            raise InvalidRoutingTableParameterError("routable is not an instance of Routable")
        
        for r in self.table:
            route = r.values()[0]
            m = route.matchFilters(routable)
            if m is not None:
                return m
        
        return None
    
"""MT Routing table
"""
class MTRoutingTable(RoutingTable):
    type = 'mt'
    
"""MO Routing table
"""
class MORoutingTable(RoutingTable):
    type = 'mo'