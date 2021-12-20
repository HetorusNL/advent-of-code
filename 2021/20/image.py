class Image:
    def __init__(self):
        self._image = {}
        self._ipa = None
        self._min_x = 0
        self._min_y = 0
        self._max_x = 0
        self._max_y = 0
        self._edge_pixel = None

    def set_image_processing_algorithm(self, image_processing_algorithm):
        self._ipa = image_processing_algorithm

    def get_ipa_result(self, value):
        return self._ipa[value] == "#"

    def add_pixel(self, x, y, value):
        if x not in self._image:
            self._image[x] = {}
        self._image[x][y] = value == "#"
        self._max_x = max(self._max_x, x)
        self._max_y = max(self._max_y, y)

    def get_pixel(self, x, y):
        if self._edge_pixel is not None:
            if x < self._min_x + 2 or x > self._max_x - 2:
                return self._edge_pixel is True
            if y < self._min_y + 2 or y > self._max_y - 2:
                return self._edge_pixel is True
        if x not in self._image:
            return False
        return self._image[x].get(y) is True

    def apply_algorithm(self):
        new_image = {}
        self._min_x -= 2
        self._min_y -= 2
        self._max_x += 2
        self._max_y += 2
        # loop through all current pixels
        for x in range(self._min_x, self._max_x + 1):
            new_image[x] = {}
            for y in range(self._min_y, self._max_y + 1):
                # loop through the 3x3 grid around each pixel
                bvalue = 0
                for sy in range(y - 1, y + 2):
                    for sx in range(x - 1, x + 2):
                        bvalue *= 2
                        bvalue += self.get_pixel(sx, sy)
                new_image[x][y] = self.get_ipa_result(bvalue)
        self._edge_pixel = new_image[self._min_x + 1][self._min_y + 1]
        self._image = new_image

    def print_image(self):
        for y in range(self._min_y, self._max_y + 1):
            for x in range(self._min_x, self._max_x + 1):
                print("#" if self.get_pixel(x, y) else ".", end="")
            print()

    def count_pixels(self):
        pixels = 0
        for y in range(self._min_y, self._max_y + 1):
            for x in range(self._min_x, self._max_x + 1):
                if self.get_pixel(x, y):
                    pixels += 1
        return pixels
