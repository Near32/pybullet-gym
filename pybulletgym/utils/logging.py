from typing import List, Dict, Tuple
import pybullet as pb
import numpy as np


def log_contacts(p, parts: Dict[str,object], NS: Dict[str,str]) -> List[str]:
    '''
    Log contacts in a string

    # TODO : update nameswap approach when name cannot be find.

    :param p: pybullet instance
    :param NS: Dict[str,str] namespace in order to deal with obfuscated names.
    :return: contact_logs: List[str]
    '''
    contact_logs = []
    contact_points = p.getContactPoints()
    for contact in contact_points:
        bodyA = contact[1]
        bodyA_name = p.getBodyInfo(bodyA)[1].decode('utf-8') if bodyA >= 0 else 'World' 
        bodyB = contact[2]
        bodyB_name = p.getBodyInfo(bodyB)[1].decode('utf-8') if bodyB >= 0 else 'World' 
        linkA = contact[3]
        linkA_name = [part for part in parts.values() if part.bodyPartIndex==linkA]
        if len(linkA_name): linkA_name = linkA_name[0].name
        else: linkA_name = 'base'
        #if linkA == -1: linkA_name= 'base'
        #else: linkA_name = p.getJointInfo(bodyUniqueId=bodyA, jointIndex=linkA)[1].decode('utf-8')
        linkB = contact[4]
        linkB_name = [part for part in parts.values() if part.bodyPartIndex==linkB]
        if len(linkB_name): linkB_name = linkB_name[0].name
        else: linkB_name = 'base'
        #if linkB == -1: linkB_name= 'base' 
        #else: linkB_name = p.getJointInfo(bodyUniqueId=bodyB, jointIndex=linkB)[1].decode('utf-8')
        contact_position = contact[5]
        contact_position_str = ' '.join([f"{x:.2f}" for x in contact_position])
        contact_normal = contact[7]
        contact_normal_str = ' '.join([f"{x:.2f}" for x in contact_normal])
        contact_force = contact[9]
        contact_force_str = f"{contact_force:.2f}"
        #TODO: update below:
        if bodyA_name not in NS:  NS[bodyA_name] = bodyA_name
        if bodyB_name not in NS:  NS[bodyB_name] = bodyB_name
        if linkA_name not in NS:  NS[linkA_name] = linkA_name
        if linkB_name not in NS:  NS[linkB_name] = linkB_name
        contact_logs.append(f"Contact between {NS[bodyA_name]}'s link {NS[linkA_name]} and {NS[bodyB_name]}'s link {NS[linkB_name]}")
        contact_logs.append(f"position: {contact_position_str}")
        contact_logs.append(f"normal: {contact_normal_str}")
        contact_logs.append(f"force: {contact_force_str}\n")
    return contact_logs

# Function to log kinematic states
def log_kinematics(p, parts, NS, list_infos=['position', 'orientation', 'linear_velocity', 'angular_velocity']):
    kinematics_logs = []
    for part_name, part in parts.items():
        body_id = part.bodyIndex
        link_id = part.bodyPartIndex
        body_info = p.getBodyInfo(body_id)
        body_name = body_info[1].decode('utf-8')
        #TODO: update below:
        if body_name not in NS:  NS[body_name] = body_name
        if part_name not in NS:  NS[part_name] = part_name
        #DEBUG: klog = f"{NS[body_name]}({body_id})'s part {NS[part_name]}({link_id}):\n"
        klog = f"{NS[body_name]}'s part {NS[part_name]}:\n"
        if 'position' in list_infos:
          pos = part.current_position()
          pos_str = ' '.join([f"{x:.2f}" for x in pos])
          klog += f"Position: {pos_str}\n"
        if 'orientation' in list_infos:
          orn = part.current_orientation()
          orn_str = ' '.join([f"{x:.2f}" for x in orn])
          klog += f"Orientation: {orn_str}\n"
        if 'linear_velocity' in list_infos:        
          linear_vel = part.get_linear_velocity()
          lvel_str = ' '.join([f"{x:.2f}" for x in linear_vel])
          klog += f"Linear Velocities: {lvel_str}\n"
        if 'angular_velocity' in list_infos:
          angular_vel = part.get_angular_velocity()
          avel_str = ' '.join([f"{x:.2f}" for x in angular_vel])
          klog += f"Angular Velocities: {avel_str}\n"        
          kinematics_logs.append(klog)
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

