import pybullet as pb
import numpy as np


def log_contacts(p, NS):
    contact_logs = []
    contact_points = p.getContactPoints()
    for contact in contact_points:
        import ipdb; ipdb.set_trace()
        bodyA = contact[1]
        bodyA_name = p.getBodyInfo(bodyA)[1].decode('utf-8') if bodyA >= 0 else 'World' 
        bodyB = contact[2]
        bodyB_name = p.getBodyInfo(bodyB)[1].decode('utf-8') if bodyB >= 0 else 'World' 
        linkA = contact[3]
        linkA_name = p.getJointInfo(linkA)[1].decode('utf-8')
        linkB = contact[4]
        linkB_name = p.getJointInfo(linkB)[1].decode('utf-8')
        contact_position = contact[5]
        contact_normal = contact[7]
        contact_force = contact[9]
        contact_logs.append(f"Contact between body {NS[bodyA_name]}'s link {NS[linkA_name]} and body {NS[bodyB_name]}'s link {NS[linkB_name]}")
        contact_logs.append(f"Contact position: {contact_position}")
        contact_logs.append(f"Contact normal: {contact_normal}")
        contact_logs.append(f"Contact force: {contact_force}")
    return contact_logs

# Function to log kinematic states
def log_kinematics(p, parts, NS):
    printoptions = np.get_printoptions()
    np.set_printoptions(formatter={'float_kind': lambda x: "%.3f" % x})
    kinematics_logs = []
    '''
    num_bodies = p.getNumBodies()
    for i in range(num_bodies):
        body_id = i
        body_info = p.getBodyInfo(body_id)
        body_name = body_info[1].decode('utf-8')
        pos, orn = p.getBasePositionAndOrientation(body_id)
        linear_vel, angular_vel = p.getBaseVelocity(body_id)
        kinematics_logs.append(
          f"Body {NS[body_name]}:\n Position: {pos}, Orientation: {orn}\n"
          + f"Linear Velocity: {linear_vel}, Angular Velocity: {angular_vel}\n")
    '''
    for part_name, part in parts.items():
        body_id = part.bodyIndex
        body_info = p.getBodyInfo(body_id)
        body_name = body_info[1].decode('utf-8')
        pos = part.current_position()
        orn = part.current_orientation()
        linear_vel, angular_vel = part.get_linear_velocity(), part.get_angular_velocity()
        kinematics_logs.append(
          f"Body {NS[body_name]}'s part {NS[part_name]}:\nPosition: {pos}, Orientation: {orn}\n"
          + f"Linear Velocity: {linear_vel}, Angular Velocity: {angular_vel}\n")
    np.set_printoptions(**printoptions) 
    return kinematics_logs

# Function to log joint states
def log_joint_states(p, robot_id):
    printoptions = np.get_printoptions()
    np.set_printoptions(formatter={'float_kind': lambda x: "%.3f" % x})
    joint_logs = []
    num_joints = p.getNumJoints(robot_id)
    joint_id2name = dict([(i, p.getJointInfo(robot_id, i)[1].decode('utf-8')) for i in range(num_joints)])
    for i in range(num_joints):
        joint_info = p.getJointInfo(robot_id, i)
        joint_name = joint_info[1].decode('utf-8')
        linkParent_id = joint_info[-1]
        linkParent_name = joint_id2name[linkParent_id] if linkParent_id >= 0 else 'World'
        linkChild_id = i
        linkChild_name = joint_id2name[linkChild_id]
        joint_state = p.getJointState(robot_id, i)
        joint_pos = joint_state[0]
        joint_vel = joint_state[1]
        joint_force = joint_state[3]
        joint_logs.append(f"Joint {joint_name}:\nBody {linkParent_name} -> Body {linkChild_name}\nPosition: {joint_pos}, Velocity: {joint_vel}, Force: {joint_force}")
    np.set_printoptions(**printoptions) 
    return joint_logs

