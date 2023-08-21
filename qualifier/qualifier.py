from PIL import Image


def valid_input(
    image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]
) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    try:
        assert image_size[0] % tile_size[0] == 0
        assert image_size[1] % tile_size[1] == 0

        size_a = image_size[0] // tile_size[0]
        size_b = image_size[1] // tile_size[1]

        assert size_a * size_b == len(ordering)

        assert set(ordering) == set(range(len(ordering)))
        return True
    except AssertionError:
        return False


def rearrange_tiles(
    image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str
) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """
    with Image.open(image_path) as img:
        image_size = img.size
        image_mode = img.mode
        if not valid_input(image_size, tile_size, ordering):
            raise ValueError(
                "The tile size or ordering are not valid for the given image"
            )

        dx, dy = tile_size
        tiles = split_into_tiles(img, dx, dy)
        sorted_tiles = [tiles[index] for index in ordering]
        width_count = image_size[0] // dx
        height_count = image_size[1] // dy
        new_img = combine_tiles(
            sorted_tiles, width_count, height_count, dx, dy, image_mode
        )
        new_img.save(out_path)


# Split the img into tile of size (dx, dy)
def split_into_tiles(img, dx, dy):
    width, height = img.size
    tiles = [
        img.crop((x, y, x + dx, y + dy))
        for y in range(0, height, dy)
        for x in range(0, width, dx)
    ]
    return tiles


def combine_tiles(tiles, width_count, height_count, dx, dy, image_mode):
    img = Image.new(image_mode, (dx * width_count, dy * height_count))
    for i, tile in enumerate(tiles):
        # Column index of the tile, wraps around once the width of the image is reached
        x = (i % width_count) * dx
        # Row index of the tile, it increases as tiles fill up full rows
        y = (i // width_count) * dy
        img.paste(tile, (x, y))
    return img
