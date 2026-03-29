#version 430

// Set local workgroup size. The total number of workgroups will be calculated
// from the image size and these values.
layout (local_size_x = 1, local_size_y = 1, local_size_z = 1) in;

layout (binding = 0, rgba32f) uniform image2D InputImage;
layout (binding = 1, rgba32f) writeonly uniform image2D OutputImage;

layout (binding = 3, rgba32f) writeonly uniform image2D ImageVar;

void main() {
    ivec2 global_id = ivec2(gl_GlobalInvocationID.xy);
    
    vec4 color = imageLoad(InputImage, global_id.xy);

    color.rgb = vec3(1, 1, 1)-color.rgb;

    imageStore(ImageVar, ivec2(2, 3), vec4(1, 1, 1, 1));

    imageStore(OutputImage, global_id, color);
}