def part_1(layers):
    num_zeros = list(map(lambda a: a.count("0"), layers))
    less_zeros_layer = min(enumerate(num_zeros), key=lambda a: a[1])
    num_1_digits = layers[less_zeros_layer[0]].count("1")
    num_2_digits = layers[less_zeros_layer[0]].count("2")

    print("part_1 num 1 digits * num 2 digits for layer with most 0's:")
    print(f"{num_1_digits * num_2_digits}")


def part_2(layers, width, height):
    # make an array of the first layer
    output_layer = list(layers[0])
    # iteratively add the pixels if the output_layer pixels are transparent
    for layer in layers[1:]:
        for pixel_idx in range(len(output_layer)):
            if output_layer[pixel_idx] == "2":
                output_layer[pixel_idx] = layer[pixel_idx]

    # generate the output image baesd on the width
    output_image = "\n".join(
        [
            "".join(output_layer[i : i + width])
            for i in range(0, len(output_layer), width)
        ]
    )

    # replace 1's by '#' and 0's by ' ' to make the output stand out
    output_image = output_image.replace("1", "#")
    output_image = output_image.replace("0", " ")

    print("part_2 output image:")
    print(output_image)


if __name__ == "__main__":
    with open("input.txt") as f:
        # some constants
        width = 25
        height = 6
        px_per_layer = width * height
        # read the data and generate the layers as strings
        data = f.readline()
        layers = [
            data[i : i + px_per_layer]
            for i in range(0, len(data), px_per_layer)
        ]
        part_1(layers)

        part_2(layers, width, height)
