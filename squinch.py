import bpy
import math
import mathutils
from mathutils import Vector

# Populate the values below by dragging from the scene tree into this window
bottom_left = bpy.data.objects["Bottom Left"]
bottom_right = bpy.data.objects["Bottom Right"]
top_left = bpy.data.objects["Top Left"]
top_right = bpy.data.objects["Top Right"]

# Calculate the horizontal field of view to keep the camera appropriately 'zoomed'
def horizontal_fov(camera_y, camera_z, sensor_width):
    
    # find the center of the target frame. Ignore the z component as we are only worried about the horizontal FOV
    midpoint = (bottom_left.location + bottom_right.location) / 2.0
    midpoint.z = camera_z
    
    # Calculate the position of a hypothetical camera positioned inline to the target frame
    offset_camera_position = Vector([midpoint.x, camera_y, camera_z])
    
    # Find the angles between the camera and the two edges of the screen. Ignore Z.
    camera_vector_to_left = (bottom_left.location - offset_camera_position)
    camera_vector_to_left.z = 0
    camera_vector_to_right = (bottom_right.location - offset_camera_position)
    camera_vector_to_right.z = 0
    
    # Calculate the angle and convert to mm for lens
    fov_angle = camera_vector_to_left.angle(camera_vector_to_right)
    fov_in_mm = sensor_width / (2.0 * math.tan(fov_angle / 2.0))
    
    return fov_in_mm

bpy.app.driver_namespace['horizontal_fov'] = horizontal_fov


# Calculate the value for "Shift X"
def get_horizontal_shift(camera_x):
    
    # Find the frame center
    center = (top_left.location + top_right.location + bottom_left.location + bottom_right.location) / 4.0
    
    # Calculate how offset the camera is from the center as a fraction of total horizontal screen space
    camera_center_global_offset = center.x - camera_x
    camera_center_relative_offset = camera_center_global_offset / (bottom_right.location.x - bottom_left.location.x)
    
    return camera_center_relative_offset

bpy.app.driver_namespace['get_horizontal_shift'] = get_horizontal_shift

# Calculate the value for "Shift Y"
def get_vertical_shift(camera_z):
    
    # Find the frame center
    center = (top_left.location + top_right.location + bottom_left.location + bottom_right.location) / 4.0
    
    # Calculate how offset the camera is from the center as a fraction of the total *horizontal* screen space (not vertical!)
    camera_center_global_offset = center.z - camera_z
    camera_center_relative_offset = camera_center_global_offset / (bottom_right.location.x - bottom_left.location.x)
    
    return camera_center_relative_offset

bpy.app.driver_namespace['get_vertical_shift'] = get_vertical_shift
