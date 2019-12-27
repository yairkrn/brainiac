from PIL import Image


class ColorImageParser:
    field = 'color_image'

    @classmethod
    def _chunker(cls, seq, size):
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))

    @classmethod
    def _bytes_to_rgb(cls, bytes):
        return [tuple(rgb) for rgb in cls._chunker(bytes, 3)]

    def parse(self, context, snapshot):
        width = snapshot.color_image.w
        height = snapshot.color_image.h
        image = Image.new('RGB', (width, height))
        image.putdata(self._bytes_to_rgb(snapshot.color_image.colors))
        image.save(context.directory / 'color_image.png')
