import attr

# TODO: force types?


@attr.s
class ReaderUserInformation:
    user_id = attr.attrib()
    username = attr.attrib()
    birthday = attr.attrib()
    gender = attr.attrib()

    def __str__(self):
        return f'user {self.user_id}: {self.username}, born {self.birthday}' \
               f' ({self.gender})'


@attr.s
class ReaderColorImage:
    h = attr.attrib()
    w = attr.attrib()
    colors = attr.attrib()


@attr.s
class ReaderDepthimage:
    h = attr.attrib()
    w = attr.attrib()
    depths = attr.attrib()


@attr.s
class ReaderTranslation:
    x = attr.attrib()
    y = attr.attrib()
    z = attr.attrib()

    def __str__(self):
        return repr((self.x, self.y, self.z))


@attr.s
class ReaderRotation:
    x = attr.attrib()
    y = attr.attrib()
    z = attr.attrib()
    w = attr.attrib()

    def __str__(self):
        return repr((self.x, self.y, self.z, self.w))


@attr.s
class ReaderFeelings:
    hunger = attr.attrib()
    thirst = attr.attrib()
    exhaustion = attr.attrib()
    happiness = attr.attrib()


@attr.s
class ReaderSnapshot:
    timestamp = attr.attrib()
    translation = attr.attrib()
    rotation = attr.attrib()
    color_image = attr.attrib()
    depth_image = attr.attrib()
    feelings = attr.attrib()

    def __str__(self):
        return f'Snapshot from {self.timestamp} on {self.translation} / ' + \
               f'{self.rotation} with a {self.color_image.w}x' + \
               f'{self.color_image.h} color image and a ' + \
               f'{self.depth_image.w}x{self.depth_image.h} depth ' + \
               f'image.'

