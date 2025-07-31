from typing import Any, Dict


def list_to_tree(
    data_list: list[Dict[str, Any]],
    id_field: str = "id",
    parent_id_field: str = "parent_id",
    children_field: str = "children",
) -> list[Dict[str, Any]]:
    """
    将列表数据转换为树形结构

    :param data_list: 列表数据，每个元素是一个字典，包含 id 和 parent_id 字段
    :param id_field: 节点唯一标识字段名，默认为 "id"
    :param parent_id_field: 父节点标识字段名，默认为 "parent_id"
    :param children_field: 子节点字段名，默认为 "children"
    :return: 树形结构，每个节点包含 children 字段表示子节点（如果 children 为空，则不设置该字段）
    """
    # 创建一个字典，用于存储每个节点的引用
    node_map: Dict[Any, Dict[str, Any]] = {}
    # 存储根节点
    roots: list[Dict[str, Any]] = []

    # 第一次遍历：初始化每个节点的引用，并添加 children 属性
    for item in data_list:
        # 将当前节点添加到 node_map 中，并初始化 children 字段
        node_map[item[id_field]] = {**item, children_field: []}

    # 第二次遍历：将每个节点挂载到其父节点下
    for item in data_list:
        # 获取当前节点的 parent_id
        parent_id = item[parent_id_field]

        if parent_id is None:
            # 如果 parent_id 为 None，说明是根节点，直接添加到 roots 中
            roots.append(node_map[item[id_field]])
        else:
            # 否则，找到父节点，将当前节点挂载到父节点的 children 中
            if parent_id in node_map:
                node_map[parent_id][children_field].append(node_map[item[id_field]])
            else:
                # 如果父节点不存在，可以选择忽略或抛出异常
                # 这里选择忽略，直接将当前节点作为根节点
                roots.append(node_map[item[id_field]])

    # 移除空的 children 字段
    def remove_empty_children(node: Dict[str, Any]) -> Dict[str, Any]:
        if children_field in node and not node[children_field]:
            del node[children_field]
        elif children_field in node:
            # 递归处理子节点
            for child in node[children_field]:
                remove_empty_children(child)
        return node

    # 对根节点及其子节点进行处理
    roots = [remove_empty_children(node) for node in roots]

    return roots
