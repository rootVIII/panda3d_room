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
        # body_cnode.show()
        self.pusher.add_collider(body_cnode, self.ninja)  # noqa
        # Put FROM objects into traverser:
        self.cTrav.add_collider(body_cnode, self.pusher)  # noqa

        # static TO objects don't need to be put in the Traverser:
        coffee_table = scene.find('CoffeeTable')
        coffee_tale_box = CollisionBox(0.0, 0.9, 1.6, 0.2)
        coffee_table_node = coffee_table.attach_new_node(CollisionNode('coffee_table_cnode'))
        coffee_table_node.set_pos(0.0, 0.1, 0.4)
        coffee_table_node.node().add_solid(coffee_tale_box)
        # coffee_table_node.show()
        self.pusher.add_collider(coffee_table_node, coffee_table)  # noqa

        seat = scene.find('Seat')
        seat_box = CollisionBox(0.0, 0.7, 0.6, 0.3)
        seat_node = seat.attach_new_node(CollisionNode('seat_cnode'))
        seat_node.set_pos(-1.8, -8.0, 0.0)
        seat_node.set_h(40)
        seat_node.node().add_solid(seat_box)
        # seat_node.show()
        self.pusher.add_collider(seat_node, seat)  # noqa

        curtain_wall = scene.find('Curtain001')
        curtain_wall_box = CollisionBox(0.0, 2.2, 0.2, 0.6)
        curtain_wall_box_node = curtain_wall.attach_new_node(CollisionNode('curtain_wall_cnode'))
        curtain_wall_box_node.set_pos(0.7, -2.2, 0.0)
        curtain_wall_box_node.node().add_solid(curtain_wall_box)
        # curtain_wall_box_node.show()
        self.pusher.add_collider(curtain_wall_box_node, curtain_wall)  # noqa

        side_quest_wall = scene.find('fwaf')
        side_quest_wall_box = CollisionBox(0.0, 0.2, 4.0, 0.6)
        side_quest_wall_box_node = side_quest_wall.attach_new_node(CollisionNode('side_quest_wall_cnode'))
        side_quest_wall_box_node.set_pos(-2.2, 1.3, 0.0)
        side_quest_wall_box_node.node().add_solid(side_quest_wall_box)
        # side_quest_wall_box_node.show()
        self.pusher.add_collider(side_quest_wall_box_node, side_quest_wall)  # noqa

        door_wall = scene.find('Door')
        door_wall_box = CollisionBox(0.0, 3.8, 0.2, 0.6)
        door_wall_box_node = door_wall.attach_new_node(CollisionNode('door_wall_cnode'))
        door_wall_box_node.set_pos(1.8, -0.4, 0.0)
        door_wall_box_node.node().add_solid(door_wall_box)
        # door_wall_box_node.show()
        self.pusher.add_collider(door_wall_box_node, door_wall)  # noqa

        plant_wall = scene.find('Sphere002')
        plant_wall_box = CollisionBox(0.0, 0.2, 2.7, 0.6)
        plant_wall_box_node = plant_wall.attach_new_node(CollisionNode('plant_wall_cnode'))
        plant_wall_box_node.set_pos(-4.5, -1.6, 0.0)
        plant_wall_box_node.set_h(10)
        plant_wall_box_node.node().add_solid(plant_wall_box)
        # plant_wall_box_node.show()
        self.pusher.add_collider(plant_wall_box_node, plant_wall)  # noqa

        sofas = scene.find('SofaFinal')
        sofa1_box = CollisionBox(0.0, 1.0, 0.8, 0.6)
        sofa1_box_node = sofas.attach_new_node(CollisionNode('sofa1_cnode'))
        sofa1_box_node.set_pos(0.0, 2.5, 0.0)
        sofa1_box_node.node().add_solid(sofa1_box)
        # sofa1_box_node.show()
        self.pusher.add_collider(sofa1_box_node, sofas)  # noqa
        sofa2_box = CollisionBox(0.0, 0.3, 1.3, 0.6)
        sofa2_box_node = sofas.attach_new_node(CollisionNode('sofa2_cnode'))
        sofa2_box_node.set_pos(1.8, 0.1, 0.0)
        sofa2_box_node.node().add_solid(sofa2_box)
        # sofa2_box_node.show()
        self.pusher.add_collider(sofa2_box_node, sofas)  # noqa