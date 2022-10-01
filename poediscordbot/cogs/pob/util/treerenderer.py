import json
import math
from dataclasses import dataclass
from pathlib import Path

from instance import config


@dataclass
class Node:
    node_id: int
    orbit: int
    orbit_index: int
    parent_ids: [int]
    children_ids: [int]
    group: int
    is_allocated: bool = False
    is_notable: bool = False
    is_keystone: bool = False
    is_ascendancy_start: bool = False
    class_start_index: bool = False
    is_mastery: bool = False
    label: str = None
    pos_x: float = None
    pos_y: float = None
    is_large_cluster_socket: bool = False
    is_medium_cluster_socket: bool = False
    is_small_cluster_socket: bool = False
    ascendancy: str = None

    def __hash__(self) -> int:
        return hash(self.node_id)

    @classmethod
    def create_from_dict(cls, node_id, args) -> 'Node':
        orbit = args.get('orbit', None)
        group = args.get('group', None)
        orbit_index = args.get('orbitIndex', None)
        parent_ids = [int(n) for n in args.get('in', [])]
        children_ids = [int(n) for n in args.get('out', [])]

        name = args.get('name', '')
        return Node(int(node_id), orbit, orbit_index, parent_ids, children_ids, group,
                    is_notable=args.get('isNotable', None),
                    is_keystone=args.get('isKeystone', None),
                    is_ascendancy_start=args.get('isAscendancyStart', None),
                    class_start_index=args.get('classStartIndex', None),
                    is_mastery=args.get('isMastery', False),
                    label=name,
                    is_large_cluster_socket=args.get('isJewelSocket') and name and name.startswith('Large Jewel'),
                    is_medium_cluster_socket=args.get('isJewelSocket') and name and name.startswith('Medium Jewel'),
                    is_small_cluster_socket=args.get('isJewelSocket') and name and name.startswith('Small Jewel'),
                    ascendancy=args.get('ascendancyName')
                    )


@dataclass
class Edge:
    parent: Node
    child: Node
    active: bool = False

    def __hash__(self) -> int:
        return hash(self.parent) + hash(self.child)

    def __eq__(self, other: "Edge"):
        if not isinstance(other, Edge):
            return False
        return (self.parent.node_id == other.parent.node_id and self.child.node_id == other.child.node_id) or (
                self.parent.node_id == other.child.node_id and self.child.node_id == other.parent.node_id)


class TreeRenderer:
    def __init__(self, tree_json):
        tree_path = Path(tree_json)
        content = json.load(tree_path.open('r'))
        self.groups = content.get('groups')
        self.nodes = self.parse_nodes(content)
        self.orbit_radius_list, skills_per_orbit_list = self._parse_orbits(content)
        self.orbit_angles = [self.calc_orbit_angles(n) for n in skills_per_orbit_list]

    def parse_nodes(self, content: dict) -> dict[str, Node]:
        nodes = {}
        for n, data in content.get('nodes', None).items():
            if n == "root" or data.get('name', '') == 'Position Proxy':
                continue
            nodes[int(n)] = Node.create_from_dict(n, data)
        return nodes

    def calculate_node_pos(self, data, group: dict, orbit_radius_list, orbit_angles):
        angle = orbit_angles[data.orbit][data.orbit_index]
        distance = orbit_radius_list[data.orbit]
        group_x = group.get('x')
        group_y = -1 * (group.get('y'))
        x_offset = 0
        y_offset = 0
        data.pos_x = group_x + x_offset + math.sin(angle) * distance
        data.pos_y = -1 * (group_y + y_offset + math.cos(angle) * distance)

    def __build_svg(self, ascendancy, edges, selected, x_min, x_max, y_min, y_max, file_name: str = None, render_size: int = 500):
        internal_radius = 12000
        viewbox_crop = internal_radius - 1000

        import svgwrite

        svg_document = svgwrite.Drawing(filename=file_name, size=(render_size, render_size))
        svg_document.viewbox(x_min + viewbox_crop, y_min + viewbox_crop,
                             x_max + viewbox_crop, y_max + viewbox_crop)

        line_width = 64
        inactive_color = 'lightgrey'
        active_color = "darkgoldenrod"
        mastery_color = "papayawhip"
        for edge in edges:
            if edge.active:
                svg_document.add(
                    svg_document.line(start=(edge.parent.pos_x + internal_radius, edge.parent.pos_y + internal_radius),
                                      end=(edge.child.pos_x + internal_radius, edge.child.pos_y + internal_radius),
                                      stroke_width=line_width,
                                      stroke=active_color if edge.active else inactive_color,
                                      ))

        masteries = [n for _, n in self.nodes.items() if n.is_mastery]
        jewels = [n for _, n in self.nodes.items() if
                  n.is_large_cluster_socket or n.is_medium_cluster_socket or n.is_small_cluster_socket]

        for _, node in self.nodes.items():
            is_active = int(node.node_id) in selected or node.label == ascendancy
            color = active_color if is_active else inactive_color
            if node.is_mastery or node.is_large_cluster_socket or node.is_medium_cluster_socket or node.is_small_cluster_socket:
                continue
            if node.group:
                opacity = 1 if is_active else .1
                radius = line_width + 16 if node.is_keystone or node.is_notable else line_width + 8
                svg_document.add(
                    svg_document.circle(center=(node.pos_x + internal_radius, node.pos_y + internal_radius),
                                        r=radius,
                                        fill=color,
                                        opacity=opacity
                                        ))
        for node in masteries:
            if node.pos_x and node.pos_y:
                is_active = int(node.node_id) in selected
                opacity = 1 if is_active else 0
                svg_document.add(
                    svg_document.circle(center=(node.pos_x + internal_radius, node.pos_y + internal_radius),
                                        r=line_width,
                                        # stroke_width=32,
                                        # stroke=active_color,
                                        fill=mastery_color,
                                        opacity=opacity,
                                        # fill_opacity=0
                                        ))
        for node in jewels:
            if node.pos_x and node.pos_y:
                is_active = int(node.node_id) in selected
                opacity = 1 if is_active else 0
                radius = line_width * 2
                if node.is_medium_cluster_socket:
                    radius = line_width * 3
                elif node.is_large_cluster_socket:
                    radius = line_width * 4

                svg_document.add(
                    svg_document.circle(center=(node.pos_x + internal_radius, node.pos_y + internal_radius),
                                        r=radius,
                                        fill=active_color,
                                        opacity=opacity,
                                        ))

        if file_name:
            svg_document.save()
        return svg_document.tostring()

    def parse_tree(self, chosen_nodes, file_name: str = None, render_size: int = 500):
        edges = set()
        x_min = 25000
        x_max = 0
        y_min = 25000
        y_max = 0
        ascendancy = ''
        for n, node in self.nodes.items():
            if node.group:
                self.calculate_node_pos(node, self.groups[str(node.group)], self.orbit_radius_list, self.orbit_angles)
                if node.node_id in chosen_nodes:
                    x_min = min(int(node.pos_x), x_min)
                    x_max = max(int(node.pos_x), x_max)
                    y_min = min(int(node.pos_y), y_min)
                    y_max = max(int(node.pos_y), y_max)
                    if node.ascendancy:
                        ascendancy = node.ascendancy
                # filter out nodes in the if block to not connect weird places from scion and masteries
                for t in node.children_ids:
                    target = self.nodes.get(t, None)
                    active = (node.is_ascendancy_start or int(node.node_id) in chosen_nodes) and int(t) in chosen_nodes
                    if self.nodes.get(t, None) is not None and not node.label.startswith('Seven') and \
                            not self.nodes[t].label.endswith('Mastery') and not node.label.endswith('Mastery'):
                        edges.add(Edge(node, target, active))
        return self.__build_svg(ascendancy, edges, chosen_nodes, x_min, x_max, y_min, y_max, file_name, render_size)

    def _parse_orbits(self, content: dict):
        constants = content.get('constants', None)
        orbit_radius_list = constants.get("orbitRadii", None)
        skills_per_orbit = constants["skillsPerOrbit"]
        return orbit_radius_list, skills_per_orbit

    def calc_orbit_angles(self, nodes_in_orbit):
        if nodes_in_orbit == 16:  # Every 30 and 45 degrees, per https://github.com/grindinggear/skilltree-export/blob/3.17.0/README.md
            return [math.radians(x) for x in [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]]
        if nodes_in_orbit == 40:  # Every 10 and 45 degrees
            return [math.radians(x) for x in
                    [0, 10, 20, 30, 40, 45, 50, 60, 70, 80, 90, 100, 110, 120, 130, 135, 140, 150, 160, 170, 180, 190,
                     200,
                     210, 220, 225, 230, 240, 250, 260, 270, 280, 290, 300, 310, 315, 320, 330, 340, 350]]

        orbit_angles = [math.radians(360 / nodes_in_orbit * x) for x in range(nodes_in_orbit)]

        return orbit_angles


if __name__ == '__main__':
    selected_nodes1 = [7388, 2292, 15167, 23027, 9392, 12613, 48362, 34423, 26481, 34171, 49254, 45558, 26196, 49080,
                       48118, 61419, 37569, 47197, 14057, 29353, 55332, 29712, 26270, 36542, 11730, 11924, 10904, 57264,
                       26712, 4397, 36949, 36678, 58218, 5916, 37403, 27323, 44169, 44202, 15117, 34506, 24872, 4367,
                       60398, 7444, 19103, 60472, 52502, 27203, 4177, 25970, 55190, 42760, 5935, 36915, 12125, 53123,
                       7960, 21958, 19501, 11420, 61471, 2474, 26393, 31875, 22088, 35958, 19635, 13559, 34880, 46897,
                       44184, 43061, 14936, 32932, 5743, 58998, 9386, 31462, 6770, 6712, 26866, 29049, 41190, 13009,
                       21974, 4713, 34927, 27038, 25831, 54279, 37114, 41472, 64210, 12246, 53279, 12738, 56461, 27611,
                       11505, 61259, 17735, 55804, 36634, 35260, 46340, 1203, 35288, 61804, 60554, 9408, 20987, 4100,
                       5632, 41472, 43520, 4100, 4096, 8192, 6404, 6400, 38400, 8704, 10752, 4868, 4864, 39168, 36864,
                       40966, 30612, 45558, 34383, 47197, 47642, 12125, 43400, 26393, 24180, 34927, 6216, 11505]
    selected_nodes2 = [49820, 27656, 9393, 64265, 33310, 27788, 49929, 9877, 14400, 39861, 47507, 41420, 12143, 23225,
                       61419, 22748, 16882, 20807, 55867, 35894, 56158, 18769, 60440, 59606, 33753, 59866, 26528, 62744,
                       22535, 29454, 20528, 45272, 28754, 18182, 25411, 9469, 30767, 65502, 35255, 4367, 8640, 22266,
                       28859, 8833, 53615, 5823, 63251, 18436, 6250, 61653, 25260, 45593, 21958, 6797, 6538, 6570,
                       59220,
                       6910, 5296, 22090, 61834, 49978, 18770, 48999, 36858, 60405, 6799, 44184, 32555, 34678, 56295,
                       14936, 53456, 8938, 29825, 2336, 15117, 36287, 21835, 36412, 4011, 63861, 63194, 12801, 9355,
                       5972, 55571, 65528, 13219, 3042, 23334, 35598, 12412, 53114, 4656, 19501, 35283, 45838, 30679,
                       1461, 31973, 46277, 25058, 32763, 61981, 33989, 49605, 49900, 40609, 19587, 19069, 58271, 4097,
                       1,
                       4101, 4097, 6149, 6145, 8193, 513, 4613, 4609, 6661, 6657, 8705, 10753, 1029, 5121, 5127, 58447,
                       49820, 40906, 9393, 61097, 53615, 18130, 6570, 2987, 63861, 57074, 65528, 47642, 3042]
    renderer = TreeRenderer(config.ROOT_DIR + 'resources/tree_3_19.min.json')
    svg = renderer.parse_tree(selected_nodes1, file_name="mybuild1.svg", render_size=500)
    svg2 = renderer.parse_tree(selected_nodes2, file_name="mybuild2.svg", render_size=500)
