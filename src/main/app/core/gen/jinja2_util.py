import json
from datetime import datetime
from typing import List

from src.main.app.core.gen.gen_constants import GenConstants
from src.main.app.model.db_index_model import IndexDO
from src.main.app.schema.gen_table_schema import TableGen


class Jinja2Utils:
    JAVA_PROJECT_PATH = "main/java"
    PY_PROJECT_PATH = "main/app"
    MYBATIS_PATH = "main/resources/mapper"
    DEFAULT_PARENT_MENU_ID = "3"

    @staticmethod
    def prepare_context(table_gen: TableGen, index_metadata: List[IndexDO]):
        """
        设置模板变量信息
        """
        gen_table = table_gen.gen_table

        comment = gen_table.comment
        package_name = gen_table.package_name
        import_list = Jinja2Utils.get_import_list(table_gen)
        function_name = gen_table.function_name
        table_name = gen_table.table_name
        author = gen_table.function_author
        date_time = datetime.now().strftime("%Y-%m-%d")
        class_name = Jinja2Utils.capitalize(gen_table.class_name)
        c_n = Jinja2Utils.to_snake_case(class_name)
        lowercase_class_name = Jinja2Utils.uncapitalize(class_name)
        primary_key = table_gen.pk_field
        router_name = Jinja2Utils.to_kebab_case(class_name)
        kebab_case_class_name = router_name
        fields = table_gen.fields
        for field in fields:
            pass
        module_name = gen_table.module_name
        business_name = gen_table.business_name

        tpl_category = gen_table.tpl_category

        context = {
            "comment": comment,
            "package_name": package_name,
            "import_list": import_list,
            "function_name": function_name,
            "table_name": table_name,
            "author": author,
            "datetime": date_time,
            "class_name": class_name,
            "c_n": c_n,
            "ClassName": class_name,
            "ClassNames": pluralize(class_name),
            "lowercase_class_name": lowercase_class_name,
            "className": lowercase_class_name,
            "primary_key": primary_key,
            "router_name": router_name,
            "kebab_case_class_name": kebab_case_class_name,
            "cn": kebab_case_class_name,
            "fields": fields,
            "index_metadata": index_metadata,
            "business_name": business_name,
            "tree_parent_code": "parent_id",
            # "tpl_category": tpl_category,
            # "module_name": module_name,
            # "business_name": Jinja2Utils.capitalize(business_name),
            # "base_package": Jinja2Utils.get_package_prefix(package_name),
            # "permission_prefix": Jinja2Utils.get_permission_prefix(module_name, business_name),
            # "table": gen_table,
            # "dicts": Jinja2Utils.get_dicts(gen_table),
        }

        # Jinja2Utils.set_menu_context(context, gen_table)
        #
        # if tpl_category == "tree":
        #     Jinja2Utils.set_tree_context(context, gen_table)
        # elif tpl_category == "sub":
        #     Jinja2Utils.set_sub_context(context, gen_table)

        return context

    @staticmethod
    def set_menu_context(context, gen_table):
        options = gen_table.get("options", "{}")
        params_obj = json.loads(options)
        parent_menu_id = Jinja2Utils.get_parent_menu_id(params_obj)
        context["parentMenuId"] = parent_menu_id

    @staticmethod
    def set_tree_context(context, gen_table):
        options = gen_table.get("options", "{}")
        params_obj = json.loads(options)
        tree_code = params_obj.get("treeCode")
        tree_parent_code = params_obj.get("treeParentCode")
        tree_name = params_obj.get("treeName")

        context.update(
            {
                "treeCode": tree_code,
                "treeParentCode": tree_parent_code,
                "treeName": tree_name,
                "expandColumn": Jinja2Utils.get_expand_column(gen_table),
                "tree_parent_code": params_obj.get("treeParentCode"),
                "tree_name": params_obj.get("treeName"),
            }
        )

    @staticmethod
    def set_sub_context(context, gen_table):
        sub_table = gen_table.get("subTable", {})
        sub_table_name = gen_table.get("subTableName")
        sub_table_fk_name = gen_table.get("subTableFkName")

        sub_class_name = sub_table.get("className")
        sub_table_fk_class_name = Jinja2Utils.convert_to_camel_case(
            sub_table_fk_name
        )

        context.update(
            {
                "subTable": sub_table,
                "subTableName": sub_table_name,
                "subTableFkName": sub_table_fk_name,
                "subTableFkClassName": sub_table_fk_class_name,
                "subTableFkclassName": Jinja2Utils.uncapitalize(
                    sub_table_fk_class_name
                ),
                "subClassName": sub_class_name,
                "subclassName": Jinja2Utils.uncapitalize(sub_class_name),
                "subImportList": Jinja2Utils.get_import_list(sub_table),
            }
        )

    @staticmethod
    def get_template_list(
        backend: str,
        tpl_backend_type: str,
        tpl_category: str,
        tpl_web_type: str,
    ):
        """
        获取模板信息
        :param backend: 后端语言, java, python, go, rust...
        :param tpl_backend_type: 后端语言使用的模板类型, mybatis, mybatis-plus...
        :param tpl_category: 模板类别 (如 CRUD、TREE、SUB 等)
        :param tpl_web_type: 前端类型 (如 react 或 element-plus)
        :return: 模板列表
        """
        select_template = []
        if backend == GenConstants.PYTHON:
            model_tpl = "jinja2/python/modelPy.py.j2"
            schema_tpl = "jinja2/python/schemaPy.py.j2"
            mapper_tpl = "jinja2/python/mapperPy.py.j2"
            service_tpl = "jinja2/python/servicePy.py.j2"
            service_impl_tpl = "jinja2/python/serviceImplPy.py.j2"
            controller_tpl = "jinja2/python/controllerPy.py.j2"
            python_template = [
                model_tpl,
                schema_tpl,
                mapper_tpl,
                service_tpl,
                service_impl_tpl,
                controller_tpl,
            ]
            for tmp in python_template:
                select_template.append(tmp)
        if backend == GenConstants.JAVA:
            model_tpl = "jinja2/java/mybatis_plus/model.java.j2"
            mapper_tpl = "jinja2/java/mybatis_plus/mapper.java.j2"
            service_tpl = "jinja2/java/mybatis_plus/service.java.j2"
            service_impl_tpl = "jinja2/java/mybatis_plus/serviceImpl.java.j2"
            controller_tpl = "jinja2/java/mybatis_plus/controller.java.j2"
            create_tpl = "jinja2/java/command/create.java.j2"
            modify_tpl = "jinja2/java/command/modify.java.j2"
            batch_modify_tpl = "jinja2/java/command/batchModify.java.j2"
            query_tpl = "jinja2/java/command/query.java.j2"
            detail_tpl = "jinja2/java/vo/detail.java.j2"
            page_tpl = "jinja2/java/vo/page.java.j2"
            converter_tpl = "jinja2/java/converter/converter.java.j2"
            java_template = [
                model_tpl,
                mapper_tpl,
                service_tpl,
                service_impl_tpl,
                controller_tpl,
                create_tpl,
                modify_tpl,
                query_tpl,
                detail_tpl,
                page_tpl,
                converter_tpl,
                batch_modify_tpl,
            ]
            select_template.extend(java_template)
        index_tpl = "jinja2/react/index.tsx.j2"
        index_query_tpl = "jinja2/react/components/iQuery.tsx.j2"
        index_create_tpl = "jinja2/react/components/iCreate.tsx.j2"
        index_detail_tpl = "jinja2/react/components/iDetail.tsx.j2"
        index_modify_tpl = "jinja2/react/components/iModify.tsx.j2"
        index_batch_modify_tpl = "jinja2/react/components/iBatchModify.tsx.j2"
        index_import_tpl = "jinja2/react/components/iImport.tsx.j2"
        api_tpl = "jinja2/js/api.js.j2"
        type_tpl = "jinja2/js/type.js.j2"
        router_tpl = "jinja2/react/router.tsx.j2"
        react_templates = [
            index_query_tpl,
            index_modify_tpl,
            index_import_tpl,
            index_detail_tpl,
            index_batch_modify_tpl,
            index_tpl,
            index_create_tpl,
            api_tpl,
            type_tpl,
            router_tpl,
        ]

        select_template.extend(react_templates)

        # if tpl_category == "crud":
        #     templates.append(f"{use_web_type}/index.react.vm")
        # elif tpl_category == "tree":
        #     templates.append(f"{use_web_type}/index-tree.react.vm")
        # elif tpl_category == "sub":
        #     templates.append(f"{use_web_type}/index.react.vm")
        #     templates.append("vm/java/sub-model.java.j2")
        return select_template

    @staticmethod
    def get_file_name(template, table_gen):
        """
        获取文件名
        """
        gen_table = table_gen.gen_table
        file_name = ""
        package_name = gen_table.package_name
        module_name = gen_table.module_name
        class_name = gen_table.class_name
        table_name = gen_table.table_name
        business_name = gen_table.business_name

        java_path = (
            f"{Jinja2Utils.JAVA_PROJECT_PATH}/{package_name.replace('.', '/')}"
        )
        py_path = f"{Jinja2Utils.PY_PROJECT_PATH}"
        mybatis_path = f"{Jinja2Utils.MYBATIS_PATH}/{module_name}"
        client_dir = "src"
        client_module_dir = "system"
        kebab_case_class_name = Jinja2Utils.to_kebab_case(business_name)

        if "model.java.j2" in template:
            file_name = f"{java_path}/model/{class_name}DO.java"
        elif (
            "sub-model.java.j2" in template
            and gen_table.get("tplCategory") == "sub"
        ):
            sub_class_name = gen_table.get("subTable").get("className")
            file_name = f"{java_path}/domain/{sub_class_name}.java"
        elif "mapper.java.j2" in template:
            file_name = f"{java_path}/mapper/{class_name}Mapper.java"
        elif "service.java.j2" in template:
            file_name = f"{java_path}/service/I{class_name}Service.java"
        elif "serviceImpl.java.j2" in template:
            file_name = f"{java_path}/service/impl/{class_name}ServiceImpl.java"
        elif "controller.java.j2" in template:
            file_name = f"{java_path}/controller/{class_name}Controller.java"
        elif "controllerPy.py.j2" in template:
            file_name = f"{py_path}/controller/{table_name}_controller.py"
        elif "servicePy.py.j2" in template:
            file_name = f"{py_path}/service/{table_name}_service.py"
        elif "serviceImplPy.py.j2" in template:
            file_name = f"{py_path}/service/impl/{table_name}_service_impl.py"
        elif "mapperPy.py.j2" in template:
            file_name = f"{py_path}/mapper/{table_name}_mapper.py"
        elif "schemaPy.py.j2" in template:
            file_name = f"{py_path}/schema/{table_name}_schema.py"
        elif "modelPy.py.j2" in template:
            file_name = f"{py_path}/model/{table_name}_model.py"
        elif "converter.java.j2" in template:
            file_name = f"{java_path}/converter/{class_name}Converter.java"
        elif "create.java.j2" in template:
            file_name = f"{java_path}/command/{class_name}Create.java"
        elif "modify.java.j2" in template:
            file_name = f"{java_path}/command/{class_name}Modify.java"
        elif "batchModify.java.j2" in template:
            file_name = f"{java_path}/command/{class_name}BatchModify.java"
        elif "query.java.j2" in template:
            file_name = f"{java_path}/command/{class_name}Query.java"
        elif "detail.java.j2" in template:
            file_name = f"{java_path}/vo/{class_name}Detail.java"
        elif "page.java.j2" in template:
            file_name = f"{java_path}/vo/{class_name}Page.java"
        elif "mapper.xml.vm" in template:
            file_name = f"{mybatis_path}/{class_name}Mapper.xml"
        elif "sql.vm" in template:
            file_name = f"{business_name}Menu.sql"
        elif "index.tsx.j2" in template:
            file_name = f"{client_dir}/views/{client_module_dir}/{kebab_case_class_name}/index.tsx"
        elif "iQuery.tsx.j2" in template:
            file_name = f"{client_dir}/views/{client_module_dir}/{kebab_case_class_name}/components/{kebab_case_class_name}-query.tsx"
        elif "iCreate.tsx.j2" in template:
            file_name = f"{client_dir}/views/{client_module_dir}/{kebab_case_class_name}/components/{kebab_case_class_name}-create.tsx"
        elif "iDetail.tsx.j2" in template:
            file_name = f"{client_dir}/views/{client_module_dir}/{kebab_case_class_name}/components/{kebab_case_class_name}-detail.tsx"
        elif "iModify.tsx.j2" in template:
            file_name = f"{client_dir}/views/{client_module_dir}/{kebab_case_class_name}/components/{kebab_case_class_name}-modify.tsx"
        elif "iBatchModify.tsx.j2" in template:
            file_name = f"{client_dir}/views/{client_module_dir}/{kebab_case_class_name}/components/{kebab_case_class_name}-batch-modify.tsx"
        elif "iImport.tsx.j2" in template:
            file_name = f"{client_dir}/views/{client_module_dir}/{kebab_case_class_name}/components/{kebab_case_class_name}-import.tsx"
        elif "api.js.j2" in template:
            file_name = f"{client_dir}/service/{kebab_case_class_name}.ts"
        elif "type.js.j2" in template:
            file_name = f"{client_dir}/types/{kebab_case_class_name}.ts"
        elif "router.tsx.j2" in template:
            file_name = f"{client_dir}/router.ts"
        else:
            raise Exception(template)

        return file_name

    @staticmethod
    def get_package_prefix(package_name):
        """
        获取包前缀
        """
        last_index = package_name.rfind(".")
        return package_name[:last_index] if last_index != -1 else package_name

    @staticmethod
    def get_import_list(gen_table: TableGen):
        """
        根据列类型获取导入包
        """
        fields = gen_table.fields

        sub_gen_table = gen_table.sub_table
        import_list = set()

        backend = gen_table.gen_table.backend
        if GenConstants.JAVA == backend:
            if sub_gen_table:
                import_list.add("java.util.List")

            for field in fields:
                if field.gen_field.field_type == "Date":
                    import_list.add("java.util.Date")
                elif field.gen_field.field_type == "BigDecimal":
                    import_list.add("java.math.BigDecimal")
                elif field.gen_field.field_type == "LocalDateTime":
                    import_list.add("java.time.LocalDateTime")
                    return list(import_list)
        else:
            return set([field.gen_field.sql_model_type for field in fields])

    @staticmethod
    def get_dicts(gen_table):
        """
        根据列类型获取字典组
        """
        columns = gen_table.get("columns", [])
        dicts = set()
        Jinja2Utils.add_dicts(dicts, columns)

        sub_table = gen_table.get("subTable")
        if sub_table:
            sub_columns = sub_table.get("columns", [])
            Jinja2Utils.add_dicts(dicts, sub_columns)

        return ", ".join(dicts)

    @staticmethod
    def add_dicts(dicts, columns):
        """
        添加字典列表
        """
        for column in columns:
            if (
                not column.get("isSuperColumn")
                and column.get("dictType")
                and column.get("htmlType") in {"select", "radio", "checkbox"}
            ):
                dicts.add(f"'{column.get('dictType')}'")

    @staticmethod
    def get_permission_prefix(module_name, business_name):
        """
        获取权限前缀
        """
        return f"{module_name}:{business_name}"

    @staticmethod
    def get_parent_menu_id(params_obj):
        """
        获取上级菜单 ID 字段
        """
        if params_obj and "parentMenuId" in params_obj:
            return params_obj.get("parentMenuId")
        return Jinja2Utils.DEFAULT_PARENT_MENU_ID

    @staticmethod
    def get_tree_code(params_obj):
        """
        获取 TreeCode 字段
        """
        return params_obj.get("treeCode", "")

    @staticmethod
    def get_tree_parent_code(params_obj):
        """
        获取 TreeParentCode 字段
        """
        return params_obj.get("treeParentCode", "")

    @staticmethod
    def get_tree_name(params_obj):
        """
        获取 TreeName 字段
        """
        return params_obj.get("treeName", "")

    @staticmethod
    def get_expand_column(gen_table):
        """
        获取树表的展开列
        """
        columns = gen_table.get("columns", [])
        for index, column in enumerate(columns):
            if column.get("isList") and column.get("isSuperColumn") is False:
                return index
        return 0

    @staticmethod
    def convert_to_camel_case(name):
        """
        将字符串转换为驼峰命名
        """
        words = name.split("_")
        return words[0] + "".join(word.capitalize() for word in words[1:])

    @staticmethod
    def uncapitalize(name):
        """
        将字符串的首字母小写
        """
        if not name:
            return ""
        return name[0].lower() + name[1:]

    @staticmethod
    def capitalize(name):
        """
        将字符串的首字母大写
        """
        if not name:
            return ""
        return name[0].upper() + name[1:]

    @staticmethod
    def to_kebab_case(name):
        if not name:
            return name
        result = []
        for i, c in enumerate(name):
            if c.isupper():
                if i != 0:
                    result.append("-")
                result.append(c.lower())
            else:
                result.append(c)
        return "".join(result)

    @staticmethod
    def to_snake_case(name):
        if not name:
            return name
        result = []
        for i, c in enumerate(name):
            if c.isupper():
                if i != 0:
                    result.append("_")
                result.append(c.lower())
            else:
                result.append(c)
        return "".join(result)
