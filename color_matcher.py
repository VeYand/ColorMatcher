from PIL import Image
from colors import compare_colors
from collections import deque


class ColorMatcher:
    def __init__(self, image: Image):
        self.image = image
        self.width, self.height = self.image.size
        self.image_pixels = self.image.load()

    def match(self, coordinates: (int, int), threshold: float, exact: bool = True, padding: int = 0) -> Image:
        x, y = coordinates

        if not self.__valid_coordinates(x, y):
            raise IndexError("Coordinates are out of bounds")

        matched_pixels = set()
        queue_to_visit = deque([coordinates])
        target_color = self.image_pixels[x, y]

        while queue_to_visit:
            cx, cy = queue_to_visit.popleft()

            if (cx, cy) in matched_pixels:
                continue

            matched_pixels.add((cx, cy))

            for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                if self.__valid_coordinates(nx, ny) and (nx, ny) not in matched_pixels:
                    if compare_colors(
                            target_color if exact else self.image_pixels[cx, cy],
                            self.image_pixels[nx, ny]
                    ) < threshold:
                        queue_to_visit.append((nx, ny))

        if padding > 0:
            matched_pixels = self.__expand_mask(matched_pixels, padding)

        return self.__generate_output_image(matched_pixels)

    def __expand_mask(self, matched_pixels, padding: int):
        expanded_pixels = set(matched_pixels)

        for x, y in list(matched_pixels):
            for dx in range(-padding, padding + 1):
                for dy in range(-padding, padding + 1):
                    if abs(dx) + abs(dy) <= padding:
                        nx, ny = x + dx, y + dy
                        if self.__valid_coordinates(nx, ny):
                            expanded_pixels.add((nx, ny))

        return expanded_pixels

    def __generate_output_image(self, matched_pixels) -> Image:
        new_image = Image.new('RGB', (self.width, self.height))

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in matched_pixels:
                    new_image.putpixel((x, y), (0, 255, 0))
                else:
                    new_image.putpixel((x, y), self.image_pixels[x, y])

        return new_image

    def __valid_coordinates(self, x: int, y: int):
        return 0 <= x < self.width and 0 <= y < self.height
