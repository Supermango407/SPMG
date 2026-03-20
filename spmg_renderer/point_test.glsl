#version 430

// Set local workgroup size. The total number of workgroups will be calculated
// from the image size and these values.
layout (local_size_x = 1, local_size_y = 1, local_size_z = 1) in;

layout (rgba8, binding = 0) uniform image2D InputImage;
layout (rgba8, binding = 1) writeonly uniform image2D OutputImage;

layout(std430, binding = 2) buffer InputBuffer {
    ivec2 values[];
} point_buffer;

uniform int radius = 10;

void main() {
    ivec2 global_id = ivec2(gl_GlobalInvocationID.xy);
    vec4 color = imageLoad(InputImage, global_id.xy);

    // float distance = distance(point, global_id);
    // if (distance <= 100) {
    //     color = uvec4(0, 0, 0, 255);
    // }

    // ivec2 points[2];
    // points[0] = ivec2(0, 0);
    // points[1] = ivec2(256, 256);
    
    int point_count = point_buffer.values.length();
    if (point_count > 0) {
        float distance = distance(global_id, point_buffer.values[0]);
        for (int i = 1; i < point_count; ++i) {
            ivec2 point = point_buffer.values[i];
            float distance_checking = distance(global_id, point);
            if (distance_checking < distance) {
                distance = distance_checking;
            }
        }

        if (distance <= radius) {
            color = vec4(0, 0, 0, 1);
        } else {
            color = vec4(1, 1, 1, 1);
        }
    } else {
        color = vec4(1, 1, 1, 1);
    }

    imageStore(OutputImage, global_id, color);
}