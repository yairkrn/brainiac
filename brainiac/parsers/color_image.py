from PIL import Image


class ColorImageParser:
    field = 'color_image'

    @staticmethod
    def __chunker(seq, size):
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))

    def parse(self, context, snapshot):
        width = snapshot.color_image.w
        height = snapshot.color_image.h
        image = Image.new('RGB', (width, height))
        image.putdata([tuple(rgb) for rgb in self.__chunker(snapshot.color_image.colors, 3)])
        image.save(context.directory / 'color_image.png')
