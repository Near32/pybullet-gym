import xml.etree.ElementTree as ET


def extract_initial_velocities_and_masses_MJCF(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    initial_velocities = {}
    range_velocities = {}
    link_masses = {}
    range_masses = {}
    for body in root.iter('body'):
        name = body.get('name')
        velocity = body.find('velocity')
        if velocity is not None:
            linear = velocity.find('linear')
            if linear is not None:
              rlinear = [
                linear.attrib.get('xmin', -1),
                linear.attrib.get('xmax', 1), 
                linear.attrib.get('ymin', -1), 
                linear.attrib.get('ymax', 1), 
                linear.attrib.get('zmin', -1), 
                linear.attrib.get('zmax', 1),
              ]
              linear = [linear.attrib['x'], linear.attrib['y'], linear.attrib['z']]
              linear = [float(v) for v in linear]
              rlinear = [float(v) for v in rlinear]
            else:
              linear = [0, 0, 0]  # Default if not specified. 
              rlinear = [-1, 1, -1, 1, -1, 1]
            print(f"Extracting initial linear velocity for {name} : {linear}")
            angular = velocity.find('angular')  
            if angular is not None:
              rangular = [
                angular.attrib.get('xmin', -1), 
                angular.attrib.get('xmax', 1), 
                angular.attrib.get('ymin', -1), 
                angular.attrib.get('ymax', 1), 
                angular.attrib.get('zmin', -1), 
                angular.attrib.get('zmax', 1),
              ]
              angular = [angular.attrib['x'], angular.attrib['y'], angular.attrib['z']]
              angular = [float(v) for v in angular]
              rangular = [float(v) for v in rangular]
            else:
              angular = [0, 0, 0]  # Default if not specified.
              rangular = [-1, 1, -1, 1, -1, 1]
            print(f"Extracting initial angular velocity for {name} : {angular}")
            initial_velocities[name] = {
                'linear': linear,
                'angular': angular,
                'range_linear': rlinear,
                'range_angular': rangular
            }
        inertial = body.find('inertial')
        if inertial is None:  continue
        inertia = inertial.find('inertia')
        if inertia is None: continue
        mass = float(inertia.get('mass', 1.0))
        rmass = float(inertia.get('maxmass', 1.0)) 
        link_masses[name] = mass
        range_masses[name] = rmass

    rdict = {
        'initial_velocities': initial_velocities,
        'link_masses': link_masses,
        'range_velocities': range_velocities,
        'range_masses': range_masses,
    }
    
    return rdict


def calculate_impulses(
    physicsClient,
    parts,
    initial_velocities, 
    link_masses, 
    dt=1.0/240.0,
):
    ''' 
    Calculates the impulse to apply to each link to achieve the desired initial velocities.
    :param link_masses: corresponds to the mass values extracted from XML when specified.
    If left unspecified, then we use the mass of the link as provided by MuJoCo from 
    the distribution of mass of the geom used in XML, using the :param parts: dict. 
    '''
    impulses = {}
    for link_name, velocities in initial_velocities.items():
        mass = link_masses.get(link_name, None)  # Default mass if not specified
        if mass is None:
            part = parts[link_name]
            robot_id = part.bodyIndex
            link_id = part.bodyPartIndex
            mass = physicsClient.getDynamicsInfo(robot_id, link_id)[0]
        linear_impulse = [mass * v / dt for v in velocities['linear']]
        angular_impulse = [mass * v / dt for v in velocities['angular']]
        impulses[link_name] = {
            'linear': linear_impulse,
            'angular': angular_impulse
        }
    return impulses

