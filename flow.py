class Flow:
    """Abstraccion de los flows."""
    def __init__(self, flow, interconexion, priority):
        self.flow = flow
        self.interconexion = interconexion
	self.priority = priority
