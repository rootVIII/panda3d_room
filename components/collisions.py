from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import CollisionNode, CollisionBox, CollisionCapsule


class Collisions:
    def __init__(self):
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()

    def set_scene_collision_nodes(self, scene):
        # scene.ls()
        body_capsule = CollisionCapsule(0.0, 0.0, 1.2, 0.0, 0.0, 4.0, 1.5)
        body_cnode = self.ninja.attach_new_node(CollisionNode('body_cnode'))  # noqa
        body_cnode.node().add_solid(body_capsule)
        self.pusher.add_collider(body_cnode, self.ninja)  # noqa
        # Put FROM objects into traverser:
        self.cTrav.add_collider(body_cnode, self.pusher)  # noqa

        # Don't put the following static TO objects into the Traverser:
        coffee_table = scene.find('CoffeeTable')
        coffee_tale_box = CollisionBox(0.0, 0.9, 1.6, 0.2)
        coffee_table_node = coffee_table.attach_new_node(CollisionNode('coffee_table_cnode'))
        coffee_table_node.set_pos(0.0, 0.1, 0.4)
        coffee_table_node.node().add_solid(coffee_tale_box)
        self.pusher.add_collider(coffee_table_node, coffee_table)  # noqa

        seat = scene.find('Seat')
        seat_box = CollisionBox(0.0, 0.7, 0.6, 0.3)
        seat_node = seat.attach_new_node(CollisionNode('seat_cnode'))
        seat_node.set_pos(-1.8, -8.0, 0.0)
        seat_node.set_h(40)
        seat_node.node().add_solid(seat_box)
        self.pusher.add_collider(seat_node, seat)  # noqa

        sofas = scene.find('SofaFinal')
        sofa1_box = CollisionBox(0.0, 1.0, 0.8, 0.6)
        sofa1_box_node = sofas.attach_new_node(CollisionNode('sofa1_cnode'))
        sofa1_box_node.set_pos(0.0, 2.5, 0.0)
        sofa1_box_node.node().add_solid(sofa1_box)
        self.pusher.add_collider(sofa1_box_node, sofas)  # noqa
        sofa2_box = CollisionBox(0.0, 0.3, 1.3, 0.6)
        sofa2_box_node = sofas.attach_new_node(CollisionNode('sofa2_cnode'))
        sofa2_box_node.set_pos(1.8, 0.1, 0.0)
        sofa2_box_node.node().add_solid(sofa2_box)
        self.pusher.add_collider(sofa2_box_node, sofas)  # noqa

        ns_wall_dims = (0.0, 2.6, 0.2, 2.0)
        ew_wall_dims = (0.0, 0.2, 4.05, 2.0)

        walls = scene.find('Walls')
        north_wall_box = CollisionBox(*ns_wall_dims)
        north_wall_box_node = walls.attach_new_node(CollisionNode('north_wall_cnode'))
        north_wall_box_node.set_pos(0.2, -4.0, 2.0)
        north_wall_box_node.node().add_solid(north_wall_box)
        self.pusher.add_collider(north_wall_box_node, walls)  # noqa
        south_wall_box = CollisionBox(*ns_wall_dims)
        south_wall_box_node = walls.attach_new_node(CollisionNode('south_wall_cnode'))
        south_wall_box_node.set_pos(0.2, 4.5, 2.0)
        south_wall_box_node.node().add_solid(south_wall_box)
        self.pusher.add_collider(south_wall_box_node, walls)  # noqa
        east_wall_box = CollisionBox(*ew_wall_dims)
        east_wall_box_node = walls.attach_new_node(CollisionNode('east_wall_cnode'))
        east_wall_box_node.set_pos(-2.0, 0.25, 2.0)
        east_wall_box_node.node().add_solid(east_wall_box)
        self.pusher.add_collider(east_wall_box_node, walls)  # noqa

        west_wall_box = CollisionBox(*ew_wall_dims)
        west_wall_box_node = walls.attach_new_node(CollisionNode('west_wall_cnode'))
        west_wall_box_node.set_pos(2.6, 0.25, 2.0)
        west_wall_box_node.node().add_solid(west_wall_box)
        self.pusher.add_collider(west_wall_box_node, walls)  # noqa

        # body_cnode.show()
        # coffee_table_node.show()
        # seat_node.show()
        # sofa1_box_node.show()
        # sofa2_box_node.show()
        # north_wall_box_node.show()
        # south_wall_box_node.show()
        # east_wall_box_node.show()
        # west_wall_box_node.show()
