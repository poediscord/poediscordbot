import json
import math
from dataclasses import dataclass
from pathlib import Path

import svgwrite
from cairosvg import svg2png


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
        file = tree_path.open('r')
        content = json.load(file)
        file.close()

        self.groups = content.get('groups')
        self.nodes = self.parse_nodes(content)
        self.orbit_radius_list, skills_per_orbit_list = self._parse_orbits(content)
        self.orbit_angles = [self.calc_orbit_angles(n) for n in skills_per_orbit_list]
        self.inactive_color = 'grey'
        self.active_color = 'darkgoldenrod'
        self.mastery_color = 'papayawhip'

    @staticmethod
    def parse_nodes(content: dict) -> dict[int, Node]:
        nodes = {}
        for n, data in content.get('nodes', None).items():
            if n == "root" or data.get('name', '') == 'Position Proxy':
                continue
            nodes[int(n)] = Node.create_from_dict(n, data)
        return nodes

    @staticmethod
    def calculate_node_pos(data, group: dict, orbit_radius_list, orbit_angles):
        angle = orbit_angles[data.orbit][data.orbit_index]
        distance = orbit_radius_list[data.orbit]
        group_x = group.get('x')
        group_y = -1 * (group.get('y'))
        x_offset = 0
        y_offset = 0
        data.pos_x = group_x + x_offset + math.sin(angle) * distance
        data.pos_y = -1 * (group_y + y_offset + math.cos(angle) * distance)

    def __build_svg(self, ascendancy, edges, selected, x_min, x_max, y_min, y_max, file_name: str = None,
                    render_size: int = 500):

        # 0,0 point for drawing all nodes so we avoid negative vals
        internal_radius = 12500
        line_width = 64

        #calc better crop
        x0 = x_min + internal_radius
        y0 = y_min + internal_radius
        x1 = x_max + internal_radius - x0
        y1 = y_max + internal_radius - y0

        svg_document = svgwrite.Drawing(filename=file_name, size=(render_size, render_size))

        svg_document.viewbox(x0 - line_width * 2, y0 - line_width * 2,
                             x1 + line_width * 2, y1 + line_width * 2)

        for edge in edges:
            svg_document.add(
                svg_document.line(start=(edge.parent.pos_x + internal_radius, edge.parent.pos_y + internal_radius),
                                  end=(edge.child.pos_x + internal_radius, edge.child.pos_y + internal_radius),
                                  stroke_width=line_width,
                                  stroke=self.active_color if edge.active else self.inactive_color,
                                  ))

        masteries = [n for _, n in self.nodes.items() if n.is_mastery]
        jewels = [n for _, n in self.nodes.items() if
                  n.is_large_cluster_socket or n.is_medium_cluster_socket or n.is_small_cluster_socket]

        for _, node in self.nodes.items():
            is_active = int(node.node_id) in selected or node.label == ascendancy
            color = self.active_color if is_active else self.inactive_color
            if node.is_mastery or node.is_large_cluster_socket or node.is_medium_cluster_socket or node.is_small_cluster_socket:
                continue
            if node.group and self._show_node(node, x_min, x_max, y_min, y_max, is_active):
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
                                        fill=self.mastery_color,
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
                                        fill=self.active_color,
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
                    if active and target is not None and not node.label.startswith('Seven') and \
                            not self.connect_masteries(node, target) \
                            and not self.is_scion_starting_position_ascendancy(node):
                        edges.add(Edge(node, target, active))
        return self.__build_svg(ascendancy, edges, chosen_nodes, x_min, x_max, y_min, y_max, file_name, render_size)

    @staticmethod
    def is_scion_starting_position_ascendancy(node):
        return node.ascendancy == 'Ascendant' and node.label.startswith("Path of the")

    @staticmethod
    def connect_masteries(node, target):
        return target.label.endswith('Mastery') and not node.label.endswith('Mastery')

    @staticmethod
    def _parse_orbits(content: dict):
        constants = content.get('constants', None)
        orbit_radius_list = constants.get("orbitRadii", None)
        skills_per_orbit = constants["skillsPerOrbit"]
        return orbit_radius_list, skills_per_orbit

    @staticmethod
    def calc_orbit_angles(nodes_in_orbit):
        if nodes_in_orbit == 16:  # Every 30 and 45 degrees, per https://github.com/grindinggear/skilltree-export/blob/3.17.0/README.md
            return [math.radians(x) for x in [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]]
        if nodes_in_orbit == 40:  # Every 10 and 45 degrees
            return [math.radians(x) for x in
                    [0, 10, 20, 30, 40, 45, 50, 60, 70, 80, 90, 100, 110, 120, 130, 135, 140, 150, 160, 170, 180, 190,
                     200,
                     210, 220, 225, 230, 240, 250, 260, 270, 280, 290, 300, 310, 315, 320, 330, 340, 350]]

        orbit_angles = [math.radians(360 / nodes_in_orbit * x) for x in range(nodes_in_orbit)]

        return orbit_angles

    @staticmethod
    def to_png(svg_string: str, output_file: str) -> Path:
        svg2png(bytestring=svg_string, write_to=output_file)
        return Path(output_file)

    @staticmethod
    def _show_node(node: Node, x_min: int, x_max: int, y_min: int, y_max: int, active: bool):
        return active or (x_min < node.pos_x < x_max and y_min < node.pos_y < y_max and (
                not node.ascendancy or node.ascendancy))
