from imageSearch import ImageSearch


def test1():
    path = 'pattern.png'
    engine = ImageSearch()
    pos = engine.lookup(path)
    print(pos)
    x1, y1, x2, y2 = engine.get_region(path, pos)

    region_cutted = engine.cut_region(region=(x1, y1, x2, y2))
    region_cutted.save('region.png')


def test2():
    path = 'pattern2.png'
    engine = ImageSearch()
    engine.live(path)


if __name__ == '__main__':
    test2()
