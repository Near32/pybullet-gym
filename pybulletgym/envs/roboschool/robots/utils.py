import xml.etree.ElementTree as ET


def extract_initial_velocities_and_masses_MJCF(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    initial_velocities = {}
    link_masses = {}
    for body in root.findall('worldbody/body'):
        name = body.get('name')
        velocity = body.find('velocity')
        if velocity is not None:
            linear = velocity.find('linear')
            if linear is not None:
              linear = [float(v) for v in linear.attrib.values()]
            else:
              linear = [0, 0, 0]  # Default if not specified. 
            angular = velocity.find('angular')  
            if angular is not None:
              angular = [float(v) for v in angular.attrib.values()]
            else:
              angular = [0, 0, 0] 
            initial_velocities[name] = {
                'linear': linear,
                'angular': angular
            }
        inertial = body.find('inertial')
        if inertial is None:  continue
        inertia = inertial.find('inertia')
        if inertia is None: continue
        mass = float(inertia.get('mass'))
        link_masses[name] = mass

    return initial_velocities, link_masses


def calculate_impulses(initial_velocities, link_masses, dt=1.0/240.0):
    impulses = {}
    for link_name, velocities in initial_velocities.items():
        mass = link_masses.get(link_name, 1.0)  # Default mass if not specified
        linear_impulse = [mass * v / dt for v in velocities['linear']]
        angular_impulse = [mass * v / dt for v in velocities['angular']]
        impulses[link_name] = {
            'linear': linear_impulse,
            'angular': angular_impulse
        }
    return impulses

