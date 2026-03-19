#version 430

// Set local workgroup size. The total number of workgroups will be calculated
// from the image size and these values.
layout (local_size_x = 1, local_size_y = 1, local_size_z = 1) in;

layout (binding = 0, rgba8ui) uniform uimage2D InputImage;
layout (binding = 1, rgba8ui) writeonly uniform uimage2D OutputImage;

uniform ivec2 point = ivec2(0, 0);


void main() {
    ivec2 global_id = ivec2(gl_GlobalInvocationID.xy);
    
    uvec4 color = imageLoad(InputImage, global_id.xy);

    color.rgb = uvec3(255, 255, 255)-color.rgb;

    imageStore(OutputImage, global_id, color);
}