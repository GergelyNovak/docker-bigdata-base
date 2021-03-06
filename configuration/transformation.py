#!/usr/bin/python

def render_yaml(yaml_root, prefix=""):
    result = ""
    if isinstance(yaml_root, dict):
        if len(prefix)>0:
            result +="\n"
        for key in yaml_root:
            result += "{}{}: {}".format(prefix, key, render_yaml(yaml_root[key], prefix + "   "))
    elif isinstance(yaml_root, list):
        result += "\n"
        for item in yaml_root:
            result += prefix + " - " + render_yaml(item, prefix + " ")
    else:
        result += "{}\n".format(yaml_root)
    return result


def to_yaml(content):
    props = process_properties(content)

    keys = props.keys()
    yaml_props = {}
    for key in keys:
        parts = key.split(".")
        node = yaml_props
        prev_part = None
        parent_node = None
        for part in parts[:-1]:
            if part.isdigit():
                if isinstance(node, dict):
                    parent_node[prev_part] = []
                    node = parent_node[prev_part]
                while len(node) <= int(part):
                    node.append({})
                parent_node = node
                node = node[int(node)]
            else:
                if part not in node:
                    node[part] = {}
                parent_node = node
                node = node[part]
            prev_part = part
        if parts[-1].isdigit():
            if isinstance(node, dict):
                parent_node[prev_part] = []
                node = parent_node[prev_part]
            node.append(props[key])
        else:
            node[parts[-1]] = props[key]

    return render_yaml(yaml_props)

def to_yml(content):
    return to_yaml(content)

def to_properties(content):
    result = ""
    props = process_properties(content)
    for key in props.keys():
        result += "{}: {}\n".format(key, props[key])
    return result


def to_env(content):
    result = ""
    props = process_properties(content)
    for key in props.keys():
        result += "{}={}\n".format(key, props[key])
    return result


def to_sh(content):
    result = ""
    props = process_properties(content)
    for key in props.keys():
        result += "export {}=\"{}\"\n".format(key, props[key])
    return result


def to_cfg(content):
    result = ""
    props = process_properties(content)
    for key in props.keys():
        result += "{}={}\n".format(key, props[key])
    return result


def to_conf(content):
    result = ""
    props = process_properties(content)
    for key in props.keys():
        result += "export {} {}\n".format(key, props[key])
    return result


def to_xml(content):
    result = "<configuration>\n"
    props = process_properties(content)
    for key in props.keys():
        result += "<property><name>{0}</name><value>{1}</value></property>\n".format(key, props[key])
    result += "</configuration>"
    return result


def process_properties(content, sep=': ', comment_char='#'):
    """
    Read the file passed as parameter as a properties file.
    """
    props = {}
    for line in content.split("\n"):
        l = line.strip()
        if l and not l.startswith(comment_char):
            key_value = l.split(sep)
            key = key_value[0].strip()
            value = sep.join(key_value[1:]).strip().strip('"')
            props[key] = value

    return props
