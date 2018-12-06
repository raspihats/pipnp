import json


def determine_type(name, value, package):
    if "fiducial" in name.lower() or "fiducial" in package.lower():
        return "fiducial"
    if "np" in value.lower() or "dnp" in value.lower():
        return "ignore"
    return "component"


def import_file(file):
    steps = []
    with open(file, 'r') as infile:
        for line in infile:
            try:
                print("processing: {}".format(line.strip()))
                parts = line.strip().split(',')
                steps.append({
                    'name': parts[0],
                    'value': parts[4],
                    'package': parts[5],
                    'x': float(parts[1]),
                    'y': float(parts[2]),
                    'angle': float(parts[3]),
                    'type': determine_type(parts[0], parts[4], parts[5])
                })
            except Exception as e:
                raise Exception("Line: '{}' {}".format(line, str(e)))

    with open(file + ".json", 'w') as outfile:
        json.dump(steps, outfile)


if __name__ == '__main__':
    import_file("/home/fcos/Desktop/DI16ac.mnt")
