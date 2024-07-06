# Base Project

This project can be used as a base project for a variety of Django server applications. It is provided as-is without any guarantee of support or bug-fixes.

# CustomImageField

## Fields

1. aspect_ratios (array) - If specified as None it will use the aspect ratio of the uploaded image. If specified a value - has to be a string with slash eg. "1/1", "16/9"
2. file_types (array) - specifies the file types the image will be generated to
3. container width (int) - the width of the generated/modified image. Used to limit the maximum width of layouts, to promote better readability on larger screens. We default to 1200px, but you can override this setting, via the PICTURES["CONTAINER_WIDTH"] setting.
   You may also set it to None, should you not use a container.
4. width_field/height_field - to store the width and the height of the original image
5. grid_columns (int) - will generate container_width/grid_column number of pictures (eg. container_width = 1200, grid_column=2, will generate 600w and 1200w (2 pictures)). We default to 12 columns, but you can override this setting, via the PICTURES["GRID_COLUMNS"] setting.
6. pixel_densities (array of int) - generates pictures based on specified pixel densities eg. [1, 2] (will generate x2 images)
7. breakpoints - specifies the images you want to create for each breakpoint. You may define your own breakpoints, they should be identical to the ones used in your css library. Simply override the PICTURES["BREAKPOINTS"] setting.
8. max_file_size (int) - specifies the largest size the image will be stored
9. keep_original (boolean) - If **True** the original image will be kept and new images will be generated. If **False** the original image will be modified (with just ratio/container_width for now)
10. quality (int) - (ONLY WORKS WITH JPEG) specifies the image quality, on a scale from 1 (worst) to 95 (best). The default is 75. Values above 95 should be avoided; 100 disables portions of the JPEG compression algorithm, and results in large files with hardly any gain in image quality.

Note:

- If keep_original is False: The original image will be modified only to the first aspect ratio set in the aspect_ratios array. If keep_original is true then it will be the expected behavior.
- file_types only works with keep_original True (will generate pics in array of specified file type)
- grid_column and pixel densities only work with keep_original True.
- If you want to generate a specific height - You will need to calculate the specific container_width to aspect ratio that will match the current desired height.
- Quality works for JPEG format only (and currently only with keep_original=False)
- Future improvements - can choose to change image format to JPEG and quality (right now only support if original image is JPEG)
