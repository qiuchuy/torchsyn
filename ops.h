/*
 * Neural Network Operations Header File
 * Contains implementations of various neural network operators
 */

#ifndef OPS_H
#define OPS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <stdbool.h>

// Tensor utility functions with raw pointers
int compute_tensor_size(const int* shape, int ndims);
int get_tensor_offset(const int* shape, const int* indices, int ndims);
float* allocate_tensor(const int* shape, int ndims);
void free_tensor(float* data);

// Helper functions for common tensor shapes
int get_tensor_rank(float* tensor);
void get_tensor_shape(float* tensor, int* shape, int ndims);

// Basic arithmetic operations
void op_add(const float* a, const float* b, float* c, int size);
void op_sub(const float* a, const float* b, float* c, int size);
void op_mul(const float* a, const float* b, float* c, int size);
void op_div(const float* a, const float* b, float* c, int size);

// Activation functions
void op_relu(const float* x, float* y, int size);
void op_sigmoid(const float* x, float* y, int size);
void op_tanh(const float* x, float* y, int size);
void op_gelu(const float* x, float* y, int size);
void op_leaky_relu(const float* x, float* y, int size, float negative_slope);
void op_prelu(const float* x, const float* alpha, float* y, int size);
void op_softmax(const float* x, float* y, int size, int axis);
void op_elu(const float* x, float* y, int size, float alpha);
void op_celu(const float* x, float* y, int size, float alpha);
void op_selu(const float* x, float* y, int size);
void op_glu(const float* x, float* y, int size, int dim);
void op_hardsigmoid(const float* x, float* y, int size);
void op_logsigmoid(const float* x, float* y, int size);
void op_softmin(const float* x, float* y, int size, int axis);
void op_logsoftmax(const float* x, float* y, int size, int axis);
void op_silu(const float* x, float* y, int size);
void op_hardswish(const float* x, float* y, int size);
void op_mish(const float* x, float* y, int size);
void op_hardtanh(const float* x, float* y, int size, float min_val, float max_val);
void op_hardshrink(const float* x, float* y, int size, float lambd);
void op_softshrink(const float* x, float* y, int size, float lambd);
void op_relu6(const float* x, float* y, int size);
void op_softplus(const float* x, float* y, int size);

// Reduction operations
float op_sum(const float* x, int size);
float op_mean(const float* x, int size);
float op_reducemin(const float* x, int size);
float op_reducemax(const float* x, int size);
float op_reduceprod(const float* x, int size);
float op_reducel1(const float* x, int size);
float op_reducel2(const float* x, int size);

// Comparison operations
void op_min(const float* a, const float* b, float* c, int size);
void op_max(const float* a, const float* b, float* c, int size);
void op_greater(const float* a, const float* b, float* c, int size);
void op_less(const float* a, const float* b, float* c, int size);
void op_equal(const float* a, const float* b, float* c, int size);
void op_greater_equal(const float* a, const float* b, float* c, int size);
void op_less_equal(const float* a, const float* b, float* c, int size);
void op_not_equal(const float* a, const float* b, float* c, int size);

// Mathematical operations
void op_round(const float* x, float* y, int size);
void op_floor(const float* x, float* y, int size);
void op_ceil(const float* x, float* y, int size);
void op_abs(const float* x, float* y, int size);
void op_neg(const float* x, float* y, int size);
void op_reciprocal(const float* x, float* y, int size);
void op_pow(const float* a, const float* b, float* c, int size);
void op_atan(const float* x, float* y, int size);
void op_asin(const float* x, float* y, int size);
void op_acos(const float* x, float* y, int size);
void op_tan(const float* x, float* y, int size);
void op_sin(const float* x, float* y, int size);
void op_cos(const float* x, float* y, int size);
void op_log(const float* x, float* y, int size);
void op_log2(const float* x, float* y, int size);
void op_log10(const float* x, float* y, int size);
void op_log1p(const float* x, float* y, int size);
void op_exp(const float* x, float* y, int size);
void op_expm1(const float* x, float* y, int size);
void op_sqrt(const float* x, float* y, int size);
void op_rsqrt(const float* x, float* y, int size);
void op_square(const float* x, float* y, int size);
void op_cube(const float* x, float* y, int size);
void op_erf(const float* x, float* y, int size);
void op_erfc(const float* x, float* y, int size);
void op_sign(const float* x, float* y, int size);
void op_remainder(const float* a, const float* b, float* c, int size);
void op_floor_divide(const float* a, const float* b, float* c, int size);

// Matrix operations
void op_matmul(const float* a, const float* b, float* c, int M, int K, int N);
void op_transpose_2d(const float* x, float* y, int H, int W);
void op_transpose(const float* x, float* y, const int* input_shape, const int* perm, int ndims);
void op_triu(const float* x, float* y, int rows, int cols);
void op_tril(const float* x, float* y, int rows, int cols);

// Convolution operations
void op_conv2d(const float* input, const float* weight, const float* bias, float* output,
               int N, int H_in, int W_in, int C_in,
               int H_k, int W_k, int C_out,
               int stride_h, int stride_w, int pad_h, int pad_w);
void op_conv1d(const float* input, const float* weight, const float* bias, float* output,
                int batch, int in_channels, int out_channels, int input_size, int kernel_size,
                int stride, int padding);
void op_nchw_conv2d(const float* input, const float* weight, const float* bias, float* output,
                     int batch, int in_channels, int out_channels, int height, int width,
                     int kernel_h, int kernel_w, int stride_h, int stride_w, int pad_h, int pad_w);

// Pooling operations
void op_maxpool2d(const float* x, float* y, int batch, int channels, int height, int width,
                   int kernel_h, int kernel_w, int stride_h, int stride_w, int pad_h, int pad_w);
void op_avgpool2d(const float* x, float* y, int batch, int channels, int height, int width,
                   int kernel_h, int kernel_w, int stride_h, int stride_w, int pad_h, int pad_w);

// Shape manipulation operations
void op_constant(float* y, int size, float value);
void op_reshape(const float* x, float* y, int size);
void op_expand(const float* x, float* y, int input_size, int output_size);
void op_expand_last4(const float* x, float* y, int input_size, int output_size);
void op_slice(const float* x, float* y, const int* input_shape, const int* output_shape,
              const int* start_indices, int ndims);
void op_squeeze(const float* x, float* y, int input_size);
void op_unsqueeze(const float* x, float* y, int input_size);

// Logical operations
void op_and(const float* a, const float* b, float* c, int size);
void op_or(const float* a, const float* b, float* c, int size);
void op_xor(const float* a, const float* b, float* c, int size);
void op_not(const float* x, float* y, int size);
void op_where(const float* condition, const float* x, const float* y, float* output, int size);

// Bitwise operations
void op_left_shift(const float* a, const float* b, float* c, int size);
void op_right_shift(const float* a, const float* b, float* c, int size);
void op_bitwise_and(const float* a, const float* b, float* c, int size);
void op_bitwise_or(const float* a, const float* b, float* c, int size);
void op_bitwise_xor(const float* a, const float* b, float* c, int size);
void op_bitwise_not(const float* a, float* c, int size);

// Special operations
void op_clip(const float* x, float* y, int size, float min_val, float max_val);
void op_cast_bool(const float* x, float* y, int size);
void op_cast_i32(const float* x, float* y, int size);
void op_cast_f32(const float* x, float* y, int size);
void op_cast_f64(const float* x, float* y, int size);
void op_cast_i64(const float* x, float* y, int size);
void op_reflect_pad(const float* x, float* y, int input_size, int output_size, const int* pads);
void op_const_pad(const float* x, float* y, int input_size, int output_size, float pad_value);
void op_replicate_pad(const float* x, float* y, int input_size, int output_size);

// Argument operations
int op_argmin(const float* x, int size);
int op_argmax(const float* x, int size);

// Concatenation operations
void op_concat1(const float** inputs, float* output, const int* input_sizes, int num_inputs);

// Batch operations
void op_batchnorm2d(const float* x, const float* gamma, const float* beta,
                     const float* mean, const float* var, float* y, int size);

// Interpolation operations
void op_nearest_interp(const float* x, float* y, int input_size, int output_size);
void op_linear_interp(const float* x, float* y, int input_size, int output_size);
void op_bilinear_interp(const float* x, float* y, int input_size, int output_size);
void op_bicubic_interp(const float* x, float* y, int input_size, int output_size);
void op_trilinear_interp(const float* x, float* y, int input_size, int output_size);

// Special value operations
void op_isnan(const float* x, float* y, int size);
void op_isinf(const float* x, float* y, int size);
void op_isfinite(const float* x, float* y, int size);

#endif // OPS_H